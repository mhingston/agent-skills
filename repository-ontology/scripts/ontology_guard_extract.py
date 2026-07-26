"""Repository observation and conformance checks for ontology-guard."""
from __future__ import annotations

import fnmatch
import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from ontology_guard_model import (
    EvaluationContext, Finding, Relationship, normalise_repo_path, rule_can_block,
)

def git_lines(repo_root: Path, args: Sequence[str]) -> list[str] | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return [line for line in result.stdout.splitlines() if line]


def repository_files(repo_root: Path) -> tuple[str, ...]:
    tracked = git_lines(repo_root, ["ls-files", "--cached", "--others", "--exclude-standard"])
    if tracked is not None:
        return tuple(sorted(set(PurePosixPath(item).as_posix() for item in tracked)))
    files = []
    for path in repo_root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            files.append(normalise_repo_path(path, repo_root))
    return tuple(sorted(files))


def component_for_path(path: str, components: dict[str, dict[str, Any]]) -> list[str]:
    matches: list[str] = []
    for component_id, component in components.items():
        for pattern in component.get("paths", []):
            if fnmatch.fnmatch(path, pattern):
                matches.append(component_id)
                break
    return sorted(matches)


def parse_project_references(
    repo_root: Path, components: dict[str, dict[str, Any]]
) -> tuple[list[Relationship], list[Finding]]:
    project_to_component: dict[str, str] = {}
    findings: list[Finding] = []
    for component_id, component in components.items():
        project = component.get("project")
        if project:
            project_to_component[PurePosixPath(project).as_posix()] = component_id

    relationships: list[Relationship] = []
    for project_path, source_component in sorted(project_to_component.items()):
        absolute = repo_root / project_path
        if not absolute.exists():
            findings.append(
                Finding(
                    code="ONTOLOGY_EXTRACTOR_INPUT_MISSING",
                    severity="error",
                    status="unavailable",
                    message=f"Configured project file does not exist: {project_path}.",
                    blocking=True,
                    subject=source_component,
                    paths=[project_path],
                ).finalise()
            )
            continue
        try:
            root = ET.parse(absolute).getroot()
        except (ET.ParseError, OSError) as exc:
            findings.append(
                Finding(
                    code="ONTOLOGY_EXTRACTOR_FAILED",
                    severity="error",
                    status="unavailable",
                    message=f"Could not parse {project_path}: {exc}.",
                    blocking=True,
                    subject=source_component,
                    paths=[project_path],
                ).finalise()
            )
            continue
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] != "ProjectReference":
                continue
            include = element.attrib.get("Include")
            if not include:
                continue
            referenced = (absolute.parent / include.replace("\\", os.sep)).resolve()
            referenced_path = normalise_repo_path(referenced, repo_root)
            target_component = project_to_component.get(referenced_path)
            if target_component is None:
                findings.append(
                    Finding(
                        code="ONTOLOGY_UNMAPPED_PROJECT_REFERENCE",
                        severity="warning",
                        status="indeterminate",
                        message=(
                            f"Project reference {project_path} -> {referenced_path} cannot be "
                            "resolved to a governed component."
                        ),
                        blocking=False,
                        subject=source_component,
                        predicate="dependsOn",
                        paths=[project_path, referenced_path],
                    ).finalise()
                )
                continue
            relationships.append(
                Relationship(
                    subject=source_component,
                    predicate="dependsOn",
                    object=target_component,
                    evidence=(project_path,),
                )
            )
    return relationships, findings


def explicit_relationships(profile: dict[str, Any]) -> list[Relationship]:
    result: list[Relationship] = []
    for item in profile.get("observed_relationships", []):
        if not isinstance(item, dict):
            continue
        subject = item.get("subject")
        predicate = item.get("predicate")
        object_id = item.get("object")
        if all(isinstance(value, str) and value for value in (subject, predicate, object_id)):
            evidence = item.get("evidence", [])
            result.append(
                Relationship(
                    subject=subject,
                    predicate=predicate,
                    object=object_id,
                    evidence=tuple(str(value) for value in evidence),
                )
            )
    return result


def endpoint_matches(
    component_id: str, prefix: str, rule: dict[str, Any], components: dict[str, dict[str, Any]]
) -> bool:
    exact = rule.get(prefix)
    expected_type = rule.get(f"{prefix}_type")
    if exact is not None and component_id != exact:
        return False
    if expected_type is not None and components.get(component_id, {}).get("type") != expected_type:
        return False
    return exact is not None or expected_type is not None


def evaluate_relationship_rules(context: EvaluationContext) -> list[Finding]:
    findings: list[Finding] = []
    for rule in context.rules:
        kind = rule.get("kind")
        if kind not in {"forbid-relationship", "require-relationship"}:
            continue
        predicate = rule["predicate"]
        matches = [
            rel
            for rel in context.relationships
            if rel.predicate == predicate
            and endpoint_matches(rel.subject, "subject", rule, context.components)
            and endpoint_matches(rel.object, "object", rule, context.components)
        ]
        blocking = rule_can_block(rule)
        severity = rule.get("severity", "error")
        if kind == "forbid-relationship":
            for rel in matches:
                findings.append(
                    Finding(
                        code="ONTOLOGY_FORBIDDEN_RELATIONSHIP",
                        severity=severity,
                        status="reject" if blocking else "indeterminate",
                        message=(
                            f"Rule {rule['id']} forbids {rel.subject} {rel.predicate} "
                            f"{rel.object}."
                        ),
                        blocking=blocking,
                        rule_id=rule["id"],
                        subject=rel.subject,
                        predicate=rel.predicate,
                        object=rel.object,
                        paths=list(rel.evidence),
                        evidence=[{"path": path, "kind": "repository"} for path in rel.evidence],
                    ).finalise()
                )
        elif not matches:
            findings.append(
                Finding(
                    code="ONTOLOGY_REQUIRED_RELATIONSHIP_MISSING",
                    severity=severity,
                    status="reject" if blocking else "indeterminate",
                    message=f"Rule {rule['id']} requires a {predicate} relationship that was not observed.",
                    blocking=blocking,
                    rule_id=rule["id"],
                    predicate=predicate,
                ).finalise()
            )
    return findings


def evaluate_mapping_rules(context: EvaluationContext) -> list[Finding]:
    findings: list[Finding] = []
    for rule in context.rules:
        if rule.get("kind") != "require-mapping":
            continue
        pattern = rule["path_glob"]
        required_type = rule.get("component_type")
        blocking = rule_can_block(rule)
        severity = rule.get("severity", "error")
        for path in context.tracked_files:
            if not fnmatch.fnmatch(path, pattern):
                continue
            matches = component_for_path(path, context.components)
            if required_type:
                matches = [
                    component_id
                    for component_id in matches
                    if context.components[component_id].get("type") == required_type
                ]
            if len(matches) == 1:
                continue
            if not matches:
                code = "ONTOLOGY_REQUIRED_MAPPING_MISSING"
                message = f"Rule {rule['id']} requires {path} to map to one governed component."
            else:
                code = "ONTOLOGY_MAPPING_AMBIGUOUS"
                message = f"Rule {rule['id']} maps {path} to multiple components: {', '.join(matches)}."
            findings.append(
                Finding(
                    code=code,
                    severity=severity,
                    status="reject" if blocking else "indeterminate",
                    message=message,
                    blocking=blocking,
                    rule_id=rule["id"],
                    paths=[path],
                ).finalise()
            )
    return findings

