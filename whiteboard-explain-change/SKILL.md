---
name: whiteboard-explain-change
description: >
  Use when the user explicitly asks for a Whiteboard explanation of an exact PR,
  branch, commit, commit range, or working-tree change. Create a concise,
  revision-pinned account of what changed and how it works. Do not use for
  generic technical review, merge-readiness assessment, approval, or prospective
  design exploration.
compatibility: Requires dev.fast Whiteboard authoring APIs plus read access to the relevant repository/change and Git. PR targets may additionally require the runtime's supported GitHub/gh access.
---

# Explain a Change in Whiteboard

Use Whiteboard to make one implemented code change easier to understand and
inspect. The output is a source-linked explanation of the change; it is not a
technical correctness assessment and does not replace `review` or a PR judgement
workflow.

Whiteboard's returned session instructions are authoritative for authoring order,
file lenses, components, source anchors, retargeting, and lifecycle details. This
skill adds routing and responsibility boundaries rather than maintaining a
second copy of Whiteboard's protocol.

- Before authoring, check `session_capabilities`, read
  `session_get_instructions({topic:"authoring"})`, and follow the returned
  workflow, including its required file-lenses subagent instruction.
- Resolve mutable targets to the immutable source identity returned by
  Whiteboard. For PRs and branches, record and use exact base/head commit IDs;
  never treat a branch name or PR number as sufficient revision identity.
- For uncommitted work, use the authoring workflow's worktree target with
  `base: "HEAD"`, record the exact HEAD commit, and inspect `git diff HEAD`
  plus `git status` as instructed. Treat the Whiteboard worktree generation,
  base commit, and observed diff as the explained state; do not imply that HEAD
  alone identifies uncommitted contents.
- Read the resolved diff before writing and confirm it contains the intended
  change. If the target is wrong or moved, correct or retarget it before making
  source claims.
- Write incrementally. Explain what changed and why when evidence supports the
  rationale, then add only the requirements, design, and implementation detail
  warranted by the change. Link code claims to verified repository-relative
  source ranges. Mark uncertainty; do not invent motivation, test results, or
  decisions.
- When historical rationale materially matters and is not present in the change
  evidence, use Whiteboard trace archaeology only when available and according to
  its served instructions; otherwise leave the rationale unknown.
- For an existing Whiteboard, read its current content, move it to the new exact
  target as instructed, inspect the intervening changes, and repair stale source
  references.
- Read the full board back before finishing and correct contradictions or
  unsupported claims. Report the board's state accurately; never present it as a
  correctness verdict or approval to merge, release, or deploy.
- If the Whiteboard authoring runtime is unavailable, state that the requested
  board cannot be authored. Do not fabricate one. A concise chat explanation is
  acceptable only when it still serves the user's immediate intent.

Read [references/evaluation-suite.md](references/evaluation-suite.md) when
changing this skill's trigger, revision binding, or authority boundaries.
