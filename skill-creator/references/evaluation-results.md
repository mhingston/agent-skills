# Portable Evaluation Results

Use this format when an evaluation has enough runs that a deterministic summary
is useful. It standardizes recorded evidence without prescribing how any agent
harness launches, grades, or reviews the runs.

For very small evaluations, an inline table is still sufficient. Do not create
JSON merely to satisfy this format.

## Result file

Store one `result.json` for each condition in each matched trial. Normalize
condition names as follows:

- `candidate` — the skill being tested; for a new skill this is the with-skill
  condition, and for a revision this is the proposed version;
- `baseline` — the comparison condition; for a new skill this is no skill, and
  for a revision this is the previous version.

Use schema version `1`:

```json
{
  "schema_version": 1,
  "case": "descriptive-name",
  "trial": 1,
  "condition": "candidate",
  "harness": "harness name and version or null",
  "model": "model identifier or null",
  "skill_version": "path, commit, hash, or stable label",
  "prompt": "exact user task",
  "inputs": ["relative/or/absolute/path"],
  "permissions": "relevant execution constraints or null",
  "environment": "relevant environment and resource conditions or null",
  "duration_ms": null,
  "tokens": null,
  "checks": [
    {
      "id": "output-parses",
      "status": "passed",
      "evidence": "validator exited 0"
    }
  ],
  "notes": []
}
```

### Required invariants

- `case` and `trial` identify a matched pair.
- Every pair has exactly one `candidate` and one `baseline` result.
- `harness`, `model`, `prompt`, `inputs`, `permissions`, and `environment` match within the
  pair. Record `null` when a value is genuinely unavailable.
- `skill_version` identifies the actual candidate or baseline exposure and may
  differ between conditions.
- `checks` use the same stable IDs on both sides of a pair.
- Check status is `passed`, `failed`, or `not_verifiable` and always carries
  concrete evidence.
- `duration_ms` and `tokens` are non-negative numbers or `null`. Never infer a
  missing metric.

Keep subjective review outside this result schema. A blind preference, design
judgment, or user comment is evidence, but collapsing it into an objective pass
flag makes the comparison harder to interpret. Preserve that review beside the
run or report it directly.

## Deterministic aggregation

When Python 3 is already available, run the bundled standard-library helper from
any directory:

```bash
python3 /path/to/skill-creator/scripts/aggregate-evals.py \
  <workspace> \
  --json-out <workspace>/summary.json \
  --markdown-out <workspace>/summary.md
```

The helper recursively discovers `result.json` files, validates pair integrity,
and refuses to aggregate unmatched or materially different conditions. It
reports:

- pooled passed, failed, and `not_verifiable` checks per condition;
- paired candidate wins, baseline wins, ties, and non-comparable checks;
- pass-rate delta;
- variation in per-run pass rate;
- mean duration and token deltas when those metrics are present;
- warnings when objective or cost evidence is incomplete.

The helper is optional. If Python is unavailable, apply the same invariants and
show the arithmetic directly or use another deterministic calculator already
present in the environment. Do not introduce a runtime solely to run this
aggregator.

## Interpretation

Aggregation does not decide whether a skill is better. Inspect the actual outputs
and trajectories, preserve human review for subjective qualities, and explain
tradeoffs that a pooled score can hide. Treat `not_verifiable` as missing evidence,
not as a pass, and scope conclusions to the harness and model that produced the
runs.
