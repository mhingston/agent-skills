# Durable External Subscriptions

Use this reference when a workflow can pause while waiting for an external event such as CI completion, review feedback, a deployment, approval, message, job, or metric transition.

The key rule is simple: **model the wait as durable workflow state, not as a coordinator conversation that must remain alive.**

## Define subscription state

For each external wait define, where material:

- stable subscription identity and owning run/task/phase;
- authoritative external resource plus exact revision, attempt, deployment, or other correlation identity;
- event classes that may wake the workflow and the terminal condition that ends the wait;
- persisted wake/reconciliation state, including the last accepted event or cursor when the source requires one;
- duplicate, out-of-order, stale, and superseded event handling;
- expiry, cancellation, replacement-owner, and unsubscribe/cleanup semantics;
- the authoritative read or reconciliation step performed after wake-up before any state transition or repeated effect.

Treat notifications as prompts to reconcile, not proof that the desired state now holds. After a wake-up, read the current authoritative external state and bind any accepted transition to the exact identity it validates.

Make event handling idempotent so duplicate delivery cannot create duplicate workers, pull requests, approvals, deployments, or other effects.

## Coordinator replacement

A replacement coordinator must be able to reconstruct outstanding subscriptions from durable state, determine whether the external work already exists or has already completed, and continue from the earliest still-valid transition without restarting completed work.

Do not infer missing work merely because the original coordinator disappeared. Reconcile against the external system first.

When ownership or leases are material, make replacement explicit so two coordinators cannot both act on the same wake-up.

## Terminal cleanup

Stop or remove subscriptions when the owning workflow reaches a terminal, cancelled, expired, or superseded state. Late events after cleanup must not restart abandoned work.

Where physical unsubscription is impossible or unreliable, persist a terminal ownership/state check that causes later events to be ignored deterministically.

## Polling fallback

Polling may substitute for push events when the external system has no suitable subscription mechanism, but keep the same durable correlation, reconciliation, idempotency, ownership, and terminal-cleanup semantics.

Do not create a model-based poller for a condition deterministic code can check.

## Verification

Test at least these failure shapes when they are material:

- coordinator replacement while waiting on an external resource;
- duplicate, delayed, out-of-order, stale, and superseded events;
- an event for an older revision after a newer revision exists;
- process death after external work is created but before the subscription state is fully recorded;
- terminal cleanup followed by a late event;
- polling fallback after missed push delivery;
- concurrent or replacement coordinators attempting to handle the same wake-up.

Acceptance should depend on authoritative reconciliation and exact state/revision binding, not on receipt of an event by itself.
