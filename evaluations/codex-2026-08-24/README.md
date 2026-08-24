# Codex behavioural evaluation record

This directory preserves the copied-package matched run described in
[`human-review.md`](human-review.md). The runner is a thin recorder for the
repository's portable result contract; outcome checks remain for human review.

```bash
python3 evaluations/codex-2026-08-24/run.py --case AWD-E1
python3 evaluations/codex-2026-08-24/normalise-results.py
python3 skill-creator/scripts/aggregate-evals.py \
  evaluations/codex-2026-08-24/orchestration \
  --json-out evaluations/codex-2026-08-24/orchestration-summary.json \
  --markdown-out evaluations/codex-2026-08-24/orchestration-summary.md
```

The `*-summary.{json,md}` files were generated from the preserved result
records. The earlier symlink-leakage audit is deliberately kept outside this
directory and is not part of these aggregates.
