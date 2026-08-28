# Blind Reconstruction Evaluation Suite

Use this suite to decide whether de-anchored observed-change reconstruction adds
material signal beyond the existing contract-aware bidirectional reconciliation.
Follow the repository's `skill-creator/references/evaluation.md` guidance: run
matched baseline/candidate pairs in fresh contexts, hold model/harness/tools and
fixtures constant, and grade behaviour from artifacts rather than prose.

## Conditions

- **Baseline:** the `contract-reconciliation` skill from `main` before blind
  reconstruction was added.
- **Candidate:** the revised skill with the fresh `OBSERVED_CHANGE_CONTRACT`
  sub-pass.

For each case, the outer reconciliation worker receives the same canonical
contract and implementation evidence in both conditions. In the candidate
condition, verify from the worker trace or captured handoff that the blind worker
receives implementation-side evidence only and is not exposed to the canonical
contract, acceptance criteria, implementer narrative, verification-to-requirement
mapping, technical review, or expected result.

Repeat matched pairs when model variance could change the conclusion. Do not
claim improvement merely because the candidate emits an additional artifact.
Measure whether it changes supported drift detection, false positives, evidence
quality, or cost.

## Global hard failures

Fail a candidate run if it:

- leaks any externally supplied intent evidence into the blind worker;
- simulates blindness in the already contract-aware context when a fresh worker
  is unavailable;
- treats reconstruction output as authoritative requirements or as proof of
  drift without re-inspecting implementation evidence;
- lets the blind worker classify `aligned`, `missing`, `extra-scope`, or contract
  invalidation despite not having the contract;
- accepts an unsupported reconstruction claim because it sounds plausible;
- suppresses a direct contract difference because the blind worker omitted it;
- turns harmless implementation detail into scope drift merely because it was
  absent from the contract;
- blocks reconciliation solely because blind reconstruction is unavailable;
- produces a reconstruction bound to a different implementation revision without
  discarding it;
- mutates repository or external state.

## Cases

| ID | Contract and implementation fixture | What the blind worker should reconstruct | Expected reconciliation behaviour | Incremental question |
| --- | --- | --- | --- | --- |
| `BR1` | Contract: retry only transient outbound failures, maximum three attempts, preserve timeout behaviour, emit retry telemetry. Implementation introduces a generic retry wrapper that retries every exception until success; tests exercise only eventual success. | Observe generic retry responsibility, all-exception handling, lack of an evident attempt bound, and any timeout/telemetry effects that are actually visible. It must not call these contract violations. | Candidate and baseline should both identify contradicted/missing claims. Candidate should use the de-anchored observations to inspect retry breadth/bounds rather than merely echoing the contract. | Does reconstruction improve detection or evidence quality for a coherent implementation that solves a subtly different problem? |
| `BR2` | Contract: add a local validation rule to one command handler; no public API, storage, or dependency change is requested. Implementation also introduces a reusable public endpoint and shared cache to expose the result elsewhere. | Observe the new public surface, shared caching responsibility, dependency/lifecycle effects, and changed callers with evidence. | Reconciliation should classify the material public/cache expansion as `extra-scope` only after independently checking the cited code. | Does the candidate catch accidental architectural responsibility or scope expansion more reliably than direct contract-aware reading? |
| `BR3` | Contract: add a nullable response field to an existing public API while preserving compatibility. Implementation adds one private helper and renames a local variable as part of the change, with no new contract or responsibility. | Observe the public field change and may mention the helper as an implementation detail, but should not inflate the helper/rename into a material effect. | Reconciliation should remain `ALIGNED` when all contract claims are satisfied and must not create a `CR#` for harmless implementation freedom. | Does the additional worker increase false positives or ceremony on ordinary implementation detail? |
| `BR4` | Contract: preserve an existing authorization invariant and add an audit event. The implementation adds the event but silently removes an authorization check. The changed tests were rewritten to match the new behaviour. | Observe the removed/changed authorization path and audit-event addition from code/tests without knowing which behaviour was required. | Direct contract comparison must identify the authorization regression even if reconstruction is incomplete. Candidate must never use blind omission as evidence of alignment. | Does the candidate preserve the contract-aware check for requirements whose significance cannot be inferred from implementation alone? |
| `BR5` | Contract and implementation are aligned, but the harness cannot provide a genuinely fresh isolated worker. | No reconstruction should be fabricated. | Continue normal bidirectional reconciliation, record `blind_reconstruction: unavailable`, and return the same substantive result the baseline would support. | Is the feature additive rather than a new availability dependency? |
| `BR6` | Contract: modify one persistence field without changing rollout semantics. Implementation performs a broader schema migration, dual-write period, backfill job, and feature-flagged cutover that are internally coherent but not requested. | Observe migration phases, dual-write/backfill/cutover responsibilities, new operational controls, and compatibility behaviour without judging them as scope. | Reconciliation should determine whether these are required implementation freedom or material unaccepted rollout/operational scope and create evidence-backed `extra-scope` findings only when warranted. | Does reconstruction help surface coherent implementation-derived design that an anchored reviewer may rationalise as intentional? |
| `BR7` | Contract: change an internal parsing rule. Implementation is aligned. The blind worker incorrectly infers that a nearby unchanged compatibility shim was introduced by the change. | The erroneous claim should be distinguishable as inferred and have weak/no diff evidence. | Reconciler must reject or discard the unsupported observation after inspecting the cited state and must not emit a `CR#`. | Can the outer reconciler falsify reconstruction hallucinations rather than laundering them into findings? |

## Observable checks

For every candidate run record these checks as `passed`, `failed`, or
`not_verifiable`:

1. **Isolation:** blind worker input contains no externally supplied intent or
   post-hoc review evidence.
2. **Revision binding:** reconstruction and reconciliation refer to the same exact
   implementation state.
3. **Observation calibration:** every material reconstructed effect has a tight
   implementation locator and distinguishes observed/inferred/unknown.
4. **Authority boundary:** the canonical contract remains the only source of what
   should have been built.
5. **Independent validation:** a reconstructed claim influences a `CR#` only after
   the outer reconciler independently confirms the implementation evidence.
6. **Bidirectional completeness:** direct contract-to-implementation checks still
   run even when the reconstruction omits a requirement.
7. **False-positive control:** benign implementation freedom does not become
   `extra-scope` solely because the blind worker noticed it.
8. **Fallback:** absence of a fresh worker is recorded as a limitation rather than
   blocking or faking the pass.
9. **Outcome quality:** final `ALIGNED`, `IMPLEMENTATION_DRIFT`,
   `CONTRACT_INVALIDATED`, `INDETERMINATE`, or context-error result is supported
   by the fixture evidence.

## Comparison and stop rule

For each case compare baseline versus candidate on:

- supported material drift findings found/missed;
- unsupported or false-positive findings;
- evidence specificity and falsification quality;
- reconciliation outcome correctness;
- extra worker/tool cost when exposed by the harness.

The candidate earns promotion only if matched evidence shows meaningful uplift on
representative intent-drift cases without unacceptable false-positive or cost
regression. If results are ties across the drift-sensitive cases, prefer the
baseline's simpler workflow and remove or narrow the blind pass. If uplift is
concentrated in high-risk architectural or public-contract changes, use that
evidence to introduce a future applicability gate rather than making broader
claims.