# Conditional Design Assurance for Critical Plans

Use this reference only from `plan` when a **Critical architecture handoff** is being prepared and the design or handoff crosses consequential boundaries. The owner remains `plan`; this is not a new public workflow, document approval phase, code review, or PR verdict.

## Applicability and stop conditions

Run a bounded design-assurance pass when the candidate would commit an implementer to a costly-to-reverse architecture choice, a materially novel responsibility/interface boundary, or a cross-system migration or rollout design whose hidden assumptions could change implementation. The plan's existing challenge pass, responsibility/interface map, cross-slice consistency pass, and `D#` gates still apply.

- **Do not run** on Focused or routine Standard work, or merely because an available harness can spawn agents. An already-settled design with no material handoff risk does not need an extra review.
- For a Critical investigation-only or Blocked handoff, challenge the problem framing or the decision/evidence gaps *only if useful*; do not simulate an implementation-readiness review of an approach that has not been accepted.
- Do not start if adequate read-only access, confidentiality boundaries, or a safe fresh-context reviewer are unavailable. Record `NOT_RUN` and the reason. A same-context self-check may support the existing quality gate, but is **not** an independent review.
- Limit the exercise to one pass and at most three focused fresh reviewers. Do not recursively fan out, retry to obtain a favourable result, or add approval checkpoints merely because this protocol ran.

## Prepare one grounded, immutable review packet

After the candidate plan is assembled, identify its exact artifact/revision or stable snapshot. Give each reviewer only the minimal self-contained packet needed for its task:

1. The candidate's objective, requirements and non-goals (retaining canonical IDs), current-state evidence with locators, proposed design and options, relevant `D#` gates, responsibility/interface map, and applicable slices and verification.
2. Read-only access to the **authoritative source materials** actually needed to corroborate a claim: repository code, tests, contracts, policy, ADRs and cited decisions with scope/freshness recorded.
3. The assigned question and the boundary of the reviewer's authority. Identify unresolved `Q#` items as unresolved, not as permissions to design by inference.

Start reviewers in genuinely fresh contexts. **Do not** forward prior chat, the author's hidden reasoning, the author's defence of a preferred solution, or other reviewers' findings. A fresh reviewer is conversation-isolated, **not** evidence-starved: it may follow the packet's source links and inspect relevant code. Keep contexts and inputs comparable across reviewer roles, and disclose source or tool-access limitations.

## Select the smallest useful perspectives

**Cold reader — default for an eligible, implementable architecture handoff.** Ask a fresh engineer to paraphrase, *without suggesting fixes first*:

- what changes and why, and what is explicitly not changing;
- the current system and relevant authoritative boundaries as supported by sources;
- proposed responsibility/state ownership, important interface and failure semantics;
- what the first dependent slices must preserve, and which `D#` choices remain human-owned.

Compare that reconstruction with the accepted requirements and candidate, not with what the author intended to write. A different interpretation of a material requirement or interface is a **handoff ambiguity** even if every term is defined. Do not penalize the reader for missing information that is genuinely unavailable to the implementer.

**Skeptical architect — add only for consequential architecture alternatives or overdesign risk.** Challenge problem/solution alignment, existing mechanisms and reuse, complexity, coupling, security or trust boundaries, failure and rollback, cost and capacity claims, and whether the stated constraints actually justify the choice. Search current sources before claiming an existing alternative. Do not silently select among legitimate `D#` options.

**Implementation reader — add only when cross-slice or cross-service contracts are material and the design is sufficiently selected.** Reconstruct a brief execution outline, including required inputs, outputs, interface/schema semantics, ordering, verification oracles, and replanning triggers. Flag any *consequential* decision that would otherwise be delegated to the implementer. Do not demand invented file names, exact code or a step-by-step ritual when the behavioural contract is sufficient.

Use one cold reader for most eligible plans. Add another role only if its distinct question could materially change a design or handoff decision; reviewer count is not a quality metric.

## Verify and reconcile findings

The coordinating planner must validate every material claim independently where practical. For each finding:

- cite the plan section and underlying source or report the missing evidence;
- attempt to falsify the criticism against current code, tests, governing decisions and counterexamples;
- classify it as **supported gap**, **unverified risk**, **invalidated**, or **human-owned decision**;
- distinguish misunderstanding caused by missing design information from an incorrect or source-limited reviewer;
- keep the review packet/revision and reviewer provenance (fresh context confirmed, role, harness/model when exposed, shared evidence and limitations). Correlated agents remain correlated even with separate contexts.

Correct a supported factual or clarity gap in the candidate plan *without* altering canonical requirements or accepted decisions. If a finding exposes a consequential unresolved choice, create or preserve an evidence-backed `D#` gate and block **only** its dependent slices; return investigation steps instead of inventing the answer. Do not let the planner, a reviewer, or a positive review approve the architecture. Where a correction materially changes the candidate, recheck affected contracts and the final handoff fidelity; rerun an isolated reader only when there is a specific unresolved comprehension risk and budget permits.

## Report with the plan

Include a compact assurance receipt, without separate artifacts unless the user or repository expects them:

- **Execution:** `COMPLETE`, `NOT_RUN`, or `NOT_APPLICABLE`; reason when not complete.
- **Candidate and scope:** stable plan identity; which material boundaries and reviewer lenses were examined.
- **Independence:** fresh context versus same-context fallback; reviewer provenance and shared limitations.
- **Reconstruction:** cold-reader's summary and any material difference from accepted intent (when run).
- **Findings and outcome:** supported gaps and corrections, unverified risks, open `Q#`/`D#` gates, and any unexamined boundaries.

An assurance receipt is **evidence about communication and design risk**, not an approval or executable proof. `COMPLETE` does not imply `Ready`, and `NOT_RUN` alone does not automatically imply `Blocked`; retain the existing plan-status rules. Do not mislabel mechanical lint, a same-context critique, or the planner's own confidence as an independent Goldfish-style review.

## Evaluation guidance

Compare current and candidate `plan` revisions under matched prompts, fixtures, model, harness, tools and verifier. Include a consequential design with a seeded material ambiguity, an implementation-only handoff ambiguity, a routine near-miss that must skip the protocol, and a no-subagent environment that must disclose `NOT_RUN`. Grade verified material findings, unsupported complaints, decision-gate correctness, unintended ceremony, and incremental cost/latency when measurable. Static validation is not evidence of behavioural improvement.

**Reference:** [Google's Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) motivated the fresh-context comprehension and design critique approach; this protocol retains the repository's evidence, independence, authority and proportionality constraints.
