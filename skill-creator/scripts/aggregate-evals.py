#!/usr/bin/env python3
"""Validate and aggregate portable matched Agent Skill evaluation results."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
CONDITIONS = ("candidate", "baseline")
CHECK_STATUSES = {"passed", "failed", "not_verifiable"}
CHECK_DIMENSIONS = {"goal_completion", "instruction_following"}
MATCHED_FIELDS = ("harness", "model", "prompt", "inputs", "permissions", "environment")
EFFICIENCY_REGRESSION_THRESHOLD = 2.0


class EvaluationError(ValueError):
    """Raised when evaluation results are malformed or not safely comparable."""


def _expect(condition: bool, message: str) -> None:
    if not condition:
        raise EvaluationError(message)


def _load_result(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvaluationError(f"{path}: cannot read valid JSON: {exc}") from exc

    _expect(isinstance(data, dict), f"{path}: top level must be an object")
    _expect(data.get("schema_version") == SCHEMA_VERSION, f"{path}: schema_version must be {SCHEMA_VERSION}")
    _expect(isinstance(data.get("case"), str) and data["case"].strip(), f"{path}: case must be a non-empty string")
    _expect(isinstance(data.get("trial"), int) and not isinstance(data["trial"], bool) and data["trial"] >= 1,
            f"{path}: trial must be an integer >= 1")
    _expect(data.get("condition") in CONDITIONS, f"{path}: condition must be candidate or baseline")
    _expect(isinstance(data.get("skill_version"), str) and data["skill_version"].strip(),
            f"{path}: skill_version must be a non-empty string")
    _expect(isinstance(data.get("prompt"), str) and data["prompt"].strip(), f"{path}: prompt must be a non-empty string")

    for field in ("harness", "model", "permissions", "environment"):
        _expect(data.get(field) is None or isinstance(data.get(field), str), f"{path}: {field} must be a string or null")

    inputs = data.get("inputs")
    _expect(isinstance(inputs, list) and all(isinstance(item, str) for item in inputs),
            f"{path}: inputs must be an array of strings")

    for field in ("duration_ms", "tokens"):
        value = data.get(field)
        _expect(value is None or (isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0),
                f"{path}: {field} must be a non-negative number or null")

    checks = data.get("checks")
    _expect(isinstance(checks, list), f"{path}: checks must be an array")
    seen_ids: set[str] = set()
    for index, check in enumerate(checks):
        prefix = f"{path}: checks[{index}]"
        _expect(isinstance(check, dict), f"{prefix} must be an object")
        check_id = check.get("id")
        _expect(isinstance(check_id, str) and check_id.strip(), f"{prefix}.id must be a non-empty string")
        _expect(check_id not in seen_ids, f"{path}: duplicate check id {check_id!r}")
        seen_ids.add(check_id)
        _expect(check.get("status") in CHECK_STATUSES,
                f"{prefix}.status must be passed, failed, or not_verifiable")
        _expect(isinstance(check.get("evidence"), str) and check["evidence"].strip(),
                f"{prefix}.evidence must be a non-empty string")
        dimension = check.get("dimension")
        _expect(dimension is None or dimension in CHECK_DIMENSIONS,
                f"{prefix}.dimension must be goal_completion, instruction_following, or omitted")

    notes = data.get("notes", [])
    _expect(isinstance(notes, list) and all(isinstance(note, str) for note in notes),
            f"{path}: notes must be an array of strings when present")

    data["_path"] = str(path)
    return data


def load_workspace(workspace: Path) -> list[dict[str, Any]]:
    _expect(workspace.exists(), f"workspace does not exist: {workspace}")
    paths = sorted(workspace.rglob("result.json"))
    _expect(bool(paths), f"no result.json files found under {workspace}")
    return [_load_result(path) for path in paths]


def validate_pairs(results: list[dict[str, Any]]) -> dict[tuple[str, int], dict[str, dict[str, Any]]]:
    pairs: dict[tuple[str, int], dict[str, dict[str, Any]]] = defaultdict(dict)
    for result in results:
        key = (result["case"], result["trial"])
        condition = result["condition"]
        _expect(condition not in pairs[key],
                f"duplicate {condition} result for case={key[0]!r} trial={key[1]}")
        pairs[key][condition] = result

    for (case, trial), pair in sorted(pairs.items()):
        missing = [condition for condition in CONDITIONS if condition not in pair]
        _expect(not missing, f"case={case!r} trial={trial} is missing condition(s): {', '.join(missing)}")
        candidate = pair["candidate"]
        baseline = pair["baseline"]
        for field in MATCHED_FIELDS:
            _expect(candidate.get(field) == baseline.get(field),
                    f"case={case!r} trial={trial}: matched field {field!r} differs between candidate and baseline")

        candidate_checks = {check["id"]: check for check in candidate["checks"]}
        baseline_checks = {check["id"]: check for check in baseline["checks"]}
        _expect(candidate_checks.keys() == baseline_checks.keys(),
                f"case={case!r} trial={trial}: candidate and baseline check ids differ")
        for check_id in candidate_checks:
            _expect(candidate_checks[check_id].get("dimension") == baseline_checks[check_id].get("dimension"),
                    f"case={case!r} trial={trial}: check {check_id!r} dimension differs between candidate and baseline")

    return dict(pairs)


def _metric_summary(values: list[float]) -> dict[str, Any] | None:
    if not values:
        return None
    return {
        "n": len(values),
        "mean": statistics.fmean(values),
        "stddev": statistics.pstdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }


def _checks_summary(checks: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(check["status"] == "passed" for check in checks)
    failed = sum(check["status"] == "failed" for check in checks)
    not_verifiable = sum(check["status"] == "not_verifiable" for check in checks)
    verifiable = passed + failed
    return {
        "passed": passed,
        "failed": failed,
        "not_verifiable": not_verifiable,
        "verifiable": verifiable,
        "pass_rate": (passed / verifiable) if verifiable else None,
    }


def _condition_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    all_checks: list[dict[str, Any]] = []
    run_rates: list[float] = []
    durations: list[float] = []
    tokens: list[float] = []

    for result in results:
        checks = result["checks"]
        all_checks.extend(checks)
        run_summary = _checks_summary(checks)
        if run_summary["pass_rate"] is not None:
            run_rates.append(run_summary["pass_rate"])
        if result.get("duration_ms") is not None:
            durations.append(float(result["duration_ms"]))
        if result.get("tokens") is not None:
            tokens.append(float(result["tokens"]))

    return {
        "results": len(results),
        "checks": _checks_summary(all_checks),
        "run_pass_rate": _metric_summary(run_rates),
        "duration_ms": _metric_summary(durations),
        "tokens": _metric_summary(tokens),
    }


def _dimension_summary(results: list[dict[str, Any]], dimension: str) -> dict[str, Any]:
    checks = [
        check
        for result in results
        for check in result["checks"]
        if check.get("dimension") == dimension
    ]
    return _checks_summary(checks)


def _fully_passed(result: dict[str, Any]) -> bool:
    checks = result["checks"]
    return bool(checks) and all(check["status"] == "passed" for check in checks)


def _paired_efficiency_summary(
    pairs: dict[tuple[str, int], dict[str, dict[str, Any]]]
) -> tuple[dict[str, Any], list[str]]:
    flagged: list[dict[str, Any]] = []
    eligible_pairs = 0
    skipped_not_fully_passing = 0
    skipped_missing_metrics = 0
    skipped_zero_baseline = 0

    for (case, trial), pair in sorted(pairs.items()):
        candidate = pair["candidate"]
        baseline = pair["baseline"]

        if not (_fully_passed(candidate) and _fully_passed(baseline)):
            skipped_not_fully_passing += 1
            continue

        metrics = (
            candidate.get("tokens"),
            baseline.get("tokens"),
            candidate.get("duration_ms"),
            baseline.get("duration_ms"),
        )
        if any(value is None for value in metrics):
            skipped_missing_metrics += 1
            continue

        candidate_tokens = float(candidate["tokens"])
        baseline_tokens = float(baseline["tokens"])
        candidate_duration = float(candidate["duration_ms"])
        baseline_duration = float(baseline["duration_ms"])
        if baseline_tokens <= 0 or baseline_duration <= 0:
            skipped_zero_baseline += 1
            continue

        eligible_pairs += 1
        token_ratio = candidate_tokens / baseline_tokens
        duration_ratio = candidate_duration / baseline_duration
        is_regression = (
            token_ratio > 1.0
            and duration_ratio > 1.0
            and max(token_ratio, duration_ratio) >= EFFICIENCY_REGRESSION_THRESHOLD
        )
        if is_regression:
            flagged.append({
                "case": case,
                "trial": trial,
                "token_ratio": token_ratio,
                "duration_ratio": duration_ratio,
                "candidate_tokens": candidate["tokens"],
                "baseline_tokens": baseline["tokens"],
                "candidate_duration_ms": candidate["duration_ms"],
                "baseline_duration_ms": baseline["duration_ms"],
            })

    summary = {
        "threshold": EFFICIENCY_REGRESSION_THRESHOLD,
        "eligible_pairs": eligible_pairs,
        "flagged_regressions": len(flagged),
        "flagged_pairs": flagged,
        "skipped": {
            "not_fully_passing": skipped_not_fully_passing,
            "missing_metrics": skipped_missing_metrics,
            "zero_baseline_metric": skipped_zero_baseline,
        },
    }

    warnings: list[str] = []
    if skipped_missing_metrics:
        warnings.append(
            f"Efficiency regression screening skipped {skipped_missing_metrics} fully passing pair(s) with missing duration or token metrics."
        )
    if skipped_zero_baseline:
        warnings.append(
            f"Efficiency regression screening skipped {skipped_zero_baseline} fully passing pair(s) with a zero baseline duration or token metric."
        )
    return summary, warnings


def aggregate(pairs: dict[tuple[str, int], dict[str, dict[str, Any]]]) -> dict[str, Any]:
    by_condition = {
        condition: [pair[condition] for pair in pairs.values()]
        for condition in CONDITIONS
    }

    paired = {"candidate_wins": 0, "baseline_wins": 0, "ties": 0, "not_comparable": 0}
    by_case: dict[str, dict[str, int]] = defaultdict(
        lambda: {
            "candidate_wins": 0,
            "baseline_wins": 0,
            "ties": 0,
            "not_comparable": 0,
        }
    )

    for (case, _trial), pair in pairs.items():
        candidate_checks = {check["id"]: check for check in pair["candidate"]["checks"]}
        baseline_checks = {check["id"]: check for check in pair["baseline"]["checks"]}
        for check_id in sorted(candidate_checks):
            candidate_status = candidate_checks[check_id]["status"]
            baseline_status = baseline_checks[check_id]["status"]
            if "not_verifiable" in (candidate_status, baseline_status):
                outcome = "not_comparable"
            elif candidate_status == baseline_status:
                outcome = "ties"
            elif candidate_status == "passed":
                outcome = "candidate_wins"
            else:
                outcome = "baseline_wins"
            paired[outcome] += 1
            by_case[case][outcome] += 1

    candidate_summary = _condition_summary(by_condition["candidate"])
    baseline_summary = _condition_summary(by_condition["baseline"])
    efficiency_summary, efficiency_warnings = _paired_efficiency_summary(pairs)

    warnings: list[str] = []
    if candidate_summary["checks"]["verifiable"] == 0:
        warnings.append("No verifiable checks were recorded; use human review rather than claiming quantitative lift.")
    if any(result.get("duration_ms") is None for result in by_condition["candidate"] + by_condition["baseline"]):
        warnings.append("Some duration_ms values are unavailable; timing summaries use only reported values.")
    if any(result.get("tokens") is None for result in by_condition["candidate"] + by_condition["baseline"]):
        warnings.append("Some token values are unavailable; token summaries use only reported values.")
    warnings.extend(efficiency_warnings)

    candidate_rate = candidate_summary["checks"]["pass_rate"]
    baseline_rate = baseline_summary["checks"]["pass_rate"]
    pass_rate_delta = None if candidate_rate is None or baseline_rate is None else candidate_rate - baseline_rate

    dimensions: dict[str, Any] = {}
    for dimension in sorted(CHECK_DIMENSIONS):
        candidate_dimension = _dimension_summary(by_condition["candidate"], dimension)
        baseline_dimension = _dimension_summary(by_condition["baseline"], dimension)
        if candidate_dimension["verifiable"] or baseline_dimension["verifiable"] or candidate_dimension["not_verifiable"] or baseline_dimension["not_verifiable"]:
            candidate_dimension_rate = candidate_dimension["pass_rate"]
            baseline_dimension_rate = baseline_dimension["pass_rate"]
            dimensions[dimension] = {
                "candidate": candidate_dimension,
                "baseline": baseline_dimension,
                "pooled_pass_rate_delta": (
                    None
                    if candidate_dimension_rate is None or baseline_dimension_rate is None
                    else candidate_dimension_rate - baseline_dimension_rate
                ),
            }

    return {
        "schema_version": SCHEMA_VERSION,
        "pairs": len(pairs),
        "results": len(pairs) * 2,
        "conditions": {
            "candidate": candidate_summary,
            "baseline": baseline_summary,
        },
        "delta": {
            "pooled_pass_rate": pass_rate_delta,
            "mean_duration_ms": _mean_delta(candidate_summary["duration_ms"], baseline_summary["duration_ms"]),
            "mean_tokens": _mean_delta(candidate_summary["tokens"], baseline_summary["tokens"]),
        },
        "dimensions": dimensions,
        "paired_check_outcomes": paired,
        "paired_efficiency": efficiency_summary,
        "by_case": dict(sorted(by_case.items())),
        "warnings": warnings,
    }


def _mean_delta(candidate: dict[str, Any] | None, baseline: dict[str, Any] | None) -> float | None:
    if candidate is None or baseline is None:
        return None
    return candidate["mean"] - baseline["mean"]


def _fmt_rate(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1%}"


def _fmt_delta(value: float | None, suffix: str = "") -> str:
    return "n/a" if value is None else f"{value:+.1f}{suffix}"


def _fmt_rate_delta(value: float | None) -> str:
    return "n/a" if value is None else f"{value:+.1%}"


def _fmt_rate_summary(value: dict[str, Any] | None) -> str:
    if value is None:
        return "n/a"
    return f"{value['mean']:.1%} ± {value['stddev']:.1%} (n={value['n']})"


def _fmt_ratio(value: float) -> str:
    return f"{value:.2f}×"


def render_markdown(summary: dict[str, Any]) -> str:
    candidate = summary["conditions"]["candidate"]
    baseline = summary["conditions"]["baseline"]
    lines = [
        "# Skill evaluation summary",
        "",
        f"Matched pairs: **{summary['pairs']}**",
        "",
        "| Condition | Passed | Failed | Not verifiable | Pooled pass rate |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, values in (("Candidate", candidate), ("Baseline", baseline)):
        checks = values["checks"]
        lines.append(
            f"| {name} | {checks['passed']} | {checks['failed']} | {checks['not_verifiable']} | {_fmt_rate(checks['pass_rate'])} |"
        )

    delta = summary["delta"]
    paired = summary["paired_check_outcomes"]
    efficiency = summary["paired_efficiency"]
    lines.extend([
        "",
        f"Pooled pass-rate delta: **{_fmt_rate_delta(delta['pooled_pass_rate'])}**",
    ])

    if summary["dimensions"]:
        lines.extend([
            "",
            "## Outcome dimensions",
            "",
            "| Dimension | Candidate pass rate | Baseline pass rate | Delta |",
            "| --- | ---: | ---: | ---: |",
        ])
        for dimension, values in sorted(summary["dimensions"].items()):
            lines.append(
                f"| {dimension} | {_fmt_rate(values['candidate']['pass_rate'])} | {_fmt_rate(values['baseline']['pass_rate'])} | {_fmt_rate_delta(values['pooled_pass_rate_delta'])} |"
            )

    lines.extend([
        "",
        "## Run pass-rate variation",
        "",
        f"- Candidate: **{_fmt_rate_summary(candidate['run_pass_rate'])}**",
        f"- Baseline: **{_fmt_rate_summary(baseline['run_pass_rate'])}**",
        "",
        f"Mean duration delta: **{_fmt_delta(delta['mean_duration_ms'], ' ms')}**",
        f"Mean token delta: **{_fmt_delta(delta['mean_tokens'])}**",
        "",
        "## Paired check outcomes",
        "",
        f"- Candidate wins: {paired['candidate_wins']}",
        f"- Baseline wins: {paired['baseline_wins']}",
        f"- Ties: {paired['ties']}",
        f"- Not comparable: {paired['not_comparable']}",
        "",
        "## Paired efficiency regressions",
        "",
        (
            "A pair is flagged only when both conditions fully pass, both token use and duration increase, "
            f"and at least one ratio is ≥ {efficiency['threshold']:.1f}×. This is a diagnostic signal, not an automatic rejection gate."
        ),
        "",
        f"- Eligible fully passing pairs: {efficiency['eligible_pairs']}",
        f"- Flagged regressions: {efficiency['flagged_regressions']}",
    ])

    if efficiency["flagged_pairs"]:
        lines.extend([
            "",
            "| Case | Trial | Token ratio | Duration ratio |",
            "| --- | ---: | ---: | ---: |",
        ])
        for item in efficiency["flagged_pairs"]:
            lines.append(
                f"| {item['case']} | {item['trial']} | {_fmt_ratio(item['token_ratio'])} | {_fmt_ratio(item['duration_ratio'])} |"
            )

    if summary["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in summary["warnings"])

    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path, help="Workspace containing result.json files")
    parser.add_argument("--json-out", type=Path, help="Write machine-readable summary JSON")
    parser.add_argument("--markdown-out", type=Path, help="Write Markdown summary")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    args = parser.parse_args(argv)

    try:
        results = load_workspace(args.workspace)
        pairs = validate_pairs(results)
        summary = aggregate(pairs)
    except EvaluationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    markdown = render_markdown(summary)
    if args.json_out:
        args.json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown_out:
        args.markdown_out.write_text(markdown, encoding="utf-8")

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
