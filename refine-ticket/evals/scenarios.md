# Refine-ticket behavioural scenarios

Package-local outcomes for the internal `refine-ticket` module, exercised only
via the owning `refine` agent with its complete invocation context and
`references/readiness-rubric.yml`. Run matched baseline/candidate trials per
`skill-creator/references/evaluation.md`. Expose the user prompt and ordinary
ticket/repository context to the candidate, not evaluator-only setup or checks.
Grade returned statuses, prompt dependencies, gate evidence and owner routing.

**Status: NOT_RUN.** No behavioural harness or matched trials were run. Static
validation, if later successful, is not evidence of behavioural improvement.

## RT-1 — prerequisite gate before dependent gate

**User prompt:** "Make this bounded payment retry ticket agent-ready."

**Evaluator-only setup:** Unresolved rubric gate A
(`desired-outcome-and-rationale`: which attempts may retry) precedes gate B
(`completion-criteria-testable`: measurable criteria for that decision).
An independent unresolved gate C (`verification-defined`) has no dependency.
All other gates have justified assessments.

**Outcome checks:** First `NEEDS_INPUT` packet may ask A and C, but not B.
B can be prompted only in a later round once A is settled. Every prompt retains
its gate ID and a specific resolver.

## RT-2 — independent open gates obey the four-prompt cap

**User prompt:** "Assess this incomplete API migration task."

**Evaluator-only setup:** Six independent unresolved gates from the real rubric
require human answers. No evidence settles them and none depends on another.

**Outcome checks:** Returns no more than four distinct prompts on the first
`NEEDS_INPUT` packet; remaining gates are retained for a later round and are
not silently passed, skipped or forgotten.

## RT-3 — evidence-answerable gate is not a human question

**User prompt:** "Refine our retry-idempotency issue."

**Evaluator-only setup:** An existing schema and contract test establish the
current idempotency key. A retention duration remains undecided and belongs to
the named policy owner, absent from the session.

**Outcome checks:** Resolves the key-shape gap from evidence, includes the
source locator, and never asks the human for it. Returns the retention question
with a `named-owner` resolver and role; does not invent a duration, change
tracker data or return `READY` with the gate unresolved.

## RT-4 — cycle is a blocker, not an arbitrary first question

**User prompt:** "Assess the outstanding requirements for this migration."

**Evaluator-only setup:** Gate A is contingent on unanswered gate B and B on
unanswered A. Neither is answerable from source evidence; other gates are
already assessed. Include this dependency graph in the orchestrator context.

**Outcome checks:** Returns `BLOCKED` with
`CYCLIC_GATE_DEPENDENCIES`, identifies A↔B and asks the orchestrator to
reconcile the assumptions. Does not ask A or B arbitrarily or assert `READY`.
