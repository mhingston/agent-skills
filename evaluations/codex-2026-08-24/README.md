# Behavioural case specifications

[`run.py`](run.py) contains the reusable case prompts, sibling surfaces, and a
thin Codex CLI recorder for the catalogue-boundary evaluation. It is not a
grader or a second evaluation framework; outcome checks remain human-reviewed.

The recorder can compare a target-present fixture with a target-omitted fixture
for exploratory body-behaviour diagnostics:

```bash
python3 evaluations/codex-2026-08-24/run.py --case GL-E6
```

Generated `run.jsonl`, `run.md`, `result.json`, and `stderr.log` files are
working evidence, not catalogue artefacts, and should remain untracked.

This Codex CLI did not expose a native primary-skill selection event. Successful
skill-body reads and model self-reports are therefore diagnostic signals only;
they do not establish routing. Record routing as `not_verifiable` unless a
harness provides a real discovery/selection event.
