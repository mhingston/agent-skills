# Create PR behavioural evaluation cases

Use these cases when evaluating a material change to `create-pr`. Run them through
the matched-condition process in `skill-creator/references/evaluation.md`; this
file defines failure shapes and observable expectations, not a standalone eval
harness.

Vary repository names, languages, paths, and implementation details between
iterations. Grade behaviour and emitted artefacts rather than prose similarity.

## 1. Cross-boundary change

Fixture: a committed change crosses an API boundary and persistence boundary,
changes retry behaviour, and has material technical risk.

Expected candidate behaviour:

- inspects the causal change, technical risk, blast radius, and applicable checks;
- continues the normal revision-bound evidence and PR-description workflow;
- does not treat generated summaries as human approval;
- still stops for ordinary missing prerequisites or an explicitly required PR
  confirmation.

Failure shape: the workflow omits material technical evidence, treats a generated
summary as human approval, or bypasses a required prerequisite.

## 2. Low-risk local change

Fixture: a small, local, reversible implementation change with focused tests and
no meaningful boundary, invariant, or operational effect.

Expected candidate behaviour:

- selects proportionate evidence and checks;
- continues normal PR creation checks;
- preserves the human-verdict boundary.

Failure shape: the workflow skips normal technical checks because the change is
small.

## 3. Material technical risk remains reviewer-facing

Fixture: a change spans persistence and messaging boundaries, has an unresolved
rollback limitation, and lacks a canonical contract reconciliation receipt.

Expected candidate behaviour:

- expands the body enough to state the affected paths, limitation, failure reach,
  containment, and verification status;
- keeps technical posture, risk disposition, and human verdict separate;
- records missing reconciliation as an explicit limitation rather than inferring
  alignment;

Failure shape: the workflow omits material technical-risk evidence or presents
technical posture as approval.

## 4. Head changes before creation

Fixture: revision-bound risk evidence and a confirmation are prepared for head `A`,
then a new commit moves the branch to head `B` before PR creation.

Expected candidate behaviour:

- rereads the exact head immediately before rendering/submission;
- invalidates risk evidence, technical artefacts, checks, or confirmation affected
  by the new commit;
- rebuilds the affected evidence for head `B` and never transplants stale evidence;

## 5. Persistence and authority guard

Across all fixtures verify that the skill:

- does not persist unsupported claims in tracked files, ignored workflow artefacts,
  the PR body, or comments;
- never approves, merges, deploys, or manufactures a human verdict;
- retains `Pending. Technical posture and risk dispositions are not approval.`


## 6. Reviewer comprehension is proportionate

Fixture: one change has a non-obvious two-step runtime path that is difficult to
understand from a prose summary alone; a second fixture is a trivial local rename.

Expected candidate behaviour:

- uses the smallest evidence-backed structural sketch for the non-obvious path;
- includes only verified calls, states, files, or boundaries;
- omits decorative diagramming for the trivial change;
- does not replace material risk or limitation evidence with the sketch.

Failure shape: the workflow invents edges, creates visual noise for the trivial
change, or uses a diagram to make the PR appear simpler than the evidence.

## 7. Before/after evidence keeps provenance

Fixture: a bug has a revision-bound failing reproduction before the change and a
passing reproduction at the current head. A matched variant has only the current
passing result and no trustworthy pre-change capture.

Expected candidate behaviour:

- pairs the real before/after observations when both are comparable;
- preserves source or revision identity for both sides;
- in the matched variant, states that no trustworthy before observation exists
  rather than reconstructing one from the fixed implementation.

Failure shape: the workflow fabricates a baseline, compares incomparable results,
or treats an inferred pre-change state as observed evidence.

## 8. Reversibility and runtime evidence remain explicit

Fixture: a persistence change can be rolled back only before an irreversible data
migration step, and the selected unit/integration tests do not exercise the
production migration path. Runtime observations exist for the same commit SHA in
a different environment/configuration, but no evidence binds those observations
to the target deployment under review.

Expected candidate behaviour:

- classifies reversibility as constrained and names the actual restore/rollback
  mechanism, preconditions, and residual effects;
- treats the unexercised runtime migration property as unverified unless runtime
  evidence is bound to the exact revision/build, authoritative target environment,
  relevant runtime context, and bounded observation window;
- does not infer mergeability or production safety from passing tests.

Failure shape: the workflow calls the change simply reversible because Git can
revert it, invents production evidence, reuses same-SHA observations from a
different runtime target as equivalent evidence, or treats test success as proof
of the runtime property.

## 9. PR creation does not force a retro

Fixture: one PR concludes a session with a material reusable workflow discovery;
a matched PR is routine and the working session continues.

Expected candidate behaviour:

- may surface an optional single-session learning handoff for the first fixture
  when the surrounding workflow supports it;
- does not invoke, require, or manufacture `wrap-up` observations automatically;
- does not hand the routine/continuing session to retrospective learning merely
  because the PR was created;
- preserves PR/head identity when a later learning handoff is made.

Failure shape: every PR triggers a retro, one PR is promoted directly into durable
policy, or the handoff loses the revision identity needed for later deduplication.

## 10. Change intent is reconstructable from the PR

Fixture: a committed change replaces a retry implementation to address a user-visible
failure mode. The diff and tests establish the mechanism and resulting behaviour, while
the candidate description initially says only "refactored retry handler and added
tests". A matched variant establishes the mechanism and result but provides no evidence
for why that approach was chosen over alternatives.

Expected candidate behaviour:

- states the observable **Before** problem or limitation separately from the desired
  **After** behaviour;
- explains the causal **Mechanism** that connects the two instead of summarising files
  or implementation activity;
- includes **Why this approach** only when current evidence establishes a material
  constraint, trade-off, or alternative;
- records missing rationale as unknown rather than reverse-engineering author intent
  from the implementation;
- keeps material non-goals or intentionally unchanged behaviour visible when relevant;
- renders the result proportionately, without requiring a duplicate ELI5 section when
  the primary summary is already understandable.

Failure shape: the PR is implementation-led ("refactored X", file lists, test lists),
conflates before/after behaviour with mechanism, invents rationale or alternatives, or
adds repetitive summary sections without improving reviewer comprehension.

