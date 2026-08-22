#!/usr/bin/env python3
"""Regression tests for validate-context-record.py using only the stdlib."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("validate-context-record.py")


def run_validator(root: Path, index: dict) -> subprocess.CompletedProcess[str]:
    index_path = root / "context-index.json"
    index_path.write_text(json.dumps(index), encoding="utf-8")
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(index_path),
            "--root",
            str(root),
            "--format",
            "json",
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def payload(result: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(result.stdout)


def finding_codes(result: subprocess.CompletedProcess[str]) -> set[str]:
    return {finding["code"] for finding in payload(result)["findings"]}


def test_valid_index() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "docs").mkdir()
        (root / "docs" / "architecture.md").write_text("# Architecture\n", encoding="utf-8")
        (root / "docs" / "decision.md").write_text("# Decision\n", encoding="utf-8")

        result = run_validator(
            root,
            {
                "schema_version": "1",
                "records": [
                    {
                        "id": "ARCH-system",
                        "kind": "truth",
                        "path": "docs/architecture.md",
                        "authority": "canonical",
                        "state": "active",
                        "refs": ["DEC-1"],
                    },
                    {
                        "id": "DEC-1",
                        "kind": "history",
                        "path": "docs/decision.md",
                        "authority": "canonical",
                        "state": "active",
                    },
                ],
            },
        )

        assert result.returncode == 0, result.stdout + result.stderr
        assert payload(result)["valid"] is True
        assert payload(result)["findings"] == []


def test_structural_failures_are_precise() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "scratch.md").write_text("draft\n", encoding="utf-8")

        result = run_validator(
            root,
            {
                "schema_version": "1",
                "records": [
                    {
                        "id": "DRAFT-1",
                        "kind": "scratch",
                        "path": "scratch.md",
                        "authority": "canonical",
                        "state": "superseded",
                        "refs": ["MISSING"],
                    },
                    {
                        "id": "DRAFT-1",
                        "kind": "intent",
                        "path": "missing.md",
                        "authority": "informational",
                        "state": "active",
                    },
                ],
            },
        )

        assert result.returncode == 1
        codes = finding_codes(result)
        assert "CANONICAL_SCRATCH" in codes
        assert "INACTIVE_CANONICAL" in codes
        assert "DUPLICATE_ID" in codes
        assert "UNRESOLVED_REF" in codes
        assert "MISSING_PATH" in codes


def test_path_escape_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        result = run_validator(
            root,
            {
                "schema_version": "1",
                "records": [
                    {
                        "id": "OUTSIDE",
                        "kind": "truth",
                        "path": "../outside.md",
                        "authority": "informational",
                        "state": "active",
                    }
                ],
            },
        )

        assert result.returncode == 1
        assert "PATH_ESCAPE" in finding_codes(result)


def test_invalid_schema_version_is_rejected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        result = run_validator(
            root,
            {"schema_version": 1, "records": []},
        )

        assert result.returncode == 1
        assert "INVALID_SCHEMA_VERSION" in finding_codes(result)


def main() -> int:
    tests = [
        test_valid_index,
        test_structural_failures_are_precise,
        test_path_escape_is_rejected,
        test_invalid_schema_version_is_rejected,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"PASS {len(tests)} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
