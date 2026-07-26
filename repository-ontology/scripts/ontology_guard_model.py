"""Data model and structural validation for ontology-guard."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ALLOWED_ASSERTION_STATUSES = {
    "observed",
    "inferred",
    "confirmed",
    "disputed",
    "deprecated",
}
ALLOWED_ENFORCEMENT = {"block", "advisory"}
ALLOWED_RULE_KINDS = {
    "forbid-relationship",
    "require-relationship",
    "require-mapping",
}
ALLOWED_SEVERITIES = {"error", "warning", "info"}
BASELINE_ELIGIBLE_CODES = {
    "ONTOLOGY_FORBIDDEN_RELATIONSHIP",
    "ONTOLOGY_REQUIRED_RELATIONSHIP_MISSING",
    "ONTOLOGY_REQUIRED_MAPPING_MISSING",
    "ONTOLOGY_MAPPING_AMBIGUOUS",
}
WAIVER_ELIGIBLE_CODES = BASELINE_ELIGIBLE_CODES | {
    "ONTOLOGY_UNPAIRED_SEMANTIC_CHANGE",
}


class GuardError(RuntimeError):
    """Raised for invalid invocation or unreadable required inputs."""


@dataclass(frozen=True)
class Relationship:
    subject: str
    predicate: str
    object: str
    evidence: tuple[str, ...] = ()


@dataclass
class Finding:
    code: str
    severity: str
    status: str
    message: str
    blocking: bool
    rule_id: str | None = None
    subject: str | None = None
    predicate: str | None = None
    object: str | None = None
    paths: list[str] = field(default_factory=list)
    evidence: list[dict[str, str]] = field(default_factory=list)
    fingerprint: str = ""
    disposition: str = "new"
    waiver_id: str | None = None

    def finalise(self) -> "Finding":
        if not self.fingerprint:
            payload = {
                "code": self.code,
                "rule_id": self.rule_id,
                "subject": self.subject,
                "predicate": self.predicate,
                "object": self.object,
                "paths": sorted(self.paths),
            }
            encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
            self.fingerprint = hashlib.sha256(encoded).hexdigest()[:24]
        return self


@dataclass(frozen=True)
class EvaluationContext:
    repo_root: Path
    profile_path: Path
    profile: dict[str, Any]
    components: dict[str, dict[str, Any]]
    rules: list[dict[str, Any]]
    relationships: tuple[Relationship, ...]
    tracked_files: tuple[str, ...]


def load_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GuardError(f"{label} not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GuardError(f"{label} is not valid JSON: {path}: {exc}") from exc


def resolve_path(repo_root: Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def normalise_repo_path(path: Path, repo_root: Path) -> str:
    try:
        relative = path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        return path.resolve().as_posix()
    return relative.as_posix()


def rule_can_block(rule: dict[str, Any]) -> bool:
    return (
        rule.get("assertion_status") == "confirmed"
        and rule.get("enforcement") == "block"
    )


def structural_findings(profile: Any) -> list[Finding]:
    findings: list[Finding] = []

    def reject(code: str, message: str, path: str | None = None) -> None:
        findings.append(
            Finding(
                code=code,
                severity="error",
                status="reject",
                message=message,
                blocking=True,
                paths=[path] if path else [],
            ).finalise()
        )

    if not isinstance(profile, dict):
        reject("ONTOLOGY_PROFILE_INVALID", "Profile root must be a JSON object.")
        return findings
    if profile.get("schema_version") != 1:
        reject("ONTOLOGY_PROFILE_SCHEMA", "schema_version must be 1.")
    if not isinstance(profile.get("ontology_version"), str) or not profile.get(
        "ontology_version"
    ):
        reject("ONTOLOGY_PROFILE_VERSION", "ontology_version must be a non-empty string.")

    components = profile.get("components", [])
    if not isinstance(components, list):
        reject("ONTOLOGY_COMPONENTS_INVALID", "components must be an array.")
        components = []
    component_ids: set[str] = set()
    project_paths: set[str] = set()
    for index, component in enumerate(components):
        location = f"components[{index}]"
        if not isinstance(component, dict):
            reject("ONTOLOGY_COMPONENT_INVALID", f"{location} must be an object.")
            continue
        component_id = component.get("id")
        if not isinstance(component_id, str) or not component_id:
            reject("ONTOLOGY_COMPONENT_ID", f"{location}.id must be a non-empty string.")
        elif component_id in component_ids:
            reject("ONTOLOGY_DUPLICATE_COMPONENT", f"Duplicate component id: {component_id}.")
        else:
            component_ids.add(component_id)
        status = component.get("assertion_status")
        if status not in ALLOWED_ASSERTION_STATUSES:
            reject(
                "ONTOLOGY_COMPONENT_STATUS",
                f"{location}.assertion_status must be one of {sorted(ALLOWED_ASSERTION_STATUSES)}.",
            )
        component_type = component.get("type")
        if not isinstance(component_type, str) or not component_type:
            reject("ONTOLOGY_COMPONENT_TYPE", f"{location}.type must be a non-empty string.")
        paths = component.get("paths", [])
        if not isinstance(paths, list) or not all(isinstance(item, str) and item for item in paths):
            reject("ONTOLOGY_COMPONENT_PATHS", f"{location}.paths must be an array of non-empty strings.")
        project = component.get("project")
        if project is not None:
            if not isinstance(project, str) or not project:
                reject("ONTOLOGY_COMPONENT_PROJECT", f"{location}.project must be a non-empty string.")
            elif project in project_paths:
                reject("ONTOLOGY_DUPLICATE_PROJECT", f"Project path is mapped more than once: {project}.")
            else:
                project_paths.add(project)

    rules = profile.get("rules", [])
    if not isinstance(rules, list):
        reject("ONTOLOGY_RULES_INVALID", "rules must be an array.")
        rules = []
    rule_ids: set[str] = set()
    for index, rule in enumerate(rules):
        location = f"rules[{index}]"
        if not isinstance(rule, dict):
            reject("ONTOLOGY_RULE_INVALID", f"{location} must be an object.")
            continue
        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not rule_id:
            reject("ONTOLOGY_RULE_ID", f"{location}.id must be a non-empty string.")
        elif rule_id in rule_ids:
            reject("ONTOLOGY_DUPLICATE_RULE", f"Duplicate rule id: {rule_id}.")
        else:
            rule_ids.add(rule_id)
        if rule.get("kind") not in ALLOWED_RULE_KINDS:
            reject(
                "ONTOLOGY_RULE_KIND",
                f"{location}.kind must be one of {sorted(ALLOWED_RULE_KINDS)}.",
            )
        if rule.get("assertion_status") not in ALLOWED_ASSERTION_STATUSES:
            reject(
                "ONTOLOGY_RULE_STATUS",
                f"{location}.assertion_status must be explicit and recognised.",
            )
        if rule.get("enforcement") not in ALLOWED_ENFORCEMENT:
            reject(
                "ONTOLOGY_RULE_ENFORCEMENT",
                f"{location}.enforcement must be one of {sorted(ALLOWED_ENFORCEMENT)}.",
            )
        if rule.get("severity", "error") not in ALLOWED_SEVERITIES:
            reject(
                "ONTOLOGY_RULE_SEVERITY",
                f"{location}.severity must be one of {sorted(ALLOWED_SEVERITIES)}.",
            )
        if rule.get("enforcement") == "block" and rule.get("assertion_status") != "confirmed":
            reject(
                "ONTOLOGY_UNCONFIRMED_BLOCKING_RULE",
                f"Rule {rule_id or location} cannot block because its assertion_status is not confirmed.",
            )
        if rule.get("kind") in {"forbid-relationship", "require-relationship"}:
            if not isinstance(rule.get("predicate"), str) or not rule.get("predicate"):
                reject("ONTOLOGY_RULE_PREDICATE", f"{location}.predicate is required.")
            if not any(isinstance(rule.get(key), str) and rule.get(key) for key in ("subject", "subject_type")):
                reject("ONTOLOGY_RULE_SUBJECT", f"{location} requires subject or subject_type.")
            if not any(isinstance(rule.get(key), str) and rule.get(key) for key in ("object", "object_type")):
                reject("ONTOLOGY_RULE_OBJECT", f"{location} requires object or object_type.")
            for endpoint in ("subject", "object"):
                exact = rule.get(endpoint)
                if isinstance(exact, str) and exact and exact not in component_ids:
                    reject(
                        "ONTOLOGY_RULE_COMPONENT_UNKNOWN",
                        f"{location}.{endpoint} references unknown component {exact}.",
                    )
        if rule.get("kind") == "require-mapping":
            if not isinstance(rule.get("path_glob"), str) or not rule.get("path_glob"):
                reject("ONTOLOGY_RULE_PATH_GLOB", f"{location}.path_glob is required.")

    observed_relationships = profile.get("observed_relationships", [])
    if not isinstance(observed_relationships, list):
        reject("ONTOLOGY_RELATIONSHIPS_INVALID", "observed_relationships must be an array.")
    else:
        for index, relationship in enumerate(observed_relationships):
            location = f"observed_relationships[{index}]"
            if not isinstance(relationship, dict):
                reject("ONTOLOGY_RELATIONSHIP_INVALID", f"{location} must be an object.")
                continue
            for field_name in ("subject", "predicate", "object"):
                if not isinstance(relationship.get(field_name), str) or not relationship.get(field_name):
                    reject(
                        "ONTOLOGY_RELATIONSHIP_FIELD",
                        f"{location}.{field_name} must be a non-empty string.",
                    )
            for endpoint in ("subject", "object"):
                value = relationship.get(endpoint)
                if isinstance(value, str) and value and value not in component_ids:
                    reject(
                        "ONTOLOGY_RELATIONSHIP_COMPONENT_UNKNOWN",
                        f"{location}.{endpoint} references unknown component {value}.",
                    )

    extractors = profile.get("extractors", {})
    if not isinstance(extractors, dict):
        reject("ONTOLOGY_EXTRACTORS_INVALID", "extractors must be an object.")
    elif "dotnet-project-references" in extractors:
        dotnet = extractors["dotnet-project-references"]
        if not isinstance(dotnet, dict) or not isinstance(dotnet.get("enabled"), bool):
            reject(
                "ONTOLOGY_EXTRACTOR_CONFIG_INVALID",
                "extractors.dotnet-project-references.enabled must be boolean.",
            )

    decision_gate = profile.get("decision_gate", {})
    if not isinstance(decision_gate, dict):
        reject("ONTOLOGY_DECISION_GATE_INVALID", "decision_gate must be an object.")
    elif decision_gate:
        if not isinstance(decision_gate.get("enabled"), bool):
            reject("ONTOLOGY_DECISION_GATE_ENABLED", "decision_gate.enabled must be boolean.")
        if decision_gate.get("enforcement", "block") not in ALLOWED_ENFORCEMENT:
            reject(
                "ONTOLOGY_DECISION_GATE_ENFORCEMENT",
                "decision_gate.enforcement must be block or advisory.",
            )

    for path_field in ("baseline_path", "waivers_path"):
        value = profile.get(path_field)
        if value is not None and (not isinstance(value, str) or not value):
            reject("ONTOLOGY_PROFILE_PATH_INVALID", f"{path_field} must be a non-empty string.")

    return findings

