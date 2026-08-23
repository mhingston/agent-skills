---
name: fault-isolation
description: Investigate hard bugs, regressions, flaky failures, and unexplained performance problems by constructing a reproducible symptom signal, minimising the failure, testing competing causal hypotheses, and returning root-cause evidence plus a verification handoff. Use when the main uncertainty is why something fails or regressed and implementation should not begin from a plausible guess. Do not use for a straightforward already-understood fix, generic technical research, merge conflicts, or ordinary code review.
compatibility: Requires read access to the relevant repository. Executable diagnosis requires an isolated environment capable of running the affected checks without production credentials or uncontrolled side effects.
---

# Fault Isolation

Turn a reported failure into evidence about its cause before a product fix is
chosen. The primary deliverable is a reproducible diagnostic signal and a causal
finding another engineer or agent can challenge, not a patch that merely makes the
symptom disappear.

## Boundaries

- Do not modify production behaviour as the final outcome of this skill. Hand a
  supported root cause and regression-oracle candidate to an implementation or
  planning workflow.
- Temporary diagnostics, disposable harnesses, or instrumentation are allowed
  only when they are the cheapest safe way to discriminate causes. Keep them in
  an isolated workspace or remove them before returning.
- Do not use production credentials, customer data, destructive infrastructure,
  or unrestricted network access merely to reproduce a failure.
- Do not weaken, rewrite, or replace the symptom oracle because the observed
  result disagrees with a preferred hypothesis.
- Do not infer root cause from temporal proximity, a suspicious diff, one stack
  frame, one passing retry, or a plausible code smell.
- Do not force a single-command reproducer when the real signal requires a small
  repeatable procedure, but make the procedure as bounded and deterministic as
  practical.
- A failure that cannot yet be reproduced or otherwise observed reliably remains
  an evidence gap. Do not compensate by producing a more confident theory.

## Route adjacent work

Use another workflow when the primary task is:

- implementing a known bounded fix with an adequate verification seam: use the
  implementation workflow;
- answering uncertain library, runtime, API, compatibility, or performance
  semantics with a controlled experiment rather than diagnosing a concrete
  observed failure: use `code-research`;
- reconstructing why historical code changed without a current failure to isolate:
  use repository-history analysis;
- resolving an in-progress merge, rebase, or cherry-pick conflict: use an
  integration-reconciliation workflow;
- reviewing a proposed patch: use technical review.

These are routing boundaries, not runtime dependencies. This skill must remain
usable from its own directory.

## Evidence states

Keep diagnosis evidence explicit:

- **Observed (`E#`)** — directly reproduced symptom, trace, measurement, code
  path, revision, configuration, command result, or other inspected fact.
- **Inferred (`I#`)** — interpretation supported by observations. Name the
  prediction or counterfactual that would falsify it.
- **Assumed (`A#`)** — premise used to keep the investigation bounded, such as a
  representative dataset or environment. State its consequence.
- **Unknown (`U#`)** — missing, flaky, inaccessible, contradictory, or
  insufficient evidence that limits the conclusion.

A root-cause claim should be an inference backed by discriminating observations,
not a relabelled suspicion.

## 1. Define the symptom contract

State the failure in observable terms before reading deeply for causes:

- actual behaviour;
- expected behaviour and its authority when known;
- affected environment, version, revision, data shape, or workload;
- frequency or reproduction rate;
- first known bad / last known good state when available;
- operational or user impact relevant to investigation priority;
- evidence already supplied and what remains unverified.

If the report is too vague to distinguish the named failure from nearby errors,
identify the smallest missing observation needed before diagnosis can proceed.

## 2. Construct the narrowest useful feedback signal

Prefer an existing check that already observes the exact symptom. Otherwise build
the cheapest safe signal that can become meaningfully red and green for this
failure. Candidate forms include:

- a focused test at the real behavioural seam;
- a CLI or HTTP invocation over a fixture;
- replay of an attributable request, event, trace, or payload using non-sensitive
  data;
- a differential comparison between known-good and known-bad revisions,
  configurations, versions, or implementations;
- a bounded fuzz, property, stress, or repeated-run loop for intermittent
  failures;
- an automated bisection predicate;
- a disposable harness around the minimum required subsystem;
- a benchmark or profiler signal defined before a performance hypothesis is
  changed.

The signal is adequate only when it can distinguish the reported symptom from a
nearby unrelated failure. Record the exact invocation or procedure, inputs,
environment identity, observed result, and why the signal corresponds to the
user-visible or system-visible failure.

If no safe signal can be constructed, return `BLOCKED` with what was attempted and
the smallest missing artifact, access, environment, or instrumentation decision.

## 3. Tighten and characterise the signal

Before using the signal to choose causes, improve its diagnostic value:

- reduce irrelevant setup and runtime when practical;
- assert or measure the specific symptom rather than generic success/failure;
- pin time, randomness, concurrency, data, configuration, or dependencies when
  those can introduce noise;
- for intermittent failures, measure reproduction probability rather than
  pretending the loop is deterministic;
- record false-positive and false-negative risks;
- verify the signal against at least one known-good or deliberately changed case
  when practical.

Do not call a flaky test a reliable oracle merely because it failed once in the
expected direction.

## 4. Minimise the reproducer

Shrink the failing scenario while preserving the same symptom and causal path.
Change one dimension at a time where practical:

- input or fixture size;
- number of actors, requests, events, or calls;
- configuration and feature flags;
- dependency set;
- environment and timing conditions;
- code path or entry point.

After every material reduction, rerun the signal. Keep only elements that remain
load-bearing for the failure or are required to preserve environmental fidelity.
Record which removals made the failure disappear; those observations narrow the
hypothesis space.

Do not minimise so aggressively that the scenario stops exercising the real
failure mechanism.

## 5. Generate competing causal hypotheses

Unless the cause has already been established by a deterministic discriminating
observation, produce a small ranked set of materially different hypotheses.
Normally use two to five; fewer are acceptable when evidence already excludes
most alternatives.

For each hypothesis record:

- suspected cause;
- evidence supporting it;
- the prediction it makes;
- the cheapest discriminating observation or intervention;
- what result would falsify or materially weaken it.

Include credible alternative explanations such as configuration, environment,
state, caller behaviour, dependency changes, concurrency, caching, data shape, or
measurement artifacts when the evidence supports them. Do not pad the list with
implausible possibilities merely to reach a count.

## 6. Probe one causal variable at a time

Run the cheapest safe experiment that distinguishes the leading hypotheses.
Prefer observation before mutation:

1. debugger, trace, profiler, query plan, or state inspection;
2. targeted temporary instrumentation at a discriminating boundary;
3. controlled input/configuration change;
4. revision or dependency comparison;
5. a narrowly scoped code change in a disposable workspace when no observational
   probe can discriminate the cause.

Tie every probe to a prediction. Record the before/after result and update the
hypothesis set. A failed hypothesis is useful evidence; remove or downgrade it
instead of stacking another speculative patch on top.

For performance regressions, compare repeatable measurements and distributions,
not one timing. For concurrency failures, record scheduling/load assumptions and
avoid presenting one successful retry as causal proof.

## 7. Establish the earliest supported divergence

Trace the failing path backward until the earliest evidenced divergence from the
expected state, contract, control flow, data flow, or performance envelope is
identified.

A supported root cause should explain:

- why the symptom occurs;
- why the minimised reproducer retains the failure;
- why at least one discriminating probe changes or predicts the symptom;
- why the nearest credible alternatives are weaker or falsified;
- the scope in which the conclusion is valid.

When evidence narrows the fault to a subsystem or condition but does not establish
a unique cause, return `CAUSE_NARROWED` rather than forcing one explanation.

## 8. Prepare a verification handoff

When a root cause or narrow causal boundary is supported, define the strongest
candidate regression oracle for the later fix. Prefer the minimised signal when it
is independently meaningful and exercises the real failure seam.

For the handoff record:

- the symptom and reproduction procedure;
- exact environment/revision assumptions;
- the supported root cause or remaining causal alternatives;
- the candidate regression test, fixture, replay, benchmark, or other oracle;
- why its expected result is independent of the implementation strategy;
- any expectation-bearing artifact that should remain stable during remediation;
- checks needed against the original, non-minimised scenario after the fix;
- architecture or testability gaps that prevent a durable regression oracle.

A diagnostic reproducer is not automatically a good permanent test. If the
correct seam does not exist, state that explicitly rather than recommending a
brittle shallow test.

## 9. Clean up diagnostic state

Before returning:

- remove temporary debug statements, patches, probes, or disposable files from
  the product working tree;
- preserve only user-requested or repository-convention diagnostic artifacts;
- verify the original repository state is not accidentally changed by the
  investigation;
- redact secrets and sensitive payloads from retained evidence;
- record any environment or external state intentionally left changed.

Do not convert temporary instrumentation into a production observability change
without a separate implementation decision.

## Output contract

Return one status:

- `ROOT_CAUSE_SUPPORTED` — evidence supports one causal explanation strongly
  enough to hand off a fix;
- `CAUSE_NARROWED` — the failure is reproducible and bounded, but more than one
  materially different cause remains;
- `INCONCLUSIVE` — investigation produced evidence but not enough to establish a
  useful causal boundary;
- `BLOCKED` — a missing signal, access boundary, unsafe environment, or other
  prerequisite prevents responsible diagnosis.

Include:

1. **Symptom contract** — actual/expected behaviour, scope, frequency, and
   environment.
2. **Feedback signal** — exact command/procedure, inputs, observed result, and
   reliability characteristics.
3. **Minimised reproducer** — smallest supported scenario and load-bearing
   elements.
4. **Evidence ledger** — compact `E#`, `I#`, `A#`, and `U#` entries.
5. **Hypothesis table** — predictions, probes, results, and disposition.
6. **Causal finding** — supported root cause, narrowed boundary, or unresolved
   alternatives with confidence rationale.
7. **Verification handoff** — candidate regression oracle, original-scenario check,
   and architecture/testability limitations.
8. **Cleanup** — temporary state removed or explicitly retained.
9. **Next action** — implementation, planning, one bounded follow-up probe, or
   escalation.

Read [references/evaluation-suite.md](references/evaluation-suite.md) when
validating this skill or changing its trigger and routing boundaries.

## Quality gate

Before finishing, verify that:

- the investigation is about a concrete observed failure rather than generic
  technology uncertainty;
- the symptom signal can observe the reported failure specifically;
- intermittent behaviour is characterised rather than called deterministic;
- minimisation did not change the failure mechanism;
- root-cause claims are supported by discriminating evidence;
- credible alternatives are preserved or falsified explicitly;
- temporary diagnostic edits are cleaned up;
- the proposed regression oracle is independent of the intended implementation;
- no product fix, approval, deployment, or policy decision is claimed by this
  diagnostic workflow.
