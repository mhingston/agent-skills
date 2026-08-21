#!/usr/bin/env python3
"""Tests for aggregate-evals.py using only the Python standard library."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("aggregate-evals.py")


def make_result(*, case: str = "routine", trial: int = 1, condition: str, statuses=("passed", "failed"),
                duration_ms=100, tokens=200, prompt="Do the task", harness="test-harness", model="test-model"):
    return {
        "schema_version": 1,
        "case": case,
        "trial": trial,
        "condition": condition,
        "harness": harness,
        "model": model,
        "skill_version": "candidate-v1" if condition == "candidate" else "baseline-v0",
        "prompt": prompt,
        "inputs": ["fixture.txt"],
        "permissions": "read-write temp workspace",
        "environment": "isolated temp workspace",
        "duration_ms": duration_ms,
        "tokens": tokens,
        "checks": [
            {"id": f"check-{index}", "status": status, "evidence": f"evidence-{index}"}
            for index, status in enumerate(statuses, start=1)
        ],
        "notes": [],
    }


class AggregateEvalsTests(unittest.TestCase):
    def run_tool(self, results, *extra_args):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for index, result in enumerate(results):
                path = root / f"run-{index}" / "result.json"
                path.parent.mkdir(parents=True)
                path.write_text(json.dumps(result), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(root), *extra_args],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_aggregates_matched_pairs_and_deltas(self):
        candidate = make_result(condition="candidate", statuses=("passed", "passed"), duration_ms=120, tokens=250)
        baseline = make_result(condition="baseline", statuses=("passed", "failed"), duration_ms=100, tokens=200)
        completed = self.run_tool([candidate, baseline], "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["pairs"], 1)
        self.assertEqual(summary["paired_check_outcomes"]["candidate_wins"], 1)
        self.assertEqual(summary["paired_check_outcomes"]["ties"], 1)
        self.assertAlmostEqual(summary["delta"]["pooled_pass_rate"], 0.5)
        self.assertEqual(summary["delta"]["mean_duration_ms"], 20.0)
        self.assertEqual(summary["delta"]["mean_tokens"], 50.0)
        self.assertEqual(summary["paired_efficiency"]["eligible_pairs"], 0)
        markdown = self.run_tool([candidate, baseline]).stdout
        self.assertIn("## Run pass-rate variation", markdown)
        self.assertIn("## Paired efficiency regressions", markdown)
        self.assertIn("Candidate: **100.0% ± 0.0% (n=1)**", markdown)

    def test_flags_high_confidence_efficiency_regression(self):
        candidate = make_result(condition="candidate", statuses=("passed", "passed"), duration_ms=250, tokens=450)
        baseline = make_result(condition="baseline", statuses=("passed", "passed"), duration_ms=100, tokens=200)
        completed = self.run_tool([candidate, baseline], "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        efficiency = summary["paired_efficiency"]
        self.assertEqual(efficiency["eligible_pairs"], 1)
        self.assertEqual(efficiency["flagged_regressions"], 1)
        self.assertAlmostEqual(efficiency["flagged_pairs"][0]["token_ratio"], 2.25)
        self.assertAlmostEqual(efficiency["flagged_pairs"][0]["duration_ratio"], 2.5)
        markdown = self.run_tool([candidate, baseline]).stdout
        self.assertIn("| routine | 1 | 2.25× | 2.50× |", markdown)

    def test_does_not_flag_when_only_one_cost_metric_increases(self):
        candidate = make_result(condition="candidate", statuses=("passed",), duration_ms=80, tokens=500)
        baseline = make_result(condition="baseline", statuses=("passed",), duration_ms=100, tokens=200)
        completed = self.run_tool([candidate, baseline], "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        efficiency = json.loads(completed.stdout)["paired_efficiency"]
        self.assertEqual(efficiency["eligible_pairs"], 1)
        self.assertEqual(efficiency["flagged_regressions"], 0)

    def test_efficiency_screening_requires_both_conditions_to_fully_pass(self):
        candidate = make_result(condition="candidate", statuses=("passed", "failed"), duration_ms=300, tokens=600)
        baseline = make_result(condition="baseline", statuses=("passed", "passed"), duration_ms=100, tokens=200)
        completed = self.run_tool([candidate, baseline], "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        efficiency = json.loads(completed.stdout)["paired_efficiency"]
        self.assertEqual(efficiency["eligible_pairs"], 0)
        self.assertEqual(efficiency["flagged_regressions"], 0)
        self.assertEqual(efficiency["skipped"]["not_fully_passing"], 1)

    def test_by_case_counts_do_not_inherit_previous_cases(self):
        results = [
            make_result(case="first", condition="candidate", statuses=("passed",)),
            make_result(case="first", condition="baseline", statuses=("failed",)),
            make_result(case="second", condition="candidate", statuses=("failed",)),
            make_result(case="second", condition="baseline", statuses=("passed",)),
        ]
        completed = self.run_tool(results, "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["by_case"]["first"]["candidate_wins"], 1)
        self.assertEqual(summary["by_case"]["first"]["baseline_wins"], 0)
        self.assertEqual(summary["by_case"]["second"]["candidate_wins"], 0)
        self.assertEqual(summary["by_case"]["second"]["baseline_wins"], 1)

    def test_rejects_unmatched_pair(self):
        completed = self.run_tool([make_result(condition="candidate")])
        self.assertEqual(completed.returncode, 2)
        self.assertIn("missing condition(s): baseline", completed.stderr)

    def test_rejects_matched_metadata_mismatch(self):
        candidate = make_result(condition="candidate", prompt="Prompt A")
        baseline = make_result(condition="baseline", prompt="Prompt B")
        completed = self.run_tool([candidate, baseline])
        self.assertEqual(completed.returncode, 2)
        self.assertIn("matched field 'prompt' differs", completed.stderr)

    def test_allows_unverifiable_checks_and_missing_metrics(self):
        candidate = make_result(condition="candidate", statuses=("not_verifiable",), duration_ms=None, tokens=None)
        baseline = make_result(condition="baseline", statuses=("not_verifiable",), duration_ms=None, tokens=None)
        completed = self.run_tool([candidate, baseline], "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertIsNone(summary["conditions"]["candidate"]["checks"]["pass_rate"])
        self.assertEqual(summary["paired_check_outcomes"]["not_comparable"], 1)
        self.assertTrue(any("No verifiable checks" in warning for warning in summary["warnings"]))

    def test_skips_fully_passing_pair_with_missing_efficiency_metric(self):
        candidate = make_result(condition="candidate", statuses=("passed",), duration_ms=None, tokens=300)
        baseline = make_result(condition="baseline", statuses=("passed",), duration_ms=100, tokens=200)
        completed = self.run_tool([candidate, baseline], "--json")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        summary = json.loads(completed.stdout)
        self.assertEqual(summary["paired_efficiency"]["eligible_pairs"], 0)
        self.assertEqual(summary["paired_efficiency"]["skipped"]["missing_metrics"], 1)
        self.assertTrue(any("Efficiency regression screening skipped" in warning for warning in summary["warnings"]))

    def test_rejects_mismatched_check_sets(self):
        candidate = make_result(condition="candidate", statuses=("passed", "failed"))
        baseline = make_result(condition="baseline", statuses=("passed",))
        completed = self.run_tool([candidate, baseline])
        self.assertEqual(completed.returncode, 2)
        self.assertIn("check ids differ", completed.stderr)


if __name__ == "__main__":
    unittest.main()
