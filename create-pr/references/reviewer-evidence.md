# Reviewer-facing evidence and learning handoff

Read this reference when `create-pr` needs to present a non-obvious mechanism,
pair pre/post-change evidence, classify reversibility, reason about runtime
evidence beyond tests, or expose an optional learning handoff.

## Reviewer comprehension views

Use the smallest evidence-backed representation that materially reduces the
reviewer's reconstruction work:

- pseudocode for a logic or algorithm change;
- a call tree for runtime control flow;
- a shallow file or component tree for ownership/structure;
- a diff-shaped sketch when the important fact is what changed in an existing
  shape;
- a small Mermaid flow when interaction or ordering is the point.

Include only verified calls, files, states, boundaries, and ordering relevant to
the current review. Place the view next to the prose or evidence it clarifies.
Omit it for simple changes where prose is clearer. It is a rendering aid, not a
standalone visual artefact, and must not hide risk, uncertainty, or limitations.

## Before/after evidence

Prefer a compact before/after pairing when both observations:

- measure the same behaviour or contract;
- have trustworthy source or revision identity;
- are comparable without reinterpretation; and
- materially strengthen the reviewer-visible claim.

Never reconstruct a pre-change observation from the fixed implementation or call
an inferred baseline observed evidence. If either side is missing or incomparable,
state the limitation instead.

## Reversibility

Classify the committed effect from the mechanism that can actually restore it:

- `two-way` — an established rollback, revert, compatibility, or state-recovery
  path can restore the effect cheaply and without material residue;
- `constrained` — reversal exists but requires sequencing, migration, operator
  action, compatibility cost, or leaves material residual effects;
- `one-way` — the observed effect cannot be reliably restored with the available
  mechanism.

Record the restore/rollback mechanism, required preconditions, and irreversible or
residual effects. A Git revert or passing test suite alone does not establish
reversibility.

## Tests and runtime evidence

Treat tests as bounded oracles for what they actually exercise, not as proof that a
change is mergeable or production-safe. When a material claim depends on runtime
or operational behaviour outside selected checks, consume runtime/operational
evidence only when its provenance establishes the relevant running target:

- exact source revision or immutable build identity;
- target environment plus deployed service/version or equivalent authoritative
  target identity;
- evidence that the running target corresponds to that revision/build;
- material runtime configuration and dependency state when they can change the
  observed property; and
- a bounded observation or test window.

If those bindings are absent, stale, mismatched, or materially incomplete, mark
the property unverified rather than transplanting the observation. The same commit
running in a different deployment, configuration, dependency state, or observation
window is not automatically equivalent evidence.

Never invent production evidence or require deployment merely to create a PR.
Runtime evidence complements tests; it does not convert technical posture into a
human merge verdict.

## Optional learning handoff

PR creation is not itself a retro. When creation genuinely ends the active working
session and that session contains material reusable friction, correction,
discovery, or an effective pattern, an invoking workflow or operator may hand the
session to `wrap-up` when available.

Do not run or require reflective capture solely because a PR exists. Preserve
branch, exact head revision, and PR identity so later `session-lessons` analysis
can correlate the session with revision-bound PR lifecycle evidence and count the
same underlying event once. Merge is an outcome, not proof that the lesson or
review finding was valid.
