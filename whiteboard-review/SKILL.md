---
name: whiteboard-review
description: >
  Use when the user explicitly asks for a Whiteboard explanation or review of a
  PR, branch, commit, or working-tree change. Create a concise, source-pinned
  account of what changed and how it works. Do not use for generic code review
  or to issue merge, release, or deployment approval.
---

# Explain a Change in Whiteboard

Use Whiteboard to make a code change easier to understand and inspect. This
skill produces an explanation tied to source revisions; it does not establish
correctness or replace a technical review.

- Before authoring, check `session_capabilities`, read
  `session_get_instructions({topic:"authoring"})`, and follow the returned
  workflow. This includes its required file-lenses subagent instruction.
- Pin the review to the PR, commits, or worktree the user identifies. For
  uncommitted work alone, follow the authoring instructions for the `HEAD`
  base. Read the diff and confirm it contains the intended changes before
  writing. Correct a wrong target before proceeding.
- Write incrementally. Explain what changed and why, then add the requirements,
  design, and implementation detail that the change warrants. Keep code claims
  linked to verified, repository-relative source ranges. Mark uncertainty;
  don’t invent motivation, test results, or decisions.
- For an existing Whiteboard, read its current content and the changes since it
  was written, then update it and repair stale source references.
- Read the full board back before finishing. Report its state accurately;
  don’t present the board as a correctness verdict or approval to merge,
  release, or deploy.
