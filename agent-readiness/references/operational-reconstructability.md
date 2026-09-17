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

## Treat the response surface as a repair kit

Novel incidents reveal whether useful operating levers were deliberately put in
place before the failure. Do not assess incident readiness only from diagnosis
signals or written procedures. Inspect whether responders already have a small,
credible repair surface that can change system behaviour without inventing a
risky code fix under pressure.

Where consequence justifies it, look for controls such as:

- **disable and isolation** — feature flags, kill switches, consumer stops,
  dependency isolation, tenant or workload quarantine;
- **traffic and load control** — rate limiting, load shedding, routing or traffic
  shifting, back-pressure, bounded degradation, or capacity/failover controls;
- **release recovery** — known rollback paths, reversible configuration changes,
  compatible deployment sequencing, and the ability to identify the exact state
  being restored;
- **state recovery** — replay, reconciliation, repair, restore, or compensating
  actions with explicit semantics for duplicate, partial, or uncertain effects;
- **targeted diagnosis** — safe health probes, boundary correlation, deployment
  markers, domain counters, and other evidence that narrows the failure without
  requiring broad speculative changes;
- **human control** — clear ownership, authority to use the controls, escalation
  paths, and enough operational exposure that responders know how to invoke and
  verify them when normal playbooks no longer fit.

Treat the existence of a lever as weak evidence until its operating conditions are
known. For material controls, ask when it was last exercised, what preconditions
it assumes, how quickly it takes effect, what blast radius it creates, what state
it leaves behind, and what evidence proves the intended containment or recovery
actually occurred.

A documented feature flag that nobody can safely operate is not equivalent to an
exercised disable path. A rollback command that cannot restore schema, state, or
external effects is not a complete rollback. An on-call rota without the access,
authority, evidence, and repair controls needed to intervene does not establish
repairability.

Prefer the smallest durable repair surface that covers the material failure modes.
Do not demand every possible emergency control for every component, and do not add
complexity whose own operation would be harder to understand than the failure it
is intended to contain.

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

This diagnostic adapts complementary mechanisms from two sources:

- Thomas Johnson,
  [We're on call for code nobody wrote](https://leaddev.com/software-quality/were-on-call-for-code-nobody-wrote):
  when authorship and implementation recall cannot be assumed, invest in
  detection, runtime evidence, and blast-radius containment. It deliberately does
  **not** adopt the article's stronger claim that runtime behaviour is the only
  source of truth; this catalogue keeps observed behaviour, governing intent, and
  accountable human judgement as distinct evidence and authority classes.
- Carla Geisser, Mikey Dickerson, and Marina Nitze,
  [What's in Your Software Repair Kit?](https://queue.acm.org/doi/full/10.1145/3839114):
  novel incidents are easier to handle when diagnosis, containment, traffic,
  rollback, repair, and human operating capabilities are deliberately
  pre-positioned before a crisis rather than invented during one. This diagnostic
  adapts that mechanism as an evidence question: not merely whether emergency
  controls exist, but whether they are bounded, operable, exercised, and capable
  of producing observable recovery.
