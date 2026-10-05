---
name: whiteboard-plan
description: >
  Use when the user explicitly asks to plan or explore a software change in
  Whiteboard before implementation. Use the scratchpad for visual discussion
  and the existing plan skill for repository evidence and an executable plan.
  Do not use for generic planning or post-change reviews.
---

# Plan with Whiteboard

Use Whiteboard as a visual space for early design discussion. This skill covers
the Whiteboard workflow; the existing `plan` skill owns evidence gathering,
design challenge, and any executable implementation plan.

- Before writing, check `session_capabilities` and read
  `session_get_instructions({topic:"scratchpad"})`. Follow those instructions.
  Draw only when the Desktop and scratchpad are available. Otherwise explain
  that and continue in the normal planning workflow.
- Use the fixed `scratchpad` document. Do not create, rename, delete, dismiss,
  or share it.
- For claims about existing code, register the repository, resolve source pins,
  and read the cited code at those pins. Keep observed behavior distinct from
  proposed design and open decisions.
- Keep the board compact: the smallest useful explanation, flow, or comparison.
  Treat it as a discussion log, not the canonical plan or a record of approval.
- End the Whiteboard session as its instructions require. Put agreed decisions
  in the project’s usual decision record only when that write is separately
  authorized.
