# Modernization certificate and promotion guidance

Use this reference when the modernization needs more than a trivial test/build
gate or when promotion policy, risk tiering, or cutover evidence is material.

## Design the certificate from the failure model

Do not begin with a generic checklist. Start from the target requirements,
protected behaviours, and plausible modernization failure modes.

For each certificate condition `C#`, make explicit:

| Field | Purpose |
| --- | --- |
| protected claim | What target requirement or compatibility property this check supports |
| oracle | Test, replay, comparator, scan, benchmark, telemetry query, review, or other evidence mechanism |
| bound identity | Exact source/target revision, artefact, environment, fixture/data version |
| pass/fail semantics | What result is accepted, rejected, inconclusive, or flaky |
| independence | Whether the producer can influence the oracle or its configuration |
| cost | Runtime, infrastructure, model, reviewer, or data cost |
| failure action | Retry, investigate, redesign, escalate, or block |
| retention | Evidence needed for audit, regression, or later reinterpretation |

Prefer individually interpretable conditions over a weighted aggregate score.

## Oracle patterns by modernization type

These are candidate mechanisms, not mandatory checklists.

### Uplift

The old and target systems usually share enough implementation structure that
existing checks remain useful.

Strong candidates include:

- original tests and characterization tests;
- clean build/type checks on the target toolchain;
- dependency/security/licence policy;
- performance and resource bounds;
- compatibility checks for changed runtimes/frameworks;
- smoke or end-to-end checks over the real external surface;
- anti-regression CI that prevents already-modernized partitions returning to
  unsupported versions or APIs.

Passing existing tests is insufficient when those tests do not cover the changed
runtime semantics, serialization, concurrency, security, or operational surface.

### Transform

The implementation stack changes while protected behaviour remains fixed, so old
implementation tests may not execute against the target.

Strong candidates include:

- production-derived or representative request replay;
- differential old/new execution over the same inputs;
- golden fixtures grounded in observed/required behaviour;
- persistence and serialization round trips;
- API/wire/schema compatibility checks;
- performance/resource comparison;
- shadow or parallel runtime telemetry;
- independent semantic review of mappings that cannot be reduced to deterministic
  comparison.

When differential outputs disagree, do not automatically force the target to
match the old system. First determine whether the difference is a regression, an
approved behaviour change, or an exposed legacy defect.

### Reimagine

Changed behaviour must be judged against authoritative intended behaviour rather
than old-system parity.

Strong candidates include:

- acceptance and property tests derived from the behavioural specification;
- examples reviewed by accountable product/domain owners;
- retained differential checks for behaviours explicitly marked `preserve`;
- invariant, security, accessibility, performance, resilience, and operational
  checks;
- independent semantic review where the specification cannot be compiled into an
  objective oracle.

A vague specification makes a weak certificate. Treat repeated certificate
ambiguity as evidence that the target contract needs refinement rather than
allowing reviewers or agents to invent local intent.

## Stage checks by cost

Where safe, order checks from cheap/high-rejection-value to expensive:

1. parse/build/type/schema;
2. deterministic unit/contract/static/security checks;
3. targeted characterization or compatibility checks;
4. differential/replay suites;
5. integration/end-to-end execution;
6. performance/load/recovery tests;
7. staging, shadow, or parallel-runtime observation;
8. scarce human review or approval.

Do not move a check later merely because it is expensive if an earlier stage can
create unsafe side effects without it.

## Preserve evaluator independence

The same worker that produces a modernization change must not be able to pass by
rewriting:

- the target requirement;
- the certificate threshold;
- replay/golden fixtures;
- expected outputs;
- security policy;
- protected test infrastructure;
- reviewer instructions;
- promotion classification.

If these controls genuinely need to change, scope that as a separate governed
change and revalidate affected modernization evidence.

## Promotion policy

Promotion policy answers a different question from the certificate:

- **Certificate:** what evidence supports technical correctness against the target?
- **Promotion policy:** given that evidence and this change's consequence, who or
  what may move it to the next state?

Prefer existing organisational change/risk classifications when available. A
simple local policy may classify by:

- blast radius;
- data/schema/persistence impact;
- externally consumed interface changes;
- security or privilege impact;
- irreversible migration;
- availability/recovery consequence;
- novelty or absence of a proven oracle;
- cross-team ownership.

For each class define:

- mandatory `C#` conditions;
- required human/domain/security/operations review;
- merge/release/cutover authority;
- rollout and rollback expectations;
- evidence-retention requirements;
- conditions that force escalation.

Do not use agent/model confidence as a substitute for these signals. Confidence
can help triage investigation, but it is not an independently verifiable control.

## Review information design

Design reviewer packets around the decision reviewers must make, not around a
large generated diff.

Useful information can include:

- target requirement and behaviour disposition affected;
- source and target revisions;
- certificate condition results with links/receipts;
- material old/new behavioural differences;
- unresolved or waived findings and who owns them;
- migration/cutover and rollback impact;
- generated change explanation only where it reduces comprehension cost.

Do not hide failed or inconclusive evidence behind a summary. A shorter packet is
better only when it preserves the information needed for accountable judgement.

## Capacity and admission control

Agentic production can create a queue of technically plausible but unverified
changes. Track at least enough flow evidence to detect when:

- certified candidate arrival exceeds verified completion;
- review or integration WIP grows persistently;
- reviewers rely on summaries because batch size is too large to understand;
- concurrent changes collide at shared compatibility or migration boundaries;
- reconciliation/retest cost erases local generation gains.

When this occurs, reduce batch size/concurrency, strengthen earlier deterministic
gates, or widen legitimate review capacity. Do not restore throughput by weakening
certificate conditions or required human judgement.

## Pilot evidence and cost extrapolation

Use the representative pilot to measure:

- implementation and verification cost separately;
- per-condition failure/retry rates;
- reviewer and SME effort;
- integration/reconciliation effort;
- environment/setup failures;
- elapsed time and queueing;
- runtime or cutover evidence.

Extrapolate only quantities the pilot actually sampled. Mark unsampled work such
as organisation-wide reconciliation, data migration, change freezes, or final
cutover as unknown rather than hiding it in a precise estimate.

## Provenance

This guidance adapts mechanisms described in Anthropic's field note
"How to prepare for AI-driven code modernization projects" (2026-09-23):
https://claude.com/blog/how-to-prepare-for-ai-driven-code-modernization-projects

The reusable mechanisms retained here are target classification, correctness
certificates, promotion policy, prerequisites, representative end-to-end pilots,
workflow-level correction of recurring failures, and controlled scaling.

This package deliberately strengthens several boundaries for general use:

- existing behaviour is not automatically required behaviour;
- model confidence is not a promotion authority;
- model review is evidence rather than human approval;
- verification/review capacity constrains safe generation throughput;
- pilot success supports a bounded scale decision rather than authorising release
  or cutover.
