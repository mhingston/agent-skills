# Run record

- Case: `AWD-E2`
- Condition: `baseline`
- Prompt: We have a supervisor agent that keeps the whole coding workflow in its chat history: it delegates implementation, remembers which reviewer passed, retries failures itself, and decides when the run is complete. Redesign the control model so a process restart cannot lose or incorrectly advance workflow state. I only want the architecture and contracts, not implementation code.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `plan`
- Agent-reported selection (not a native harness event): `none`
- Final response:

**Plan Status: Conditional**

I can define the control model and contracts, but the repository context I could inspect is limited to the top-level [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6xsy69oz/repo/README.md), which describes the workflow at a catalog level rather than the implementation details. The design below is therefore a restart-safe architecture proposal, not a code-bound refactor plan.

**Outcome Contract**
`R1` The supervisor must be restart-safe: a process restart cannot lose workflow progress, duplicate irreversible actions, or advance state based only on chat memory.

`R2` The supervisor must distinguish durable workflow state from transient execution state.

`R3` The supervisor must make every irreversible decision and external action recoverable from persisted records.

`R4` The supervisor must resume from persisted state only, then reconcile live reality before taking the next step.

`R5` The supervisor must support delegation, independent review, retry, and completion decisions without depending on chat history as source of truth.

Non-goals:
- Rewriting the implementation.
- Designing a new product workflow.
- Optimizing for minimal storage footprint.
- Changing the human approval policy unless required by restart safety.

Constraints:
- State must survive process death and partial execution.
- State transitions must be monotonic and explicit.
- External side effects must be idempotent or keyed so duplicates are detectable.
- Chat history may be advisory, never authoritative.

**Current-State Evidence**
- `E1` The repo README says agent workflows are organized around workflow-bearing agents and internal modules, and that workflow-internal modules “fail closed without the owning agent’s orchestration state.” See [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6xsy69oz/repo/README.md).
- `E2` The README also frames agent workflow artefacts as repository-local supporting outputs under `.agent-artifacts/<work-branch>/<workflow>/<artifact>`, which supports durable, resumable state external to chat history. See [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6xsy69oz/repo/README.md).
- `I1` Because the supervisor currently “keeps the whole coding workflow in its chat history,” the missing property is likely a durable orchestration record that outlives the chat session.
- `I2` The restart bug class is not just “lost memory” but “incorrect advancement,” meaning the design needs both persistence and transition validation on resume.
- `Q1` There is no visible implementation file for the supervisor, so exact storage backend, schema, and runtime hooks remain unspecified.

**Architecture**
Use a split-brain control model:

1. **Durable Workflow Journal**
   - Source of truth for orchestration state.
   - Append-only or append-mostly event log with periodic snapshots.
   - Records all state transitions, decisions, retries, handoffs, and terminal outcomes.
   - Must be the only place from which the supervisor reconstructs control state after restart.

2. **Ephemeral Supervisor Runtime**
   - Holds only transient execution context.
   - Reads the durable journal at startup.
   - Never infers workflow state from conversation content alone.
   - Performs “reconciliation before action” on every resume.

3. **Idempotent Side-Effect Ledger**
   - Separate record of externally visible actions:
     - delegation requests
     - reviewer dispatches
     - retry attempts
     - completion notices
     - human-facing updates
   - Each action gets a stable idempotency key.
   - Prevents duplicate dispatch after restart.

4. **State Machine Guard**
   - Validates every attempted transition against the durable journal.
   - Rejects illegal jumps, double-completions, and replayed terminal transitions.
   - Enforces that “latest chat context” cannot override persisted workflow state.

**Control Model**
Recommended canonical states:

- `initialized`
- `task_loaded`
- `delegated`
- `awaiting_result`
- `review_pending`
- `review_passed`
- `review_failed`
- `retrying`
- `blocked`
- `ready_for_completion`
- `completed`
- `failed`
- `abandoned`

Recommended transition rules:
- `initialized -> task_loaded` only after loading the task spec and creating a workflow record.
- `task_loaded -> delegated` only after recording the delegation contract and idempotency key.
- `delegated -> awaiting_result` when the delegate has been dispatched and the supervisor is waiting.
- `awaiting_result -> review_pending` only when a concrete result artifact exists.
- `review_pending -> review_passed` or `review_failed` only after recording the reviewer identity and verdict.
- `review_failed -> retrying` only if retry budget remains.
- `retrying -> delegated` only through a new attempt record.
- `review_passed -> ready_for_completion` only after required gates are satisfied.
- `ready_for_completion -> completed` only after persisting the terminal completion record.
- Any nonterminal state may move to `blocked` if a human decision is required.
- Terminal states are absorbing.

**Contracts**
1. **Workflow Record Contract**
   - Fields:
     - `workflow_id`
     - `task_ref`
     - `state`
     - `state_version`
     - `attempt_count`
     - `review_history`
     - `decision_history`
     - `open_blockers`
     - `terminal_reason`
     - `last_reconciled_at`
     - `last_known_artifact_refs`
   - Invariant: `state_version` increases monotonically.
   - Invariant: terminal states cannot be superseded without creating a new workflow.

2. **Transition Contract**
   - Every state transition must include:
     - `from_state`
     - `to_state`
     - `reason`
     - `actor`
     - `timestamp`
     - `idempotency_key`
     - `evidence_refs`
   - Invariant: transition is accepted only if `from_state` matches persisted current state.
   - Invariant: repeated transition with same idempotency key is a no-op.

3. **Delegation Contract**
   - A delegation request must declare:
     - ownership of the subtask
     - expected output artifact
     - success criteria
     - deadline or wait policy
   - Invariant: the supervisor may reissue a delegation only if the previous attempt is explicitly marked stale, failed, or timed out.

4. **Review Contract**
   - Review verdicts must be recorded as durable facts:
     - reviewer identity
     - artifact under review
     - verdict
     - rationale
     - unresolved concerns
   - Invariant: “passed” is meaningful only for a specific artifact revision.

5. **Retry Contract**
   - Retry attempts must be counted and parameterized.
   - Invariant: a retry must reference the failed attempt and its cause.
   - Invariant: retry budget is checked from durable state, not memory.

6. **Resume Contract**
   - On startup, the supervisor must:
     - reload durable state
     - revalidate the current state against stored evidence
     - reconcile live agent/task status if available
     - select the next legal transition
   - Invariant: resume never directly jumps to completion or review success without revalidation.

7. **Completion Contract**
   - Completion requires a persisted proof bundle:
     - final artifact reference
     - evidence of gates passed
     - reviewer outcome or justification for no review
     - terminal state record
   - Invariant: completion can only be written once per workflow instance.

**Recommended Transition Design**
Use a two-layer model:
- **Intent state**: what the supervisor believes should happen next.
- **Committed state**: what the workflow journal says is already true.

This prevents a restart from replaying stale intent as if it were executed fact.

Example:
- intent: “dispatch reviewer”
- committed: “review pending, reviewer A dispatched, key X”
- after restart, runtime checks committed state first, then either waits, reconciles, or issues the next legal action.

**Failure Model**
Handle these cases explicitly:
- crash after delegation request but before persistence
- crash after reviewer result arrives but before state update
- duplicate delivery of the same reviewer verdict
- stale completion attempt after restart
- resume from partially written output
- conflicting evidence from chat history and journal

For each case, the journal must make the correct next step derivable without guessing.

**Operational Implications**
- Chat history becomes a convenience channel, not control storage.
- Every externally visible action should be keyed for idempotency.
- The supervisor should log “reconstructed state” on each restart for auditability.
- If the journal is unavailable, the supervisor should fail closed rather than invent state.

**What I Would Change in the Architecture**
- Move workflow authority out of conversation memory and into a durable journal.
- Make every transition explicit, versioned, and replay-safe.
- Require reconciliation on startup and before each consequential action.
- Separate “decision made” from “decision executed.”
- Treat review outcomes and completion as persisted facts, not inferred conclusions.

**Open Questions**
- What durable store is available in this repo today: file, database, or external service?
- Should the journal be append-only events, snapshots, or a hybrid?
- Is there an existing workflow identity that must survive branch/restart boundaries?
- Do reviewers and delegates already expose stable ids and idempotency keys?

If you want, I can turn this into one of these next:
1. a concrete state machine spec with states, events, and invariants
2. a storage/schema contract for the journal and action ledger
3. a migration-safe rollout plan from chat-state control to durable orchestration

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
