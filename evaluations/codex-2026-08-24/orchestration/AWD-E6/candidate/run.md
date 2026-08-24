# Run record

- Case: `AWD-E6`
- Condition: `candidate`
- Prompt: Plan the repository changes needed to add an idempotency key to our payment creation endpoint. Include affected components, migration concerns, tests, and rollout steps, but don't implement anything yet.
- Expected routing: `no target skill`
- Loaded skills observed in Codex events: `plan`
- Agent-reported selection (not a native harness event): `none`
- Final response:

**Plan Status**  
`Conditional` - the repository snapshot available here does not include the payment endpoint implementation, so the plan is based on the requested behaviour and the repo-level evidence that this workspace is a skill/documentation repository, not an application codebase. The main unresolved item is the actual payment service stack and persistence layer.

**Outcome Contract**  
`R1` Payment creation becomes idempotent when the client supplies an idempotency key. Replaying the same request with the same key returns the original successful result instead of creating a second payment.

`R2` The API rejects or cleanly handles key reuse with a different request payload according to the chosen contract.

`R3` Idempotency state is durable across retries and service restarts.

`R4` The change is backward compatible for clients that do not send a key unless the current product decision is to make the key required.

`R5` The implementation is observable, test-covered, and safe to roll out incrementally.

Scope:
- Payment creation endpoint only.
- API contract, persistence, application service logic, and tests.
- Deployment and migration steps needed to preserve existing behaviour.

Non-goals:
- No changes to payment authorization, capture, refund, or ledger semantics unless they share the same creation path.
- No unrelated refactors.
- No UI changes unless the endpoint contract is surfaced there.

Constraints and invariants:
- One idempotency key must map to at most one committed payment creation outcome.
- A retry must not create duplicate side effects.
- If the request body differs for the same key, the system must not silently return a mismatched result.
- The replay response should be deterministic and derived from stored outcome data, not recomputed from scratch.

Governing context:
- The only repo-local evidence available is the repository README, which defines the workspace as a catalogue of reusable Agent Skills and agent workflow artefacts, not an application-specific payment system. See [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ntaxypax/repo/README.md#L1) and the artifact conventions in [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ntaxypax/repo/README.md#L55).

**Current-State Evidence**  
`E1` The repo root currently contains only `README.md` from the visible snapshot, so the payment endpoint source is not present in the inspected tree. This limits file-specific planning.  
Source: [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ntaxypax/repo/README.md)

`E2` The README defines repository-local workflow artefact conventions under `.agent-artifacts/...`, which matters if implementation planning or review artefacts need to be stored, but it does not describe the application domain.  
Source: [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ntaxypax/repo/README.md#L55)

`Q1` What stack backs the payment creation endpoint: HTTP framework, language, ORM, and database?  
This determines the exact migration and test slices.

`Q2` Is the idempotency key optional for all clients, or will it be required for some or all callers?  
This determines the compatibility strategy.

`Q3` What response should be returned on duplicate submission with the same key and same payload: cached full response, payment ID only, or a typed “already processed” response?  
This determines storage shape and replay behaviour.

**Approach and Decisions**  
Selected design:
- Store an idempotency record keyed by a client-provided token and scoped to the payment-creation operation.
- Associate that record with the resulting payment identifier, status, request fingerprint, and response payload or enough fields to reconstruct the response.
- Enforce uniqueness at the persistence layer so concurrency races cannot create duplicates.

Alternatives considered:
- In-memory deduplication: rejected, because it is not durable across restarts.
- Payment-table-only uniqueness on a client reference: acceptable only if the product already has a stable external reference field; otherwise insufficient because it couples business identity to retry identity.
- Hash-only deduplication without a client key: rejected, because legitimate retries can differ in non-semantic fields and payload hashing alone can be fragile.

Transition strategy:
- Add the persistence and service logic in an additive way first.
- Backfill or default existing rows only if the endpoint needs to replay historical requests.
- Keep the old behaviour available for clients that do not send a key until rollout is complete.

Continuity status:
- `new` because there is no visible prior implementation or decision record in the inspected repo.

**Implementation Slices**  

1. **Outcome**: Define the endpoint contract for idempotent payment creation.  
   **Basis**: `R1`, `R2`, `R4`, `Q2`, `Q3`.  
   **Why**: The storage and retry semantics depend on the public API contract.  
   **Affects**: API spec, request/response schema, error mapping, and developer docs.  
   **Work**: Specify whether the idempotency key is required or optional, where it is passed, how mismatched payload reuse is handled, and what response is replayed.  
   **Dependencies**: Product decision on key requirement and replay semantics.  
   **Produces**: Stable request/response contract for the application and tests.  
   **Verify**: Contract tests or schema validation for accepted, replayed, and rejected duplicate requests.  
   **End state**: API behaviour is defined without ambiguity.  
   **Replan if**: The product decides the key must be global instead of endpoint-scoped, or replay must return a different shape.

2. **Outcome**: Add durable idempotency storage.  
   **Basis**: `R1`, `R3`, `R5`.  
   **Why**: Durable deduplication needs persistence and a uniqueness guarantee.  
   **Affects**: Database schema, migration, ORM model, repository layer.  
   **Work**: Introduce an idempotency table or equivalent columns with a unique constraint on `(operation, idempotency_key)` or equivalent scope. Store request fingerprint, payment ID, status, timestamps, and replay payload or enough reconstructable fields.  
   **Dependencies**: Schema ownership and migration tooling in the actual codebase.  
   **Consumes**: Contract from slice 1 about scope and replay semantics.  
   **Produces**: Durable lookup for retries and race prevention.  
   **Verify**: Migration applies cleanly; uniqueness constraint prevents duplicate inserts; model round-trip tests pass.  
   **End state**: The system can record and look up idempotent payment attempts durably.  
   **Replan if**: The current payment schema already has a safe, stricter uniqueness mechanism that can absorb this requirement.

3. **Outcome**: Implement service-layer idempotency logic in payment creation.  
   **Basis**: `R1`, `R2`, `R3`.  
   **Why**: The endpoint must consult idempotency state before creating a payment and must make the create operation race-safe.  
   **Affects**: Payment service, repository methods, transaction boundaries, and error translation.  
   **Work**: On request entry, look up by key; if found with matching fingerprint, return stored outcome; if found with mismatched fingerprint, return the agreed conflict/error; if absent, create the payment and idempotency row atomically or with a safe retryable transaction pattern.  
   **Dependencies**: Slice 2 complete.  
   **Consumes**: The contract and storage model from prior slices.  
   **Produces**: Idempotent create path with a deterministic replay path.  
   **Verify**: Unit tests for first write, same-key retry, mismatched payload reuse, and concurrency race handling.  
   **End state**: Duplicate submissions do not create duplicate payments.  
   **Replan if**: The existing transaction model cannot safely support atomic create-plus-record without broader refactoring.

4. **Outcome**: Update endpoint wiring and request validation.  
   **Basis**: `R1`, `R2`, `R4`.  
   **Why**: The transport layer must enforce the contract and propagate the key to the service.  
   **Affects**: HTTP handler/controller, validation middleware, DTOs, API docs.  
   **Work**: Parse the idempotency key from the agreed location, validate presence if required, pass it through to the service, and surface the correct replay/conflict responses.  
   **Dependencies**: Slices 1 and 3.  
   **Consumes**: The service contract and error semantics.  
   **Produces**: End-to-end API behaviour consistent with the contract.  
   **Verify**: Handler-level tests or endpoint integration tests for accepted, replayed, and rejected cases.  
   **End state**: The endpoint exposes the feature correctly to clients.  
   **Replan if**: The request format differs materially from the assumed header/body placement.

5. **Outcome**: Add regression coverage and rollout observability.  
   **Basis**: `R1`-`R5`.  
   **Why**: Idempotency bugs are usually concurrency or contract regressions, so the safety net must exercise both.  
   **Affects**: Test suite, logging/metrics/tracing, deployment checks.  
   **Work**: Add focused tests for retry semantics and race conditions; add metrics for idempotency hits, misses, conflicts, and duplicate-prevented creations; ensure logs can correlate a payment attempt with its idempotency key without exposing sensitive data.  
   **Dependencies**: Slices 2-4.  
   **Produces**: Regression protection and rollout signals.  
   **Verify**: Automated tests pass; metrics appear in staging; logs/traces allow replay diagnosis.  
   **End state**: The change is measurable and diagnosable in production.  
   **Replan if**: The repository has a mandated observability standard that requires a different instrumentation path.

**Verification Map**  
`R1`:
- Slice 1: contract tests define replay semantics.
- Slice 3: unit tests verify same-key retries return the original result.
- Slice 4: end-to-end endpoint tests confirm correct transport behaviour.

`R2`:
- Slice 1: contract test for same-key/different-payload conflict.
- Slice 3: service tests verify mismatch detection.
- Slice 4: endpoint test asserts the correct error status and body.

`R3`:
- Slice 2: migration and unique-constraint validation.
- Slice 3: transactional tests prove persistence survives retries/restarts.

`R4`:
- Slice 1: explicit optional-versus-required decision.
- Slice 4: validation tests confirm old clients still work if optional.

`R5`:
- Slice 5: metrics/logging assertions and staging smoke checks.
- All slices: CI gates for unit, integration, and migration validation.

**Operational Transition**  
Migration:
- Add the idempotency schema in an additive migration first.
- If historical replay support is required, consider a backfill only if there is an existing stable client reference to map from.
- Keep rollback easy by making the feature read-compatible before write-enforcing.

Compatibility:
- Prefer additive request support over breaking required-field changes unless the product decision says otherwise.
- If the key is optional, clients can adopt it incrementally.
- If the key is required, phase it behind a warning period or versioned endpoint if the current API is public.

Rollout:
- Deploy schema first.
- Deploy application code that writes and reads idempotency records.
- Enable observability and confirm duplicate-hit counters remain low but nonzero in retry scenarios.
- Gradually expose the contract if there is any risk of breaking existing clients.

Rollback:
- Application rollback should remain possible after schema deployment.
- If the schema cannot be safely rolled back, use a forward-only migration plan and keep the code compatible during rollback windows.

**Handoff Controls**  
- Revalidate the actual payment codebase, framework, and persistence layer before implementation.
- Resolve `Q1`-`Q3` before starting work that would otherwise be speculative.
- Treat the idempotency contract as authoritative once approved; do not silently change replay or conflict semantics during implementation.
- If the current repository differs from the assumed shape, re-scope the slices to the actual files and migration system before coding.

If you want, I can turn this into a tighter, repo-specific implementation plan once you point me at the payment service files or the actual codebase.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
