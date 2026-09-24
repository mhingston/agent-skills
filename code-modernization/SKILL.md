---
name: code-modernization
description: Prepare and govern large-scale code modernization by classifying the modernization type, reconstructing current behaviour, defining the target, establishing an independent correctness certificate and promotion policy, proving the approach on a representative pilot, and scaling only when evidence and verification capacity support it. Use for legacy-system modernization, broad runtime/framework uplifts, cross-language or cross-stack transforms, and reimagined replacements. Do not use for ordinary refactors, one small dependency upgrade, planning one bounded ticket, or implementing a modernization change.
---

# Prepare and Govern Code Modernization

Treat modernization as an evidence-governed change programme, not a batch rewrite.

The objective is to make the target, correctness evidence, promotion path, and
scale conditions explicit before generated change volume outruns the organisation's
ability to verify, understand, integrate, and safely release it.

## Core invariants

1. **Observed legacy behaviour is evidence, not automatic product intent.**
2. **The modernization type must be explicit.** Do not silently mix behaviour
   preservation with behaviour redesign.
3. **The producer does not own its own correctness bar.** Certificate conditions,
   policy, and approval authority must be independent of the change being judged.
4. **A green certificate is evidence, not approval.** Human-owned product,
   architecture, security, compliance, release, and risk decisions remain where
   the organisation assigns them.
5. **Do not scale an unproven workflow.** Complete at least one representative
   slice through generation, verification, review, promotion, and landing before
   increasing throughput.
6. **Optimise verified outcomes, not generated output.** If implementation arrives
   faster than integration, verification, review, or accountable comprehension can
   absorb it, reduce admission pressure rather than weakening the bar.

## Boundaries

- This skill owns the **modernization contract and programme controls**: current
  behaviour evidence, target definition, correctness certificate, promotion policy,
  prerequisites, pilot design/assessment, and scale gate.
- Remain read-only unless the user separately invokes an execution workflow. Do
  not rewrite production code, merge changes, deploy, or perform cutover merely
  because the modernization contract is ready.
- Do not infer required behaviour solely from the current implementation, tests,
  comments, historical prevalence, or model interpretation.
- Do not let a modernization worker edit or weaken the certificate, evaluator,
  policy, or acceptance oracle used to judge that same work unless the control
  change is independently scoped and reviewed.
- Do not treat model confidence, self-review, successful generation, compilation,
  test count, or coverage percentage alone as sufficient promotion evidence.
- Do not invent a risk appetite, code-freeze policy, release authority, or human
  approval rule. Record the missing decision and its owner.
- Do not claim full-program cost, duration, or throughput from a pilot without
  separating measured quantities from extrapolation and unobserved reconciliation,
  migration, or organisational work.

## Route adjacent work

Use this skill when the primary outcome is a reusable modernization contract and
safe path from legacy/current state to a target state.

Use another capability when the primary task is:

- understanding one current subsystem or flow without deciding a modernization:
  use `codebase-walkthrough`;
- planning one bounded repository change: use `plan`;
- making one selected implementation change: use the repository's implementation
  workflow;
- executing large quality-sensitive work against an already accepted contract:
  use `gauntlet-loop` when its overhead is justified;
- designing the agent state machine, handoffs, retries, permissions, or runtime:
  use `agent-workflow-design`;
- establishing reusable product-driving verification infrastructure:
  use `project-verification`;
- assessing the repository's supported coding-agent autonomy:
  use `agent-readiness`;
- reviewing one patch or PR: use `review` or the PR-review lifecycle;
- preserving durable project truth and source authority: use `project-context`;
- experimentally proving one uncertain runtime/library/compatibility claim:
  use `code-research`.

These capabilities may supply evidence to a modernization, but this package must
remain independently usable and must not depend on another skill directory.

## Evidence discipline

Classify material claims:

- **Observed (`E#`)** — directly supported by current source, executable
  behaviour, configuration, tests, schemas, telemetry, authoritative
  documentation, or user evidence.
- **Inferred (`I#`)** — a reasoned interpretation of observations; state what
  supports it and what would falsify it.
- **Unknown (`U#`)** — missing, inaccessible, stale, contradictory, or not yet
  tested evidence.
- **Required (`R#`)** — an authoritative target requirement or invariant.
- **Decision (`D#`)** — a human-owned unresolved choice that materially changes
  the target, certificate, promotion policy, or cutover.

Do not convert `E#` into `R#` merely because the old system behaves that way.
Do not convert `I#` into a certificate condition without an authoritative basis
or an explicitly accepted decision.

## 1. Define the modernization contract

Establish:

- system, repositories, services, interfaces, data stores, and environments in
  scope;
- why the modernization is being considered;
- the cost/risk of not modernizing when relevant;
- accountable product, engineering, security, data, compliance, operations, and
  release owners;
- target dates or external constraints such as end-of-support deadlines;
- protected behaviours and consequences of regression;
- permitted coexistence with current development;
- expected cutover shape;
- evidence sources and access limitations.

### Classify the modernization type

Choose one primary type:

| Type | Meaning | Typical target |
| --- | --- | --- |
| **Uplift** | Same broad stack and behaviour; runtime, compiler, framework, dependency, or platform version moves forward. | Version/package/platform set plus compatibility constraints. |
| **Transform** | Implementation stack changes while externally required behaviour is intentionally preserved. | New language/framework/architecture plus a parity contract. |
| **Reimagine** | Implementation and material behaviour both change. | New stack plus an authoritative behavioural specification. |

A programme may contain different types in different partitions, but classify each
partition explicitly. Do not call a behaviour-changing rewrite a transform merely
to make parity verification easier, and do not turn a transform into a reimagine
because engineers discover legacy behaviour they dislike.

When stakeholders disagree about the type, record `D#` and stop any downstream
work whose correctness would depend on that choice.

## 2. Reconstruct the current behavioural surface

Build the smallest behaviour and dependency model sufficient to define the target
and verification strategy.

Inspect where relevant:

- externally visible inputs, outputs, errors, side effects, and timing;
- business rules, edge cases, defaults, ordering, retries, and idempotency;
- persistence schemas, migrations, serialization, and wire formats;
- downstream/upstream contracts and compatibility pressure;
- runtime dependencies, build graph, deployment topology, and configuration;
- performance, availability, recovery, security, audit, and operational
  characteristics that may need preservation;
- current tests, fixtures, replay data, telemetry, and production evidence;
- known bugs, workarounds, undocumented rules, and contradictory documentation.

For every material behaviour, create a **behaviour disposition**:

| Behaviour | Evidence | Disposition | Authority |
| --- | --- | --- | --- |
| current behaviour | `E# / I# / U#` | `preserve / change / drop / undecided` | requirement, decision, or unresolved owner |

Do not assume a bug must be preserved because it is observable. Do not assume an
undocumented edge case may be removed because it looks accidental.

## 3. Define the target

Turn the desired end state into a contract another engineer or workflow could
evaluate without rediscovering intent.

For all modernization types define:

- target runtime/platform/dependency set;
- target interfaces and compatibility boundaries;
- target persistence and wire-format expectations;
- architecture constraints that are genuinely authoritative;
- security, compliance, operability, performance, and recovery requirements;
- behaviours explicitly preserved, changed, dropped, or still unresolved.

For **transform**, make the parity boundary explicit: what must remain equivalent,
what implementation details may differ, and which old artefacts cannot serve as
oracles on the new stack.

For **reimagine**, require an authoritative behavioural specification for changed
areas. Existing code may still provide evidence for behaviours marked
`preserve`, but it cannot define newly intended behaviour by itself.

If the target contains unresolved decisions that would change implementation or
verification, return `BLOCKED` for those partitions rather than filling gaps with
model preference.

## 4. Build the correctness certificate

A **certificate** is the predeclared evidence bundle required for a modernization
slice to be considered technically eligible for promotion.

Read
[`references/certificate-and-promotion.md`](references/certificate-and-promotion.md)
when defining non-trivial evidence, risk tiers, or promotion rules.

For every certificate condition `C#`, record:

- protected requirement or behaviour;
- exact oracle/check and environment;
- pass and fail semantics;
- source/fixture/data version;
- revision or artefact identity the evidence binds to;
- independence requirement;
- cost and expected runtime;
- whether the result is deterministic, comparative, statistical, model-judged, or
  human-owned.

Prefer cumulative independent evidence over one aggregate score. Typical signals
include:

- existing tests where they genuinely apply;
- new characterization/spec-derived tests;
- build, type, lint, architecture, static-analysis, and security checks;
- differential old/new execution or replay;
- persisted-state and wire-format round trips;
- performance and resource bounds;
- staged or parallel-runtime telemetry;
- independent adversarial review for properties that executable checks cannot
  establish.

Order expensive checks behind cheaper decisive gates when that does not weaken
coverage. A worker may iterate until certificate conditions pass, but passing the
certificate must not allow it to redefine the target or approve production.

## 5. Define the promotion policy

The promotion policy maps **evidence plus risk** to the organisation's existing
review, approval, integration, and release path.

Define:

- risk/blast-radius classes using organisational policy where available;
- protected paths, behaviours, data, and interfaces that force higher scrutiny;
- required certificate subset per class;
- human review depth and accountable owner per class;
- escalation conditions and unresolved-decision handling;
- merge, release, rollout, rollback, and cutover authority;
- traceability from promoted change to target, certificate evidence, reviews, and
  decisions.

Do **not** use model confidence as an approval signal. Confidence may be diagnostic
metadata, but promotion should depend on independently inspectable evidence and
human-owned policy.

Account for capacity. If certified candidates arrive faster than reviewers,
integrators, release processes, or accountable owners can absorb them, cap batch
size or concurrency. Do not solve a promotion bottleneck by silently weakening
verification or human judgement.

## 6. Check prerequisites before implementation

Classify each prerequisite as `Ready`, `Partial`, `Missing`, or `Unknown`.

Check where applicable:

- reproducible source and target build/runtime environments;
- test, replay, benchmark, staging, or parallel-run capacity required by the
  certificate;
- dependency map and treatment of unsupported/changed dependencies;
- CI gates that can prevent regression into already-modernized partitions;
- source/target data access and lawful handling of production-derived fixtures;
- secrets, PII, licences, vulnerabilities, and least-privilege access;
- traceability of generated changes and evidence;
- review/SME capacity and approval availability;
- coexistence, branch, freeze, and reconciliation policy while normal development
  continues;
- rollback, failback, migration, and recovery mechanisms.

A missing prerequisite is not automatically a programme blocker. State which
modernization stage it blocks and the smallest evidence or remediation needed.

## 7. Design one representative pilot

Choose a vertical slice that is:

- small enough to fail cheaply;
- representative of meaningful dependencies and behaviour;
- capable of exercising the real certificate;
- capable of traversing the real promotion path;
- consequential enough that success teaches something about the full programme.

The pilot must run end to end:

```text
source evidence
  → target interpretation
  → implementation candidate
  → certificate
  → review / approval
  → integration / release path
  → observed runtime evidence
```

Predeclare what the pilot will measure, such as:

- certificate failures by condition;
- escaped defects or reviewer-found issues;
- review and integration effort;
- retry/rework patterns;
- cost and elapsed time by stage;
- reconciliation overhead with concurrent development;
- verification and human-attention capacity.

Do not collapse these into one success score. A fast pilot with high review debt
or weak parity evidence has not demonstrated safe scale.

## 8. Learn by changing the system, not hand-fixing every output

When pilot issues recur, classify the failure:

- target ambiguity;
- missing or incorrect source behaviour;
- weak certificate/oracle;
- worker context or transformation logic;
- tool/environment failure;
- promotion/reviewer information gap;
- integration/reconciliation pressure;
- policy/authority gap.

Fix the owning contract, oracle, workflow, context, or prerequisite, then rerun a
representative case. Do not normalize repeated manual correction as the operating
model for scale.

Preserve failures as regression fixtures when they are reproducible and
generalizable.

## 9. Gate scale explicitly

Return `READY_TO_SCALE` only when evidence supports all applicable claims:

- the target and behaviour dispositions are sufficiently resolved;
- the certificate catches the failure modes the pilot exposed;
- the representative pilot completed through the real promotion path;
- no unresolved `D#` can materially change correctness;
- required environments and checks are reproducible;
- rollback/failback is credible for the planned cutover;
- review, verification, integration, and release capacity can absorb the proposed
  batch/concurrency level;
- the scaling strategy preserves compatibility with ongoing development.

A scale gate is not permission to merge, deploy, or cut over. It states that the
modernization mechanism is supported by the available evidence at the declared
scope and capacity.

### Scaling strategy

Choose a strategy appropriate to the type and codebase:

- dependency-aware partitions;
- leaf-first modernization where it reduces compatibility pressure;
- vertical slices when end-to-end behaviour is the stronger boundary;
- bounded batches with explicit WIP limits;
- in-place uplift with partition freeze and anti-regression CI when necessary;
- side-by-side transform/reimagine with differential or parallel runtime evidence;
- staged cutover with compatibility windows and rollback/failback.

Keep the smallest batch that preserves useful learning and integration safety.
Spare agent capacity is not a reason to increase concurrency.

## Output contract

Return one primary status:

- `MODERNIZATION_PREPARED` — target, certificate, promotion policy,
  prerequisites, and pilot contract are sufficiently defined to begin a pilot.
- `PILOT_ASSESSED` — pilot evidence has been evaluated but scale is not yet
  justified or requested.
- `READY_TO_SCALE` — the pilot and programme controls support the declared next
  scale step; this is not release approval.
- `BLOCKED` — a missing decision, authority, oracle, prerequisite, or evidence
  source prevents a coherent next step.

Include only the sections needed for the current mode, drawn from:

1. **Scope and justification**
2. **Modernization type**
3. **Current behaviour / disposition map**
4. **Target contract**
5. **Correctness certificate**
6. **Promotion policy**
7. **Prerequisites and gaps**
8. **Pilot contract or pilot evidence**
9. **Scale / cutover strategy**
10. **Open decisions and owners**
11. **Handoffs to adjacent execution or verification capabilities**

Keep observed facts, requirements, inference, and unresolved decisions visibly
separate.

## Evaluation

When changing routing, applicability, certificate semantics, promotion policy, or
scale behaviour, read
[`references/evaluation-suite.md`](references/evaluation-suite.md) and run matched
routing/outcome cases in a real harness when available. Keep adjacent skills
discoverable in both conditions. If behavioural execution is unavailable, report
it as `NOT_RUN` or `BLOCKED`; static validation is not evidence of behavioural
lift.
