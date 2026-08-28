---
name: contract-reconciliation
description: >-
  Internal implement-agent module for comparing one reviewed implementation
  against the immutable canonical ticket contract before final validation and
  publication. Uses a fresh de-anchored observed-change reconstruction when
  available to challenge contract-aware comparison without making implementation
  evidence authoritative. Use only when the implement agent supplies the accepted
  contract, exact working-tree identity, current diff, verification evidence, and
  an independent review for the same state.
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
commit, push, mutate the tracker, update the accepted contract, or create a pull
request. The `implement` orchestrator owns lifecycle and mutation. Do not invoke
another agent except the single fresh observed-change reconstruction worker
described below; that worker is read-only, non-recursive, and cannot become a
source of requirements.

## Boundaries

- Treat the canonical ticket packet as the contract for this run. Do not let the
  implementation, review prose, tests, comments, reconstruction output, or model
  reasoning invent missing requirements or silently weaken existing ones.
- Treat implementation and verification as evidence about what was built, not as
  authority for what should have been built.
- Treat review findings as independently grounded technical evidence, not as new
  acceptance criteria or permission to redesign the task.
- Treat a blind reconstruction as a de-anchored observation aid only. Its absence,
  disagreement, or inference is never itself a contract difference.
- Compare observable behaviour, contracts, constraints, non-goals, invariants,
  and material scope. Ignore harmless implementation freedom the contract leaves
  open.
- Preserve canonical contract identifiers such as `AC-N` and `NG-N` whenever
  they exist. Do not renumber, paraphrase away, or replace them with report-local
  identifiers merely for convenience.
- Extra unrequested behaviour, cleanup, refactoring, migration, dependency
  expansion, public surface, or operational change is drift when it materially
  expands the accepted scope, even when it appears beneficial.
- Do not infer that a canonical claim is wrong merely because the implementation
  chose another design, a reconstruction suggests another apparent intent, or a
  test currently passes.
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

For each ledger entry include:

- `contract_ref` — preserve the canonical source identifier when present, such as
  `AC-2` or `NG-1`; otherwise assign a report-local `C1`, `C2`, ... identifier;
- `kind` — acceptance criterion, non-goal, constraint, invariant, outcome, or
  another accurate contract category;
- `source_text` — wording close enough to the accepted source that another
  reviewer can trace what was compared.

Canonical `AC-N` and `NG-N` identifiers outrank report-local numbering. Never
assign a `C#` alias merely because a canonical identifier exists. Do not add a
contract claim because the code, tests, review, or blind reconstruction suggest
that it would be sensible.

## 3. Reconstruct the observed change without contract context

When the harness can provide a genuinely fresh isolated worker, dispatch exactly
one read-only observed-change reconstruction before performing the semantic
comparison. The purpose is to obtain a second description of what the
implementation appears to do without priming that description with what the
implementation was supposed to do.

Give the worker only the minimum implementation-side evidence needed to inspect
the change:

- repository root and applicable repository inspection instructions;
- pinned base revision and exact current working-tree or commit identity;
- the complete in-scope diff, or read-only access sufficient to inspect that diff
  and necessary unchanged code;
- tests, schemas, configuration, documentation, and other repository artefacts
  when they are part of or directly illuminate the implemented change.

Deliberately withhold all intent-side and post-hoc interpretation evidence:

- the ticket, plan, specification, acceptance criteria, constraints, and non-goals;
- the implementation handoff and implementer's narrative or reasoning;
- the implementation verification map when it maps checks back to intended
  acceptance criteria;
- the independent technical review and its findings;
- any previous reconciliation result or expected blind-reconstruction outcome.

Do not replace withheld material with a paraphrase, hint, filename, prompt, or
expected answer that leaks the original contract. Repository artefacts that are
part of the changed implementation remain inspectable even when they happen to
state behaviour; the isolation boundary is against externally supplied intent,
not against the codebase itself.

Require the worker to inspect evidence fresh and return one compact
`OBSERVED_CHANGE_CONTRACT` containing:

- `state_identity` — the exact implementation state observed;
- `behavioural_changes` — material runtime or caller-visible changes;
- `external_contracts` — public APIs, events, persisted or wire formats,
  configuration, security, compatibility, or migration effects;
- `data_and_operational_effects` — data lifecycle, deployment, rollout,
  observability, performance, or operational responsibility introduced or
  changed when materially evidenced;
- `architectural_responsibilities` — material new ownership, dependency,
  coordination, caching, retry, concurrency, or lifecycle responsibilities;
- `apparent_invariants_and_constraints` — behaviours that the implementation
  appears deliberately to preserve or impose;
- `other_material_effects` — consequential implementation effects not captured
  above;
- `uncertain_inferences` — plausible intent or effect that cannot be established
  from implementation evidence alone;
- `evidence` — tight file, symbol, diff, test, schema, or configuration locators
  for every material observation.

The worker must distinguish `observed`, `inferred`, and `unknown`; it must not
invent motivations, requirements, acceptance criteria, or product rationale.
It must not classify anything as `extra-scope`, `missing`, `aligned`, or
`contract-invalidated`, because those judgments require the withheld contract.
It must not delegate further.

Bind the reconstruction to the same exact product-state identity as the
reconciliation. If the worker inspected a stale or different state, or returns
claims without inspectable evidence, discard the affected reconstruction output
rather than repairing it from contract-aware context.

If no genuinely fresh worker is available, do not simulate blindness in this
already contract-aware context. Record `blind_reconstruction: unavailable` and
continue with the existing direct bidirectional comparison. The reconstruction
is an additional de-anchoring signal, not a prerequisite for contract
reconciliation.

## 4. Compare contract to implementation in both directions

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

When a valid `OBSERVED_CHANGE_CONTRACT` is available, use its evidence-backed
observations as a de-anchored checklist for the reverse comparison. For each
material observation, independently inspect the cited implementation evidence
and ask whether the canonical contract requires, permits as harmless
implementation freedom, contradicts, or says nothing material about that effect.
Do not promote an observation into a `CR#` merely because the blind worker
mentioned it, and do not suppress a direct contract difference because the blind
worker omitted it. A disagreement between the reconstruction and the
contract-aware reading is a reason to inspect the underlying code more closely,
not a result by itself.

Do not classify routine implementation detail as `extra-scope` merely because it
was not named. The test is whether the change creates a material outcome,
responsibility, contract, risk, or maintenance burden outside the accepted
contract.

## 5. Detect contract invalidation separately from implementation drift

Sometimes new repository, platform, schema, operational, or authoritative
evidence shows that the accepted contract itself is materially wrong,
incomplete, internally inconsistent, or impossible to satisfy safely.

Return `CONTRACT_INVALIDATED` only when concrete evidence establishes that at
least one load-bearing contract claim must change before a coherent
implementation can proceed. Record:

- the exact canonical `contract_ref` when one exists, plus the accepted claim;
- the contradicting or newly discovered evidence and stable locator;
- why fixing only the implementation cannot satisfy the accepted contract;
- which acceptance criteria, constraints, invariants, or downstream slices are
  affected;
- the smallest canonical-source decision or clarification required.

Do not use `CONTRACT_INVALIDATED` for an implementation preference, difficult
engineering work, a reconstruction's inferred intent, a reviewer's suggested
design, missing verification that could be added without changing intent, or an
ordinary implementation defect.

This module never edits the contract. The orchestrator must stop. A later run may
continue only from a new canonical source version or explicitly accepted snapshot
that resolves the invalidated claim.

## 6. Produce explicit contract differences

For every non-aligned implementation difference, create a `CR#` record containing:

- `contract_refs` — one or more related canonical `AC-N` / `NG-N` identifiers or
  report-local `C#` references; use `[]` only for genuinely `extra-scope`
  behaviour with no accepted contract claim;
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

## 7. Return the reconciliation receipt

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
- the material contract ledger with preserved canonical `contract_ref` values;
- `blind_reconstruction` — `used`, `unavailable`, or `discarded`, plus the exact
  observed state identity and a compact `OBSERVED_CHANGE_CONTRACT` when used;
- any reconstruction limitations, discarded unsupported observations, or known
  context-isolation limitations;
- each `CR#` difference, its `contract_refs`, and evidence, including `open`
  status;
- overall result and limitations.

For `ALIGNED`, the receipt must explicitly say `unresolved_differences: 0`.
Do not claim the implementation is correct, safe, approved, or ready to merge;
this stage establishes contract alignment only. The orchestrator still owns the
full project gate, publication, and human responsibility boundaries.

## Evaluation

When changing the blind-reconstruction behaviour, use
[references/evaluation-suite.md](references/evaluation-suite.md) with the
repository's `skill-creator` evaluation guidance. Require matched baseline versus
candidate evidence before claiming that the additional worker improves drift
detection enough to justify its cost.