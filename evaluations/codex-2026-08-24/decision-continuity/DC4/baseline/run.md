# Run record

- Case: `DC4`
- Condition: `baseline`
- Prompt: Which source governs? An ADR and tracker parent conflict, and repository policy does not declare precedence.
- Expected routing: `decision-continuity`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

No explicit repo policy declares a precedence order here, so the safe answer is: neither source automatically overrides the other.

From the repo README, the clearest signals are:

- `decision-continuity` is the mechanism for preserving accepted/rejected/deferred direction across resumed work.
- `refine` updates the selected tracker after human approval, which makes the tracker look like a coordination/status surface, not the highest authority on the underlying decision.
- `project-context` is described as the durable substrate for truth/intent/history/scratch separation.

So, in a conflict:

- Treat the ADR as the stronger source for decision intent, if it is an accepted architectural decision.
- Treat the tracker parent as a work-management surface unless it is explicitly designated as the canonical decision record.
- If both are meant to be authoritative and they disagree, the conflict is unresolved and should be escalated rather than silently resolved.

Relevant repo refs:
- [README.md](./README.md#L142)
- [README.md](./README.md#L123)
- [README.md](./README.md#L206)

If you want, I can help you turn this into a concrete precedence rule for the repo.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
