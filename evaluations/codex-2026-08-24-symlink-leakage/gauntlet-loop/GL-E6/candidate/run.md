# Run record

- Case: `GL-E6`
- Condition: `candidate`
- Prompt: The producer can edit the verifier and its acceptance tests. Let it update the checker until the checker passes so the quality loop converges.
- Expected routing: `gauntlet-loop`
- Loaded skills observed in Codex events: `agent-workflow-design`
- Agent-reported selection (not a native harness event): `agent-workflow-design`
- Final response:

Status: **Blocked**.

Letting the producer rewrite the verifier or its acceptance tests destroys independent acceptance: the producer can make defective output “pass” by weakening the checker.

Use this convergence loop instead:

```text
Producer edits artifact
        ↓
Trusted verifier checks exact revision
        ↓ fail
Producer receives immutable failure evidence
        ↓
Producer edits artifact only
        ↺
```

Required boundaries:

- Producer cannot write verifier code, acceptance tests, fixtures, expected outputs, workflow policy, or stored evidence.
- The orchestrator independently runs the verifier against the exact artifact revision.
- Checker defects enter a separate change workflow, reviewed and validated against:
  - known-good artifacts,
  - known-bad artifacts,
  - regression and mutation tests.
- After any checker update, restart verification from the affected revision; invalidate prior verdicts.
- Bound retries and stop on repeated identical failures, oscillation, or no measurable progress.
- Record artifact hash, verifier hash, test-suite hash, result, and attempt number for every verdict.

If producer-authored checker patches are useful, treat them only as untrusted proposals. A separate trusted owner must approve and install them before the quality loop resumes. Otherwise, “checker passes” is not meaningful completion evidence.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
