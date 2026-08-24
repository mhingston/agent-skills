# Run record

- Case: `PC-E2`
- Condition: `candidate`
- Prompt: Plan how to add an idempotency key to this existing POST endpoint. The repo has a clear architecture doc, ADRs, tests, and a ready ticket.
- Expected routing: `plan`
- Loaded skills observed in Codex events: `plan`
- Agent-reported selection (not a native harness event): `none`
- Final response:

**Plan status**: `Blocked`

I can’t produce a grounded implementation plan yet because the repo-visible evidence does not include the artifacts you referenced.

**Outcome contract**
- `R1`: Add idempotency-key support to the existing `POST` endpoint without changing unrelated behaviour.
- `R2`: Preserve the endpoint’s current contract for successful, duplicate, and error responses.
- `R3`: Keep the change aligned with the repo’s established architecture, ADRs, tests, and the ready ticket.
- `R4`: Define verification that proves repeated requests with the same idempotency key are safe and deterministic.

**Current-state evidence**
- `E1`: The repository root only exposed [`README.md`](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6na4q0vh/repo/README.md) and the `.codex/skills` directory when I enumerated files.
- `E2`: [`README.md`](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6na4q0vh/repo/README.md) describes the repo as a catalogue of reusable agent skills and agent definitions, not an application codebase with endpoint implementation details.
- `E3`: No architecture doc, ADRs, test files, or ticket files were present in the visible tree.
- `Q1`: The actual endpoint implementation, repository architecture, ADR set, and ticket content were not available to inspect.
- `A1`: The “existing POST endpoint” and “ready ticket” may exist outside the visible checkout or in a different branch/worktree. If that is wrong, the task scope is currently underspecified.

**Approach and decisions**
- `I1`: Because the requested plan depends on the endpoint’s current request/response shape, persistence model, and existing test strategy, the plan cannot be made evidence-grounded from the current visible files alone.
- `I2`: The right next step is not to guess an idempotency design, but to locate or provide the governing artefacts first.
- `D1` decision gate: the exact endpoint contract, ADR guidance, and ticket acceptance criteria must be supplied or made visible before implementation planning can be finalized.

**Implementation slices**
1. **Outcome**: Recover the governing sources.
   - **Basis**: `E1`, `E2`, `E3`, `Q1`
   - **Why**: The endpoint semantics and the repo’s architectural constraints are unknown.
   - **Affects**: architecture doc, ADRs, tests, ticket
   - **Work**: Make the endpoint code, the relevant ADRs, and the ready ticket visible in this workspace or provide their paths/contents.
   - **Dependencies**: none
   - **Verify**: repo tree contains the endpoint code, relevant docs, and ticket
   - **End state**: enough evidence exists to plan safely
   - **Replan if**: the endpoint or ticket lives elsewhere and differs materially from the current repository shape

2. **Outcome**: Build the actual idempotency plan from evidence.
   - **Basis**: recovered docs, endpoint code, tests, ticket
   - **Why**: only then can the plan specify storage, replay semantics, conflict handling, and verification
   - **Affects**: endpoint handler, persistence layer, test suite, possibly schema/migrations
   - **Work**: map the request flow, choose the idempotency boundary, define key storage/replay rules, and enumerate exact tests
   - **Dependencies**: slice 1
   - **Verify**: plan traces every requirement to concrete code and tests
   - **End state**: implementable, reviewable plan
   - **Replan if**: the ADRs conflict with the ticket or implementation path

**Verification map**
- `R1` and `R2` require endpoint-level request/retry tests, but I cannot name them without the repository’s test files.
- `R3` requires reading the architecture doc and ADRs before choosing any design.
- `R4` requires a concrete test oracle from the existing test suite or ticket acceptance criteria.

**Handoff controls**
- Revalidate the endpoint source, architecture doc, ADRs, tests, and ticket before planning.
- If the artefacts are in another branch, workspace, or ticketing system, provide their locations and I’ll turn this into a proper `Ready` plan.
- If you want, I can next help you locate the relevant files in the repo or you can paste the ticket and I’ll produce the plan from that.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
