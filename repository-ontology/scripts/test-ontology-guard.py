#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).with_name("ontology-guard.py")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def base_profile() -> dict:
    return {
        "schema_version": 1,
        "ontology_version": "1.0.0",
        "components": [
            {
                "id": "component.web",
                "type": "presentation-component",
                "assertion_status": "confirmed",
                "paths": ["src/Web/**"],
                "project": "src/Web/Web.csproj",
            },
            {
                "id": "component.database",
                "type": "database-component",
                "assertion_status": "confirmed",
                "paths": ["src/Database/**"],
                "project": "src/Database/Database.csproj",
            },
        ],
        "extractors": {"dotnet-project-references": {"enabled": True}},
        "rules": [
            {
                "id": "ARCH-001",
                "kind": "forbid-relationship",
                "predicate": "dependsOn",
                "subject_type": "presentation-component",
                "object_type": "database-component",
                "assertion_status": "confirmed",
                "enforcement": "block",
                "severity": "error",
            }
        ],
    }


class OntologyGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        (self.repo / "src/Web").mkdir(parents=True)
        (self.repo / "src/Database").mkdir(parents=True)
        (self.repo / "src/Database/Database.csproj").write_text(
            '<Project Sdk="Microsoft.NET.Sdk"></Project>\n', encoding="utf-8"
        )
        (self.repo / "src/Web/Web.csproj").write_text(
            '<Project Sdk="Microsoft.NET.Sdk"><ItemGroup>'
            '<ProjectReference Include="../Database/Database.csproj" />'
            '</ItemGroup></Project>\n',
            encoding="utf-8",
        )
        self.profile_path = self.repo / "ontology-guard.json"
        write_json(self.profile_path, base_profile())

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_guard(self, *extra: str) -> tuple[subprocess.CompletedProcess[str], dict | None]:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "check",
                "--repo-root",
                str(self.repo),
                "--profile",
                "ontology-guard.json",
                "--json",
                *extra,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        payload = json.loads(result.stdout) if result.stdout else None
        return result, payload

    def test_confirmed_forbidden_dependency_blocks(self) -> None:
        result, payload = self.run_guard()
        self.assertEqual(result.returncode, 1, result.stderr)
        assert payload is not None
        self.assertEqual(payload["status"], "reject")
        self.assertEqual(payload["summary"]["blocking"], 1)
        self.assertEqual(payload["findings"][0]["code"], "ONTOLOGY_FORBIDDEN_RELATIONSHIP")

    def test_inferred_rule_cannot_be_configured_to_block(self) -> None:
        profile = base_profile()
        profile["rules"][0]["assertion_status"] = "inferred"
        write_json(self.profile_path, profile)
        result, payload = self.run_guard()
        self.assertEqual(result.returncode, 1)
        assert payload is not None
        codes = {finding["code"] for finding in payload["findings"]}
        self.assertIn("ONTOLOGY_UNCONFIRMED_BLOCKING_RULE", codes)

    def test_inferred_advisory_rule_reports_without_blocking(self) -> None:
        profile = base_profile()
        profile["rules"][0]["assertion_status"] = "inferred"
        profile["rules"][0]["enforcement"] = "advisory"
        write_json(self.profile_path, profile)
        result, payload = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        assert payload is not None
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["summary"]["advisory"], 1)

    def test_baseline_ratchets_exact_existing_finding(self) -> None:
        first, payload = self.run_guard()
        self.assertEqual(first.returncode, 1)
        assert payload is not None
        fingerprint = payload["findings"][0]["fingerprint"]
        profile = base_profile()
        profile["baseline_path"] = "baseline.json"
        write_json(self.profile_path, profile)
        profile_sha256 = hashlib.sha256(
            json.dumps(profile, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        write_json(
            self.repo / "baseline.json",
            {
                "schema_version": 1,
                "ontology_version": "1.0.0",
                "profile_sha256": profile_sha256,
                "accepted_findings": [fingerprint],
            },
        )
        result, second = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        assert second is not None
        finding = next(item for item in second["findings"] if item["code"] == "ONTOLOGY_FORBIDDEN_RELATIONSHIP")
        self.assertEqual(finding["disposition"], "baseline")
        self.assertFalse(finding["blocking"])

    def test_expired_waiver_does_not_suppress_violation(self) -> None:
        first, payload = self.run_guard()
        assert payload is not None
        fingerprint = payload["findings"][0]["fingerprint"]
        write_json(
            self.repo / "waivers.json",
            {
                "waivers": [
                    {
                        "id": "WAIVER-1",
                        "finding_fingerprint": fingerprint,
                        "reason": "Migration",
                        "approved_by": "team.architecture",
                        "expires_at": (date.today() - timedelta(days=1)).isoformat(),
                    }
                ]
            },
        )
        profile = base_profile()
        profile["waivers_path"] = "waivers.json"
        write_json(self.profile_path, profile)
        result, second = self.run_guard()
        self.assertEqual(result.returncode, 1)
        assert second is not None
        finding = next(item for item in second["findings"] if item["code"] == "ONTOLOGY_FORBIDDEN_RELATIONSHIP")
        self.assertEqual(finding["disposition"], "expired-waiver")
        self.assertTrue(finding["blocking"])

    def test_valid_waiver_suppresses_exact_violation(self) -> None:
        _, payload = self.run_guard()
        assert payload is not None
        fingerprint = payload["findings"][0]["fingerprint"]
        write_json(
            self.repo / "waivers.json",
            {
                "waivers": [
                    {
                        "id": "WAIVER-1",
                        "finding_fingerprint": fingerprint,
                        "reason": "Time-bounded migration",
                        "approved_by": "team.architecture",
                        "expires_at": (date.today() + timedelta(days=30)).isoformat(),
                    }
                ]
            },
        )
        profile = base_profile()
        profile["waivers_path"] = "waivers.json"
        write_json(self.profile_path, profile)
        result, second = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stderr)
        assert second is not None
        finding = next(item for item in second["findings"] if item["code"] == "ONTOLOGY_FORBIDDEN_RELATIONSHIP")
        self.assertEqual(finding["disposition"], "waived")
        self.assertFalse(finding["blocking"])

    def test_baseline_command_writes_only_ratchetable_findings(self) -> None:
        output = self.repo / "generated-baseline.json"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "baseline",
                "--repo-root",
                str(self.repo),
                "--profile",
                "ontology-guard.json",
                "--output",
                str(output),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(payload["ontology_version"], "1.0.0")
        self.assertEqual(len(payload["accepted_findings"]), 1)

    def test_baseline_refuses_unavailable_extractor(self) -> None:
        (self.repo / "src/Web/Web.csproj").unlink()
        output = self.repo / "generated-baseline.json"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "baseline",
                "--repo-root",
                str(self.repo),
                "--profile",
                "ontology-guard.json",
                "--output",
                str(output),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertFalse(output.exists())
        self.assertIn("baseline refused", result.stderr)

    def test_stale_baseline_blocks_instead_of_suppressing(self) -> None:
        first, payload = self.run_guard()
        self.assertEqual(first.returncode, 1)
        assert payload is not None
        fingerprint = payload["findings"][0]["fingerprint"]
        baseline = self.repo / "baseline.json"
        write_json(
            baseline,
            {
                "schema_version": 1,
                "ontology_version": "1.0.0",
                "profile_sha256": "0" * 64,
                "accepted_findings": [fingerprint],
            },
        )
        result, stale = self.run_guard("--baseline", "baseline.json")
        self.assertEqual(result.returncode, 1)
        assert stale is not None
        codes = {finding["code"] for finding in stale["findings"]}
        self.assertIn("ONTOLOGY_BASELINE_STALE", codes)
        forbidden = next(
            finding
            for finding in stale["findings"]
            if finding["code"] == "ONTOLOGY_FORBIDDEN_RELATIONSHIP"
        )
        self.assertTrue(forbidden["blocking"])
        self.assertEqual(forbidden["disposition"], "new")

    def test_semantic_change_requires_accepted_decision(self) -> None:
        subprocess.run(["git", "init", "--quiet"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.repo, check=True)
        profile = base_profile()
        profile["decision_gate"] = {
            "enabled": True,
            "enforcement": "block",
            "decisions_path": "decisions.json",
        }
        profile["rules"] = []
        write_json(self.profile_path, profile)
        subprocess.run(["git", "add", "."], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "--quiet", "-m", "baseline"], cwd=self.repo, check=True)

        profile["components"].append(
            {
                "id": "component.application",
                "type": "application-component",
                "assertion_status": "confirmed",
                "paths": ["src/Application/**"],
            }
        )
        write_json(self.profile_path, profile)
        result, payload = self.run_guard("--base", "HEAD")
        self.assertEqual(result.returncode, 1, result.stderr)
        assert payload is not None
        self.assertIn(
            "ONTOLOGY_UNPAIRED_SEMANTIC_CHANGE",
            {finding["code"] for finding in payload["findings"]},
        )

        write_json(
            self.repo / "decisions.json",
            {
                "decisions": [
                    {
                        "id": "ADR-1",
                        "status": "accepted",
                        "affects": ["component.application"],
                        "change_kinds": ["component-added"],
                    }
                ]
            },
        )
        result, payload = self.run_guard("--base", "HEAD")
        self.assertEqual(result.returncode, 0, result.stderr)
        assert payload is not None
        self.assertEqual(payload["status"], "pass")


if __name__ == "__main__":
    unittest.main()
