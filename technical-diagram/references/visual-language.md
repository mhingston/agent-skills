# Technical diagram visual language

Use this reference when the user asks for a polished explainer graphic, supplies a
visual reference, or the default presentation style materially affects the
result. The goal is a reusable editorial system, not imitation of a particular
publisher's branded artwork.

## Default style: `bold-explainer`

The default should feel clear, friendly, and presentation-ready rather than like
a formal modelling tool.

### Canvas

- Prefer a `16:9` landscape canvas for architecture and mechanism explainers.
- Default SVG viewBox: `0 0 1600 900`.
- Use a white page/frame around a warm pale working area when a framed infographic
  composition helps.
- Keep outer margins generous: roughly `28–48px` on a 1600×900 canvas.
- Use one large composition before considering multiple panels.

### Palette

Use semantic roles rather than hard-coding every object to a unique colour.

```text
ink              #111111
paper            #FFFFFF
warm-ground      #FFF8D6
purple           #6525D1
purple-light     #E9DDFB
mint             #69D99B
mint-light       #DDF8E9
amber            #FFBE5C
amber-light      #FFE6AE
blue             #66B8F4
blue-light       #DDEEFF
red              #D64B28
muted            #5A5A5A
```

Rules:

- use black/near-black for all important text and structural outlines;
- use one primary accent and up to two supporting accents;
- reserve red/orange-red for failure, danger, rejection, or a genuinely adverse
  state;
- do not use colour alone to communicate sequence or state;
- avoid gradients unless the reference image clearly uses them and they improve,
  rather than decorate, the explanation.

A supplied reference may change the palette, but preserve semantic consistency
inside the generated diagram.

### Typography

Use system fonts only in portable artifacts.

- Default family: `Inter, Arial, Helvetica, sans-serif`; fall back safely when
  Inter is unavailable.
- Title: bold, approximately `38–48px` at 1600×900.
- Section heading: bold, approximately `24–30px`.
- Object label: bold, approximately `20–26px`.
- Secondary label: `17–21px`.
- Small callout/meta label: never below roughly `15px` at full canvas size.
- Prefer sentence case or compact title case; avoid long all-caps text except
  short section banners.

Technical labels must remain literal. Do not trade precision for a friendlier
word when the real term is the useful term.

### Strokes and geometry

- Major outlines: `3–4px` near-black.
- Secondary connectors: `2.5–3px`.
- Rounded rectangles: radius roughly `8–14px`; use larger pill radii only for
  banners or badges.
- Dashed containers: broad dash rhythm such as `12 10`; keep them visually lighter
  than object outlines.
- Use simple geometric icons with the same stroke weight as the rest of the
  illustration.
- Avoid drop shadows by default. If separation is needed, prefer spacing, border,
  or a pale grouped region.

### Title treatment

A strong default title is a black rounded pill centred near the top of the page
with white bold text. Use it only when the artifact is an infographic/explainer;
for formal architecture documentation, a plain heading may be more appropriate.

The title should answer one of:

- what mechanism is being shown;
- what change is being compared;
- what problem the diagram explains.

Avoid meta titles such as "Architecture Diagram" when a concrete title such as
"How distributed caches work" is available.

### Containers and sections

Use a large pale background region or dashed outline to communicate a meaningful
scope, such as:

- cache cluster;
- application boundary;
- fallback/resiliency lane;
- trust boundary;
- deployment unit.

A section banner may sit across or just above the container. Keep the banner short
and visually distinct, commonly purple with white text.

Do not draw a container around every pair of elements. Group only when the group
changes interpretation.

### Objects

Prefer recognisable, low-detail symbols:

- person/group for user or caller;
- rounded service/card for application/service;
- stacked cylinder for database/cache/storage;
- envelope/queue rail for messaging;
- hexagon only when it usefully distinguishes a tool/external capability;
- speech bubble or terminal card for a user-facing outcome;
- small circular badge for sequence number or status.

Keep icons subordinate to labels. Readers should not need to decode custom
pictograms before understanding the system.

### Arrows and connectors

- Primary path: solid black arrow.
- Highlighted primary interaction: solid accent arrow when one step deserves
  emphasis.
- Failure/secondary/asynchronous path: dashed line, optionally with a semantic
  accent such as red for failure.
- Feedback or response path: route separately rather than putting arrowheads on
  both ends of one line.
- Keep horizontal and vertical segments mostly orthogonal; gentle curves are fine
  when they reduce overlap.
- Place labels near the segment they describe and leave breathing room around the
  arrowhead.

Avoid:

- crossing arrows;
- arrows entering text;
- arrowheads hidden under nodes;
- five different connector styles with no legend;
- long looping connectors that make the reader search for endpoints.

### Numbered sequence markers

Use numbered circular markers when the flow contains a meaningful order that is
not visually obvious from placement.

- keep markers small but readable;
- use the primary accent fill with white text;
- place them next to action labels rather than floating far from the relevant
  connector;
- do not number purely spatial architecture diagrams.

### Callouts

Good callouts explain one mechanism or consequence:

- `Cache hit → fast reply`
- `Populate cache + TTL`
- `Keys are sharded across nodes`
- `Source of truth`

A callout should normally fit on one line. If it becomes a paragraph, move the
explanation outside the diagram or split the concept.

### Failure and resiliency treatment

Failure should be visible without making the whole canvas feel alarming.

- mark the failed object with one compact red status badge or strike state;
- move recovery/fallback into a secondary lane or group;
- show the reroute/rebalance path explicitly;
- return the reader to a useful outcome when resilience is the thesis;
- distinguish "unavailable", "degraded", and "stale" if those states have
  different system behaviour.

### Outcome/benefit cards

A bottom row of two to four compact cards can summarise consequences after the
mechanism is already clear, for example:

- lower latency;
- reduced database load;
- horizontal scaling;
- TTL/eviction controls freshness.

Use these only when they add interpretation. Do not turn every diagram into a
marketing infographic.

## Reference-image adaptation

When a user supplies an image, inspect it for design variables rather than
copyable content.

Capture:

```text
aspect_ratio
background_role
primary_accent
secondary_accents
stroke_weight
corner_radius
font_category
heading_treatment
connector_style
container_style
icon_abstraction
object_density
whitespace_density
reading_direction
```

Then map those variables onto the target diagram's own components. Preserve the
subject's correct architecture and relationships even when that requires a
composition unlike the reference.

## Density rules

At 1600×900, a healthy default is:

- 4–8 major objects;
- 5–10 primary connectors;
- 0–2 grouped regions in addition to the outer frame;
- 0–6 short callouts;
- 0–4 outcome cards;
- no body paragraphs.

Treat these as design pressure, not a compliance target. A three-object diagram
can be excellent. A twelve-object diagram can be acceptable when the structure
is naturally repetitive and still scans quickly.

## Thumbnail review

Shrink the diagram to around one quarter of its display width and ask:

- can the title still be read?
- are the major regions still visually distinct?
- is the primary path obvious?
- do any details collapse into visual noise?
- is one object accidentally dominating because of colour or size?

If the structure fails at thumbnail size, simplify before polishing full-size
labels.

## Accessibility

- Maintain strong text/background contrast.
- Never rely only on red/green to communicate state.
- Keep text as real SVG/HTML text where practical rather than converting it to
  paths.
- Supply a concise description of the diagram's mechanism with the artifact.
- Preserve keyboard/zoom usability when the artifact contains HTML controls;
  static diagrams normally need no interaction.

## Anti-patterns

Avoid:

- decorative clouds, gears, or circuit traces that do not encode meaning;
- tiny text used to rescue an overloaded layout;
- one colour per component with no semantics;
- gradients, shadows, bevels, glass effects, or 3D merely for polish;
- fake precision such as arbitrary percentages or timings;
- literal copying of a reference publisher's logo, mascot, or branded frame;
- formal architecture notation mixed with playful infographic symbols without a
  clear reason.
