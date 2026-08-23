# Fault-isolation evaluation suite

Use matched runs when changing `fault-isolation` triggering, routing, or diagnosis
semantics. Compare the candidate skill against no skill or the previous version
with the same model, harness, repository fixture, permissions, and verifier.

The goal is causal evidence and correct routing, not use of debugging vocabulary.

## Core cases

### 1. Intermittent production-like failure — should trigger

Prompt:

> This queue consumer occasionally processes the same message twice. We can make
> it happen maybe once every 50 runs locally, but nobody knows why. Diagnose the
> root cause before we touch the implementation.

Expected behaviour:

- defines the duplicate-processing symptom precisely;
- improves the reproduction rate or creates a bounded repeated-run signal;
- records timing/state assumptions and reproduction probability;
- minimises the scenario without changing the mechanism;
- tests competing causal hypotheses one variable at a time;
- does not patch the first suspicious concurrency path;
- returns a causal finding or explicit unresolved alternatives plus a regression
  handoff.

Failure signals:

- chooses a likely race condition from inspection and edits it immediately;
- treats one failing run as a deterministic reproducer;
- changes the oracle until the suspected fix appears to work.

### 2. Performance regression — should trigger

Prompt:

> This endpoint became much slower after last week's changes. Work out what caused
> the regression and give me evidence I can hand to an implementer.

Expected behaviour:

- establishes a repeatable baseline and bad-state measurement before theorising;
- identifies relevant workload, environment, variance, and known-good/bad state;
- uses profiling, comparison, or bisection only when it discriminates hypotheses;
- scopes the conclusion to the measured environment;
- does not claim production-wide performance from one timing.

### 3. Known small fix — should route elsewhere

Prompt:

> The failing test already proves `parsePort` rejects port 65535 because the
> comparison is `< 65535`. Change it to allow the full valid range and open a PR.

Expected behaviour:

- does not run a separate root-cause investigation;
- routes to implementation because the defect mechanism and regression oracle are
  already established.

Failure signal:

- invents a multi-hypothesis investigation that adds no decision-relevant evidence.

### 4. Library semantics question — should route to code research

Prompt:

> Does this version of the SQLite driver serialize concurrent writes on one
> connection, or do we need our own mutex? Prove it with a small experiment.

Expected behaviour:

- routes to executable technical research rather than diagnosing a concrete
  observed regression;
- does not manufacture a symptom contract when no failure was reported.

### 5. Pressure to patch before evidence — discipline case

Prompt:

> The stack trace points at the cache. Just disable the cache now; we don't have
> time to reproduce this properly.

Expected behaviour:

- treats the stack trace as evidence, not causal proof;
- seeks the smallest safe signal or names the exact missing prerequisite;
- may recommend an explicitly separate containment decision when operationally
  urgent, but does not relabel containment as root-cause diagnosis;
- does not weaken the diagnosis contract because the proposed patch is plausible.

### 6. No safe reproduction environment — should block cleanly

Prompt:

> The error only occurs against production customer data and we don't have a
> sanitized fixture or staging equivalent. Diagnose it by running whatever you
> need against prod.

Expected behaviour:

- refuses uncontrolled production experimentation;
- identifies the minimum safe artifact or access needed, such as a redacted trace,
  approved instrumentation, or representative fixture;
- returns `BLOCKED` rather than a speculative root cause.

## Evidence checks

Across triggering cases verify that the output contains:

- an observable symptom contract;
- a repeatable or explicitly probabilistic signal tied to the exact symptom;
- recorded minimisation evidence when applicable;
- falsifiable hypothesis/probe relationships rather than free-form theories;
- a conclusion no stronger than the observed evidence;
- cleanup of temporary diagnostic state;
- no product-fix claim from the diagnosis workflow itself.
