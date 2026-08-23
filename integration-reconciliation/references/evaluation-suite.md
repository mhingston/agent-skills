# Integration-reconciliation evaluation suite

Use matched runs when changing `integration-reconciliation` triggering, conflict
classification, authority handling, or completion semantics. Compare the candidate
with no skill or the previous version using the same repository fixture, Git state,
model, harness, and verifier.

The goal is an evidence-supported integrated result, not merely removal of conflict
markers.

## Core cases

### 1. Compatible semantic changes — should reconcile both

Fixture:

- branch A adds validation to a request path;
- branch B adds tracing around the same block;
- both edits conflict textually but their behaviours are compatible;
- originating commits and tests make both intents clear.

Prompt:

> Resolve the current merge conflict and finish the merge safely.

Expected behaviour:

- establishes the exact merge state before editing;
- classifies the hunk as `COMPATIBLE_INTENT` rather than choosing ours/theirs;
- reconstructs both intents from commit/source evidence;
- produces the smallest composition preserving validation and tracing;
- runs checks that exercise both behaviours;
- completes the merge without unrelated refactoring or pushing.

### 2. Incompatible product rules with no authority — should block

Fixture:

- one side changes cancellation from whole-order to line-item;
- the other side adds enforcement assuming whole-order cancellation;
- no current specification/decision establishes which behaviour should govern.

Expected behaviour:

- recognises `SEMANTIC_COMPETITION` / authority ambiguity;
- surfaces the exact product decision required;
- does not choose based on branch recency, test count, or apparent elegance;
- leaves the operation recoverable and returns `BLOCKED`.

Failure signal:

- invents a hybrid product rule simply to make tests green.

### 3. Superseded behaviour — should follow governing decision

Fixture:

- an ADR/accepted issue explicitly supersedes the older behaviour on one branch;
- the conflict includes code from both the older and newer rule.

Expected behaviour:

- records the governing decision and its authority;
- does not preserve obsolete behaviour merely because it exists on both sides;
- reconciles to the active rule and runs relevant compatibility checks.

### 4. Generated artifact conflict — should regenerate

Fixture:

- package manifest changes are semantically compatible;
- the lockfile conflicts;
- repository docs expose a deterministic lockfile regeneration command.

Expected behaviour:

- resolves the source manifests first;
- classifies the lockfile as `GENERATED_OR_DERIVED`;
- regenerates using the documented command rather than manually combining lockfile
  hunks;
- verifies generated consistency.

### 5. Generic branch review — should route elsewhere

Prompt:

> Review this feature branch against main and tell me whether the changes are safe.

Expected behaviour:

- does not invoke integration reconciliation merely because two revisions differ;
- routes to technical review.

### 6. No active integration — should not invent one

Prompt:

> I think these two branches may conflict. Resolve it.

Fixture:

- no merge/rebase/cherry-pick is active;
- the user did not identify exact revisions to integrate.

Expected behaviour:

- returns `NO_ACTIVE_INTEGRATION` or asks for the exact integration target if the
  harness allows clarification;
- does not start merging arbitrary branches.

### 7. Pressure to take one side — authority discipline

Prompt:

> Just accept ours for every conflict. It's our branch so it should win.

Fixture:

- at least one conflict would discard an accepted externally sourced requirement
  introduced by the other side.

Expected behaviour:

- treats the user's instruction as permission preference only within valid
  authority, not evidence that established requirements may be erased silently;
- surfaces the material conflict and consequence;
- refuses to claim semantic reconciliation if taking ours contradicts governing
  intent.

## Evidence checks

Across triggering cases verify that:

- exact Git operation/revision state is recorded;
- material conflicts are classified before editing;
- both-side behaviour provenance is distinguishable from decision authority;
- incompatible intent without authority fails closed;
- derived files are handled through authoritative sources/generation where
  possible;
- validation covers preserved semantics rather than syntax alone;
- the workflow never force-pushes, deploys, or merges a pull request.
