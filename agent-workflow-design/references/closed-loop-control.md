# Closed-loop control with graduated authority

Use this reference when an agent workflow responds to recurring operational,
quality, security, delivery, or telemetry signals and the response may become
more consequential as evidence strengthens.

The goal is to close the loop without letting a model redefine the trigger,
escalation threshold, or authority boundary that governs its own actions.

## Core pattern

Separate four concerns:

1. **Detect deterministically** — compute the signal, threshold, invariant breach,
   or event class outside the model when the rule can be expressed reliably.
2. **Diagnose probabilistically** — use a model only when interpretation,
   synthesis, ranking, or investigation is required.
3. **Graduate authority by policy** — map independently established severity or
   state to an explicit maximum response capability.
4. **Verify effects independently** — bind any proposed or performed effect to
   receipts, read-back, revision identity, and recovery evidence.

A useful default ladder is:

| Level | Permitted response | Typical boundary |
| --- | --- | --- |
| `observe` | record evidence and update derived status | no mutation |
| `diagnose` | inspect authorised evidence and return structured hypotheses | read-only tools |
| `propose` | prepare a patch, PR, runbook invocation, or other bounded change proposal | isolated mutation or proposal only |
| `act` | perform one pre-authorised consequential effect | explicit policy/approval plus reconciliation and tested recovery |

The ladder is not a maturity score. A workflow may deliberately stop at
`diagnose` or `propose` forever when the consequence does not justify autonomous
action.

## Keep detection outside the model

When severity depends on explicit thresholds, policy, schema, health state,
rate-of-change, invariant violations, or another computable rule, calculate it in
code. Preserve:

- detector and policy version;
- exact inputs and freshness;
- threshold or rule that fired;
- resulting severity/state;
- missing or invalid data treatment.

Do not ask the model to decide whether its own permissions should expand. A model
may interpret why a signal occurred, but it must not promote `observe` to `act`,
waive a threshold, or reinterpret a failed precondition as satisfied.

When detection itself is genuinely semantic, treat the model result as a claim
that still requires a separately owned policy decision before authority changes.

## Make escalation monotonic in evidence, not confidence

More model confidence is not stronger authority. Increase the permitted response
only when independently checkable evidence satisfies an explicit transition.

For each transition define:

- source state and target state;
- detector/policy condition;
- evidence required;
- maximum capabilities enabled;
- approval requirement;
- expiry or downgrade rule;
- effect and recovery requirements.

A higher-severity condition may justify broader investigation without justifying
broader mutation. Keep read, propose, mutate, merge, deploy, message, purchase,
or production operations distinct when their blast radius differs.

## Preserve bounded effects

For every mutating response define:

- exact resource/write scope;
- maximum effect size or rate;
- idempotency or expected-version semantics;
- preconditions checked immediately before the effect;
- durable receipt or authoritative read-back;
- rollback, compensation, or safe-stop path;
- conditions that require a human decision rather than retry.

Do not treat an approved runbook name as proof that the runbook is safe in the
current state. Bind approval and recovery evidence to the actual environment,
version, and effect where those can drift.

## Avoid self-amplifying loops

Closed-loop automation needs explicit protection against feedback that increases
its own authority or repeatedly applies ineffective changes.

Detect and stop on:

- unchanged failure after equivalent remediation;
- oscillation between states or fixes;
- duplicate events for the same underlying condition;
- stale signals after the source state has moved;
- model recommendations that would alter the detector, policy, gate, evaluator,
  or authority configuration that judges the same run;
- cost, attempt, time, or effect-budget exhaustion.

Changes to detector thresholds, policy, evaluator configuration, or authority
should enter a separate governed change path rather than being applied as an
ordinary remediation effect.

## Verification cases

At minimum test:

- a low-severity event remains non-mutating even when the model recommends a fix;
- a high-severity event may trigger diagnosis or a proposal but cannot cross an
  ungranted approval/effect boundary;
- stale or missing detector inputs cannot silently increase authority;
- repeated equivalent failures trigger no-progress escalation instead of an
  unbounded remediation loop;
- a permitted consequential action records a receipt/read-back and exercises the
  configured recovery path in a representative safe environment before higher
  autonomy depends on it.

Use deterministic tests for detector, transition, permission, and budget logic.
Use model or human evaluation only for the semantic quality of diagnosis or
proposal content.