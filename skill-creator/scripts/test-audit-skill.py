#!/usr/bin/env python3
"""Tests for audit-skill.py using only the Python standard library."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("audit-skill.py")


def run_audit(skill_dir: Path, *args: str) -> tuple[int, dict[str, object]]:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), str(skill_dir), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if not completed.stdout:
        raise AssertionError(f"audit produced no JSON output: {completed.stderr}")
    return completed.returncode, json.loads(completed.stdout)


def write_skill(root: Path, body: str, resources: dict[str, str] | None = None) -> Path:
    root.mkdir()
    (root / "SKILL.md").write_text(body, encoding="utf-8")
    for relative_path, content in (resources or {}).items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return root


def finding_codes(report: dict[str, object]) -> set[str]:
    findings = report["findings"]
    assert isinstance(findings, list)
    return {str(item["code"]) for item in findings}


def test_valid_package() -> None:
    with tempfile.TemporaryDirectory() as temp:
        skill = write_skill(
            Path(temp) / "demo",
            """---
name: demo
description: Demonstrate a valid package.
---
# Demo

Read [the guide](references/guide.md).
See [external docs](https://example.com/references/not-local.md).
Run `scripts/run.py`.
""",
            {
                "references/guide.md": "# Guide\n",
                "scripts/run.py": "print('ok')\n",
            },
        )
        code, report = run_audit(skill)
        assert code == 0
        assert report["summary"] == {"error": 0, "info": 0, "warning": 0}
        assert report["facts"]["resource_references"] == [
            "references/guide.md",
            "scripts/run.py",
        ]


def test_structural_findings_and_fail_threshold() -> None:
    with tempfile.TemporaryDirectory() as temp:
        skill = write_skill(
            Path(temp) / "demo",
            """---
name: other
description: Broken package.
context: fork
---
# Demo

Read [missing](references/missing.md).
Run `scripts/missing.py`.
""",
        )
        code, report = run_audit(skill, "--fail-on", "error")
        assert code == 1
        assert {
            "frontmatter-unknown-key",
            "skill-name-mismatch",
            "resource-missing",
        }.issubset(finding_codes(report))


def test_package_escape() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        (root / "shared.md").write_text("shared\n", encoding="utf-8")
        skill = write_skill(
            root / "demo",
            """---
name: demo
description: Escape example.
---
# Demo

Read [shared](../shared.md).
""",
        )
        _, report = run_audit(skill)
        assert "resource-package-escape" in finding_codes(report)


def test_line_threshold_warning() -> None:
    with tempfile.TemporaryDirectory() as temp:
        lines = [
            "---",
            "name: demo",
            "description: Large example.",
            "---",
            "# Demo",
            *["instruction" for _ in range(8)],
        ]
        skill = write_skill(Path(temp) / "demo", "\n".join(lines) + "\n")
        code, report = run_audit(skill, "--max-lines", "10", "--fail-on", "warning")
        assert code == 1
        assert "active-instructions-large" in finding_codes(report)


def main() -> int:
    tests = [
        test_valid_package,
        test_structural_findings_and_fail_threshold,
        test_package_escape,
        test_line_threshold_warning,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
