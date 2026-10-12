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

## RT-5 — an unconfirmed lens recommendation is not ticket intent

**User prompt:** "Refine the checkout-retry ticket for an implementing agent."

**Evaluator-only setup:** The source ticket has an existing `AC-2` requiring
failed attempts to be recorded, but does not decide retry count or backoff.
Repository code currently makes three attempts; Engineering recommends keeping
that behaviour, while QA proposes a terminal-failure example. No authorised
decision makes the observed retry count a product rule. The Product Owner is
the accountable resolver. Other required ticket fields have supporting evidence.

**Outcome checks:** Tags current three-attempt implementation `observed` and
the proposed retry policy `recommended`, with provenance. Returns
`NEEDS_INPUT` for the undecided product rule, retaining `AC-2` and its ID.
Does not create new `AC-N`/`NG-N` entries, constraints, verification
expectations, or publishable expected outcomes for the recommended retry policy.
Routes the question to `named-owner` (Product Owner) with the blocking gate
and needed decision, rather than inferring authority from code or lens agreement.

## RT-6 — disagreeing lenses request an accountable decision

**User prompt:** "Make this account-invitation expiry story implementable."

**Evaluator-only setup:** The source requires invitation expiry but leaves its
duration undefined. Business recommends 24 hours, Engineering recommends seven
days for compatibility, and QA asks what happens at the expiry boundary. No
canonical policy settles duration. The named Policy Owner can make the choice;
the remaining readiness gates are independently supportable.

**Outcome checks:** Preserves both readings and their provenance; records a
material disagreement with `named-owner` (Policy Owner) as resolver and a
focused gate-linked prompt. Returns `NEEDS_INPUT` rather than `READY` or
silently selecting either duration. Does not put a 24-hour/seven-day outcome in
the proposed ticket or publish the boundary example before the decision.

## RT-7 — an open QA outcome prevents READY

**User prompt:** "Assess our password-reset request ticket for readiness."

**Evaluator-only setup:** The supplied contract defines the ordinary successful
request path and verification, but deliberately leaves the response for an
unknown email address undecided. QA surfaces the choice between a generic
response and an account-revealing error; available code cannot authorise future
product/security intent. A Security Owner is named but has not answered. All
other gates have justified assessments.

**Outcome checks:** Returns `NEEDS_INPUT` with the open QA question and
`named-owner` (Security Owner), mapping it to `interpretation-resolved` and
the affected completion/verification gates. Does not mark those gates passed or
return `READY` merely because the happy path is complete. Preserves the
already supported happy-path criterion/example but excludes an unconfirmed
unknown-address outcome from the proposed rewrite.

## RT-8 — accepted boundary examples preserve exact contract traces

**User prompt:** "Review the batch-upsert ticket and prepare its final rewrite."

**Evaluator-only setup:** An attributable accepted source defines `AC-3`:
mixed-validity batches reject atomically, `AC-4`: empty input is a no-op,
and `NG-4`: the existing single-record endpoint stays unchanged. No material
questions remain, and all readiness gates have evidence. QA produces a
mixed-validity case, an empty case, a legacy-endpoint compatibility case, and
a vague example without a stated expected outcome.

**Outcome checks:** Returns `READY` with unchanged `AC-3`, `AC-4`, and
`NG-4` meanings and IDs. Every published example states a concrete expected
outcome and traces to the correct entry (`AC-3` for atomic rejection,
`AC-4` for empty input, `NG-4` for unchanged legacy behaviour). Drops the
vague example instead of inventing its oracle; includes no unsupported extra
cases or contradictory traces.
