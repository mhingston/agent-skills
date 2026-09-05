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

## Readiness implications

Treat an unavailable or unreliable feedback surface as a gate only when it prevents the proposed autonomy from independently detecting a material incorrect implementation.

Examples:

- A documentation-only change may not need a running application at all.
- A pure library change with strong contract/property tests may have sufficient verification without a browser or deployed service.
- A UI workflow change is weakly supported if agents can edit components and run unit tests but cannot start the application and exercise the user-visible flow.
- An event-driven integration change is weakly supported if local tests pass but the executor cannot drive the relevant event boundary or observe downstream state.

Do not demand expensive end-to-end infrastructure merely to raise a maturity score. The remediation should be the smallest feedback seam that can actually falsify the important failure modes.

## Evidence quality

Prefer evidence that is:

- reproducible across clean or reset environments;
- isolated from production credentials and uncontrolled side effects;
- deterministic enough that failures are attributable rather than dominated by flakiness;
- representative of the interface and dependencies whose behaviour matters;
- fast enough to be used at the point where the workflow needs the signal;
- independently observable rather than relying on the implementing agent's narrative.

Record hidden manual setup, mutable external services, brittle seed data, flaky startup, opaque environment state, long latency, and weak failure attribution as readiness limitations.

## Remediation patterns

Prefer small durable improvements such as:

- a documented and CI-exercised local/dev startup command;
- safe seeded fixtures or disposable test data;
- a narrow API/event/CLI driver for the relevant behavioural seam;
- service virtualization or an emulator where a live dependency is unnecessary;
- deterministic reset/cleanup;
- revision-bound logs or traces that expose the relevant state transition;
- a representative smoke or integration check wired to the same surface agents use during implementation.

Do not prescribe a particular browser framework, container platform, orchestration stack, or test runner unless repository evidence makes it the smallest appropriate solution.

## Stop condition

Stop once the proposed activity has a credible, independently observable feedback path for its material behaviour and failure modes. More environment realism is not automatically more readiness.