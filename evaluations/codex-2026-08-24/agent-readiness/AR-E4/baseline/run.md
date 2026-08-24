# Run record

- Case: `AR-E4`
- Condition: `baseline`
- Prompt: Design a resumable coding-agent workflow with durable state, typed handoffs, approval gates, retries by failure class, independent verification, and recovery after uncertain external effects. I am not asking whether a particular repository is ready for it yet.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `plan`
- Agent-reported selection (not a native harness event): `none`
- Final response:

**Plan status**: `Ready`

**Outcome contract**

`R1` Define a resumable coding-agent workflow whose authoritative state survives process death, pause/resume, and retries.

`R2` Represent every material transition with durable, typed state and receipts, not conversation memory.

`R3` Use typed handoffs between coordinator, worker, reviewer, and approval steps.

`R4` Require explicit approval gates for consequential or irreversible effects.

`R5` Classify failures and retry only the classes that are safe to retry, with budgets and escalation.

`R6` Verify work independently of the actor that produced it.

`R7` Recover safely after uncertain external effects by reconciling intent, receipts, and external reality.

`R8` Ensure every paused or interrupted intermediate state is externally visible, diagnosable, and safe to remain paused in.

Non-goals: this plan does not assume a specific repository, language, or orchestration framework, and does not implement the workflow.

Constraints and invariants:

- The model may propose decisions, but deterministic policy owns state transitions and side effects.
- The model context is a projection; the durable task store is the source of truth.
- No step may assume “best effort” completion for an uncertain external effect.
- A worker may not act as its own final verifier for the same slice.
- Approval is stateful and may expire, be superseded, or be rejected.
- Every retry must preserve the original failure class and attempt history.

Governing durable context: the workflow design is grounded in the agentic-system planning guidance, especially the requirements for authoritative state, structured proposals, deterministic policy around tools/effects, interruption/resumption, bounded retries, and independent verification.

**Current-state evidence**

- `E1` The planning skill requires resumability to be a state-machine property, with explicit launch/continue/pause/resume/cancel/expire/inspect operations and checkpointing before waiting for humans, other agents, or external systems. Source: [/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-31391k92/repo/.codex/skills/plan/references/agentic-systems.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-31391k92/repo/.codex/skills/plan/references/agentic-systems.md)
- `E2` The same reference requires structured model outputs, deterministic validation, effect receipts, idempotency, and reconciliation when external reality disagrees with stored intent. Source: [/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-31391k92/repo/.codex/skills/plan/references/agentic-systems.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-31391k92/repo/.codex/skills/plan/references/agentic-systems.md)
- `E3` The plan skill requires evidence-grounded slices, explicit decision gates only where human-owned choices exist, and deterministic verification before subjective review. Source: [/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-31391k92/repo/.codex/skills/plan/SKILL.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-31391k92/repo/.codex/skills/plan/SKILL.md)
- `I1` A robust design should center on a persisted workflow state machine with transition guards, not on a long-running agent loop that depends on memory. This follows from `E1` and `E2`; it would be falsified by a platform that guarantees process survival and exactly-once side effects, which the reference explicitly does not assume.
- `I2` Typed handoffs should be schema-validated action/result envelopes, because free-form prose is too ambiguous for retry, approval, and recovery policy. Supported by `E2`; falsified only if the orchestration layer already enforces stronger typed contracts.
- `A1` The implementation target can persist durable state and effect receipts somewhere reliable. If not, the plan must add that storage as a prerequisite.
- `A2` The workflow needs at least one independent verification role, whether a separate worker, deterministic checker, or external test harness. If that cannot be provisioned, `R6` becomes partially blocked.
- `Q1` Exact storage and runtime technology are unspecified, so the plan stays interface-level rather than naming concrete tables, queues, or APIs.

**Approach and decisions**

Selected design:

- Use a coordinator-owned workflow state machine as the authority for run/task/action status.
- Represent each step as a typed command/result pair with versioned schemas.
- Separate proposal from effect: the model proposes, deterministic policy validates, and an executor performs only authorized effects.
- Record every effect with a receipt that can represent `requested`, `accepted`, `started`, `completed`, `failed`, or `unknown`.
- Put approval as its own durable state, with explicit expiry and supersession rules.
- Make recovery a reconciliation pass over durable state plus external reality, not a replay of the last prompt.

Relevant alternatives and why they were not chosen:

- Pure conversational memory: rejected because it is not durable, inspectable, or replay-safe.
- Unstructured agent autonomy: rejected because retry, approval, and recovery policy become implicit and brittle.
- Immediate execution from model output: rejected because it collapses proposal, validation, and side effect into one unsafe step.

Transition state strategy:

- Start with additive states and receipts.
- Keep old execution paths read-compatible during migration.
- Introduce destructive cleanup only after reconciliation and verification prove the new workflow is authoritative.

Continuity status: `new`

Decision gates:

- `D1` Human approval required before any irreversible external effect class is enabled in the workflow policy.
- `D2` Human approval required before allowing the workflow to execute outside the intended repository or environment boundary, if applicable.
- `D3` Human approval required if a later design introduces self-modifying prompts or unbounded delegation.

Responsibility and interface map:

- Coordinator: owns run state, transition policy, retries, approval gating, and final completion status.
- Worker: consumes a typed slice contract, produces a typed result plus evidence, and never mutates authoritative workflow state directly.
- Reviewer/verifier: consumes the worker result and evidence, produces pass/fail plus findings, and cannot approve its own produced result.
- Effect executor: consumes an authorized action envelope with idempotency key and expected version, produces an effect receipt.
- Reconciler: consumes workflow state plus external reality, produces repaired status or an explicit uncertainty state.

**Implementation slices**

1. **Outcome**: Define the durable workflow state model and transition rules.
   - **Basis**: `R1`, `R2`, `E1`, `E2`, `I1`
   - **Why**: nothing else can be made safe until there is an authoritative state machine.
   - **Affects**: workflow state, action state, approval state, effect receipt state, terminal states.
   - **Work**: specify run identifiers, task identifiers, action identifiers, allowed states, version checks, terminal states, expiry states, and reconciliation states.
   - **Dependencies**: none.
   - **Consumes**: durable state primitives capable of atomic read/write with versioning. `A1`
   - **Produces**: a canonical state contract that later slices must use verbatim.
   - **Verify**: state-transition tests that reject invalid transitions, stale versions, duplicate completion, and illegal resumes.
   - **End state**: a paused or terminated run can be inspected and resumed from durable state.
   - **Replan if**: the target runtime cannot persist or version state reliably.

2. **Outcome**: Define typed handoff schemas for proposals, approvals, worker results, and effect receipts.
   - **Basis**: `R3`, `R4`, `R5`, `E2`, `I2`
   - **Why**: every model decision and tool action must be structurally validated.
   - **Affects**: request/response payloads, validation layer, tool envelopes, error payloads.
   - **Work**: define versioned schemas for proposal, approval request, approval decision, worker completion, verifier finding, effect request, effect receipt, and recovery report.
   - **Dependencies**: Slice 1.
   - **Consumes**: the state identifiers and versions defined in Slice 1.
   - **Produces**: typed contracts for all subsequent slices.
   - **Verify**: schema validation tests for required fields, invalid combinations, unsupported actions, stale state references, and malformed results.
   - **End state**: every handoff is machine-checkable.
   - **Replan if**: the workflow must accept free-form decisions or untyped tool results.

3. **Outcome**: Implement deterministic policy around tool invocation and approval gating.
   - **Basis**: `R4`, `R5`, `E2`
   - **Why**: the model must not directly control side effects.
   - **Affects**: tool allowlists, capability checks, idempotency, approval state, effect dispatch.
   - **Work**: gate effect execution on state, role, data classification, expected version, and approval status; reject disallowed or expired actions; require idempotency keys.
   - **Dependencies**: Slices 1 and 2.
   - **Consumes**: typed effect requests and approval decisions.
   - **Produces**: deterministic accept/reject behavior for every requested effect.
   - **Verify**: policy tests covering allowed, denied, expired, superseded, duplicate, and stale-version requests.
   - **End state**: high-impact actions pause at a durable approval gate until explicitly authorized.
   - **Replan if**: a consequential effect cannot be represented as a validated request/receipt pair.

4. **Outcome**: Add bounded retries and failure-class routing.
   - **Basis**: `R5`, `E1`, `E2`
   - **Why**: retry behavior must differ by failure class.
   - **Affects**: retry policy, attempt counters, backoff rules, timeout handling, escalation states.
   - **Work**: classify failures into retryable execution failure, invalid decision, policy denial, missing authority, incompatible state, terminal business outcome, and uncertain external effect; define retry limits and escalation triggers for each.
   - **Dependencies**: Slices 1 and 2.
   - **Consumes**: structured failure payloads and effect receipts.
   - **Produces**: bounded retry loops with explicit stop conditions.
   - **Verify**: tests for bounded retries, repeated-equivalent-failure detection, escalation after budget exhaustion, and no retry on terminal or policy failures.
   - **End state**: repeated failure cannot spin forever or silently degrade.
   - **Replan if**: failure classes cannot be discriminated from the available evidence.

5. **Outcome**: Separate worker implementation from independent verification.
   - **Basis**: `R6`, `E3`
   - **Why**: the verifier must not be the same agentic path that produced the change.
   - **Affects**: worker contract, verifier contract, acceptance criteria, artifact comparison.
   - **Work**: make workers produce evidence-bearing results; make verifiers consume those results plus independent oracles such as tests, diffs, or runtime checks; prevent self-approval.
   - **Dependencies**: Slices 1 and 2.
   - **Consumes**: worker result schema and verification criteria.
   - **Produces**: pass/fail verification objects with findings and residual risks.
   - **Verify**: tests that a worker result cannot be accepted without a distinct verifier outcome, and that the verifier can fail a superficially successful result.
   - **End state**: acceptance is based on independent evidence, not self-report.
   - **Replan if**: no separate verification source exists for a given slice.

6. **Outcome**: Add interruption, pause, resume, and expiry handling.
   - **Basis**: `R1`, `R8`, `E1`
   - **Why**: resumability must survive process termination and human wait states.
   - **Affects**: checkpointing, lease/lock handling, resume validation, expiration, cancellation.
   - **Work**: write a checkpoint before any wait; on resume, re-read state, revalidate version and approvals, detect stale or superseded context, and either continue or branch to reconciliation.
   - **Dependencies**: Slices 1, 2, and 3.
   - **Consumes**: durable state, approval state, and effect receipts.
   - **Produces**: explicit paused, resumed, expired, cancelled, and superseded states.
   - **Verify**: tests for resume after pause, resume after state change, approval expiry, cancelled run rejection, and lease contention.
   - **End state**: any paused run can be inspected and safely resumed or rejected.
   - **Replan if**: resumption requires implicit in-memory context that cannot be rebuilt.

7. **Outcome**: Add recovery after uncertain external effects.
   - **Basis**: `R7`, `E2`
   - **Why**: process death or network interruption can happen between selection, invocation, and receipt recording.
   - **Affects**: effect executor, receipt store, reconciler, conflict resolution.
   - **Work**: distinguish `requested`, `accepted`, `started`, `completed`, `failed`, and `unknown`; on restart, reconcile the durable intent with external reality, dedupe by idempotency key, and route ambiguity to a recovery state instead of pretending success.
   - **Dependencies**: Slices 1, 2, and 3.
   - **Consumes**: effect receipts plus external state probes or readbacks.
   - **Produces**: reconciled completion, explicit uncertainty, or compensating action request.
   - **Verify**: injected termination before and after effect invocation, followed by restart and reconciliation tests.
   - **End state**: uncertain outcomes are visible and recoverable.
   - **Replan if**: the external system offers no way to infer or reconcile effect outcome.

**Verification map**

- `R1` and `R8` map to Slice 1 state-transition tests and Slice 6 pause/resume/expiry tests.
- `R2` maps to Slices 1, 2, and 7 through durable state, typed receipts, and reconciliation.
- `R3` maps to Slice 2 schema validation and slice-to-slice contract tests.
- `R4` maps to Slice 3 policy tests and approval-expiry tests in Slice 6.
- `R5` maps to Slice 4 bounded-retry tests and failure-class routing tests.
- `R6` maps to Slice 5 independent verification tests.
- `R7` maps to Slice 7 termination/restart/reconciliation tests.
- `R8` maps to Slice 6 checkpoint-before-wait and safe-paused-state tests.

Deterministic checks first:

1. schema and transition validation
2. policy and authorization checks
3. idempotency and duplicate-delivery checks
4. restart/recovery tests with injected failure points
5. independent verification tests
6. manual review only for residual semantic judgment that cannot be encoded

**Operational transition**

- Migration: introduce the durable state model and typed envelopes alongside any existing flow, then route new work through the durable path first.
- Compatibility: keep old consumers read-compatible until all active runs have moved or been drained.
- Recovery: any run that lands in an unknown external-effect state must enter reconciliation before further progress.
- Rollback: rollback should be by state transition and routing change, not by replaying untracked side effects.
- Observability: surface counts for paused, resumed, expired, retried, rejected, approved, completed, failed, and unknown-effect states, plus lease contention and approval wait time.

**Handoff controls**

- Revalidate `A1` and `A2` before execution.
- Revalidate durable state versioning and receipt persistence before each dependent slice.
- Revalidate approval freshness before any step gated by `D1`.
- Stop and replan if a new effect class cannot be represented as a typed request plus receipt.
- Stop and escalate if independent verification cannot be separated from implementation.
- Stop and reconcile if an effect result is uncertain, contradictory, or missing.

If you want, I can turn this into a more concrete architecture memo next, with a compact state diagram and example typed schemas for the handoff envelopes.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
