# Run record

- Case: `DW-E4`
- Condition: `candidate`
- Prompt: Build a Mastra workflow that sends repository implementation tasks to an ACP coding agent, then runs an independent review step. Keep the coding harness swappable rather than hard-coding one vendor.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `dynamic-workflows`
- Agent-reported selection (not a native harness event): `none`
- Final response:

I can’t complete the build in this workspace because the filesystem is read-only, so file writes are blocked.

I did verify the right shape for the solution:

- use Mastra as the orchestration runtime
- wrap the coding harness behind an ACP adapter resolved from config
- run implementation first, then an independent review step
- keep the worker choice swappable via `ACP_COMMAND` / `ACP_ARGS` / `ACP_CWD`, not a vendor-specific import

The scaffold I was going to add was:

- `mastra-acp-implement-review/SKILL.md`
- `mastra-acp-implement-review/references/acp-worker.ts`
- `mastra-acp-implement-review/references/workflow.ts`

That would define:
- a `repository-coding-worker` ACP tool for implementation
- an `independent-review-worker` step that consumes only the implementation output
- JSON-schema input/output boundaries
- a config-driven harness selection layer

If you can provide a writable workspace, I can apply the files directly. If you want, I can also paste the exact scaffold here so you can drop it in manually.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
