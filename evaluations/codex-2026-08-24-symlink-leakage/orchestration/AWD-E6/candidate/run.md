# Run record

- Case: `AWD-E6`
- Condition: `candidate`
- Prompt: Plan the repository changes needed to add an idempotency key to our payment creation endpoint. Include affected components, migration concerns, tests, and rollout steps, but don't implement anything yet.
- Expected routing: `no target skill`
- Loaded skills observed in Codex events: `plan`
- Final response:

## Plan status: Blocked

The workspace does not contain a payment service or application code. It currently contains only an agent-skills catalogue ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-t6ru9m2z/repo/README.md)); there are no endpoint definitions, persistence models, migrations, tests, manifests, deployment configuration, or committed Git history to inspect.

Accordingly, the component names and commands below are proposed responsibilities, not repository-observed implementation details. The implementation plan must be reconciled against the actual payment repository before execution.

## Outcome contract

- **R1 — Retry safety:** Repeating payment creation with the same authenticated caller, idempotency key, and request payload returns the original result without creating another payment or repeating external payment-provider effects.
- **R2 — Conflict detection:** Reusing a key with a materially different request is rejected with a stable client error.
- **R3 — Concurrency safety:** Concurrent requests with the same key cannot both create payments.
- **R4 — Compatibility:** Clients that omit the key continue to receive the currently supported behavior unless the API owner explicitly makes the key mandatory.
- **R5 — Durable replay:** Successful responses remain replayable for the documented retention period, including across process restarts.
- **R6 — Safe failure handling:** The system distinguishes an in-progress operation, a completed operation, and a retryable/terminal failure without producing duplicate side effects.
- **R7 — Operability:** Logs and metrics expose idempotency hits, conflicts, in-progress collisions, and failures without logging the raw key or sensitive payment data.

Non-goals: changing payment-provider selection, redesigning payment state transitions, deduplicating historically created payments, or making unrelated endpoint cleanup.

### Invariants

- At most one payment creation operation wins for a given idempotency scope and key.
- A key is bound to one canonical request fingerprint.
- The idempotency record and local payment creation are committed atomically where the storage architecture permits.
- Replay does not call the provider, publish duplicate events, or repeat other downstream effects.
- Retrying after an ambiguous timeout cannot silently create a second payment.

## Evidence and open decisions

- **E1:** The inspected README describes a catalogue of reusable agent skills, not a payment application.
- **E2:** The repository has no commits and exposes no application source, migration framework, test runner, CI checks, or deployment mechanism.
- **I1:** The requested change needs durable coordination between API handling, payment orchestration, and persistence; in-memory deduplication would not satisfy R3 or R5.
- **A1:** Payment creation is backed by transactional storage. If it is not, the executor must design an equivalent atomic reservation mechanism.
- **A2:** Existing clients must remain compatible, so the key initially remains optional.
- **Q1:** Where is the actual payment service repository or subtree?
- **Q2:** What identifies an idempotency scope: authenticated account, merchant, API credential, or another tenant boundary?
- **Q3:** How long must completed keys be retained?
- **Q4:** Should terminal failures be replayed, released for retry, or retained only for diagnosis?
- **Q5:** Which response attributes can be stored and replayed safely?

### Required decision gates

- **D1 — API semantics:** The payment API owner must approve whether the header is optional or required, its format/length limits, retention period, and the response for key/payload conflicts. This blocks final API and storage contracts.
- **D2 — Failure semantics:** The payment/domain owner must choose how in-progress, retryable failure, and terminal failure records behave. This blocks the state machine and recovery logic.
- **D3 — Data policy:** The security/data owner must approve which response fields are persisted and the retention/deletion policy. This blocks response snapshot storage and cleanup.

Recommended defaults are an optional `Idempotency-Key` header during rollout, scope by tenant/account plus key, a hash of a canonicalized creation request, and a conflict response when the same scoped key carries a different fingerprint.

## Affected responsibilities

| Responsibility | Proposed change |
|---|---|
| API contract and request validation | Accept the idempotency header, validate bounds, and document replay/conflict semantics. |
| Payment creation handler/service | Pass caller scope, key, and canonical request data into an idempotent creation operation. |
| Idempotency coordinator | Atomically reserve keys, compare fingerprints, replay completed results, and classify in-progress or failed operations. |
| Persistence schema/repository | Store scope, key or keyed digest, request fingerprint, operation status, payment identifier, replay data, timestamps, and expiry. Enforce uniqueness on scope plus key. |
| Payment/provider integration | Ensure only the winning reservation can invoke the provider; preserve any provider-native idempotency key where supported. |
| Event/outbox path | Confirm replay cannot republish payment-created events; couple event publication to the original transaction/outbox record. |
| Error and response mapping | Define stable validation, conflict, in-progress, and replay responses. |
| Cleanup operations | Expire records only after the approved replay window and any payment-provider retry window. |
| Observability | Add low-cardinality metrics and redacted structured logs for outcome classes and latency. |
| API documentation/client examples | Describe key generation, retry behavior, retention, and conflict handling. |

## Implementation slices

### 1. Re-establish repository evidence and settle contracts

- Locate the payment endpoint, authentication scope, service call path, transaction boundary, provider invocation, event/outbox path, schema migrations, test fixtures, and deployment process.
- Characterize current behavior for ordinary creation, validation errors, provider rejection, timeouts, and concurrent requests.
- Resolve D1–D3 and write falsifiable endpoint examples for first request, replay, conflict, in-progress collision, and failure retry.
- Identify exact source files, migration commands, test commands, and CI gates.
- **End state:** an evidence-backed replacement for this provisional topology; no production behavior changed.
- **Replan if:** payment creation spans independently committed services, has no durable transactional store, or already delegates idempotency to an authoritative upstream component.

### 2. Add an additive persistence model

- Add an idempotency record through the repository’s migration framework.
- Enforce uniqueness on the approved scope plus key representation.
- Include an explicit state model such as `in_progress`, `completed`, and the approved failure states.
- Store a canonical request fingerprint and only the minimum replay information approved by D3.
- Add indexes supporting lookup and expiry without introducing a table-wide cleanup scan.
- Keep the migration additive: no backfill of historical payments should be required because old requests have no keys.
- **End state:** old application versions continue operating while the new schema is unused.
- **Verify:** migration applies to an empty database and a representative existing database; rollback or forward-recovery procedure is demonstrated; uniqueness and required-field constraints reject invalid records.

### 3. Implement atomic reservation and replay semantics

- Introduce one owning coordinator for key reservation, fingerprint comparison, state transition, and result replay.
- On the first request, atomically reserve the scoped key before any provider call.
- On a duplicate:
  - replay the completed result when fingerprints match;
  - reject when fingerprints differ;
  - return the approved in-progress behavior when the original operation is unresolved.
- Couple local payment persistence and idempotency completion in one transaction where possible.
- Ensure provider calls, outbox writes, and domain events occur only for the winning request. Forward a stable derived key to providers that support native idempotency.
- Define recovery for a process crash after reservation and before completion.
- **End state:** the capability exists internally but can remain disabled or unused by the public handler.
- **Replan if:** the provider call occurs inside an unsafe long-running database transaction or the current architecture cannot reconcile ambiguous provider outcomes.

### 4. Evolve the endpoint compatibly

- Validate and normalize the header without changing requests that omit it.
- Derive scope exclusively from authenticated server-side identity, never from a client-controlled tenant field.
- Build the fingerprint from fields that determine payment semantics; exclude transport-only data while including amount, currency, destination/customer, and other behavior-changing inputs.
- Route keyed requests through the coordinator and preserve the existing path for unkeyed requests during the compatibility window.
- Return the original externally observable result for a replay, subject to approved treatment of dynamic headers and timestamps.
- Update the canonical API specification and examples.
- **End state:** mixed old and new clients can coexist.

### 5. Add cleanup, telemetry, and operational controls

- Add the repository-standard scheduled cleanup mechanism using bounded batches.
- Do not expire in-progress or unresolved records automatically without a reconciliation rule.
- Emit metrics for first-use requests, successful replays, fingerprint conflicts, in-progress collisions, recovery attempts, and cleanup failures.
- Redact raw keys, fingerprints, payment details, and stored response data from logs.
- Add a runbook for diagnosing stuck records and reconciling ambiguous provider outcomes.
- **End state:** the feature is operable and records have a controlled lifecycle.

## Verification map

Tests should cover:

- First keyed request creates exactly one payment and one downstream side effect.
- Sequential duplicate with the same payload returns the original result and makes no additional provider/event calls.
- Same scoped key with a different payload returns the documented conflict.
- The same key under different approved scopes creates independent payments.
- Many concurrent identical requests produce one winner and one payment.
- A duplicate arriving while the first request is in progress follows D2.
- Retry after application restart replays from durable state.
- Provider rejection, timeout, crash after reservation, crash after provider success, and database commit failure follow the approved recovery policy.
- Unkeyed requests retain current behavior.
- Invalid, missing, oversized, and malformed headers follow the API contract.
- Sensitive values and raw keys do not appear in logs.
- Expiry removes eligible completed records but preserves unresolved records.
- Migration upgrade and recovery work with representative existing data.
- Existing endpoint integration and end-to-end suites remain green.

Exact commands cannot be supplied until the application repository and its manifests are available.

## Rollout and rollback

1. Deploy the additive migration before code that reads or writes idempotency records.
2. Deploy code with keyed handling disabled, dark-launched, or limited to internal clients if the repository supports feature controls.
3. Enable for a canary client or small traffic segment and monitor duplicate creations, conflicts, stuck records, provider-call counts, errors, and latency against existing service objectives.
4. Expand gradually after confirming that replayed requests do not generate provider calls or duplicate events.
5. Publish client guidance and begin adoption. Make the header mandatory only through a separately approved, versioned compatibility change.
6. Start cleanup only after the retention and reconciliation behavior has been observed safely.

Rollback should disable keyed routing while retaining the additive table and records. Avoid dropping the schema during the rollback window: older application versions should ignore it, and retaining records preserves recovery evidence. If duplicate side effects appear, stop expansion, disable new reservations, retain affected records, and reconcile local payments against provider transaction identifiers before retrying or refunding anything.

Implementation remains blocked until the actual payment codebase is available and D1–D3 have accountable owners.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
