#!/usr/bin/env python3
"""Deterministic preflight for an Agent Skill package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
REQUIRED_FRONTMATTER_KEYS = {"name", "description"}
TOP_LEVEL_KEY = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
PACKAGE_PATH = re.compile(
    r"(?<![A-Za-z0-9._/-])((?:scripts|references|assets)/"
    r"(?:[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*))"
)
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


def finding(severity: str, code: str, message: str, path: str = "SKILL.md") -> dict[str, str]:
    return {
        "severity": severity,
        "code": code,
        "path": path,
        "message": message,
    }


def parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], list[dict[str, str]], int | None]:
    findings: list[dict[str, str]] = []
    values: dict[str, str] = {}

    if not lines or lines[0].strip() != "---":
        findings.append(
            finding(
                "error",
                "frontmatter-missing",
                "SKILL.md must start with YAML frontmatter delimited by '---'.",
            )
        )
        return values, findings, None

    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break

    if end is None:
        findings.append(
            finding(
                "error",
                "frontmatter-unclosed",
                "The opening frontmatter delimiter has no closing '---'.",
            )
        )
        return values, findings, None

    seen: set[str] = set()
    for line in lines[1:end]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL_KEY.match(line)
        if not match:
            continue
        key, value = match.group(1), (match.group(2) or "").strip()
        if key in seen:
            findings.append(
                finding(
                    "error",
                    "frontmatter-duplicate-key",
                    f"Top-level frontmatter key '{key}' is declared more than once.",
                )
            )
            continue
        seen.add(key)
        values[key] = value

    for key in sorted(REQUIRED_FRONTMATTER_KEYS - values.keys()):
        findings.append(
            finding(
                "error",
                "frontmatter-required-key-missing",
                f"Required top-level frontmatter key '{key}' is missing.",
            )
        )

    for key in sorted(values.keys() - ALLOWED_FRONTMATTER_KEYS):
        findings.append(
            finding(
                "error",
                "frontmatter-unknown-key",
                f"Top-level frontmatter key '{key}' is not part of the canonical skill contract.",
            )
        )

    return values, findings, end


def scalar_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def markdown_target(raw: str) -> str | None:
    target = raw.strip()
    if target.startswith("<"):
        close = target.find(">")
        if close == -1:
            return target[1:]
        target = target[1:close]
    else:
        target = target.split(maxsplit=1)[0] if target else ""

    if not target or target.startswith("#"):
        return None

    target = unquote(target)
    if re.match(r"^[A-Za-z]:[\\/]", target):
        return target

    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    return parsed.path or None


def referenced_paths(text: str) -> set[str]:
    refs: set[str] = set()

    for match in MARKDOWN_LINK.finditer(text):
        target = markdown_target(match.group(1))
        if target:
            refs.add(target)

    refs.update(match.group(1) for match in PACKAGE_PATH.finditer(text))
    return refs


def within(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def audit(skill_dir: Path, max_lines: int) -> dict[str, object]:
    root = skill_dir.resolve()
    skill_md = root / "SKILL.md"
    findings: list[dict[str, str]] = []

    if not skill_md.is_file():
        findings.append(
            finding(
                "error",
                "skill-md-missing",
                "The target directory does not contain SKILL.md.",
            )
        )
        return result(root.name, None, {}, [], findings)

    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()

    frontmatter, frontmatter_findings, _ = parse_frontmatter(lines)
    findings.extend(frontmatter_findings)

    frontmatter_name = scalar_value(frontmatter.get("name", ""))
    if frontmatter_name and frontmatter_name != root.name:
        findings.append(
            finding(
                "error",
                "skill-name-mismatch",
                f"Frontmatter name '{frontmatter_name}' does not match directory name '{root.name}'.",
            )
        )

    if max_lines > 0 and len(lines) > max_lines:
        findings.append(
            finding(
                "warning",
                "active-instructions-large",
                f"SKILL.md has {len(lines)} lines, above the configured {max_lines}-line review threshold.",
            )
        )

    refs = sorted(referenced_paths(text))
    for ref in refs:
        if re.match(r"^[A-Za-z]:[\\/]", ref) or Path(ref).is_absolute():
            findings.append(
                finding(
                    "error",
                    "resource-absolute-path",
                    f"Resource reference '{ref}' is machine-specific; use a package-relative path.",
                    ref,
                )
            )
            continue

        candidate = (root / ref).resolve()
        if not within(root, candidate):
            findings.append(
                finding(
                    "error",
                    "resource-package-escape",
                    f"Resource reference '{ref}' escapes the skill package.",
                    ref,
                )
            )
            continue

        if not candidate.exists():
            findings.append(
                finding(
                    "error",
                    "resource-missing",
                    f"Referenced package resource '{ref}' does not exist.",
                    ref,
                )
            )

    return result(root.name, len(lines), frontmatter, refs, findings)


def result(
    skill: str,
    line_count: int | None,
    frontmatter: dict[str, str],
    refs: list[str],
    findings: list[dict[str, str]],
) -> dict[str, object]:
    findings = sorted(
        findings,
        key=lambda item: (
            SEVERITY_ORDER[item["severity"]],
            item["code"],
            item["path"],
            item["message"],
        ),
    )
    summary = {
        severity: sum(1 for item in findings if item["severity"] == severity)
        for severity in ("error", "warning", "info")
    }
    return {
        "version": 1,
        "skill": skill,
        "facts": {
            "line_count": line_count,
            "frontmatter_name": scalar_value(frontmatter.get("name", "")) or None,
            "frontmatter_keys": sorted(frontmatter),
            "resource_references": refs,
        },
        "summary": summary,
        "findings": findings,
    }


def should_fail(report: dict[str, object], threshold: str) -> bool:
    if threshold == "never":
        return False
    summary = report["summary"]
    assert isinstance(summary, dict)
    errors = int(summary.get("error", 0))
    warnings = int(summary.get("warning", 0))
    if threshold == "error":
        return errors > 0
    return errors > 0 or warnings > 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run deterministic package checks before semantic skill review."
    )
    parser.add_argument("skill_dir", help="Path to the target skill directory.")
    parser.add_argument(
        "--max-lines",
        type=int,
        default=500,
        help="Warn when SKILL.md exceeds this many lines; use 0 to disable.",
    )
    parser.add_argument(
        "--fail-on",
        choices=("never", "error", "warning"),
        default="never",
        help="Choose which finding severity should produce exit status 1.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON report.",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    if not skill_dir.exists() or not skill_dir.is_dir():
        parser.error(f"skill directory does not exist or is not a directory: {skill_dir}")

    report = audit(skill_dir, args.max_lines)
    print(
        json.dumps(
            report,
            indent=2 if args.pretty else None,
            sort_keys=True,
        )
    )
    return 1 if should_fail(report, args.fail_on) else 0


if __name__ == "__main__":
    sys.exit(main())
