"""Decision, baseline, waiver, and outcome policy for ontology-guard."""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from ontology_guard_extract import git_lines
from ontology_guard_model import (
    BASELINE_ELIGIBLE_CODES, WAIVER_ELIGIBLE_CODES, Finding, GuardError, load_json,
    normalise_repo_path, rule_can_block,
)

def profile_from_git(repo_root: Path, base: str, profile_path: Path) -> dict[str, Any] | None:
    try:
        relative = profile_path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return None
    lines = git_lines(repo_root, ["show", f"{base}:{relative}"])
    if lines is None:
        return None
    try:
        value = json.loads("\n".join(lines))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def semantic_changes(old: dict[str, Any], new: dict[str, Any]) -> list[tuple[str, str]]:
    changes: list[tuple[str, str]] = []
    old_components = {item["id"]: item for item in old.get("components", []) if isinstance(item, dict) and "id" in item}
    new_components = {item["id"]: item for item in new.get("components", []) if isinstance(item, dict) and "id" in item}
    for component_id in sorted(new_components.keys() - old_components.keys()):
        changes.append((component_id, "component-added"))
    for component_id in sorted(old_components.keys() - new_components.keys()):
        changes.append((component_id, "component-removed"))
    material_component_fields = ("type", "paths", "project", "assertion_status")
    for component_id in sorted(old_components.keys() & new_components.keys()):
        if any(old_components[component_id].get(key) != new_components[component_id].get(key) for key in material_component_fields):
            changes.append((component_id, "component-semantics-changed"))

    old_rules = {item["id"]: item for item in old.get("rules", []) if isinstance(item, dict) and "id" in item}
    new_rules = {item["id"]: item for item in new.get("rules", []) if isinstance(item, dict) and "id" in item}
    for rule_id in sorted(new_rules.keys() - old_rules.keys()):
        changes.append((rule_id, "rule-added"))
    for rule_id in sorted(old_rules.keys() - new_rules.keys()):
        changes.append((rule_id, "rule-removed"))
    for rule_id in sorted(old_rules.keys() & new_rules.keys()):
        if old_rules[rule_id] != new_rules[rule_id]:
            changes.append((rule_id, "rule-changed"))
    return changes


def load_decisions(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    value = load_json(path, "decisions")
    if isinstance(value, dict):
        value = value.get("decisions", [])
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def has_accepted_decision(
    decisions: Iterable[dict[str, Any]], affected_id: str, change_kind: str
) -> bool:
    for decision in decisions:
        if decision.get("status") != "accepted":
            continue
        affects = decision.get("affects", [])
        kinds = decision.get("change_kinds", ["*"])
        if affected_id in affects and ("*" in kinds or change_kind in kinds):
            return True
    return False


def evaluate_decision_gate(
    repo_root: Path,
    profile_path: Path,
    profile: dict[str, Any],
    base: str | None,
    decisions_path: Path | None,
) -> list[Finding]:
    gate = profile.get("decision_gate", {})
    if not isinstance(gate, dict) or not gate.get("enabled", False):
        return []
    blocking = gate.get("enforcement", "block") == "block"
    if not base:
        return [
            Finding(
                code="ONTOLOGY_DECISION_BASE_UNAVAILABLE",
                severity="error",
                status="indeterminate",
                message="Decision gate is enabled but no --base revision was supplied.",
                blocking=blocking,
            ).finalise()
        ]
    old_profile = profile_from_git(repo_root, base, profile_path)
    if old_profile is None:
        return [
            Finding(
                code="ONTOLOGY_DECISION_BASE_UNAVAILABLE",
                severity="error",
                status="unavailable",
                message=f"Could not read the ontology profile at base revision {base}.",
                blocking=blocking,
            ).finalise()
        ]
    decisions = load_decisions(decisions_path)
    findings: list[Finding] = []
    for affected_id, change_kind in semantic_changes(old_profile, profile):
        if has_accepted_decision(decisions, affected_id, change_kind):
            continue
        findings.append(
            Finding(
                code="ONTOLOGY_UNPAIRED_SEMANTIC_CHANGE",
                severity="error",
                status="reject" if blocking else "indeterminate",
                message=(
                    f"{change_kind} for {affected_id} lacks an accepted decision "
                    "covering that semantic change."
                ),
                blocking=blocking,
                subject=affected_id,
            ).finalise()
        )
    return findings


def profile_fingerprint(profile: dict[str, Any]) -> str:
    encoded = json.dumps(profile, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def baseline_fingerprints(
    path: Path | None, ontology_version: str, active_profile_sha256: str
) -> tuple[set[str], list[Finding]]:
    if path is None or not path.exists():
        return set(), []
    value = load_json(path, "baseline")
    if not isinstance(value, dict):
        raise GuardError(f"baseline must be a JSON object: {path}")
    if value.get("schema_version") != 1:
        raise GuardError(f"baseline schema_version must be 1: {path}")
    if (
        value.get("ontology_version") != ontology_version
        or value.get("profile_sha256") != active_profile_sha256
    ):
        return set(), [
            Finding(
                code="ONTOLOGY_BASELINE_STALE",
                severity="error",
                status="indeterminate",
                message=(
                    "Baseline ontology_version or profile_sha256 does not match the "
                    "active profile; review and regenerate the baseline explicitly."
                ),
                blocking=True,
                paths=[normalise_repo_path(path, path.parent)],
            ).finalise()
        ]
    fingerprints = value.get("accepted_findings", [])
    return {str(item) for item in fingerprints}, []


def load_waivers(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    value = load_json(path, "waivers")
    if isinstance(value, dict):
        value = value.get("waivers", [])
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def apply_baseline_and_waivers(
    findings: list[Finding], baseline: set[str], waivers: Iterable[dict[str, Any]]
) -> None:
    today = date.today()
    by_fingerprint = {
        waiver.get("finding_fingerprint"): waiver
        for waiver in waivers
        if isinstance(waiver.get("finding_fingerprint"), str)
    }
    for finding in findings:
        finding.finalise()
        if finding.code in BASELINE_ELIGIBLE_CODES and finding.fingerprint in baseline:
            finding.blocking = False
            finding.disposition = "baseline"
            continue
        if finding.code not in WAIVER_ELIGIBLE_CODES or finding.status != "reject":
            continue
        waiver = by_fingerprint.get(finding.fingerprint)
        if waiver is None:
            continue
        expiry = waiver.get("expires_at")
        try:
            expired = not isinstance(expiry, str) or date.fromisoformat(expiry) < today
        except ValueError:
            expired = True
        if expired:
            finding.disposition = "expired-waiver"
            finding.waiver_id = str(waiver.get("id", "unknown"))
            finding.message += f" Matching waiver {finding.waiver_id} is expired or invalid."
            continue
        if not waiver.get("approved_by") or not waiver.get("reason"):
            finding.disposition = "invalid-waiver"
            finding.waiver_id = str(waiver.get("id", "unknown"))
            finding.message += f" Matching waiver {finding.waiver_id} lacks approval or rationale."
            continue
        finding.blocking = False
        finding.disposition = "waived"
        finding.waiver_id = str(waiver.get("id", "unknown"))


def overall_status(findings: Iterable[Finding]) -> str:
    blocking = [finding for finding in findings if finding.blocking]
    if not blocking:
        return "pass"
    if any(finding.status == "reject" for finding in blocking):
        return "reject"
    if any(finding.status == "unavailable" for finding in blocking):
        return "unavailable"
    return "indeterminate"

