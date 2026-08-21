---
name: contract-reconciliation
description: >-
  Internal implement-agent module for comparing one reviewed implementation
  against the immutable canonical ticket contract before final validation and
  publication. Use only when the implement agent supplies the accepted contract,
  exact working-tree identity, current diff, verification evidence, and an
  independent review for the same state.
metadata:
  mhingston.internal: "true"
  mhingston.owner-agent: "implement"
  mhingston.user-invocable: "false"
---

# Reconcile Implementation Against Contract

Compare the reviewed implementation with the exact accepted contract that
started the implementation run. Make drift explicit before the final project
gate. Do not revise requirements, change code, accept deviations, or create a
new source of intent.

This module answers one question: **does the implementation still implement the
accepted outcome, no more and no less, on the evidence available for this exact
working-tree state?**

## Invocation contract

Run only when `implement` supplies all of:

- `contract_reconciliation_state: RECONCILE`;
- canonical ticket/source identity and captured source version or supplied
  snapshot digest;
- the complete immutable ticket packet used for implementation, including the
  accepted outcome, acceptance criteria, constraints, non-goals, and material
  invariants;
- repository root, pinned base revision, exact feature branch, and the current
  deterministic working-tree fingerprint or committed revision;
- the complete in-scope diff for that state, or read-only access sufficient to
  inspect it completely;
- the implementation verification map and observed focused results for that
  same state;
- the current independent technical review and its reviewed state identity.

If required context is missing, inconsistent, stale, or refers to different
working-tree states, do not inspect further. Return
`REQUIRED_ORCHESTRATOR_CONTEXT` with the mismatch.

Never create or switch branches, edit files, run remediation, change tests,
commit, push, mutate the tracker, update the accepted contract, invoke another
agent, or create a pull request. The `implement` orchestrator owns lifecycle and
mutation.

## Boundaries

- Treat the canonical ticket packet as the contract for this run. Do not let the
  implementation, review prose, test names, comments, or model reasoning invent
  missing requirements or silently weaken existing ones.
- Treat implementation and verification as evidence about what was built, not as
  authority for what should have been built.
- Treat review findings as independently grounded technical evidence, not as new
  acceptance criteria or permission to redesign the task.
- Compare observable behaviour, contracts, constraints, non-goals, invariants,
  and material scope. Ignore harmless implementation freedom the contract leaves
  open.
- Extra unrequested behaviour, cleanup, refactoring, migration, dependency
  expansion, public surface, or operational change is drift when it materially
  expands the accepted scope, even when it appears beneficial.
- Do not infer that a canonical claim is wrong merely because the implementation
  chose another design or a test currently passes.
- Do not accept a chat-only waiver, model-authored rationale, implementation
  progress, or absence of objection as a contract change. A material change to
  the contract requires reconciliation in its canonical source and a new source
  version or accepted snapshot.
- Preserve uncertainty. If the available evidence cannot establish alignment,
  return `INDETERMINATE` rather than assuming compliance.

## 1. Verify revision and source identity

Before comparing semantics, require all supplied evidence to refer to the same
repository, branch, pinned base, and current product state.

Confirm:

- the source identity/version or digest equals the packet originally handed to
  implementation;
- the working-tree fingerprint or commit identity matches the diff being
  compared;
- the verification evidence describes that same product state;
- the independent review is bound to that same state.

A later product edit invalidates the reconciliation. A later source change
invalidates the accepted contract. Return `REQUIRED_ORCHESTRATOR_CONTEXT` for a
state-evidence mismatch and let the orchestrator re-establish the correct stage.

## 2. Build the minimal contract ledger

Extract only material claims that constrain implementation:

- intended observable outcome;
- each acceptance criterion;
- explicit constraints and quality attributes;
- explicit non-goals and excluded cleanup;
- caller-visible, persisted, wire, schema, security, compatibility, migration,
  rollout, or operational contracts when present;
- invariants that must remain true;
- explicitly accepted dependencies or scope boundaries.

Assign stable report-local identifiers `C1`, `C2`, ... for this reconciliation
receipt. Preserve source wording closely enough that another reviewer can trace
what was compared. Do not add a contract claim because the code, tests, or review
suggest that it would be sensible.

## 3. Compare contract to implementation in both directions

For each material contract claim, inspect the actual diff, unchanged context when
needed, verification evidence, and current review evidence. Classify it as one
of:

- `aligned` — implementation evidence supports the claim and no material
  contradiction is observed;
- `missing` — required behaviour or contract is absent;
- `contradicted` — observed implementation behaviour conflicts with the claim;
- `constraint-regression` — a constraint, non-goal, invariant, or compatibility
  boundary is weakened or violated;
- `unverified` — evidence is insufficient to establish whether the claim holds.

Then run the reverse comparison from implementation to contract. Identify
material implementation effects that no accepted claim requires. Classify these
as `extra-scope` when they expand behaviour, contracts, dependencies, cleanup,
architecture, data, rollout, or operational responsibility beyond what was
accepted.

Do not classify routine implementation detail as `extra-scope` merely because it
was not named. The test is whether the change creates a material outcome,
responsibility, contract, risk, or maintenance burden outside the accepted
contract.

## 4. Detect contract invalidation separately from implementation drift

Sometimes new repository, platform, schema, operational, or authoritative
evidence shows that the accepted contract itself is materially wrong,
incomplete, internally inconsistent, or impossible to satisfy safely.

Return `CONTRACT_INVALIDATED` only when concrete evidence establishes that at
least one load-bearing contract claim must change before a coherent
implementation can proceed. Record:

- the exact contract claim;
- the contradicting or newly discovered evidence and stable locator;
- why fixing only the implementation cannot satisfy the accepted contract;
- which acceptance criteria, constraints, invariants, or downstream slices are
  affected;
- the smallest canonical-source decision or clarification required.

Do not use `CONTRACT_INVALIDATED` for an implementation preference, difficult
engineering work, a reviewer's suggested design, missing verification that could
be added without changing intent, or an ordinary implementation defect.

This module never edits the contract. The orchestrator must stop. A later run may
continue only from a new canonical source version or explicitly accepted snapshot
that resolves the invalidated claim.

## 5. Produce explicit contract differences

For every non-aligned implementation difference, create a `CR#` record containing:

- `contract_claim` — related `C#`, or `none` for `extra-scope`;
- `classification` — `missing`, `contradicted`, `constraint-regression`,
  `extra-scope`, or `unverified`;
- `observed_implementation` — concise behaviour-first description;
- `evidence` — exact diff, symbol, file, check, or review locator;
- `impact` — what accepted outcome, boundary, or proof is affected;
- `required_resolution` — smallest safe next action;
- `verification` — evidence that would demonstrate closure;
- `status` — always `open` in this module's result.

Use these resolution rules:

- `missing`, `contradicted`, `constraint-regression`, or `extra-scope` -> fix the
  implementation within the existing accepted contract, then independently
  review the changed state and reconcile again;
- `unverified` -> obtain stronger evidence or return `INDETERMINATE`; never call
  absence of proof alignment;
- evidence that the contract itself must change -> use `CONTRACT_INVALIDATED`,
  not an implementation-drift record.

There is deliberately no local "acknowledge and continue" disposition. If a
material deviation is intentional, change the canonical contract through the
appropriate accountable workflow and restart from the new source version. This
prevents an exception ledger from becoming a second source of truth.

## 6. Return the reconciliation receipt

Return exactly one of:

- `ALIGNED` — no unresolved material difference exists and every load-bearing
  claim has sufficient alignment evidence;
- `IMPLEMENTATION_DRIFT` — one or more implementation differences require
  remediation within the existing contract;
- `CONTRACT_INVALIDATED` — evidence requires the accepted contract itself to be
  reconciled before implementation can continue;
- `INDETERMINATE` — alignment cannot be established from available evidence;
- `REQUIRED_ORCHESTRATOR_CONTEXT` — invocation or state identity is invalid.

Always include a compact `CONTRACT_RECONCILIATION_RECEIPT` with:

- canonical source identity and captured version or digest;
- repository, branch, base revision, and reconciled state identity;
- independent review state identity;
- the material `C#` contract ledger;
- each `CR#` difference and evidence, including `open` status;
- overall result and limitations.

For `ALIGNED`, the receipt must explicitly say `unresolved_differences: 0`.
Do not claim the implementation is correct, safe, approved, or ready to merge;
this stage establishes contract alignment only. The orchestrator still owns the
full project gate, publication, and human responsibility boundaries.