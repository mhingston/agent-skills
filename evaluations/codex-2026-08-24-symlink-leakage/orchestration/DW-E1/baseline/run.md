# Run record

- Case: `DW-E1`
- Condition: `baseline`
- Prompt: Build a Mastra dynamic workflow for coding tasks where the decomposition can change per request. I want a planner to propose a bounded graph, validate it, require approval before repository mutation, then execute it and preserve a run receipt.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `agent-workflow-design`
- Final response:

Blocked: the workspace is mounted read-only, and the attempted patch was rejected. No files were changed.

The intended implementation is a TypeScript Mastra package with:

- A planner producing a schema-constrained, size-capped DAG of registered coding operations.
- Deterministic validation for acyclicity, dependency integrity, primitive allowlists, path scope, graph limits, and protected control-plane files.
- An approval step that suspends the Mastra run and binds approval to both the plan digest and repository revision.
- Pre-execution revalidation that fails closed if the plan, approval, revision, or working-tree baseline has changed.
- A bounded executor that records actual mutations and rejects undeclared paths.
- An append-only run receipt containing planning provenance, validation checks, approval identity/time, execution attempts, revision bindings, observed changes, verification results, and terminal status.
- Tests covering malformed graphs, cycles, stale approvals, revision drift, unauthorized writes, rejection, cancellation, and successful resumption.

This design aligns with Mastra’s current dynamic-workflow support, which requires `@mastra/core` 1.58.0 or later, and its persisted suspend/resume mechanism for human approval. [Dynamic workflows](https://mastra.ai/blog/introducing-dynamic-workflows), [workflow snapshots](https://mastra.ai/en/reference/workflows/snapshots).

Granting write access to the workspace is required for me to build and verify it.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
