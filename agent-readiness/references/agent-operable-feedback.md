# Agent-operable feedback surfaces

Use this reference when the target agent activity changes behaviour that must be exercised through a running application, service, API, event/data pipeline, CLI, browser flow, or another system boundary rather than being established adequately by static or isolated checks alone.

## Principle

A repository can have strong tests and still be weak for autonomous application-level work if the executor cannot reliably start the relevant system, drive the behaviour it is changing, and observe a result attributable to the exact revision under test.

Assess the **feedback surface the target activity actually needs**, not whether the repository has an end-to-end test framework in the abstract.

## What to inspect

Determine whether an authorised isolated executor can reproducibly:

- start the minimum relevant services or application slice;
- provision safe non-production dependencies, fixtures, accounts, data, or emulators;
- exercise the meaningful interface through which the behaviour is observed, such as HTTP, UI, event, queue, database boundary, data pipeline, or CLI;
- capture outputs, state transitions, logs, telemetry, screenshots, events, or other evidence needed to distinguish success from a plausible wrong implementation;
- bind that evidence to the exact source/revision and configuration under test;
- reset or recreate state so repeated runs remain interpretable;
- tear down cleanly and distinguish environment failure from product failure.

A manually documented demo path is useful evidence, but it is weaker than a repeatable harness or command that another authorised executor can reproduce.

## Layer feedback by cost and discrimination

Prefer the cheapest feedback that can falsify the current claim, then escalate only when a broader surface can reveal material failures the cheaper layer cannot.

A typical ladder is:

1. parser/schema/type/static checks;
2. focused unit, property, or contract checks;
3. component or integration checks;
4. application/service startup plus representative interface exercise;
5. end-to-end, performance, recovery, or post-deployment evidence when the risk requires it.

This is not a universal test pyramid. Choose layers according to the observable behaviour and failure modes of the target change.

## Treat feedback latency as part of operability

A feedback path can be technically correct yet operationally weak if its useful
signal arrives so late that implementation throughput, context retention, or safe
iteration becomes dominated by waiting. This matters more when agents can generate
candidate changes much faster than the verification system can discriminate them.

Do not impose a universal duration target or optimise CI latency in isolation.
Instead ask:

- how long the cheapest discriminating check takes relative to the cadence at which
  candidate changes are produced;
- whether checks can run incrementally or in parallel without weakening evidence;
- whether a slow broad check is being used where a narrower earlier check could
  reject the same failure class;
- whether long feedback delay causes excess WIP, stale context, speculative parallel
  changes, or repeated rework;
- whether the constraint belongs to useful verification work or avoidable setup,
  queueing, flaky infrastructure, or opaque failure triage.

A slow but necessary high-confidence gate may remain appropriate for consequential
changes. The improvement target is the earliest reliable signal, not the smallest
wall-clock number.

## Prefer machine-actionable feedback

For checks intended to sit inside an agent execution loop, prefer outputs that the
executor can interpret without reconstructing meaning from an unbounded human log.
Useful properties include:

- stable non-zero exit status or explicit pass/fail state;
- structured or bounded error output;
- precise failing test, rule, schema, file, endpoint, or trace locator;
- distinction between environment/setup failure and product/implementation failure;
- deterministic reproduction instructions where the failure is not self-contained;
- preserved revision, configuration, and environment identity.

Human-readable prose remains valuable, but do not make an agent infer a machine
verdict from ambiguous free-form logs when a deterministic interface can expose the
same result directly.

## Readiness implications

Treat an unavailable or unreliable feedback surface as a gate only when it prevents the proposed autonomy from independently detecting a material incorrect implementation.

Examples:

- A documentation-only change may not need a running application at all.
- A pure library change with strong contract/property tests may have sufficient verification without a browser or deployed service.
- A UI workflow change is weakly supported if agents can edit components and run unit tests but cannot start the application and exercise the user-visible flow.
- An event-driven integration change is weakly supported if local tests pass but the executor cannot drive the relevant event boundary or observe downstream state.
- A repository where focused tests complete quickly but the only application-level check takes an hour may still support bounded local work while leaving broader unattended iteration constrained until a faster discriminating seam exists.

Do not demand expensive end-to-end infrastructure merely to raise a maturity score. The remediation should be the smallest feedback seam that can actually falsify the important failure modes.

## Evidence quality

Prefer evidence that is:

- reproducible across clean or reset environments;
- isolated from production credentials and uncontrolled side effects;
- deterministic enough that failures are attributable rather than dominated by flakiness;
- representative of the interface and dependencies whose behaviour matters;
- fast enough to be used at the point where the workflow needs the signal;
- machine-actionable enough that the executor can identify the failing boundary without speculative log interpretation;
- independently observable rather than relying on the implementing agent's narrative.

Record hidden manual setup, mutable external services, brittle seed data, flaky startup, opaque environment state, long latency, queueing delay, weak failure attribution, and unstructured failure output as readiness limitations.

## Remediation patterns

Prefer small durable improvements such as:

- a documented and CI-exercised local/dev startup command;
- safe seeded fixtures or disposable test data;
- a narrow API/event/CLI driver for the relevant behavioural seam;
- service virtualization or an emulator where a live dependency is unnecessary;
- deterministic reset/cleanup;
- revision-bound logs or traces that expose the relevant state transition;
- a representative smoke or integration check wired to the same surface agents use during implementation;
- splitting one slow broad validation path so a cheaper discriminating check fails earlier while the broader gate remains authoritative where needed;
- stable structured failure output or a small wrapper that exposes machine-readable status without changing the underlying verifier.

Do not prescribe a particular browser framework, container platform, orchestration stack, or test runner unless repository evidence makes it the smallest appropriate solution.

## Behavioural calibration cases

### AOF-C1 — generation is fast but verification dominates the loop

An agent can produce a candidate service change in three minutes. The only useful
integration signal enters a shared CI queue, starts after ten minutes, runs for
another fifteen, and returns a large free-form log. Most failures are schema or
fixture mismatches that could be detected locally.

Expected behaviour:

- identify feedback latency and failure triage as material workflow constraints;
- do not conclude that faster model generation is the next optimisation target;
- recommend the cheapest reliable earlier discriminator for the recurring failure
  classes while preserving the broader gate for failures it uniquely detects;
- prefer machine-actionable status and locators over asking the agent to mine an
  opaque log;
- avoid inventing a universal acceptable CI duration.

### AOF-C2 — slow consequential gate is still justified

A migration check takes twenty minutes because it exercises representative recovery
and compatibility paths that cheaper tests cannot observe. The check is stable,
revision-bound, parallel with unrelated work, and required only for migration-class
changes.

Expected behaviour:

- keep the gate when its unique evidence is proportionate to the consequence;
- avoid treating elapsed time alone as evidence of poor readiness;
- look for earlier complementary checks or setup improvements only when they add
  useful discrimination without weakening the authoritative gate.

## Stop condition

Stop once the proposed activity has a credible, independently observable feedback path for its material behaviour and failure modes. More environment realism is not automatically more readiness, and lower latency is not automatically better when it removes necessary evidence.

## Source provenance

The latency and machine-actionability refinements are informed by Honeycomb's 2026
engineering posts on AI-first engineering practices and safely handling increased
pull-request throughput. The transferable mechanism is that once implementation
becomes much cheaper, slow or opaque verification can become the dominant system
constraint; improve the earliest reliable feedback seam rather than merely driving
more generation throughput.
