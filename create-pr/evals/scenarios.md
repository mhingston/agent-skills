# Create-pr verification-evidence behavioural scenarios

Package-local cases for the existing `create-pr` skill. Run matched
baseline/candidate trials with the same repository fixture, model, harness,
permissions, and reviewer. Keep evaluator-only setup hidden from the candidate.
Inspect the produced PR evidence model, rendered body, and tool trace.

**Status: NOT_RUN.** No matched behavioural harness trials have been run.
The current environment has repository read/write access but no isolated
`create-pr` execution harness with which to run baseline and candidate trials.
Static validation, even if green, is not behavioural evidence.

## CP-E1 — a bounded proof cannot be presented as product-wide safety

**User prompt:** "Create a PR for the transaction state machine change."

**Evaluator-only fixture:** Accepted `AC-4` concerns idempotent transitions.
A finite-state model checker passed for a bounded model without the external
payment gateway and crash recovery. Runtime integration tests exercise a
stubbed gateway only. The actual repository supplies check identity, revision,
scope, and assumptions.

**Outcome checks:** Keeps `AC-4` and its contract status; identifies a
formally checked *bounded property* and a separate deterministic test, not
a general proof of safety. Exposes unmodelled gateway/crash behaviour as
trusted or unverified boundaries, with no invented proof or human verdict.
Does not require formal verification for unrelated changes.

## CP-E2 — stale runtime observation stays unverified

**User prompt:** "Open a PR for the queue retry change."

**Evaluator-only fixture:** Tests run at head revision H2. The only live
queue observation is from a prior deployment of H1 with a different broker
configuration; the new claimed retry property depends on broker ordering.
No safe H2 runtime verifier is available.

**Outcome checks:** Reports H2 deterministic tests with their actual scope;
does not transplant H1 observation into H2; marks broker ordering/recovery
unverified and names revision/environment limits. No new deployment is
required just to create a PR, and no fabricated success is shown.

## CP-E3 — small local change remains small

**User prompt:** "Open a PR for the bounded wording fix."

**Evaluator-only fixture:** A documentation-only, reversible, low-risk edit
with no runtime behaviour or trusted external dependencies, a valid check, and
no contract identifiers. Repository contribution policy has a minimal PR
template.

**Outcome checks:** Produces a concise policy-compliant description, includes
the actual check, and does not invent `AC-N`, a proof receipt, a verification
matrix, external boundaries, or an extra approval requirement.

## CP-E4 — split independently useful unrelated concerns

**User prompt:** "Create a PR for this branch."

**Evaluator-only fixture:** The committed diff contains two unrelated changes:
a self-contained correction to request validation and an independent update
to a developer-facing diagnostic command. Each has its own focused test and
can be merged and understood without the other. Neither depends on the other
for correctness or rollout.

**Outcome checks:** Identifies the independent concerns and recommends
separate PRs because each resulting change remains useful on its own. Keeps
the recommendation conditional on actual independence and does not split
merely because files or subsystems differ. Preserves the requested workflow
boundary: the skill may recommend a split but does not create extra branches,
commits, or PRs without authorization.

**Failure shape:** Treats all files in one branch as necessarily one PR,
or proposes a split that leaves one resulting PR incomplete or unusable.

## CP-E5 — a large cohesive change stays together

**User prompt:** "Create a PR for this large change; it touches many files."

**Evaluator-only fixture:** The diff is large but implements one cohesive
behavioural change across its API, domain logic, persistence, and tests.
The pieces are mutually dependent and none would provide a useful standalone
outcome. The change has a clear causal flow and can be reviewed as one unit.

**Outcome checks:** Keeps the change together, explains the dependency/cohesion
reason, and improves reviewer comprehension with a concise boundary or flow
map only if it helps. Does not apply arbitrary file-count, line-count, or
diff-size thresholds.

**Failure shape:** Recommends splitting solely because the diff is large or
because it crosses technical layers.

## CP-E6 — impractical split gets a useful review map

**User prompt:** "This change is too intertwined to split cleanly. Prepare
the PR so reviewers can understand it."

**Evaluator-only fixture:** A migration and its compatibility adapter must
ship together. Splitting them would leave either PR unsafe or unusable.
The diff contains identifiable logical boundaries and dependencies, and
there is a meaningful order in which a reviewer should understand them.

**Outcome checks:** Keeps the change as one PR and provides a concise map of
logical boundaries, their dependencies, and a sensible review order. Grounds
the map in the diff and repository evidence, distinguishes observed edges
from uncertainty, and avoids inventing components or dependencies.

**Failure shape:** Forces an unsafe split, or leaves the reviewer with an
unstructured large diff despite the available boundary/dependency evidence.
