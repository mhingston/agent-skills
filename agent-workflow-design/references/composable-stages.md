# Composable autonomous stages

Use this reference when a workflow combines several meaningful stages into a higher-autonomy path, especially when the same stages may also be invoked, inspected, retried, or stopped independently.

## Principle

Prefer **composition over a second autonomous implementation path**.

If `investigate`, `implement`, `review`, and `verify` are meaningful standalone stages, a higher-autonomy workflow should normally orchestrate those same contracts rather than introduce a separate monolithic agent that reimplements their behaviour internally.

The goal is not to maximise the number of stages. It is to make the boundaries that already matter operationally usable for both humans and automation.

## What a composable stage needs

A stage is independently operable when it has enough of a contract to be started, observed, stopped, and reasoned about without relying on hidden state from the surrounding autonomous run. Define, where material:

- a bounded externally meaningful outcome;
- typed or otherwise unambiguous inputs and outputs;
- source, revision, or state identity;
- authority and effect boundaries that do not expand merely because the caller is autonomous;
- acceptance and failure evidence;
- retry, cancellation, stale-input, and supersession semantics;
- durable receipts or checkpoints needed by a later stage;
- the earliest safe point from which an operator can resume or redirect work.

Do not split a coherent responsibility merely to create more checkpoints. A stage boundary earns its existence when it improves independent verification, authority separation, interruption/recovery, manual intervention, or reuse.

## One contract, multiple invocation modes

Manual, supervised, scheduled, and autonomous invocation should preserve the same stage semantics unless an explicit policy difference is part of the design.

Avoid hidden autonomous-only behaviour such as:

- weaker validation because the outer loop will "catch it later";
- broader tool or write permissions than the standalone stage receives;
- private retry logic that bypasses the stage's normal failure contract;
- a different implementation path whose results cannot be reproduced by running the constituent stages;
- implicit state that exists only in the orchestrator's model context.

The autonomous path may decide **when** to invoke a stage, but it should not silently redefine what that stage means or what evidence makes it complete.

## Operator control

For a long or consequential run, define where an operator can:

- inspect the current exact state and accumulated evidence;
- pause before a consequential transition;
- cancel work that has not yet produced required effects;
- redirect from a failed or invalidated strategy;
- rerun only the smallest invalid stage when its inputs and authority remain current;
- resume without discarding still-valid evidence from earlier stages.

Do not require a human checkpoint at every boundary. The purpose is controllability and recoverability, not approval ceremony.

## Model and reasoning budget

Treat model allocation as an empirical workflow design decision, not a prestige hierarchy.

When stages differ materially in decision leverage, it can be reasonable to spend more reasoning budget on bounded planning, design, diagnosis, or independent review and less on high-volume mechanical execution. Validate that choice against the complete workflow rather than nominal per-call pricing.

Measure, where the harness permits:

- end-to-end cost per completed task, including failed attempts and retries;
- success or acceptance rate;
- downstream remediation/review work caused by earlier model choices;
- latency and context pressure;
- the marginal benefit of a stronger or more expensive model at the stage being changed.

Do not assume the cheapest model is cheapest end-to-end if it causes more retries, and do not assume a stronger model belongs on every stage. Pin model, harness, workflow, and evaluation versions when comparing allocations.

## Failure modes

Treat these as design smells:

- a "night mode" or autonomous entry point contains a second copy of stage logic;
- the operator cannot tell which stage is active or which evidence justified advancement;
- stopping the orchestrator loses valid stage outputs or makes them unusable;
- manual execution and autonomous execution produce materially different contracts without an explicit reason;
- retries restart the whole pipeline when only one stage is invalid;
- model tiering is justified only by per-token price or intuition rather than end-to-end evidence.

## Stop condition

Do not introduce this machinery for a short deterministic procedure or one coherent model decision. Use it when independent stage operation materially improves control, verification, recovery, reuse, or gradual adoption of higher autonomy.