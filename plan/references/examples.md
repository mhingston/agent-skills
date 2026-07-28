# Representative Examples

These are fictional calibration examples. Their `E#` entries are observations supplied by each scenario, not claims about a real repository. Preserve the structure and evidence discipline, not the technology choices or amount of prose.

## Contents

1. Focused validation change
2. Cross-cutting online data migration
3. Ambiguous infrastructure replacement

## 1. Focused validation change

### Prompt

> Cap `pageSize` at 100 on the list-orders endpoint and give me an implementation plan.

### Illustrative plan

**Plan status: Ready.** The current validation owner, tests, and repository commands are evidenced; no material design decision is open.

#### Outcome contract

- `R1`: Requests with an integer `pageSize` from 1 through 100 retain their current behaviour.
- `R2`: Requests with `pageSize` greater than 100 return the endpoint's existing 400 validation envelope.
- `R3`: Invalid requests do not invoke order retrieval.
- Scope: list-orders request validation and its focused route tests.
- Non-goals: changing the default page size, pagination protocol, error-envelope format, or other endpoints.
- Invariant: the HTTP validation layer remains the single owner of transport input bounds.
- Completion: focused tests demonstrate both boundaries and the repository type check passes.

#### Current-state evidence

| ID | Class | Statement and locator | Implication |
| --- | --- | --- | --- |
| `E1` | Observed | `src/http/orders/list-orders.ts`, symbol `listOrdersQuerySchema`, accepts positive integers and defaults to 25 but sets no maximum | Change the existing schema rather than adding service-layer policy |
| `E2` | Observed | `test/http/orders/list-orders.test.ts`, describe block `pageSize validation`, already covers zero and non-integer values and asserts the common error envelope | Extend the existing boundary-test location and assertion style |
| `E3` | Observed | The route passes validated input to `OrderReader.list`; the test fixture exposes a call spy | `R3` can be checked without a new test seam |
| `E4` | Observed | `package.json` defines `test:unit` and `typecheck`; CI invokes both | Use repository-owned commands |

#### Approach

Keep the bound in `listOrdersQuerySchema`, where adjacent transport validation already lives. Add boundary cases before changing the schema. No alternative design is warranted because moving the rule into the service would duplicate transport validation and expand scope.

#### Implementation slice

**`S1` — Enforce and prove the page-size boundary**

- **Outcome:** the endpoint accepts 100, rejects 101 with the existing validation response, and performs no retrieval for the rejected request.
- **Basis:** `R1–R3`, `E1–E4`.
- **Why:** one owner and one focused test cycle fully deliver this local behaviour.
- **Affects:** `listOrdersQuerySchema` and its existing route-test block.
- **Work:** first add cases for 100 and 101, including the retrieval-spy assertion for 101; confirm the 101 case fails for the missing maximum; then add the maximum constraint to the existing schema without changing the default or error mapping.
- **Dependencies:** none.
- **Verify:** run `pnpm test:unit -- test/http/orders/list-orders.test.ts`; expect the new 101 case to fail before the schema change and the whole file to pass afterward. Run `pnpm typecheck`; expect exit code 0 and no new diagnostics.
- **End state:** a buildable, reviewable local change with no migration, rollout, or compatibility mechanism.
- **Replan if:** the failing test shows a downstream limit or different validation owner, or another public endpoint shares this schema.

#### Verification map

| Requirement | Slice | Deterministic evidence |
| --- | --- | --- |
| `R1` | `S1` | boundary test for 100 passes |
| `R2` | `S1` | 101 test observes existing 400 envelope |
| `R3` | `S1` | retrieval spy remains uncalled for 101 |
| Invariant | `S1` | validation remains in the existing schema; type check passes |

#### Handoff controls

Revalidate that the schema and commands are unchanged before execution. Stop and replan if the schema is shared with another endpoint because the affected consumer set would be broader than this plan.

## 2. Cross-cutting online data migration

### Prompt

> Move account preference JSON into a dedicated table without user-visible downtime. Plan the work.

### Illustrative plan

**Plan status: Conditional.** The safe transition is evidenced, but the owner must set the production consistency and soak gates before read cutover and cleanup.

#### Outcome contract

- `R1`: Preserve the exact preference document observed by users throughout the migration.
- `R2`: Support rolling application deployments in which adjacent versions coexist.
- `R3`: Do not lose a preference update during backfill, cutover, rollback, or retry.
- `R4`: Make read cutover reversible without a data restore while the compatibility window is open.
- `R5`: Remove the legacy column only in a later change after an approved exit gate.
- Scope: preference persistence, online migration machinery, comparison telemetry, deployment gates, runbook, and eventual cleanup.
- Non-goals: changing preference semantics, normalizing individual preference keys, or redesigning the account aggregate.
- Invariants: account ID remains the preference identity; writes are idempotent; one representation is named authoritative at each stage; mixed versions never require a schema they cannot use.
- Completion: migration validation, concurrency tests, a zero-mismatch consistency check, canary health, a demonstrated read rollback, and an approved cleanup gate.

#### Current-state evidence

| ID | Class | Statement and locator | Implication |
| --- | --- | --- | --- |
| `E1` | Observed | `accounts.preferences_json` is read and written only through `AccountPreferencesRepository`; callers exchange a domain `Preferences` value | Preserve the repository contract while changing storage behind it |
| `E2` | Observed | `accounts.updated_at` advances in the same transaction as preference updates | Use it to prevent an older backfill value from overwriting a newer mirrored write |
| `E3` | Observed | Database migrations are additive first; existing online migrations use reviewed triggers and `./gradlew flywayValidate` | A temporary database mirror fits established transition practice |
| `E4` | Observed | Deployments are rolling and may run adjacent application versions | New-table-only writes are unsafe during initial rollout |
| `E5` | Observed | `BatchJob` provides checkpointed, retryable database batches and emits OpenTelemetry counters | Reuse it for bounded backfill and progress evidence |
| `E6` | Observed | `FeatureFlags` supports percentage read rollout and immediate disable | Use it for reversible read cutover |
| `Q1` | Open | Which existing service objective and mismatch duration constitute approval to cut reads over? | The owner must define the gate before `S5` |
| `Q2` | Open | How long must rollback compatibility remain before legacy storage may be contracted? | The owner must define the gate before `S6` |

#### Approach and transition states

Keep the current column authoritative while mixed old versions may write it. Add a dedicated table and a temporary old-to-new database mirror so every version participates. Backfill idempotently using account update time, then compare old and new reads. Deploy dual-write-capable application code while the old column is still authoritative. Cut reads to the new table behind the existing flag only after the consistency gate. Retain both writes through the rollback window; contract the old representation separately.

A direct one-shot migration was rejected because it conflicts with rolling deployment and makes `R2–R4` difficult to prove. Immediate application dual writes were rejected for the first stage because old application versions would still write only the old column.

#### Implementation slices

**`S1` — Establish migration contracts**

- **Outcome:** executable tests capture repository semantics, concurrent update behaviour, mixed-version compatibility, and rollback expectations before storage changes.
- **Basis:** `R1–R4`, `E1–E4`.
- **Why:** the transition must preserve existing behaviour and reject lost-update designs.
- **Affects:** repository integration tests and database-migration test fixtures.
- **Work:** add characterization tests for document round trips and absence semantics; add a concurrency case in which a user update races a backfill candidate; add compatibility fixtures representing the schema visible to the current and next application versions.
- **Dependencies:** none.
- **Verify:** run `./gradlew test --tests '*AccountPreferencesRepository*'` and the repository's migration compatibility test task; expect new transition cases to fail only for missing migration behaviour, while existing characterization cases pass.
- **End state:** production code is unchanged; migration invariants are executable.
- **Replan if:** preference writes bypass the repository or account update time is not transactionally reliable.

**`S2` — Expand storage and mirror authoritative writes**

- **Outcome:** a dedicated preference table can receive an account's document and source update time; all old-column writes are mirrored idempotently while the old column remains authoritative.
- **Basis:** `R2–R4`, `E2–E4`, `S1`.
- **Why:** additive storage plus a database-level mirror covers mixed application versions.
- **Affects:** migration definitions, schema validation, and migration runbook.
- **Work:** add the table with account identity, document, and source-update ordering needed by the race test; add the reviewed temporary mirror using the repository's established trigger convention; keep reads and application writes unchanged.
- **Dependencies:** `S1`; database owner review.
- **Verify:** run `./gradlew flywayValidate` and migration integration tests; expect forward migration from the supported prior schema, mirrored insert/update/delete semantics, and compatibility fixtures to pass.
- **End state:** both representations exist; the old column is authoritative; disabling the trigger and reverting the additive migration before backfill remains possible.
- **Replan if:** trigger execution cannot preserve transaction or ordering semantics under representative load.

**`S3` — Backfill with resumable integrity evidence**

- **Outcome:** existing accounts are copied without overwriting newer mirrored values, and progress can resume after interruption.
- **Basis:** `R1`, `R3`, `E2`, `E5`, `S2`.
- **Why:** cutover cannot rely on unmeasured or non-repeatable data movement.
- **Affects:** a `BatchJob` migration job, counters, an invariant query, and its runbook.
- **Work:** add checkpointed batches ordered by stable account identity; make retries idempotent and conditional on source update time; emit scanned, copied, skipped-newer, failed, and mismatch counts; define the zero-mismatch consistency query used by later gates.
- **Dependencies:** `S2`.
- **Verify:** run the batch-job integration tests with interruption, retry, and concurrent preference update; run the invariant query on the test fixture and expect zero semantic mismatches.
- **End state:** the new table is populated but not read by users; the job is safe to rerun; reads still require no rollback.
- **Replan if:** representative batch load violates an existing database budget or mismatches cannot be classified deterministically.

**`S4` — Add comparison reads and transactionally safe dual writes**

- **Outcome:** new application versions can compare both representations and maintain both in one transaction without changing user-visible reads.
- **Basis:** `R1–R4`, `E1`, `E4`, `E6`, `S3`.
- **Why:** shadow evidence must precede authority change, and dual writes preserve simple rollback after it.
- **Affects:** `AccountPreferencesRepository`, comparison telemetry, feature-flag configuration, and integration tests.
- **Work:** retain old reads as the returned value; read the new value for comparison and emit redacted mismatch categories; update both representations transactionally in the established repository boundary; retain the temporary mirror for old versions and make repeated new writes idempotent.
- **Dependencies:** `S3`.
- **Verify:** run repository, concurrency, and mixed-version integration tests plus `./gradlew check`; expect identical returned behaviour, no lost update, redacted comparison data, and no duplicate side effects.
- **End state:** old reads remain authoritative; both stores stay current; comparison can be disabled without a deployment.
- **Replan if:** both writes cannot share a transaction or comparison exposes sensitive document content.

**`S5` — Gate and cut reads over**

- **Outcome:** production reads move gradually to the new table with observable abort conditions and immediate fallback to the old read path.
- **Basis:** `R1–R4`, `E6`, `Q1`, `S4`.
- **Why:** real traffic evidence is required before the new representation becomes authoritative for reads.
- **Affects:** read-routing flag, deployment runbook, dashboards, alerts, and post-deploy verification.
- **Work:** obtain the owner-defined `Q1` gate; deploy comparison mode first; require completed backfill and zero unexplained mismatches; increase the existing percentage flag in approved stages; verify service and preference correctness signals at each gate; document flag disable as the first rollback action.
- **Dependencies:** `S4`, resolved `Q1`, production approval.
- **Verify:** run the post-deploy consistency check and existing service health checks at each stage; expect the approved mismatch and service-objective gates to hold. Exercise flag disable in a non-production environment and observe immediate old-path reads without lost writes.
- **End state:** the new table is read-authoritative; both writes continue; rollback is a flag change.
- **Replan if:** mismatches, latency, error rate, or replication behaviour breach the approved gate.

**`S6` — Close compatibility and contract legacy storage**

- **Outcome:** the temporary mirror, legacy writes, and old column are removed only after rollback obligations end.
- **Basis:** `R5`, `Q2`, `S5`.
- **Why:** destructive cleanup must not collapse the proven rollback window.
- **Affects:** repository write path, trigger migration, legacy column migration, runbook, and obsolete telemetry.
- **Work:** obtain the owner-defined `Q2` exit gate; first deploy new-table-only code while retaining the legacy column; verify no supported version or recovery path uses it; remove the mirror; contract the column in a separate additive-compatible release boundary; delete comparison telemetry only after the final integrity record is retained.
- **Dependencies:** successful `S5`, resolved `Q2`, confirmation that no old application version can run.
- **Verify:** run migration validation, full repository checks, deployment compatibility checks, and the final invariant query; expect no legacy references, zero unexplained mismatches, and a clean supported-version matrix.
- **End state:** one authoritative representation remains; rollback now uses normal database recovery rather than read fallback.
- **Replan if:** an old application version or operational recovery procedure still depends on the column.

#### Verification map

| Requirement | Slices | Deterministic evidence |
| --- | --- | --- |
| `R1` | `S1`, `S3–S5` | round-trip tests and zero-mismatch invariant |
| `R2` | `S1`, `S2`, `S4` | schema compatibility and mixed-version tests |
| `R3` | `S1–S4` | concurrent update, interruption, retry, and idempotency tests |
| `R4` | `S4`, `S5` | dual-write tests and exercised read-flag rollback |
| `R5` | `S6` | supported-version scan, migration validation, final invariant |

#### Handoff controls

Revalidate the current schema revision, supported application versions, flag behaviour, and database migration conventions before each slice. Stop equivalent retries after two failed attempts and retain the failure evidence. Replan if any writer bypasses the observed repository boundary, if migration load exceeds existing budgets, or if the business changes preference semantics during the transition.

## 3. Ambiguous infrastructure replacement

### Prompt

> Replace our Redis queue with Kafka. Plan it.

### Illustrative plan

**Plan status: Blocked.** Repository evidence describes current semantics but neither the desired outcome nor the target platform constraints. Selecting Kafka or writing implementation slices now would be architecture-first speculation.

#### Provisional outcome contract

- Stated request: replace the current queue technology.
- Missing outcome: no measured reliability, throughput, ordering, cost, operability, or product problem explains the replacement.
- Provisional non-goal: do not alter queue implementation or provision infrastructure during investigation.
- Current invariants discovered: at-least-once delivery, per-account ordering, delayed retry, explicit dead-letter handling, and bounded worker shutdown.

#### Current-state evidence

| ID | Class | Statement and locator | Implication |
| --- | --- | --- | --- |
| `E1` | Observed | `JobQueue` exposes enqueue, reserve, acknowledge, retry-at, and dead-letter operations | A replacement must preserve or deliberately revise these semantics |
| `E2` | Observed | Worker integration tests assert duplicate-safe processing and per-account order | “Kafka-compatible” is not sufficient acceptance evidence |
| `E3` | Observed | Deployment configuration provisions managed Redis; no Kafka client, topic, ACL, schema registry, or operator runbook exists | The change crosses application and platform ownership |
| `E4` | Observed | Repository metrics expose queue age, retry count, and dead letters, but no retained production values are accessible | The planner cannot establish the current problem or baseline |
| `I1` | Inferred | The request may be driven by scale or reliability, but `E1–E4` do not establish which | Do not optimize for an imagined motive |
| `Q1` | Open | What user or operational problem must be solved, and what measurable target defines success? | Determines whether replacement is justified |
| `Q2` | Open | Is there an approved, operated Kafka platform with named ownership, security, retention, and schema conventions? | Determines feasibility and responsibility |
| `Q3` | Open | Must in-flight work migrate without pause, and which current delivery, ordering, delay, and dead-letter semantics may change? | Determines architecture and transition strategy |

#### Bounded investigation plan

**`S0` — Establish the decision criteria and current baseline**

- **Outcome:** an owner-approved problem statement and measurable comparison criteria.
- **Basis:** `E4`, `I1`, `Q1`.
- **Why:** technology replacement is not an outcome.
- **Affects:** no implementation; produces a decision record using existing telemetry.
- **Work:** obtain representative queue-age, throughput, failure, retry, cost, and incident evidence from the service owner; identify the breached or future target; record data range and source.
- **Dependencies:** access to production telemetry and the service owner.
- **Verify:** the decision record names a baseline, target, measurement window, and owner; missing evidence remains explicit.
- **End state:** no repository or infrastructure mutation.
- **Replan if:** the evidence shows the problem is outside the queue or can be solved within current constraints.

**`S1` — Specify required queue semantics and platform constraints**

- **Outcome:** an executable behaviour contract and an owned platform capability matrix.
- **Basis:** `E1–E3`, `Q2`, `Q3`.
- **Why:** delivery and operational semantics, not API resemblance, determine substitutability.
- **Affects:** investigation artifacts only.
- **Work:** map each observed queue operation and worker test to required delivery, ordering, delay, backpressure, replay, poison-message, shutdown, retention, privacy, and recovery semantics; have the platform owner confirm available Kafka services, ACLs, schemas, quotas, support, and environments.
- **Dependencies:** platform and service owners.
- **Verify:** every current invariant has an explicit preserve/change decision and at least one proposed deterministic acceptance check; every required platform capability has an authoritative source.
- **End state:** a reviewable contract, not an adapter or infrastructure change.
- **Replan if:** an invariant lacks an owner or the approved platform cannot provide a required semantic.

**`S2` — Compare options and choose the next plan**

- **Outcome:** a justified decision among retaining/tuning the current queue, adopting Kafka, or another approved mechanism.
- **Basis:** `S0`, `S1`.
- **Why:** only evidence can show whether migration cost and risk buy the required outcome.
- **Affects:** decision record and subsequent planning scope.
- **Work:** compare credible options against the approved targets, semantic fit, operational ownership, migration of in-flight work, security, cost, verification, reversibility, and failure recovery. If Kafka remains preferred, define the cheapest non-production experiment needed to test the highest-risk semantic before producing implementation slices.
- **Dependencies:** completed `S0–S1`.
- **Verify:** the chosen option traces to measured criteria, rejected options have evidence-based reasons, and any experiment has a falsifiable decision rule.
- **End state:** either no migration is needed or enough context exists to create a new Standard or Critical implementation plan.
- **Replan if:** options cannot be distinguished with available evidence.

#### Targeted clarification

Ask the responsible owners:

1. What current or forecast problem is this intended to solve, and which measurable target would make the change successful?
2. Which Kafka platform is approved and who owns its security, reliability, retention, and operational support?
3. Which existing queue semantics and in-flight jobs must survive migration without behavioural change?

Do not produce Kafka implementation steps until these answers and the bounded investigation establish a defensible transition.
