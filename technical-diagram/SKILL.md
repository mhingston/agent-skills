---
name: technical-diagram
description: Create polished standalone technical diagrams and explainer graphics when the visual artifact itself is the requested deliverable. Use for architecture overviews, request/data flows, failure and fallback paths, distributed-system explainers, state/lifecycle diagrams, before/after comparisons, or prompts such as "draw how this works", "visualise this architecture", "turn this into an infographic", or "make a ByteByteGo-style technical diagram". Prefer `eli5` when the primary goal is a quick prose orientation with only a supporting visual, and `codebase-walkthrough` when the primary goal is investigating how an existing codebase works.
compatibility: Requires filesystem or artifact support to create a self-contained HTML/SVG diagram. Optional PNG export requires a browser or screenshot-capable renderer.
---

# Technical Diagram

Create presentation-ready technical visuals whose structure communicates the
mechanism before the reader studies the labels. The visual is the primary output,
not decoration attached to a prose answer.

Use an original bold editorial visual language rather than reproducing a third
party's branded artwork. A supplied reference image may guide palette, line
weight, spacing, density, typography class, and composition, but do not copy
logos, distinctive branded illustrations, or a reference layout mechanically.

## Use when

Use this skill when the requested outcome is primarily a diagram, infographic,
architecture visual, or technical explainer graphic, including:

- request, event, data, or control flow;
- distributed-system mechanics such as caches, queues, replication, or routing;
- error, retry, degradation, and fallback paths;
- component or service architecture at an explanatory level;
- state/lifecycle transitions;
- before/after or option comparisons;
- a slide, README, article, or design-review visual;
- restyling an existing technical diagram while preserving its meaning.

## Avoid when

Do not use this skill merely because another task could contain a diagram.

- Use `eli5` when the user wants a quick plain-language orientation and the
  visual is secondary.
- Use `codebase-walkthrough` when the primary work is discovering how an existing
  subsystem behaves from repository evidence. A walkthrough may later hand its
  established model to this skill for rendering.
- Use `agent-workflow-design`, `plan`, or another owning design capability when
  the unresolved job is choosing the architecture rather than drawing an already
  supported one.
- Use a table or prose when relationships are trivial and a visual would add
  ceremony without comprehension.

## Output contract

Create one self-contained HTML file containing inline CSS and SVG. Start from
[assets/diagram-template.html](assets/diagram-template.html) unless an existing
user artifact is a better base.

The artifact must:

- render without network resources;
- use a fixed SVG `viewBox` so it scales cleanly;
- remain legible at slide or laptop width;
- contain accessible text and a concise `aria-label` or `<title>/<desc>`;
- keep repository/user-derived text escaped rather than executable;
- avoid analytics, remote fonts, external images, `fetch`, or browser persistence.

If the environment can reliably export the HTML/SVG to PNG, provide the PNG as a
convenience while preserving the editable HTML/SVG source. Do not return raw
Mermaid, raw SVG source, or HTML code in chat and call that the finished visual.

If artifact creation is unavailable, explain that limitation and provide a
compact diagram specification rather than pretending an unrendered code block is
the requested graphic.

## Fast path

1. **State the one message.** Write one sentence describing what the reader should
   understand after looking for five seconds.
2. **Choose one pattern.** Read
   [references/diagram-patterns.md](references/diagram-patterns.md) only as needed
   and select the smallest pattern that expresses the mechanism.
3. **Reduce the cast.** Keep roughly 4–8 major visual objects. Collapse internals
   that do not change the explanation.
4. **Write labels first.** Prefer short noun labels and short verb-led callouts;
   remove explanatory prose that belongs outside the visual.
5. **Lay out the happy path.** Establish one dominant left-to-right or top-to-bottom
   reading direction before adding exceptions.
6. **Add secondary behaviour.** Add failure, fallback, replication, or alternate
   paths only when they materially change the mental model.
7. **Render using the visual language.** Read
   [references/visual-language.md](references/visual-language.md) when the default
   style or a supplied visual reference matters.
8. **Inspect at two scales.** Check thumbnail readability first, then inspect text,
   arrows, clipping, and semantics at full size.

## Diagram grammar

Prefer a simple explanatory grammar over formal notation unless the user asks for
UML, C4, sequence diagrams, or another established notation.

Use:

- **objects** for actors, services, stores, queues, models, tools, or outcomes;
- **solid arrows** for the primary flow;
- **dashed arrows** for secondary, failure, asynchronous, or conditional flow;
- **containers** for real grouping boundaries such as clusters or trust zones;
- **callouts** for a short mechanism, invariant, or consequence;
- **numbered markers** only when sequence order would otherwise be ambiguous;
- **bottom cards** sparingly for outcomes, benefits, or constraints that should
  not interrupt the main path.

Do not mix semantic meanings for the same line style or colour in one graphic.
Do not draw a boundary merely to fill space.

## Complexity budget

Default to:

- one primary message;
- one dominant reading direction;
- 4–8 major objects;
- at most two secondary lanes or grouped regions;
- at most three accent colours plus neutrals;
- labels normally no longer than six words;
- explanatory callouts normally one short line;
- no connector crossings unless there is no clearer decomposition.

If the source material needs more than about eight equally important objects,
more than two distinct stories, or repeated crossing arrows, split the output
into multiple diagrams or choose a higher-level abstraction. Do not shrink text
to make an overloaded canvas technically fit.

## Reference-image adaptation

When the user supplies a visual reference, extract only reusable design
properties:

- aspect ratio and framing;
- background warmth or neutrality;
- palette roles rather than exact brand ownership;
- stroke weight and corner treatment;
- typography category and hierarchy;
- arrow and connector treatment;
- whitespace and object density;
- icon abstraction level;
- grouping and callout conventions.

Preserve the target diagram's own semantics. Do not force the reference's exact
object count, layout, wording, logo, or iconography onto unrelated content.

When no reference is supplied, use the `bold-explainer` defaults in
[references/visual-language.md](references/visual-language.md).

## Content fidelity

A polished wrong diagram is a failed diagram.

- Preserve the difference between request flow, data ownership, replication,
  sharding, caching, fan-out, retry, and fallback.
- Do not imply causality merely because two components are adjacent.
- Do not invent service boundaries, failure behaviour, ordering, or persistence.
- If the source evidence is incomplete, omit the unsupported edge or visibly mark
  the uncertainty instead of smoothing it into the picture.
- Keep visual labels consistent with the terminology used by the source or user.

For architecture derived from a repository, ticket, or design source, treat that
source as evidence rather than visual inspiration. The diagram must not become a
new source of truth.

## Visual hierarchy

The reader should discover information in this order:

1. title and thesis;
2. primary path;
3. grouped mechanism or important boundary;
4. alternate/failure path;
5. benefits, constraints, or implementation detail.

If decorative elements compete with the primary path, remove them.

## Validation

Before delivery, verify:

1. **Five-second test** — the main mechanism is apparent without reading every
   label.
2. **Path test** — the eye has one obvious starting point and primary direction.
3. **Thumbnail test** — title, major objects, and hierarchy still work when the
   artifact is reduced substantially.
4. **Label test** — no clipped text, tiny text, accidental wrapping, or paragraphs
   inside nodes.
5. **Connector test** — arrow direction and line style are unambiguous; crossings
   are absent or justified.
6. **Semantic test** — every edge and grouping says something true and necessary.
7. **Style test** — palette, strokes, radii, typography, icons, and spacing are
   internally consistent.
8. **Accessibility test** — sufficient contrast and a usable textual description
   exist.
9. **Artifact test** — the file works offline and contains no external resource or
   unsafe interpolation.

## Delivery

Return the rendered artifact first, followed by at most a few short notes about
scope, assumptions, or alternate versions when those materially help. Do not bury
the requested visual under a long explanation of how it was made.

Read [references/evaluation.md](references/evaluation.md) when changing the
trigger, sibling boundaries, visual behaviour, complexity budget, or output
contract.
