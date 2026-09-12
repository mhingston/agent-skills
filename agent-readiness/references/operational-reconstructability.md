# Operational reconstructability

Use this diagnostic when the target operating model accepts that accountable
engineers may not retain implementation-level familiarity with every material
code path, or when incident response and recovery must remain reliable after the
original author, agent run, or implementation context is unavailable.

The objective is not to make runtime telemetry replace design, specifications, or
human judgement. It is to test whether responders can reconstruct what the
running system is doing, bound the effect of a failure, and recover safely without
depending on author recall.

Keep three questions separate:

- **specification reconstructability** — can we recover what the system is
  supposed to do from authoritative intent and independent verification?
- **operational reconstructability** — can we determine what the deployed system
  is actually doing, where a material failure is propagating, and how to contain
  or recover it from trustworthy evidence?
- **cognitive debt** — do accountable humans retain enough theory to make the
  consequential judgements required for the target activity?

Strong evidence in one dimension does not prove the others.

## Pager counterfactual

Ask:

> If the pager fired for this path and nobody remembered the implementation,
> could an accountable responder establish the current behaviour, impact,
> containment boundary, and recovery state quickly enough to operate it safely?

Inspect the smallest evidence set that can answer the question. Where material,
look for the ability to establish:

- the exact deployed revision, configuration, model/prompt bundle, schema, or
  other runtime identity that could change behaviour;
- the user/request/job/event path affected and the dependencies it crossed;
- first useful failure signals plus enough metrics, logs, traces, events, or
  domain evidence to distinguish likely failure boundaries;
- the affected users, data, contracts, queues, downstream systems, or other
  blast-radius surfaces;
- known-good baselines or comparative signals that make abnormal behaviour
  recognisable;
- a bounded containment action such as disable, isolate, shed load, fail over, or
  stop a consumer without requiring speculative code changes;
- rollback, replay, reconciliation, repair, or other recovery semantics for
  material side effects;
- evidence that recovery succeeded and that uncertain side effects were resolved;
- an escalation route when product, architecture, security, data, or operational
  judgement is still required.

Do not require a specific observability stack. A small service with strong health
checks, structured domain events, deployment markers, and a tested feature flag
may be more operable than a heavily traced system whose signals cannot answer the
incident questions above.

## Treat runtime evidence as observed truth, not governing intent

Runtime evidence is often the strongest source for **what happened under observed
conditions**. It is not automatically the authority for **what should happen**.

Do not turn an observed production behaviour into a requirement merely because it
is visible in telemetry. Reconcile conflicts against accepted specifications,
contracts, policy, schemas, and human-owned decisions. Code remains useful causal
evidence when investigating a mechanism; the diagnostic only removes dependence
on somebody remembering that mechanism from authorship.

A green dashboard is weak evidence when the signals cannot observe the relevant
failure mode. Likewise, an alert proves that a condition was detected, not that
its cause, impact, containment, or recovery is reconstructable.

## Correlate change and runtime state

Prefer evidence that lets responders connect a material runtime symptom to the
state that could have produced it. Depending on the system this can include:

- deployment/change markers and exact revision identities;
- configuration, flag, schema, dependency, model, or prompt versions;
- correlation identifiers across important service/event boundaries;
- immutable receipts for consequential writes, retries, replays, or external
  actions;
- current ownership plus the runbook, disable, rollback, or reconciliation path.

Do not retain sensitive payloads merely to improve reconstructability. Prefer
stable identities, redacted summaries, hashes, and protected evidence references.

## Interpret by consequence and containment

Limited implementation familiarity is more acceptable when behaviour is governed
by independent contracts, verification reaches the material outcomes, runtime
state is reconstructable, blast radius is narrow, and containment/recovery are
credible. It is less acceptable where failures are hard to detect, effects are
irreversible, shared state has unclear ownership, or diagnosis would require an
agent to speculate from its own generated code.

Operational reconstructability does not waive a human-understanding requirement
when the target activity contains consequential judgement. For business rules,
security boundaries, shared data ownership, safety constraints, migration
semantics, or similar areas, use the [cognitive-debt diagnostic](cognitive-debt.md)
to establish whether accountable humans retain enough theory even when runtime
signals are strong.

Treat gaps as activity-specific readiness evidence rather than a universal demand
for more telemetry. Prefer the smallest durable improvement that changes the
operating decision: a deployment marker, a domain metric, a boundary correlation
ID, an executable health probe, an exercised disable path, a reconciliation
receipt, or a focused runbook backed by observed recovery evidence.

Stop when additional instrumentation is unlikely to change the autonomy decision,
incident response path, or remediation order.

## Evaluation pressure

Use [operational reconstructability evaluation](operational-reconstructability-evaluation.md)
when changing this diagnostic or adjacent readiness guidance.

## Source adaptation

This diagnostic adapts the useful operational mechanism from Thomas Johnson,
[We're on call for code nobody wrote](https://leaddev.com/software-quality/were-on-call-for-code-nobody-wrote):
when authorship and implementation recall cannot be assumed, invest in detection,
runtime evidence, and blast-radius containment. It deliberately does **not** adopt
the article's stronger claim that runtime behaviour is the only source of truth;
this catalogue keeps observed behaviour, governing intent, and accountable human
judgement as distinct evidence and authority classes.
