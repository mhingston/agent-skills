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
      "dimension": "goal_completion",
      "status": "passed",
      "evidence": "validator exited 0"
    }
  ],
  "notes": []
}
```

`dimension` is optional and backward-compatible within schema version `1`. Use it
only when separating task success from skill-specific behavioural constraints
improves interpretation:

- `goal_completion` — the requested result or artefact is correct and usable;
- `instruction_following` — material workflow, authority, evidence, convention,
  or process constraints owned by the skill were followed.

Leave a check unclassified when the distinction is not useful. Do not encode
routing as a check dimension; routing remains a separate harness-specific
experiment.

### Required invariants

- `case` and `trial` identify a matched pair.
- Every pair has exactly one `candidate` and one `baseline` result.
- `harness`, `model`, `prompt`, `inputs`, `permissions`, and `environment` match within the
  pair. Record `null` when a value is genuinely unavailable.
- `skill_version` identifies the actual candidate or baseline exposure and may
  differ between conditions.
- `checks` use the same stable IDs on both sides of a pair.
- When a check uses `dimension`, the same check ID uses the same dimension on both
  sides of the pair.
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
- optional `goal_completion` and `instruction_following` pass-rate deltas when
  those dimensions are present;
- variation in per-run pass rate;
- mean duration and token deltas when those metrics are present;
- high-confidence paired efficiency regressions for fully passing pairs;
- warnings when objective or cost evidence is incomplete.

Dimension summaries are diagnostic slices over the same objective checks. They do
not replace the pooled result, and a strong instruction-following delta must not
hide a goal-completion regression.

For efficiency screening, a pair is eligible only when both conditions have at
least one objective check and every check passes. The helper then flags a
conspicuous regression when candidate token use and duration both increase and at
least one is `>= 2.0x` the baseline. It reports the per-pair token and duration
ratios and keeps skipped pairs visible when metrics are missing or a baseline cost
is zero.

Treat this threshold as a triage signal, not an automatic rejection gate. A
higher-cost skill may be justified when it produces stronger evidence or protects
a consequential outcome. Conversely, mean cost deltas can hide a small number of
severe paired regressions, which is why the helper reports both views.

The helper is optional. If Python is unavailable, apply the same invariants and
show the arithmetic directly or use another deterministic calculator already
present in the environment. Do not introduce a runtime solely to run this
aggregator.

## Triage confirmed regressions

After a matched comparison establishes a candidate loss, inspect the paired
outputs and trajectories before editing the skill. Classify the smallest supported
cause rather than treating the label as a verdict:

- **Functional loss:** task-implementation fault, artifact misplacement,
  environment mismatch, or applicability mismatch.
- **Efficiency regression:** excessive procedure, context bloat, or dependency
  resolution. Within excessive procedure, distinguish excessive verification,
  a heavy implementation pipeline, or excessive exploration when the evidence
  supports that distinction.

Tie the category to concrete differential evidence: the skill instruction or
reference that changed behaviour, the resulting implementation/environment/path
difference, or the phase/action where extra cost appeared. Do not infer a cause
from totals alone. If the evidence does not discriminate causes, report the
regression without forcing a taxonomy label.

These categories and the conservative `2.0x` efficiency signal are adapted from
Dong et al., *Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced
Failures in LLM Agents* (arXiv:2608.11888v1). Keep them as diagnostic aids rather
than universal policy thresholds.

## Interpretation

Aggregation does not decide whether a skill is better. Inspect the actual outputs
and trajectories, preserve human review for subjective qualities, and explain
tradeoffs that a pooled score can hide. Treat `not_verifiable` as missing evidence,
not as a pass, and scope conclusions to the harness and model that produced the
runs.

Repeated negligible skill lift across representative cases can make a skill a
simplification or retirement candidate, but it is not sufficient evidence for
removal. Before retiring a skill, check whether it still provides material value
through weaker-model lift, cross-harness portability, governance or authority
boundaries, deterministic tooling, or failure protection not exercised by the
sampled cases.
