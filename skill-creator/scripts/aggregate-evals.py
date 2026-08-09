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
MATCHED_FIELDS = ("harness", "model", "prompt", "inputs", "permissions", "environment")


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

        candidate_checks = {check["id"] for check in candidate["checks"]}
        baseline_checks = {check["id"] for check in baseline["checks"]}
        _expect(candidate_checks == baseline_checks,
                f"case={case!r} trial={trial}: candidate and baseline check ids differ")

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


def _condition_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    passed = failed = not_verifiable = 0
    run_rates: list[float] = []
    durations: list[float] = []
    tokens: list[float] = []

    for result in results:
        run_passed = sum(check["status"] == "passed" for check in result["checks"])
        run_failed = sum(check["status"] == "failed" for check in result["checks"])
        run_not_verifiable = sum(check["status"] == "not_verifiable" for check in result["checks"])
        passed += run_passed
        failed += run_failed
        not_verifiable += run_not_verifiable
        if run_passed + run_failed:
            run_rates.append(run_passed / (run_passed + run_failed))
        if result.get("duration_ms") is not None:
            durations.append(float(result["duration_ms"]))
        if result.get("tokens") is not None:
            tokens.append(float(result["tokens"]))

    verifiable = passed + failed
    return {
        "results": len(results),
        "checks": {
            "passed": passed,
            "failed": failed,
            "not_verifiable": not_verifiable,
            "verifiable": verifiable,
            "pass_rate": (passed / verifiable) if verifiable else None,
        },
        "run_pass_rate": _metric_summary(run_rates),
        "duration_ms": _metric_summary(durations),
        "tokens": _metric_summary(tokens),
    }


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

    warnings: list[str] = []
    if candidate_summary["checks"]["verifiable"] == 0:
        warnings.append("No verifiable checks were recorded; use human review rather than claiming quantitative lift.")
    if any(result.get("duration_ms") is None for result in by_condition["candidate"] + by_condition["baseline"]):
        warnings.append("Some duration_ms values are unavailable; timing summaries use only reported values.")
    if any(result.get("tokens") is None for result in by_condition["candidate"] + by_condition["baseline"]):
        warnings.append("Some token values are unavailable; token summaries use only reported values.")

    candidate_rate = candidate_summary["checks"]["pass_rate"]
    baseline_rate = baseline_summary["checks"]["pass_rate"]
    pass_rate_delta = None if candidate_rate is None or baseline_rate is None else candidate_rate - baseline_rate

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
        "paired_check_outcomes": paired,
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
    lines.extend([
        "",
        f"Pooled pass-rate delta: **{_fmt_rate_delta(delta['pooled_pass_rate'])}**",
        f"Mean duration delta: **{_fmt_delta(delta['mean_duration_ms'], ' ms')}**",
        f"Mean token delta: **{_fmt_delta(delta['mean_tokens'])}**",
        "",
        "## Paired check outcomes",
        "",
        f"- Candidate wins: {paired['candidate_wins']}",
        f"- Baseline wins: {paired['baseline_wins']}",
        f"- Ties: {paired['ties']}",
        f"- Not comparable: {paired['not_comparable']}",
    ])

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
