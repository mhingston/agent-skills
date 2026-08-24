# Run record

- Case: `DW-E4`
- Condition: `baseline`
- Prompt: Build a Mastra workflow that sends repository implementation tasks to an ACP coding agent, then runs an independent review step. Keep the coding harness swappable rather than hard-coding one vendor.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

I can’t complete the build in this workspace because the filesystem is read-only, so `apply_patch` is blocked.

What I would add is:

- a `dynamic-workflows/SKILL.md` that defines the Mastra workflow contract
- an `agents/mastra-acp.md` orchestration file for the implementation/review state machine
- a narrow `CodingHarnessAdapter` interface so the coding worker stays swappable
- an independent review stage that consumes the implementation artifact, not the worker’s self-assessment

If you want, I can still give you the exact file contents for those two files so you can apply them directly, or I can adapt the design to the specific Mastra project structure you’re using.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
