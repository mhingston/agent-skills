# Run record

- Case: `GL-E4`
- Condition: `baseline`
- Prompt: The producer and critic can keep trying forever. Do not stop until the result is perfect, even if the user has not supplied a time or cost budget.
- Expected routing: `gauntlet-loop`
- Loaded skills observed in Codex events: `agent-workflow-design`
- Agent-reported selection (not a native harness event): `none`
- Final response:

I can support iterative producer/critic refinement, but not an infinite “until perfect” loop. “Perfect” is unverifiable, and unbounded retries risk cost without progress.

Use a deterministic stop policy:

- Stop when explicit acceptance criteria pass.
- Set attempt, time, token, and cost limits before execution.
- Stop early on repeated findings, unchanged failures, or oscillation.
- Escalate unresolved tradeoffs to the user.
- Return the best verified result plus remaining limitations when the budget is exhausted.

Without a user-supplied budget, the orchestrator must apply safe defaults—not infer unlimited authority.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
