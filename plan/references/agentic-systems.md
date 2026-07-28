# Planning Agentic Systems

Use this reference when a proposed system lets a model select tools, control a loop, delegate work, pause for external input, resume after interruption, or initiate consequential external effects. Apply only the sections whose triggers are present.

This is not a separate planning workflow. Use it to sharpen the outcome contract, design decisions, transition states, verification map, and implementation slices required by `SKILL.md`.

## Contents

1. Place model judgement deliberately
2. Establish authority and durable state
3. Own instructions and context construction
4. Treat model decisions as structured proposals
5. Put deterministic policy around tools and effects
6. Design interruption, resumption, and recovery
7. Bound errors, retries, and escalation
8. Decompose agents and coordination
9. Verify trajectories and operational behaviour

## 1. Place model judgement deliberately

Start from the behaviour and identify the smallest decisions that genuinely require probabilistic judgement. Prefer deterministic code or a fixed workflow when rules, inputs, and transitions can be expressed directly.

For every model-controlled decision, state:

- the question the model is allowed to answer;
- the evidence and context available to it;
- the structured output it must produce;
- the deterministic validation applied afterwards;
- the states and effects it is not authorised to select;
- the fallback when the output is invalid, ambiguous, or low confidence.

Do not make an entire workflow agentic because one decision benefits from a model. Treat agents as components inside a wider system whose state, policy, and side effects remain independently inspectable.

## 2. Establish authority and durable state

Separate model context from authoritative system state. The model input is a projection assembled for one decision; it is not the source of truth for task status, approvals, attempts, ownership, or completed effects.

Inspect and plan explicitly:

- the authoritative owner of task, workflow, and business state;
- stable identities for runs, tasks, actions, approvals, and external effects;
- allowed states and transitions, including terminal, blocked, cancelled, expired, and superseded states;
- the event or receipt evidence retained for each transition;
- versioning or optimistic-concurrency rules for competing updates;
- reconciliation when stored intent and external reality disagree;
- retention, privacy, and audit requirements for prompts, outputs, tool arguments, and results.

Avoid duplicating one fact across hidden model memory, conversation history, and application state without declaring which copy is authoritative and how the others are rebuilt.

## 3. Own instructions and context construction

Treat the effective instructions and context-building logic as application behaviour that must be inspectable, versioned, and testable.

Identify:

- canonical prompts, policies, tool descriptions, and output schemas;
- framework-generated or harness-injected instructions that materially alter behaviour;
- the sources from which context is assembled and their authority, freshness, and provenance;
- selection, ordering, truncation, summarisation, and compaction rules;
- secrets, personal data, untrusted content, and prompt-injection boundaries;
- the maximum context required for a decision and the evidence used to choose it;
- how an operator can reconstruct the effective instruction and context supplied for a past decision.

Prefer a compact decision-specific projection over replaying an unbounded transcript. Preserve durable evidence separately, then build the smallest context that contains the current objective, constraints, relevant state, prior effects, and available actions.

## 4. Treat model decisions as structured proposals

Model outputs should describe proposed actions or decisions, not directly perform them. Define an explicit schema or tagged result for each allowed outcome.

For each result type, specify:

- required and optional fields;
- semantic validation beyond syntax;
- references to current state and expected versions;
- confidence or uncertainty only when there is a defined consumer and threshold;
- whether the result is advisory, executable, approval-seeking, terminal, or blocking;
- how unknown actions, malformed arguments, and unsupported combinations are rejected.

Do not parse consequential intent from free-form prose when a structured contract can make the allowed decision space explicit.

## 5. Put deterministic policy around tools and effects

Treat tools as capabilities behind deterministic policy and validation, not as permissions granted merely because the model named an action.

Plan where relevant:

- capability allowlists scoped by role, state, environment, tenant, and data classification;
- argument validation, preconditions, policy checks, and resource limits;
- least-privilege credentials and separation between proposing and invoking an effect;
- human approval for high-impact or difficult-to-reverse actions;
- idempotency keys, expected-version checks, deduplication, and replay behaviour;
- effect receipts that distinguish requested, accepted, started, completed, failed, and outcome-unknown states;
- compensating action or reconciliation where atomic rollback is impossible;
- redaction and compact representation of tool results before they re-enter model context.

Pause between action selection and invocation when approval, long-running work, or external coordination can materially change whether the action remains valid.

## 6. Design interruption, resumption, and recovery

When work may outlive one process or interaction, define resumability as a state-machine property rather than relying on an in-memory loop.

Specify:

- launch, continue, pause, resume, cancel, expire, and inspect operations;
- the checkpoint written before waiting for a human, another agent, a timer, or an external system;
- what state must be re-read and revalidated after resumption;
- how stale approvals, moved repository revisions, changed inputs, or superseded tasks invalidate continuation;
- ownership, lease, or concurrency rules preventing two workers from advancing the same state unsafely;
- recovery after process termination between selecting, invoking, and recording an effect;
- the earliest safe state from which each failed or interrupted transition can resume.

A valid intermediate state must be externally visible, independently diagnosable, and safe to remain paused in. Do not claim resumability when the only recovery is to restart the full workflow and hope repeated effects are harmless.

## 7. Bound errors, retries, and escalation

Distinguish retryable execution failures from invalid decisions, policy denials, missing authority, incompatible state, and terminal business outcomes.

For each retrying path, define:

- the retry owner and unit of retry;
- attempt, time, cost, token, and transition budgets where material;
- backoff, jitter, timeout, and cancellation behaviour;
- the error representation retained durably and the compact form returned to the model;
- no-progress signals such as equivalent repeated actions, unchanged failures, or oscillating states;
- the threshold and evidence for diagnose, replan, switch strategy or model, request human input, or stop;
- whether partial results remain usable after the failure.

Do not feed unbounded raw logs or repeated stack traces back into context. Preserve full diagnostics outside the context projection and present the model with the smallest error evidence that can change its next decision.

## 8. Decompose agents and coordination

Prefer focused agents or model decision points with one responsibility, a bounded action set, and an explicit completion contract. Do not create multiple agents when ordinary functions or deterministic stages are sufficient.

When delegation or multiple agents are material, define:

- the coordinator's authoritative responsibilities and the responsibilities it may delegate;
- the task contract passed to a worker, including outcome, scope, constraints, evidence, and return schema;
- ownership of mutable resources and integration boundaries;
- independence requirements, such as preventing the implementer from acting as its own reviewer;
- global and per-worker budgets, cancellation propagation, and escalation rights;
- duplicate-work, stale-result, worker-loss, and late-result handling;
- the evidence required before the coordinator accepts a worker's completion claim.

Parallelism is safe only when ownership is clear, shared mutable state is controlled, and results meet at a planned integration gate.

## 9. Verify trajectories and operational behaviour

Evaluate both the accepted outcome and the path that produced it. A correct final response does not prove that permissions, transitions, retries, approvals, and effects were handled safely.

Map requirements and invariants to deterministic checks such as:

- schema and semantic validation for every model result type;
- transition tests that reject actions from invalid states;
- policy and authorization tests for allowed and denied tool calls;
- idempotency, duplicate-delivery, stale-version, cancellation, and timeout tests;
- injected termination before and after external effects, followed by restart and reconciliation;
- approval expiry, rejection, amendment, and supersession tests;
- bounded-loop tests for repeated errors, no progress, and escalation;
- context-construction tests for authority, freshness, redaction, provenance, and token bounds;
- coordinator tests for worker loss, duplicate workers, late results, and invalid completion evidence;
- trajectory evaluation using retained decisions, actions, results, errors, transitions, and approvals;
- operational signals for success, blocked work, retry exhaustion, stuck leases, policy denial, cost, and human wait time.

Use model-based or human semantic evaluation only for properties that deterministic checks cannot establish. Keep evaluator prompts and versions separate from the system under evaluation, and do not accept self-reported completion as sufficient evidence.

## Planning quality gate

Before finalising an agentic-system plan, verify that:

- each model-controlled decision is necessary, bounded, and followed by deterministic validation;
- authoritative state is independent of the model context and survives restart;
- effective instructions, context construction, and tool contracts are inspectable and testable;
- consequential effects have policy checks, approval boundaries where needed, and durable receipts;
- pause, resume, cancellation, retry, and uncertain-outcome paths end in explicit states;
- loops and delegation have budgets, no-progress detection, and escalation behaviour;
- focused responsibilities and ownership make integration and independent review possible;
- verification exercises trajectories, recovery, and policy boundaries rather than only the happy-path output;
- every included concern changes a design decision, implementation slice, check, or gate rather than adding checklist prose.