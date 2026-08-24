# Run record

- Case: `DW-E4`
- Condition: `candidate`
- Prompt: Build a Mastra workflow that sends repository implementation tasks to an ACP coding agent, then runs an independent review step. Keep the coding harness swappable rather than hard-coding one vendor.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `dynamic-workflows`
- Final response:

I couldn’t build the workflow because this workspace is mounted read-only; the complete scaffold patch was rejected before any files changed.

The prepared implementation uses:

- A deterministic Mastra dynamic workflow: `implement → review`
- Two separately registered `createACPTool()` workers
- Fresh ACP processes for both roles (`persistSession: false`)
- Environment-configured commands and arguments, including role-specific overrides
- Explicit task/result mappings and a two-call, zero-retry budget
- LibSQL persistence and a local CLI runner
- Reviewer instructions to inspect the actual diff independently

This follows Mastra’s current [dynamic workflow API](https://mastra.ai/docs/workflows/dynamic-workflows) and [ACP tool interface](https://mastra.ai/reference/acp/create-acp-tool).

No repository files were modified. Enable workspace write access and rerun the request to apply and type-check the scaffold.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
