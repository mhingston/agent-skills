#!/usr/bin/env python3
"""Validate a lightweight project-context index.

The index is intentionally small: it gives agents and deterministic tooling stable
record identities and relationships without prescribing where project documentation
must live.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


KINDS = {"truth", "intent", "history", "scratch"}
AUTHORITIES = {"canonical", "derived", "informational"}
STATES = {"active", "superseded", "archived"}
REQUIRED_FIELDS = {"id", "kind", "path", "authority", "state"}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    record_id: str | None = None

    def as_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.record_id is not None:
            result["record_id"] = self.record_id
        return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a project-context JSON index and its local references."
    )
    parser.add_argument("index", type=Path, help="Path to the context index JSON file")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository/project root used to resolve record paths (default: cwd)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text)",
    )
    return parser.parse_args()


def load_index(path: Path) -> tuple[Any | None, list[Finding]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle), []
    except FileNotFoundError:
        return None, [Finding("INDEX_NOT_FOUND", f"Index does not exist: {path}")]
    except json.JSONDecodeError as exc:
        return None, [
            Finding(
                "INVALID_JSON",
                f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            )
        ]
    except OSError as exc:
        return None, [Finding("INDEX_UNREADABLE", f"Cannot read index: {exc}")]


def validate_index(data: Any, root: Path) -> list[Finding]:
    findings: list[Finding] = []

    if not isinstance(data, dict):
        return [Finding("INVALID_ROOT", "Index root must be a JSON object.")]

    if data.get("schema_version") != "1":
        findings.append(
            Finding(
                "INVALID_SCHEMA_VERSION",
                "schema_version must be the string \"1\".",
            )
        )

    records = data.get("records")
    if not isinstance(records, list):
        findings.append(Finding("INVALID_RECORDS", "records must be a JSON array."))
        return findings

    root_resolved = root.resolve()
    seen_ids: set[str] = set()
    valid_ids: set[str] = set()
    parsed_records: list[dict[str, Any]] = []

    for index, raw_record in enumerate(records):
        synthetic_id = f"record[{index}]"
        if not isinstance(raw_record, dict):
            findings.append(
                Finding("INVALID_RECORD", "Record must be a JSON object.", synthetic_id)
            )
            continue

        record_id = raw_record.get("id")
        display_id = record_id if isinstance(record_id, str) and record_id else synthetic_id

        missing = sorted(field for field in REQUIRED_FIELDS if field not in raw_record)
        if missing:
            findings.append(
                Finding(
                    "MISSING_FIELDS",
                    f"Missing required fields: {', '.join(missing)}.",
                    display_id,
                )
            )

        if not isinstance(record_id, str) or not record_id.strip():
            findings.append(
                Finding("INVALID_ID", "id must be a non-empty string.", display_id)
            )
        elif record_id in seen_ids:
            findings.append(
                Finding("DUPLICATE_ID", f"Duplicate record id: {record_id}.", record_id)
            )
        else:
            seen_ids.add(record_id)
            valid_ids.add(record_id)

        kind = raw_record.get("kind")
        if kind not in KINDS:
            findings.append(
                Finding(
                    "INVALID_KIND",
                    f"kind must be one of: {', '.join(sorted(KINDS))}.",
                    display_id,
                )
            )

        authority = raw_record.get("authority")
        if authority not in AUTHORITIES:
            findings.append(
                Finding(
                    "INVALID_AUTHORITY",
                    f"authority must be one of: {', '.join(sorted(AUTHORITIES))}.",
                    display_id,
                )
            )

        state = raw_record.get("state")
        if state not in STATES:
            findings.append(
                Finding(
                    "INVALID_STATE",
                    f"state must be one of: {', '.join(sorted(STATES))}.",
                    display_id,
                )
            )

        refs = raw_record.get("refs", [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref for ref in refs):
            findings.append(
                Finding("INVALID_REFS", "refs must be an array of non-empty strings.", display_id)
            )

        record_path = raw_record.get("path")
        if not isinstance(record_path, str) or not record_path.strip():
            findings.append(
                Finding("INVALID_PATH", "path must be a non-empty string.", display_id)
            )
        else:
            candidate = Path(record_path)
            if candidate.is_absolute():
                findings.append(
                    Finding("ABSOLUTE_PATH", "path must be relative to --root.", display_id)
                )
            else:
                resolved = (root_resolved / candidate).resolve()
                try:
                    resolved.relative_to(root_resolved)
                except ValueError:
                    findings.append(
                        Finding("PATH_ESCAPE", "path escapes the configured --root.", display_id)
                    )
                else:
                    if not resolved.exists():
                        findings.append(
                            Finding(
                                "MISSING_PATH",
                                f"Referenced path does not exist: {record_path}.",
                                display_id,
                            )
                        )

        if kind == "scratch" and authority == "canonical":
            findings.append(
                Finding(
                    "CANONICAL_SCRATCH",
                    "Scratch records cannot be canonical authority.",
                    display_id,
                )
            )

        if authority == "canonical" and state in {"superseded", "archived"}:
            findings.append(
                Finding(
                    "INACTIVE_CANONICAL",
                    "A superseded or archived record cannot remain canonical authority.",
                    display_id,
                )
            )

        parsed_records.append(raw_record)

    for index, record in enumerate(parsed_records):
        record_id = record.get("id")
        display_id = record_id if isinstance(record_id, str) and record_id else f"record[{index}]"
        refs = record.get("refs", [])
        if not isinstance(refs, list):
            continue
        for ref in refs:
            if isinstance(ref, str) and ref and ref not in valid_ids:
                findings.append(
                    Finding(
                        "UNRESOLVED_REF",
                        f"Reference does not resolve to a record id: {ref}.",
                        display_id,
                    )
                )

    return findings


def emit(findings: list[Finding], output_format: str) -> None:
    if output_format == "json":
        payload = {
            "valid": not findings,
            "finding_count": len(findings),
            "findings": [finding.as_dict() for finding in findings],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    if not findings:
        print("VALID: project context index passed all checks.")
        return

    print(f"INVALID: {len(findings)} finding(s).")
    for finding in findings:
        location = f" [{finding.record_id}]" if finding.record_id else ""
        print(f"- {finding.code}{location}: {finding.message}")


def main() -> int:
    args = parse_args()
    data, load_findings = load_index(args.index)
    findings = list(load_findings)
    if data is not None:
        findings.extend(validate_index(data, args.root))
    emit(findings, args.format)
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
