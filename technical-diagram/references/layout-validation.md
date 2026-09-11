# Technical diagram layout validation

Use this reference when an artifact contains enough labels, connectors, lanes, or
containers that freehand SVG placement could clip or collide. The objective is to
make geometry a deterministic concern wherever practical instead of relying on
model spatial judgement.

## Rendering pipeline

Prefer this order:

```text
source/evidence
→ semantic diagram spec
→ pattern/layout rails
→ SVG/HTML template
→ text fitting
→ browser layout lint
→ simplify/split or deliver
```

The model owns the semantic choices: what objects exist, what each edge means,
which pattern is appropriate, and what the labels say. Layout helpers own
mechanical concerns such as fitting, reserved lanes, padding, and overlap checks.

Do not start by inventing arbitrary SVG coordinates for every element. First write
or hold a compact semantic spec containing at least:

- title and one-sentence thesis;
- selected pattern;
- major objects and groups;
- ordered primary edges;
- secondary/failure edges;
- short labels/callouts;
- optional outcome cards;
- any uncertain or omitted relationships.

Then map that spec onto the closest pattern rails.

## Template layout contract

The bundled HTML template exposes attributes used by its inline layout helper and
browser-backed linter.

### Fit constrained text

For text that must remain inside a specific box, give the box an `id` and annotate
the text:

```html
<rect id="title-pill" ... />
<text data-fit-box="title-pill"
      data-min-font-size="28"
      data-padding="28">...</text>
```

The runtime helper reduces the font size only as far as the declared minimum. If
text still does not fit, lint fails. Do not keep shrinking until the diagram is
technically valid.

Use `data-fit-box` for:

- title pills;
- section banners;
- labels inside service/store cards;
- single-line callouts;
- benefit-card titles where the available width is bounded.

Prefer rewriting a label over reducing it to the minimum size.

### Layout objects

Mark peer objects that must not overlap:

```html
<g data-layout-object="service-a">...</g>
```

Do not mark intentional parent/child compositions (for example an icon inside a
service card) as separate peer objects. Group the composition and mark the outer
`<g>` once.

### Connectors

Mark semantic flow paths with:

```html
<path data-connector="primary" ... />
```

The runtime lint samples the rendered path and reports connector/text collisions.
Keep labels offset from the line or place a small opaque label plate behind them.
Never lay text directly over a connector and rely on colour contrast to make it
readable.

### Ignoring intentional intersections

A small number of intentional intersections may be excluded with
`data-lint-ignore="true"`, but use this only when the overlap itself communicates
meaning. Do not use it to suppress a crowded layout.

## Pattern rails

### Linear flow

Reserve one horizontal lane for nodes and one narrow label lane above or below
connectors. Keep response/fallback traffic in a separate lane.

### Primary path with fallback

Lay out the happy path first. Put fallback/recovery in a lower bounded region and
rejoin the main outcome explicitly. Do not weave fallback arrows through the
primary path.

### Cluster/shards

Treat the cluster as one outer object for primary-flow placement. Position peer
nodes on an internal regular grid/row. Put the routing invariant in a dedicated
internal callout band rather than floating it across nodes.

### Sequence / request-response

Use fixed participant columns and monotonically increasing interaction rows:

```text
participant heading row
│          │          │
│ step 1 → │          │
│ ← reply  │          │
│ step 2 ────────────→ │
│ ← reply ──────────── │
```

Requirements:

- participant x positions remain fixed;
- each interaction owns one row; request and response rows must not overlap;
- action text sits in a reserved label band above its connector;
- numbered markers sit beside the label band, not on top of text;
- callout cards occupy their own row or side gutter;
- footer/legend content is outside the interaction rows.

This pattern is preferred for DNS/TCP/TLS/HTTP style explainers. Do not treat a
sequence as a generic canvas with independently guessed y coordinates.

## Runtime linter

The template sets `window.__diagramLayoutReport` after fonts are ready and layout
fitting has completed. The report contains `errors`, `warnings`, and the applied
text-fit adjustments.

Mechanical failures include:

- `TEXT_OUTSIDE_VIEWBOX`;
- `TEXT_OUTSIDE_FIT_BOX`;
- `TEXT_BELOW_MIN_SIZE`;
- `TEXT_TEXT_OVERLAP`;
- `TEXT_CONNECTOR_COLLISION`;
- `LAYOUT_OBJECT_OVERLAP`.

The checks deliberately favour false-positive pressure over silently shipping
clipped output. If a report is wrong because an intersection is semantically
intentional, structure the SVG more clearly before adding an ignore annotation.

## CLI linter

When Playwright or Puppeteer is available, run:

```bash
node technical-diagram/scripts/lint-diagram-layout.mjs path/to/diagram.html
```

The command launches a real browser, waits for the template runtime report, emits
JSON, and exits:

- `0` — no layout errors;
- `1` — layout errors were found;
- `2` — the browser driver/environment was unavailable or the artifact could not
  be loaded.

Exit `2` is **not** a pass. If a renderer is available through another harness,
open the artifact there and inspect `window.__diagramLayoutReport` instead.

## Recovery policy

When lint fails, fix in this order:

1. shorten the offending label while preserving the real term;
2. increase the owning box or reserved lane without breaking the primary hierarchy;
3. move the label/callout to a dedicated lane or gutter;
4. simplify secondary information;
5. split the story into multiple diagrams.

Do not:

- move elements a few pixels repeatedly without understanding the collision;
- shrink below the declared minimum font size;
- hide overflow;
- place an opaque patch over clipped text;
- suppress lint because a stronger model might have laid it out differently.

## Delivery gate

When a browser-backed renderer is available, a diagram with layout-lint errors is
not deliverable. Fix or split it and rerun the lint.

When mechanical lint cannot be executed, apply the same contract conservatively,
inspect the rendered artifact at full size and thumbnail size if possible, and
state that mechanical layout lint was not run. Do not claim the layout was
validated by the script.