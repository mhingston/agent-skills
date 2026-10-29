"""Regression tests for deterministic README catalogue checks."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_skill_catalogue import check_catalogue


class CatalogueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ("alpha", "beta"):
            skill = self.root / name
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: test\n---\n", encoding="utf-8")

    def readme(self, entries: str) -> None:
        (self.root / "README.md").write_text(
            "## Public skill catalogue\n" + entries +
            "\n## Responsibility boundaries\n"
            "\nSee [alpha](alpha/SKILL.md) elsewhere.\n",
            encoding="utf-8",
        )

    def test_complete_catalogue_passes(self) -> None:
        self.readme("[alpha](alpha/SKILL.md)\n[beta](beta/SKILL.md)")
        self.assertEqual(check_catalogue(self.root), [])

    def test_missing_extra_and_duplicate_are_reported(self) -> None:
        self.readme(
            "[alpha](alpha/SKILL.md)\n[alpha](alpha/SKILL.md)\n"
            "[obsolete](obsolete/SKILL.md)"
        )
        findings = check_catalogue(self.root)
        self.assertTrue(any("unlisted top-level skill: beta" in x for x in findings))
        self.assertTrue(any("nonexistent skill: obsolete" in x for x in findings))
        self.assertTrue(any("duplicate catalogue entry: alpha" in x for x in findings))

    def test_missing_headings_fail_closed(self) -> None:
        (self.root / "README.md").write_text("No catalogue\n", encoding="utf-8")
        self.assertTrue(check_catalogue(self.root))


if __name__ == "__main__":
    unittest.main()
