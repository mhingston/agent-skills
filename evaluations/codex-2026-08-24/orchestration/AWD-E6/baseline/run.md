# Run record

- Case: `AWD-E6`
- Condition: `baseline`
- Prompt: Plan the repository changes needed to add an idempotency key to our payment creation endpoint. Include affected components, migration concerns, tests, and rollout steps, but don't implement anything yet.
- Expected routing: `no target skill`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

This repository does not currently contain any payment-service code to inspect beyond the skills catalog, so I can’t name exact files yet. Based on the requested change, the repository plan should cover these areas:

**Plan**
1. API contract
- Add `idempotency_key` to the payment creation request schema.
- Define validation rules: required vs optional, max length, allowed charset, and whether the key is scoped per user/account/merchant.
- Define response behavior for duplicate keys:
- Same request payload: return the original payment response.
- Same key, different payload: reject with a conflict/error.

2. Payment service logic
- Resolve the request through an idempotency lookup before creating a payment.
- Ensure the create flow is atomic so two concurrent requests with the same key cannot create two payments.
- Persist the idempotency record before or as part of the payment write, depending on current transaction boundaries.
- Decide what to return for in-flight retries: existing result, retry-after, or a bounded “processing” state.

3. Persistence layer
- Add an idempotency table or equivalent storage if one does not already exist.
- Store at minimum:
- idempotency key
- actor/tenant scope
- request fingerprint or payload hash
- created payment identifier
- response status and body reference, if needed
- timestamps and expiry metadata
- Add a uniqueness constraint over the key plus scope.
- Add TTL/expiry cleanup policy if keys should only be retained for a window.

4. Migration concerns
- Create a forward-only migration for the new table/index/constraint.
- If the existing schema already has a candidate field, decide whether to reuse it or add a dedicated table.
- Backfill is likely not needed unless you want historical deduplication.
- Plan for rollback: schema removal is easy, but any live retries after rollback may lose deduplication guarantees.
- If multiple services consume payment creation, confirm whether the idempotency scope must be shared across them.

5. Error handling and observability
- Emit structured logs for idempotency hits, misses, conflicts, and replayed responses.
- Add metrics for duplicate submissions, conflict rate, and replay latency.
- Make sure error payloads do not leak sensitive request data.
- Document retry semantics for clients and support teams.

6. Tests
- Unit tests:
- first request creates payment
- repeated request with same key returns same payment
- same key with different payload is rejected
- expired key behavior
- key scoping behavior
- Integration tests:
- concurrent duplicate requests create only one payment
- persistence survives service restart
- replay returns the original status code and body
- API contract tests:
- request validation
- backward compatibility for clients that do not yet send the key, if supported
- Regression tests:
- ensure non-idempotent behavior is not reintroduced via alternate code paths, webhooks, or retries

7. Rollout steps
- Ship schema migration first.
- Deploy code that accepts the new field but preserves existing behavior for callers not using it, if backward compatibility is required.
- Enable idempotency enforcement behind a feature flag if you want a controlled rollout.
- Roll out to a small traffic slice or one tenant first.
- Monitor duplicate submission metrics, conflict rates, and payment creation success rates.
- Remove the flag once behavior is stable and documented.

8. Client/documentation updates
- Update API docs with retry guidance and examples.
- Tell clients whether they generate the key per user action, per checkout attempt, or per API retry.
- Clarify key lifetime and uniqueness scope.

If you want, I can next turn this into a concrete implementation checklist mapped to your actual repo once you point me at the payment-service codebase.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
