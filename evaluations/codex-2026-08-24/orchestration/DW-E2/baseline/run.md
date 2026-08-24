# Run record

- Case: `DW-E2`
- Condition: `baseline`
- Prompt: Implement a Mastra workflow that always runs lint, tests, a read-only review, and then publishes a verification report in that fixed order. The topology is known and should be repeatable.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `agent-readiness, agent-workflow-design, implement-ticket, plan, programmatic-tool-calling`
- Agent-reported selection (not a native harness event): `none`
- Final response:

I couldn’t apply the change in this session because the workspace is read-only, so file writes are blocked.

What I would add is a new skill at [`dynamic-workflows/SKILL.md`](./dynamic-workflows/SKILL.md) that defines a fixed sequential Mastra workflow with this exact topology:

1. `lint`
2. `tests`
3. read-only `review`
4. `publishReport`

The skill would make the workflow contract explicit:
- the order is invariant
- the review step cannot mutate state
- the report is always published at the end
- each stage records evidence and status
- the final report is bound to the exact run/revision

If you want, I can provide the full file contents here so you can apply them directly, or I can retry in a writable workspace.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
