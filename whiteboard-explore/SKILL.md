---
name: whiteboard-explore
description: >
  Use when the user explicitly asks to explore or think through a prospective
  software change in Whiteboard before implementation. Own the interactive
  scratchpad exploration and keep observed code, proposed design, and open
  decisions distinct. Do not use for generic implementation planning, an exact
  implemented-change explanation, or technical review.
compatibility: Requires dev.fast Whiteboard session APIs for Whiteboard output; drawing requires Whiteboard Desktop with the scratchpad enabled. Repository-backed code claims require read access to the relevant checkout and Git.
---

# Explore a Change in Whiteboard

Use Whiteboard as an interactive visual space for early software-design
discussion. The output is the exploration itself: the smallest useful visual
model of the current system, proposed change, alternatives, or open decisions.

This skill is self-contained. It may hand evidence and decisions to a separately
installed planning workflow, but it does not require another skill and does not
produce an executable implementation plan.

Whiteboard's returned session instructions are authoritative for tool sequencing,
component shapes, source-link mechanics, and lifecycle details. This skill owns
only the routing, evidence, and responsibility boundaries around that runtime
workflow.

- Before drawing, call `session_capabilities` and read
  `session_get_instructions({topic:"scratchpad"})`. Follow the returned
  instructions. Draw only when Desktop and the scratchpad are available.
- If Whiteboard drawing is unavailable, say why once and continue only with the
  same bounded exploration in chat. Do not pretend a board was created and do
  not delegate to another skill merely to compensate for the missing runtime.
- Use the fixed `scratchpad` document. Do not create, rename, delete, dismiss,
  or share it.
- For claims about existing code, register each repository, resolve immutable
  source pins, and read the cited code at those pins before linking it. Keep
  observed behaviour separate from proposed design, assumptions, and open
  decisions.
- Prefer one compact flow, sequence, comparison, code peek, or other smallest
  useful view over a document-shaped board. Treat the scratchpad as a discussion
  log, not the canonical implementation plan, decision record, or approval.
- When historical rationale materially affects the exploration and Whiteboard
  exposes trace archaeology, use its served instructions to recover evidence.
  Otherwise mark the rationale unknown rather than inventing it.
- End the Whiteboard activity exactly as the served scratchpad instructions
  require. Persist agreed decisions elsewhere only when that write is separately
  authorised.

If the user subsequently wants an executable implementation plan, hand the
established evidence, constraints, alternatives, and open decisions to whatever
planning capability is available rather than expanding this skill into planning.

Read [references/evaluation-suite.md](references/evaluation-suite.md) when
changing this skill's trigger, fallback, or evidence boundaries.
