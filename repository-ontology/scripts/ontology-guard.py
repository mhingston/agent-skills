#!/usr/bin/env python3
"""Deterministic repository-ontology drift guard.

The guard evaluates an explicitly operationalised, JSON constraint profile. It
never derives blocking policy from free-form ontology prose or model confidence.
Only confirmed rules marked with ``enforcement: block`` can block.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Sequence

from ontology_guard_extract import (
    evaluate_mapping_rules, evaluate_relationship_rules, explicit_relationships,
    git_lines, parse_project_references, repository_files,
)
from ontology_guard_model import (
    BASELINE_ELIGIBLE_CODES, EvaluationContext, Finding, GuardError, load_json,
    resolve_path, structural_findings,
)
from ontology_guard_policy import (
    apply_baseline_and_waivers, baseline_fingerprints,
    evaluate_decision_gate, load_waivers, overall_status, profile_fingerprint,
)

def evaluate(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    profile_path = Path(args.profile)
    if not profile_path.is_absolute():
        profile_path = (repo_root / profile_path).resolve()
    profile = load_json(profile_path, "profile")
    findings = structural_findings(profile)
    if any(finding.blocking for finding in findings):
        status = overall_status(findings)
        return report(args, profile if isinstance(profile, dict) else {}, findings, status)

    components = {item["id"]: item for item in profile.get("components", [])}
    rules = list(profile.get("rules", []))
    relationships = explicit_relationships(profile)
    extractor_findings: list[Finding] = []
    extractors = profile.get("extractors", {})
    if isinstance(extractors, dict) and extractors.get("dotnet-project-references", {}).get(
        "enabled", False
    ):
        extracted, extraction_findings = parse_project_references(repo_root, components)
        relationships.extend(extracted)
        extractor_findings.extend(extraction_findings)

    context = EvaluationContext(
        repo_root=repo_root,
        profile_path=profile_path,
        profile=profile,
        components=components,
        rules=rules,
        relationships=tuple(sorted(set(relationships), key=lambda item: (item.subject, item.predicate, item.object, item.evidence))),
        tracked_files=repository_files(repo_root),
    )
    findings.extend(extractor_findings)
    findings.extend(evaluate_relationship_rules(context))
    findings.extend(evaluate_mapping_rules(context))

    decisions_path = resolve_path(
        repo_root, args.decisions or profile.get("decision_gate", {}).get("decisions_path")
    )
    findings.extend(
        evaluate_decision_gate(
            repo_root,
            profile_path,
            profile,
            args.base,
            decisions_path,
        )
    )

    if args.command == "baseline":
        baseline, baseline_findings, waivers = set(), [], []
    else:
        baseline_path = resolve_path(
            repo_root, args.baseline or profile.get("baseline_path")
        )
        baseline, baseline_findings = baseline_fingerprints(
            baseline_path, profile["ontology_version"], profile_fingerprint(profile)
        )
        waivers_path = resolve_path(repo_root, args.waivers or profile.get("waivers_path"))
        waivers = load_waivers(waivers_path)
    findings.extend(baseline_findings)
    apply_baseline_and_waivers(findings, baseline, waivers)
    status = overall_status(findings)
    return report(args, profile, findings, status)


def report(
    args: argparse.Namespace,
    profile: dict[str, Any],
    findings: list[Finding],
    status: str,
) -> dict[str, Any]:
    sorted_findings = sorted(
        (finding.finalise() for finding in findings),
        key=lambda item: (
            not item.blocking,
            item.severity,
            item.code,
            item.rule_id or "",
            item.fingerprint,
        ),
    )
    return {
        "schema_version": 1,
        "hook": "all",
        "status": status,
        "exit_decision": "block" if status != "pass" else "pass",
        "ontology_version": profile.get("ontology_version"),
        "profile_sha256": profile_fingerprint(profile) if profile else None,
        "base_revision": args.base,
        "profile": str(args.profile),
        "findings": [asdict(finding) for finding in sorted_findings],
        "summary": {
            "blocking": sum(finding.blocking for finding in sorted_findings),
            "advisory": sum(not finding.blocking for finding in sorted_findings),
            "total": len(sorted_findings),
        },
    }


def render_human(result: dict[str, Any]) -> str:
    lines = [
        "Hook: ontology all",
        f"Status: {result['status']}",
        f"Blocks: {'true' if result['exit_decision'] == 'block' else 'false'}",
        f"Findings: {result['summary']['total']}",
        "",
    ]
    for finding in result["findings"]:
        marker = "BLOCK" if finding["blocking"] else "ADVISORY"
        lines.append(
            f"{marker} {finding['severity'].upper()}: {finding['code']} "
            f"[{finding['fingerprint']}] {finding['message']}"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_result(result: dict[str, Any], args: argparse.Namespace) -> None:
    text = (
        json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.json
        else render_human(result)
    )
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def create_baseline(result: dict[str, Any], output: Path, repo_root: Path) -> None:
    accepted = sorted(
        finding["fingerprint"]
        for finding in result["findings"]
        if finding["blocking"] and finding["code"] in BASELINE_ELIGIBLE_CODES
    )
    payload = {
        "schema_version": 1,
        "ontology_version": result.get("ontology_version"),
        "profile_sha256": result.get("profile_sha256"),
        "source_revision": git_lines(repo_root, ["rev-parse", "HEAD"]),
        "accepted_findings": accepted,
    }
    if isinstance(payload["source_revision"], list):
        payload["source_revision"] = payload["source_revision"][0] if payload["source_revision"] else None
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "baseline"))
    parser.add_argument("--profile", required=True, help="Path to the JSON constraint profile.")
    parser.add_argument("--repo-root", default=".", help="Repository root. Defaults to the current directory.")
    parser.add_argument("--base", help="Git base revision used by the semantic decision gate.")
    parser.add_argument("--baseline", help="Override the baseline path declared by the profile.")
    parser.add_argument("--waivers", help="Override the waivers path declared by the profile.")
    parser.add_argument("--decisions", help="Override the decisions path declared by the profile.")
    parser.add_argument("--json", action="store_true", help="Emit stable JSON output.")
    parser.add_argument("--output", help="Write output to a file instead of stdout.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = evaluate(args)
        if args.command == "baseline":
            if not args.output:
                raise GuardError("baseline requires --output to avoid implicit repository mutation")
            unsafe = [
                finding
                for finding in result["findings"]
                if finding["blocking"] and finding["code"] not in BASELINE_ELIGIBLE_CODES
            ]
            if unsafe:
                sys.stderr.write(
                    "ontology-guard: baseline refused because mandatory non-ratchetable "
                    "checks did not pass: "
                    + ", ".join(sorted({finding["code"] for finding in unsafe}))
                    + "\n"
                )
                return 1
            create_baseline(result, Path(args.output), Path(args.repo_root).resolve())
            return 0
        write_result(result, args)
        return 0 if result["status"] == "pass" else 1
    except GuardError as exc:
        sys.stderr.write(f"ontology-guard: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
