# Mechanical-port execution patterns

Load this reference only when a `code-modernization` **transform** is a large, predominantly behaviour-preserving language/runtime port and the operator needs concrete execution-partition guidance. This is not a new execution workflow: `code-modernization` owns target, correctness certificate, pilot and scale gate; the selected implementation workflow/harness owns mutation, worker scheduling and retries. Do not use for ordinary refactors or behaviour-changing reimagination.

## Establish translation decisions before fan-out

For a representative dependency-bearing pilot, record unresolved semantic translations with stable IDs, source examples, approved mappings, evidence/owner, and an executable or review oracle. Useful dimensions include:
- ownership, aliasing, lifetime and deallocation boundaries;
- integer width, overflow, signedness, timestamps and timezone handling;
- eager/lazy evaluation, errors, panics, exceptions and cancellation;
- async scheduling, locking, ordering, retries and reentrancy;
- strings, Unicode, serialization, wire formats, ABI/FFI and persistence.

Keep a versioned mapping register (a table is sufficient); use structured inventory files only when automation consumes them. A mapping inferred from the source is not automatically authoritative intent. Mark uncertain mappings and route narrow falsifiable questions to `code-research`; an unapproved semantic choice must not spread across workers. Preserve a small source-to-target fixture for each risky mapping.

## Create verifiable repair units

1. Pin source revision, target revision, toolchains and exact certificate/fixture versions.
2. Complete an end-to-end pilot through the original modernization certificate, independent review and promotion route before scaling.
3. Partition along the dependency graph or mechanically disjoint scopes, with an owner and acceptance check for each.
4. Convert *actual* compiler, linker, test, or replay failures into bounded, reproducible repair tasks: failing command/fixture, observed diagnostic, affected scope, expected invariant and stop condition. Preserve raw logs/evidence.
5. Re-run the failing check and relevant regression checks against the exact resulting revision. Rebuild the task queue from fresh diagnostics; do not assume a previous error count represents current progress.
6. On repeated failures, revise the mapping rule, fixture, partition or tool environment, then replay a representative failed case. Cap retries and stop on non-convergence; do not endlessly reprompt.

Compile-success is a diagnostic milestone, **not** behavioural parity. For source/target disagreement classify each case as regression, approved change, exposed legacy defect or unknown; never automatically force the target to reproduce an old defect.

## Isolate concurrent mutation and shared tools

Default to a single mutation lane. Parallel work is conditional on isolated worktrees/containers or mechanically disjoint file ownership, explicit integration responsibility, and a controlled shared-build strategy. Workers must not mutate each other's branches, Git state, certificate/oracle inputs, or common build outputs. Serialize or resource-limit expensive compilation and tests where necessary. Limit generation WIP to the throughput of integration, independent verification and accountable review.

After integrating partitions, run fresh cross-partition and cross-platform evidence; individually green branches do not imply an integrated green build.

## Detect shortcut success and preserve independence

A producer may not satisfy a compiler/test target by substituting placeholders, stubbing unsupported functionality, deleting/skipping tests, weakening assertions, excluding failing modules, suppressing relevant diagnostics or modifying golden fixtures or certificate thresholds. Genuine changes to these controls require separate authority, review and revalidation. Watch for semantic workarounds that preserve signatures but lose behaviour.

Use fresh independent semantic review for mappings not established by executable checks, without treating multiple same-model reviews as fully independent proof. Prefer differential/replay, property tests, sanitizers/fuzzing where appropriate, compatibility fixtures, and production-shadow evidence proportionate to risk. Bind every receipt to its revision and environment.

## Stop conditions and handoff

Stop/escalate when semantic decisions are unresolved, a reliable oracle is absent, failures repeat without measurable progress, shared state conflicts, cost/resource limits trip, or verification/review queues grow faster than completed certified work. Return the affected mapping IDs, diagnostics, unchanged certificate conditions, revision-bound evidence, remaining uncertainty, and the smallest next pilot/repair step. Never turn a passing check into release approval.

## Provenance

Adapted as an execution-oriented complement to the programme contract from Bun's 2026 Zig-to-Rust account: https://bun.com/blog/bun-in-rust . The transfer is the bounded mapping-and-verification loop, not Bun's specific model, agent count, cost, language, or parallelism settings.
