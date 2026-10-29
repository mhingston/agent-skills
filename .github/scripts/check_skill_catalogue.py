#!/usr/bin/env python3
"""Check README catalogue links against the actual top-level skill packages."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ENTRY = re.compile(r"\]\((?:\./)?([a-z0-9][a-z0-9-]*)/SKILL\.md\)")
START = "## Public skill catalogue"
END = "## Responsibility boundaries"


def check_catalogue(root: Path) -> list[str]:
    readme = root / "README.md"
    if not readme.is_file():
        return ["README.md is missing"]
    text = readme.read_text(encoding="utf-8")
    if START not in text or END not in text:
        return ["README.md catalogue headings were not found"]
    section = text.split(START, 1)[1].split(END, 1)[0]
    mentions = ENTRY.findall(section)
    actual = {
        path.name
        for path in root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    listed = set(mentions)
    counts = Counter(mentions)
    findings = [
        f"unlisted top-level skill: {name}"
        for name in sorted(actual - listed)
    ]
    findings.extend(
        f"catalogue links to nonexistent skill: {name}"
        for name in sorted(listed - actual)
    )
    findings.extend(
        f"duplicate catalogue entry: {name} ({count} occurrences)"
        for name, count in sorted(counts.items())
        if count > 1
    )
    if not mentions:
        findings.append("no skill links found in README.md catalogue")
    return findings


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    findings = check_catalogue(root)
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}", file=sys.stderr)
        return 1
    print("README skill catalogue matches top-level skill packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
