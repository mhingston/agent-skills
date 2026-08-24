# Run record

- Case: `AWD-E6`
- Condition: `baseline`
- Prompt: Plan the repository changes needed to add an idempotency key to our payment creation endpoint. Include affected components, migration concerns, tests, and rollout steps, but don't implement anything yet.
- Expected routing: `no target skill`
- Loaded skills observed in Codex events: `plan`
- Final response:

## Plan status: Blocked

The current workspace does not contain the payment service or its application code. It contains only a skills catalogue in [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ouh_lljy/repo/README.md); the `master` branch has no commits, and no endpoint, schema, migration framework, tests, or deployment configuration can be inspected.

Consequently, the component names and commands below are intentionally expressed as responsibilities rather than invented files or symbols. The plan becomes executable once the payment repository—or the correct path/revision—is available.

## Outcome contract

- **R1 — First creation:** A payment-creation request carrying a valid idempotency key creates at most one logical payment.
- **R2 — Safe replay:** Repeating the same key with an equivalent canonical request returns the original outcome and does not repeat payment-provider or other external side effects.
- **R3 — Conflict detection:** Reusing a key with materially different creation parameters returns a stable client error rather than returning or creating the wrong payment.
- **R4 — Concurrency:** Concurrent requests using the same key cannot create two payments.
- **R5 — Compatibility:** Existing clients remain supported according to an explicit policy for whether the key is initially optional or required.
- **R6 — Operability:** Operators can distinguish new requests, successful replays, conflicting reuse, in-progress contention, and failed attempts without logging sensitive key or payment data.
- **R7 — Recovery:** Rollback of application code does not require immediately dropping or rewriting stored idempotency data.

Non-goals: generalized idempotency across every endpoint, provider-wide deduplication, unrelated payment refactoring, and immediate removal of compatibility behavior.

Core invariants:

- The deduplication scope must include the correct tenant/account or merchant boundary, not merely the raw key.
- Claiming a key and establishing the authoritative payment result must be transactionally safe.
- A committed successful payment cannot later be associated with a different request.
- A replay must not repeat downstream side effects such as provider calls, ledger writes, events, or notifications.

## Current evidence and open decisions

- **E1:** Only `README.md` is present; it describes an Agent Skills catalogue, not a payment application.
- **E2:** There are no committed revisions, application manifests, schemas, migrations, tests, CI definitions, or deployment files available.
- **I1:** Exact affected components and verification commands cannot be identified from E1–E2.
- **Q1:** Which repository, service, endpoint version, and revision own payment creation?
- **Q2:** Where is the payment’s authoritative state, and which transaction boundary covers payment persistence and side effects?
- **Q3:** Is the key supplied in an HTTP header, request field, or both? What length, character, and retention limits apply?
- **Q4:** Must clients provide a key immediately, or is adoption additive first?
- **Q5:** What should happen when the original request is still processing or ended in an ambiguous provider timeout?
- **Q6:** Are key records subject to retention, privacy, audit, or regional-storage requirements?

### Decision gates

- **D1 — API policy, owner: payments API/product owner.** Decide key location, validation, required-versus-optional compatibility window, conflict status/error contract, and retention period. Blocks final API and schema contracts.
- **D2 — Failure semantics, owner: payments engineering owner.** Decide whether failures are replayed, retried, or reconciled, especially for ambiguous downstream timeouts. Blocks state-machine implementation and recovery behavior.
- **D3 — Rollout acceptance, owner: service operations owner.** Select existing latency/error objectives and abort thresholds for the canary. Blocks production expansion, not implementation.

## Proposed responsibility and interface map

These are proposed boundaries to validate against the real repository:

| Responsibility | Contract |
|---|---|
| API transport/validation | Extract and validate the idempotency key while preserving the existing payment request contract |
| Payment application service | Canonicalize relevant request semantics, coordinate key acquisition, and return created/replayed/conflict outcomes |
| Idempotency store or payment repository | Atomically enforce uniqueness for a scoped key and retain request fingerprint, processing state, payment/result reference, and timestamps |
| Provider/ledger/event integrations | Execute only for the request that successfully owns the key |
| API error mapping | Expose stable validation, conflict, and in-progress/retry semantics |
| Telemetry | Record outcome classes and latency with hashed/redacted identifiers |
| Cleanup/retention process | Expire records only after the approved replay and reconciliation window |

Preferred design: a database-enforced unique key such as `(merchant_or_account_scope, endpoint_operation, idempotency_key)`, combined with a canonical request fingerprint. The database constraint—not a check-then-insert application query—should arbitrate concurrent ownership.

A separate idempotency table is usually preferable to placing the raw key directly on `payments`: it can represent in-progress and failed attempts before a payment ID exists. This remains conditional on the actual schema and transaction model.

## Implementation slices

### 1. Repository and behavior discovery

- **Outcome:** Replace Q1–Q6 with observed contracts and locate every side effect in the creation path.
- **Work:** Trace routing → validation → payment orchestration → database transaction → provider/ledger/events; inspect retries, error mapping, migrations, tests, deployment, and telemetry.
- **Verify:** Produce an evidenced call path, transaction boundary, consumer inventory, and discovered test/migration commands.
- **Replan if:** Payment creation spans independently deployed services or side effects occur outside a recoverable transaction/outbox mechanism.

### 2. Freeze API and idempotency semantics

- **Dependencies:** D1 and D2.
- **Outcome:** A single documented state machine and compatibility contract.
- **Work:** Define scope, normalization, fingerprint fields, replay response, conflict response, in-progress behavior, failure retry policy, key limits, retention, and whether generated server keys are forbidden.
- **Produces:** Behavioral contract consumed by storage, service logic, tests, documentation, and telemetry.
- **Verify:** Contract tests cover absent/invalid keys, equivalent replay, conflicting reuse, concurrency, failures, and tenant isolation.
- **Replan if:** Existing clients already use a conflicting key convention or intermediaries strip the chosen header.

### 3. Add storage through an expand-only migration

- **Outcome:** New idempotency state can be stored without changing existing request behavior.
- **Work:** Add the record structure and database uniqueness constraint. Include scoped key or protected representation, canonical fingerprint, status, payment/result reference, timestamps, and any required lease/version metadata.
- **Migration concerns:**
  - Keep the migration additive; no initial backfill is normally needed for pre-existing payments.
  - Avoid a table rewrite or long blocking index build at production scale.
  - Size indexes using expected request volume and retention.
  - Define cleanup so records cannot expire while a provider result remains ambiguous.
  - Encrypt or hash keys if they can contain customer information; never treat hashing alone as a uniqueness strategy without collision handling.
- **Verify:** Migration succeeds on an empty and representative populated database; uniqueness and tenant isolation are proven; old application versions operate with the expanded schema.
- **End state:** Deployable and reversible by leaving unused storage in place.
- **Replan if:** The database cannot atomically arbitrate claims or schema changes require downtime.

### 4. Integrate atomic claim, replay, and conflict handling

- **Outcome:** One request owns payment creation; equivalent retries replay its result.
- **Work:** Within the strongest available transaction boundary:
  1. attempt to claim the scoped key;
  2. compare the stored fingerprint on collision;
  3. return conflict for a mismatch;
  4. replay a completed equivalent result;
  5. apply the approved in-progress/failure policy;
  6. ensure only the owner invokes downstream effects.
- **Verify:** Unit and integration tests exercise transaction rollback, provider failures, process interruption, and simultaneous requests. Assert exactly one payment and one downstream-effect set.
- **Replan if:** Provider execution and local persistence can produce an unreconcilable ambiguous state; add provider idempotency and/or an outbox/reconciliation design before rollout.

### 5. Complete API integration and client compatibility

- **Outcome:** The endpoint exposes the approved behavior without unexpectedly breaking older callers.
- **Work:** Add extraction/validation, response mapping, API schema/documentation, examples, and generated-client updates if the repository owns them. During an additive window, observe missing-key traffic before enforcing a requirement.
- **Verify:** Endpoint/contract tests prove existing request behavior, new-key behavior, stable error payloads, and replay response equivalence.
- **End state:** Old and new clients can coexist for the D1-approved window.

### 6. Add telemetry and operational recovery

- **Outcome:** The feature can be diagnosed and safely controlled.
- **Work:** Add counters and traces for claims, replays, conflicts, contention, failures, ambiguous states, and reconciliation age. Redact raw keys and payment data. Add operator guidance for stuck records and ambiguous provider results.
- **Verify:** Tests or a non-production exercise demonstrate each signal and recovery path. Confirm telemetry has bounded cardinality.
- **Replan if:** Operators cannot correlate a stuck idempotency record to its payment/provider attempt without exposing sensitive data.

### 7. Roll out progressively

- Deploy the additive migration first and confirm database health.
- Deploy code with enforcement disabled or the key optional, if the repository supports a suitable reversible control.
- Enable internal/test traffic; verify creation, replay, conflict, concurrency, and provider-call counts.
- Canary a small production cohort and compare existing latency/error objectives plus duplicate-payment signals.
- Expand gradually after D3 acceptance.
- If the key will become mandatory, announce the compatibility window, measure missing-key use, update clients, then enforce in a later release.
- Retain the old code-compatible schema through the rollback window; consider destructive cleanup only as a separate change.

Rollback should disable the new behavior or restore the previous routing path while leaving the additive table/columns intact. Do not drop idempotency records during rollback: they may be required to prevent repeats or reconcile ambiguous attempts.

## Verification map

- **R1/R4:** Parallel integration test → exactly one payment and one downstream-effect set; uniqueness constraint remains satisfied.
- **R2:** Same scoped key and equivalent request → same payment/result, no additional provider/ledger/event calls.
- **R3:** Same scoped key and different canonical request → approved conflict response, no new payment.
- **R5:** Contract tests for old and new clients throughout the compatibility window.
- **R6:** Telemetry exercise emits bounded, redacted signals for every state.
- **R7:** Rollback rehearsal runs the prior application version against the expanded schema without losing deduplication/reconciliation data.
- **Tenant invariant:** Same raw key in different authorized scopes behaves independently; cross-scope lookup cannot disclose another payment.
- **Failure invariant:** Forced provider timeout and process interruption produce the D2-approved retry or reconciliation state, never an untracked second attempt.

Handoff remains blocked until the payment repository and revision are supplied. Once available, the discovery slice should be run first and the placeholder component names, contracts, and commands replaced with exact repository evidence before implementation begins.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
