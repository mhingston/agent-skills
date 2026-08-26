# ELI5 story graphics

Read this only when the verbal explanation has a real sequence, before/after, request flow, state transition, or one thing acting on another. The graphic is a secondary aid; the verbal explainer must already stand on its own.

## Deliverable

Create one self-contained HTML file and attach/render it as an artifact. Start from [../assets/story-graphic-template.html](../assets/story-graphic-template.html).

Never emit a Mermaid block, raw SVG, HTML source, or another code-fenced diagram in chat and call it the visual. If rendered-file support is unavailable, skip the visual instead.

## Story structure

Build a **vertical comic strip**, not one clever diagram.

- Use a stack of dead-simple scenes read top to bottom.
- Give each scene exactly one meaningful action. If a scene contains two actions, split it.
- Keep each scene to roughly 3–4 recognizable elements.
- Make every panel title a plain subject-verb-object sentence.
- Ensure reading the titles alone, top to bottom, tells the entire mechanism.
- Put one short caption under each scene for the important aside, constraint, or "why this matters" truth.
- Never make the reader trace a curve, hunt for numbered nodes, or decode a dense topology.

A good title sequence looks like:

1. "Everyone shares one copy of the code."
2. "You take your own copy."
3. "You edit it."
4. "You merge — the two become one."

The pictures support that story; they do not carry hidden logic the titles fail to explain.

## Cast

Use a small, consistent drawn cast and reuse the same visual symbols across panels. Good recurring characters include:

- a person;
- a document/file;
- a robot;
- a browser/window;
- a server or service.

Prefer reusable inline SVG `<symbol>` definitions so the same character remains recognizable from scene to scene. Do not replace the cast with changing abstract rectangles unless the topic itself is inherently about those shapes.

## Copy rules

- The page title should be the actual topic question or explanatory claim.
- A panel title advances the story.
- A subhead or caption must add a new fact, example, caveat, or consequence; never paraphrase the panel title.
- Remove meta copy such as `/eli5`, "engineering", "here's a fun visual", or explanations of the explainer format.
- The page is the explanation, not a frame around the explanation.

## Visual style

Use system fonts only.

- **Title and panel titles:** Georgia serif, regular weight (`400`).
- **Body, captions, and labels:** Helvetica/Arial/sans-serif.
- **Ground:** `#F7F8FC`.
- **Lavender fills/bands:** `#E7EAF6` and `#DDE2F2`.
- **Ink:** `#111111`.
- **Muted secondary:** `#5F6272`.
- **Single accent:** brick red `#C42A1C`.

Use the accent sparingly for step labels, the active or "your" element, key terms, or one arrow. Keep neutral/shared elements black. Do not introduce extra accent colours unless the user's request requires them.

Prefer editorial, restrained geometry:

- near-square corners (`3–4px` radius);
- `1.5px solid #111111` borders;
- a full-width lavender hero band with a black bottom rule;
- tiny uppercase step labels around `11px` with letter spacing around `.12em`.

## Complexity test

Before attaching the file, perform both checks:

1. Read only the panel titles. Do they explain the whole mechanism in order?
2. Look at each scene by itself. Can it be understood in roughly two seconds without tracing or decoding?

If either answer is no, simplify or split panels.

## Content fidelity

Do not let the visual introduce claims, terminology, or sequencing that contradicts the verbal explanation. Keep names and mechanics literal enough that the reader can map the graphic back to the real system.

Use Mermaid `gitGraph` inside the HTML only when a genuine Git timeline is materially clearer than comic panels. The deliverable is still the rendered HTML artifact, never a chat code block.
