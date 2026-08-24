# Run record

- Case: `AWD-E2`
- Condition: `baseline`
- Prompt: We have a supervisor agent that keeps the whole coding workflow in its chat history: it delegates implementation, remembers which reviewer passed, retries failures itself, and decides when the run is complete. Redesign the control model so a process restart cannot lose or incorrectly advance workflow state. I only want the architecture and contracts, not implementation code.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `dynamic-workflows, plan`
- Final response:

Plan status: Ready. This is a runtime-neutral control-plane design; storage and messaging technologies remain implementation choices.

## Target architecture

Replace the conversational supervisor with a durable workflow controller:

```text
Commands / worker results
           │
           ▼
  Durable workflow store ◄──── Artifact/evidence store
  (authoritative state)         (revision-bound receipts)
           │
           ▼
 Transactional scheduler/outbox
           │
           ▼
 Replaceable implementation and review workers
```

The controller is deterministic. Models may plan, implement, diagnose, or review, but they never decide whether a transition committed, a retry is allowed, or the workflow is complete.

Chat history becomes a disposable context projection rebuilt from durable state.

## Core invariants

- Every run is identified by an immutable `run_id` and `workflow_definition_version`.
- Every state mutation uses compare-and-set against the current `state_version`.
- A successful review applies only to the exact artifact revision and acceptance-contract version reviewed.
- Worker completion claims are proposals until validated and committed by the controller.
- Dispatch, result ingestion, retry, cancellation, approval, and completion are idempotent.
- At most one active mutation lease exists for a mutable workspace.
- No terminal state is entered without a deterministic completion predicate.
- A restart may delay progress, but cannot manufacture progress.
- Missing or ambiguous evidence produces `blocked` or `reconciling`, never success.

## Durable records

### WorkflowRun

```text
run_id
workflow_definition_id
workflow_definition_version
acceptance_contract_id
acceptance_contract_version
status
state_version
created_at
updated_at
terminal_reason?
budget
authority_snapshot
input_snapshot_ref
```

`status` is one of:

```text
pending
running
waiting_for_worker
waiting_for_review
retry_scheduled
reconciling
blocked
cancelling
cancelled
failed
succeeded
```

The definition, inputs, authority, and acceptance criteria are immutable snapshots. Amendments create a new version and invalidate affected downstream claims.

### WorkItem

```text
work_item_id
run_id
kind                  # implement | verify | review | diagnose | integrate
status
attempt
max_attempts
input_contract_ref
expected_output_schema
workspace_id?
base_revision?
target_revision?
lease_epoch?
deadline?
last_error_ref?
```

A work item is the unit of retry. Re-dispatching the same attempt must not create a logically new attempt.

### Dispatch

```text
dispatch_id
work_item_id
attempt
idempotency_key
worker_capability
input_digest
status                # pending | sent | acknowledged | uncertain | closed
created_at
acknowledged_at?
```

Create the dispatch and advance the workflow state in the same transaction. An outbox dispatcher performs delivery afterward.

### WorkerResult

```text
result_id
dispatch_id
work_item_id
attempt
worker_identity
worker_session_id?
input_digest
result_status
structured_claims
artifact_refs
artifact_digests
verification_receipts
started_at
finished_at
signature_or_provenance
```

Uniqueness on `dispatch_id` makes duplicate delivery harmless. Results with a mismatched attempt, input digest, lease epoch, or revision are retained for audit but cannot advance state.

### ReviewAttestation

```text
review_id
run_id
reviewer_identity
reviewer_independence_class
acceptance_contract_version
subject_revision
subject_digest
verdict               # pass | fail | abstain | invalid
findings_ref
checks
created_at
supersedes_review_id?
```

A `pass` is valid only while all binding fields still match current run state. Any subsequent mutation, contract amendment, or reviewer-policy change invalidates it explicitly.

### TransitionReceipt

```text
transition_id
run_id
from_state
to_state
expected_state_version
committed_state_version
trigger_type
trigger_id
decision_rule
evidence_refs
actor
timestamp
```

This append-only record explains every advancement. The materialized run state is a cacheable projection of committed transitions.

### Lease

```text
resource_id
run_id
work_item_id
owner_id
lease_epoch
expires_at
heartbeat_at
```

Workers receive the current epoch. A late worker holding an expired epoch cannot publish authoritative mutations or results.

## Transition contract

All advancement goes through one controller operation:

```text
ApplyTransition(
  run_id,
  expected_state_version,
  trigger,
  proposed_transition
) -> committed_state | conflict | rejected
```

The controller must:

1. Load the run and governing definition.
2. Confirm `expected_state_version`.
3. Authenticate the actor and check recorded authority.
4. Validate the trigger schema and provenance.
5. Confirm attempt, lease epoch, input digest, and revision bindings.
6. Evaluate the deterministic transition guard.
7. Atomically write state, transition receipt, invalidations, and any outbox messages.
8. Return the newly committed version.

No worker-facing API may directly set `status`, increment attempts, mark reviews passed, or declare the run complete.

## State-machine rules

A representative implementation/review loop is:

```text
pending
  → running
  → waiting_for_worker
  → waiting_for_review
      ├─ pass → completion evaluation
      ├─ fail, retry allowed → retry_scheduled → waiting_for_worker
      ├─ fail, retry exhausted → blocked | failed
      └─ invalid/stale → waiting_for_review
```

Important guards:

- `waiting_for_worker → waiting_for_review` requires a valid result, a resolvable produced revision, and required implementation evidence.
- `waiting_for_review → retry_scheduled` requires an applicable failing review and remaining retry/no-progress budget.
- `waiting_for_review → succeeded` requires the completion predicate below.
- Any uncertain external outcome enters `reconciling`.
- Cancellation prevents new dispatches immediately; terminal `cancelled` waits until active leases are revoked or fenced.

## Completion predicate

`Succeeded` is derived, never asserted by an agent:

```text
all required work items are accepted
AND current artifact revision equals the accepted implementation revision
AND every required review dimension has a valid passing attestation
AND every attestation is bound to:
    current artifact digest,
    current acceptance-contract version,
    current workflow-definition version
AND required deterministic verification receipts pass
AND no required item is pending, running, uncertain, blocked, or invalidated
AND no unresolved approval or policy gate exists
AND all critical side effects have confirmed receipts
```

The controller records which facts satisfied each clause in the terminal transition receipt.

## Restart and recovery protocol

On startup, the controller reconstructs projections from durable state and then reconciles nonterminal work:

- `pending` outbox entry: deliver it.
- Sent but unacknowledged dispatch: query the worker when possible; otherwise redeliver with the same idempotency key.
- Expired lease: fence the old worker and either reconcile its external effect or create the next attempt.
- Result stored but transition absent: re-run `ApplyTransition`; idempotency and compare-and-set make this safe.
- Transition committed but follow-up dispatch absent: regenerate the deterministic outbox entry.
- External effect with unknown outcome: remain in `reconciling`; inspect the target using its idempotency key or receipt. Never retry blindly.
- Late or duplicate result: record it, reject it for advancement, and preserve the rejection reason.
- Stale review: mark it invalid and schedule review of the current revision.

Recovery operates on durable records rather than trying to resume the former supervisor conversation.

## Retry contract

Retries are policy, not model discretion:

```text
retry_policy:
  retryable_error_classes
  max_attempts
  elapsed_time_budget
  cost_budget
  backoff
  no_progress_rule
  escalation_target
```

Each new attempt gets a new `attempt` number and dispatch ID. Equivalent failures or unchanged artifacts count toward no-progress detection. Exhaustion transitions to `blocked` or `failed`; it never silently broadens scope, permissions, or budgets.

A diagnosis worker may recommend a different strategy, but the controller validates that recommendation against permitted strategies before scheduling it.

## Worker contract

Workers receive a self-contained task envelope:

```text
run identity and versions
work-item and attempt identity
objective and acceptance criteria
bounded scope and authority
base/target revision
input and context digests
lease epoch and deadline
allowed capabilities
required output schema
artifact and receipt publication rules
```

Workers return structured claims and evidence. Hidden conversation state, remembered reviewer verdicts, and prior worker sessions are never prerequisites for correctness.

Implementation and review identities must satisfy an explicit independence policy. A restarted implementation worker may replace its predecessor; a reviewer cannot inherit implementer authority merely because it has access to the same transcript.

## Concurrency and consistency

Use single-writer semantics per run, implemented through serialized transactions or optimistic concurrency. Multiple controllers may operate concurrently, but only one transition for a given `state_version` can commit.

Parallel read-only work is safe. Parallel mutation requires isolated workspaces and a distinct integration item. The integration revision invalidates reviews of its inputs and must receive its own verification and review.

## Authority boundaries

Persist an immutable authority snapshot covering:

- Allowed repositories, workspaces, tools, networks, and credentials.
- Mutation and external-effect permissions.
- Approval requirements.
- Worker capability constraints.
- Budget ceilings.

A planner or worker may request additional authority; only the designated policy or human authority can grant it. Restarting the controller cannot reinterpret silence or prior progress as approval.

## Verification contract for the redesign

The architecture is acceptable only if deterministic tests demonstrate:

- Termination immediately before and after every transactional transition.
- Termination before dispatch, after delivery, and before acknowledgment.
- Duplicate commands, dispatches, results, and reviews.
- Worker loss and lease expiry.
- Late results from fenced workers.
- Review pass followed by a new artifact revision.
- Acceptance-contract amendment after review.
- Two controllers racing to advance the same run.
- Retry exhaustion and repeated no-progress outcomes.
- Cancellation during implementation, review, and reconciliation.
- Unknown external-effect outcomes.
- Projection deletion followed by complete reconstruction.
- Refusal to reach `succeeded` when any completion clause lacks evidence.

The essential shift is simple: the process owns execution, durable records own truth, deterministic guards own advancement, and agents contribute bounded proposals plus evidence. Conversation history can then disappear without affecting correctness.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
