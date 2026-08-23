---
name: integration-reconciliation
description: Resolve in-progress Git merge, rebase, or cherry-pick conflicts by reconstructing the intent and authority behind each side, classifying semantic compatibility, making only evidence-supported resolutions, validating the integrated behaviour, and finishing the operation when safe. Use when version-control integration is blocked by conflicts and line-level conflict markers are insufficient to decide the correct result. Do not use for ordinary code review, generic decision history, contract reconciliation, or unrelated implementation work.
compatibility: Requires Git access to the repository and read access to relevant history. Validation may require an isolated executor for repository-controlled build and test commands.
---

# Integration Reconciliation

Resolve conflicted version-control integration by reconciling **meaning**, not by
choosing whichever side is newer, cleaner, or easier to compile.

A conflict is evidence that two change histories cannot be combined mechanically.
The goal is to recover the intended integrated state, preserve compatible intent,
and stop when authority or requirements are insufficient to choose between
incompatible meanings.

## Boundaries

- Start only from an explicit integration request or an already active merge,
  rebase, or cherry-pick. Do not create a new integration operation merely because
  branches differ.
- Do not `reset --hard`, force-update refs, force-push, discard unrelated work, or
  abort an operation unless the user separately and explicitly asks for that
  recovery action.
- Unlike a line-oriented resolver, this workflow may return `BLOCKED`. Never
  invent product behaviour simply to eliminate conflict markers.
- Do not infer intent from code alone when a commit, issue, PR, ADR, specification,
  or attributable decision can establish it more directly.
- Do not treat a passing build as proof that incompatible business or architectural
  intent was reconciled correctly.
- Do not silently reopen an accepted/rejected decision or let one side's recency
  override a more authoritative governing source.
- Keep the scope to the integration conflict and the minimum adjacent changes
  required for a coherent merge result. Report unrelated defects separately.
- Invocation authorises in-scope conflict edits, staging, and the normal
  `merge --continue`, `rebase --continue`, or `cherry-pick --continue` steps needed
  to finish the named operation when the reconciliation is supported. It does not
  authorise pushing, merging a pull request, deployment, or unrelated cleanup.

## Route adjacent work

Use another workflow when the primary task is:

- reconciling a proposal or resumed work against earlier accepted/rejected intent
  without a concrete Git conflict: use `decision-continuity`;
- comparing implemented behaviour with a canonical ticket contract: use the
  implementation workflow's contract-reconciliation stage;
- reviewing a branch or pull request: use technical review;
- implementing a new product decision exposed by the conflict: stop this workflow
  and route to planning/refinement after the accountable decision is made;
- diagnosing a failing integrated result whose cause is unclear after conflict
  resolution: use a fault-isolation workflow.

These are routing boundaries, not package dependencies.

## Evidence model

For each material conflict preserve:

- **Observed (`E#`)** — Git state, conflict hunk, commit content, source file,
  test result, issue/PR/ADR/spec text, or other inspected evidence.
- **Inferred (`I#`)** — interpretation of what a side is trying to preserve. State
  the evidence and what would falsify it.
- **Unknown (`U#`)** — missing authority, unavailable source, ambiguous intent, or
  unresolved compatibility that can change the resolution.

Also distinguish **behaviour provenance** from **decision authority**. A commit can
prove that a behaviour existed on one side; it does not by itself prove that the
behaviour is still intended or authorised to override another accepted rule.

## 1. Establish the exact integration state

Inspect Git before editing:

- current operation type: merge, rebase, or cherry-pick;
- current branch / detached state and `HEAD`;
- merge/rebase/cherry-pick metadata and commits being integrated;
- unmerged paths and conflict stages;
- pre-existing worktree changes that are not part of the operation;
- repository instructions and documented merge/rebase conventions.

If no integration operation is active and no explicit pair of revisions was
provided for a requested integration, return `NO_ACTIVE_INTEGRATION` instead of
guessing what should be combined.

If unrelated dirty state cannot be distinguished safely from operation-owned
changes, return `BLOCKED` before editing.

## 2. Classify conflicts before resolving them

For each conflicted path/hunk classify the decision shape:

- `MECHANICAL` — formatting, imports, path movement, generated ordering, or another
  conflict whose semantics are unchanged and independently checkable;
- `COMPATIBLE_INTENT` — both sides make meaningful changes that can coexist;
- `SEMANTIC_COMPETITION` — both sides change the same behaviour or invariant in
  materially different ways;
- `AUTHORITY_AMBIGUOUS` — the correct behaviour depends on a decision whose
  authority or active status is not established;
- `GENERATED_OR_DERIVED` — the conflicted artifact should be regenerated from a
  more authoritative source after that source is reconciled;
- `UNKNOWN` — evidence is insufficient to classify safely.

Do not assume a syntactically small conflict is mechanical. One line can encode a
material state transition, permission, schema, or public-contract difference.

## 3. Reconstruct each side's intent from primary evidence

For every non-mechanical material conflict, trace both sides just far enough to
understand why the change exists.

Prefer, when available:

1. canonical specification, policy, ADR, accepted ticket, or explicit decision;
2. originating PR/issue and attributable review/decision evidence;
3. commit message plus the surrounding commit diff;
4. tests or runtime evidence that establish behavioural expectations;
5. code structure as evidence of current behaviour, not retrospective rationale.

Record for each side:

- originating revision/change identity;
- observable behaviour it introduces or preserves;
- stated rationale/constraint when attributable;
- governing source and authority when known;
- tests or other checks that encode its expected behaviour;
- whether the intent remains active, superseded, rejected, or unknown.

Stop historical exploration once more context is unlikely to change compatibility,
authority, or the intended integrated state.

## 4. Derive the integration contract

State the smallest contract the resolved result must satisfy:

- the goal of the current integration operation;
- behaviours/invariants from each side that remain active;
- superseded/rejected behaviour that must not be resurrected;
- compatibility constraints and public interfaces that must survive;
- explicit unknowns or human decisions that block safe reconciliation.

When both intents can coexist, prefer the smallest composition that preserves both
without adding new behaviour. When one side clearly supersedes another under an
attributable governing decision, preserve the active decision and document the
supersession evidence.

When the sides are genuinely incompatible and no authority resolves the choice,
return `BLOCKED` with the exact decision required. Do not choose based on branch
name, timestamp, apparent code quality, or assumed product preference.

## 5. Resolve source conflicts before derived artifacts

Resolve semantic source files first.

For `GENERATED_OR_DERIVED` conflicts such as lockfiles, generated clients, build
outputs, snapshots, or compiled manifests:

1. identify the authoritative source inputs;
2. reconcile those inputs semantically;
3. discover the repository's documented regeneration command;
4. regenerate in an isolated executor when safe;
5. verify the generated result corresponds to the reconciled source.

Do not hand-edit a derived artifact when a deterministic regeneration route exists.
If the generator or exact command is unavailable, preserve the conflict or return
`BLOCKED` rather than inventing generated content.

## 6. Edit one conflict group at a time

Apply only the resolution justified by the integration contract.

After each semantically related group:

- confirm conflict markers are removed only from the intended paths;
- inspect the resulting diff against both source revisions;
- verify no active behaviour was accidentally dropped;
- stage only resolved paths whose result has been checked;
- keep unresolved paths un-staged and visible.

For simple mechanical conflicts, concise local verification is enough. For
semantic conflicts, preserve a short evidence record linking the chosen result to
the governing intent.

Do not opportunistically refactor the merged code while resolving conflicts. If a
small structural adjustment is required to compose both active intents, keep it
minimal and explain why it is part of reconciliation rather than cleanup.

## 7. Validate the integrated state

Before continuing the Git operation, discover and run the strongest relevant
checks for the affected area:

- conflict-marker and syntax checks;
- format/lint/type/static validation;
- focused tests covering each preserved behaviour/invariant;
- generated-artifact consistency;
- relevant integration tests;
- full project checks when repository policy or conflict breadth requires them.

Run repository-controlled commands in an isolated executor with no ambient
production credentials and network disabled by default. A check that succeeds
while not exercising the reconciled behaviour is not evidence of semantic
correctness.

If validation exposes a new defect whose resolution is not determined by the
integration contract, do not invent a fix inside this workflow. Classify whether
it is caused by incomplete reconciliation, a pre-existing failure, or a new
implementation problem; return `BLOCKED` or route accordingly.

## 8. Continue the operation safely

When all current conflicts are reconciled and required checks pass:

- confirm all intended conflicted paths are resolved and no conflict markers
  remain;
- inspect the staged diff and status;
- continue the active merge/rebase/cherry-pick using the repository's normal Git
  mechanism;
- if a rebase/cherry-pick exposes the next conflict set, repeat this workflow for
  that exact step;
- after completion, verify final Git status, branch/revision identity, and the
  resulting commit sequence/tree.

Do not push. Do not force-update history. If hooks or continuation commands modify
files unexpectedly, stop and revalidate the resulting state before continuing.

## Output contract

Return one status:

- `RECONCILED` — the named integration operation completed with supported
  conflict resolutions and required checks;
- `PARTIAL` — some conflict groups were safely reconciled but the operation remains
  active with clearly identified unresolved groups;
- `BLOCKED` — a material intent, authority, generator, verification, or environment
  prerequisite prevents safe completion;
- `NO_ACTIVE_INTEGRATION` — no in-progress or explicitly defined integration could
  be established.

Include:

1. **Integration state** — operation type, source/target revisions, and initial
   conflict paths.
2. **Conflict ledger** — classification, both-side intent/provenance, governing
   evidence, and resolution disposition for each material conflict group.
3. **Integration contract** — active behaviours/invariants and superseded or
   unresolved decisions.
4. **Resolution summary** — exact paths/groups changed and why.
5. **Validation** — commands/checks, observed results, and limitations.
6. **Git outcome** — operation state, resulting revision when completed, and
   remaining conflicts when partial/blocked.
7. **Required decision or next action** — only when further work is needed.

Read [references/evaluation-suite.md](references/evaluation-suite.md) when
validating this skill or changing its trigger and authority boundaries.

## Quality gate

Before finishing, verify that:

- the workflow operated on a concrete integration state rather than a generic diff;
- each semantic conflict was traced to enough intent/provenance to justify the
  result;
- recency or code aesthetics were not mistaken for authority;
- compatible active intent was preserved from both sides where possible;
- incompatible intent without authority produced a visible block rather than an
  invented compromise;
- generated artifacts were regenerated from reconciled sources where practical;
- checks actually exercised the integrated behaviour;
- unrelated work was not discarded or broadened into the reconciliation;
- no push, deployment, PR merge, or force operation was performed.
