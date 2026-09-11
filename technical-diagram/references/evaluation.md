# Technical Diagram behavioural evaluation

Use this reference when changing the skill description, routing boundaries,
complexity budget, visual language, or artifact contract.

The important catalogue boundary is that `technical-diagram` owns cases where the
visual artifact itself is the requested outcome. `eli5` owns fast one-shot prose
orientation with only a supporting visual, while `codebase-walkthrough` owns
repository investigation and evidence-backed mental-model building.

## Matched conditions

Run each case as a matched pair in fresh contexts with the same model, harness,
tools, permissions, artifact support, and prompt.

- **candidate** — `technical-diagram` and adjacent public skills are discoverable.
- **baseline** — the exact base-revision catalogue is discoverable without
  `technical-diagram`.

Do not remove `eli5`, `codebase-walkthrough`, or other adjacent skills from either
condition. Routing collisions are part of the evaluation.

Record model, harness, renderer, and whether routing/skill loading is directly
observable. If not, label manual classification as a routing surrogate rather
than an end-to-end routing result.

## Cases

### TD-E1 — distributed cache explainer

**Prompt**

> Create a polished technical diagram showing how a distributed cache works. Show
> clients, application servers, a sharded cache cluster, cache hit and miss paths,
> the source-of-truth database, cache population with TTL, and what happens when a
> cache node fails. Make it suitable for a presentation slide.

**Candidate routing expectation**

`technical-diagram` should activate.

**Behavioural checks**

- produces a rendered self-contained visual artifact rather than a prose-only
  answer or raw Mermaid/SVG code block;
- uses one dominant request path and a secondary failure/rebalancing lane;
- keeps cache hit and miss semantics distinct;
- does not imply that sharding automatically means replication;
- database is visibly the source of truth rather than another peer cache node;
- failure handling does not visually overwhelm the normal path;
- remains readable at slide width and thumbnail scale;
- uses a restrained palette, strong outlines, short labels, and consistent icon
  grammar.

This case is based on the initial user trial that motivated the skill. The trial
is design evidence only; do not claim it as a matched behavioural pass.

### TD-E2 — retry and fallback path

**Prompt**

> Draw a technical explainer for an LLM-powered app. The normal path is user → app
> → LLM → tool → useful reply. LLM calls can fail because of timeout, 429, or bad
> output. Retry once, then fall back to a backup model, cached answer, or human
> help. Make the happy path immediately obvious and show resilience without making
> it look like three unrelated diagrams.

**Candidate routing expectation**

`technical-diagram` should activate.

**Behavioural checks**

- selects a primary-path-with-fallback composition;
- visually separates retry from fallback;
- shows where fallback returns to the useful outcome;
- failure states use a consistent secondary/dashed treatment;
- does not duplicate the same LLM/tool path in multiple disconnected panels;
- labels remain concise enough to scan without paragraph reading.

### TD-E3 — architecture visual with uncertain evidence

**Prompt**

> Turn this architecture note into a clean diagram. The API definitely writes to
> Postgres and publishes OrderCreated. We think the notifications service consumes
> that event, but the note is old and nobody has verified it. Show only what the
> note supports and make uncertainty visible rather than inventing the rest.

**Candidate routing expectation**

`technical-diagram` should activate.

**Behavioural checks**

- renders the confirmed API → Postgres and API → event relationships distinctly;
- does not silently upgrade the uncertain notifications consumer into a confirmed
  edge;
- uncertainty is either omitted with a note or represented explicitly and
  legibly;
- avoids filling empty space with invented components;
- artifact remains useful despite incomplete evidence.

### TD-E4 — simplify an overloaded source

**Prompt**

> Make one slide-sized diagram from this system description: 24 microservices,
> six databases, three queues, two external vendors, four scheduled jobs, and
> every service-to-service dependency. I want every component and every edge on a
> single 16:9 canvas, but it still needs to be easy to understand in five seconds.

**Candidate routing expectation**

`technical-diagram` should activate, but should challenge the incompatible
complexity requirement rather than shrinking everything until it fits.

**Behavioural checks**

- identifies that exhaustive topology and five-second comprehension conflict;
- proposes or creates a higher-level grouped overview and, when artifact support
  permits, offers decomposition into additional diagrams;
- does not reduce text below the skill's legibility floor;
- does not create a hairball of crossing arrows;
- preserves the user's important scope while being explicit about abstraction.

### TD-E5 — visual-reference adaptation

**Prompt**

> Use this attached technical infographic as the visual reference for a diagram of
> our event-driven order pipeline. I like the warm background, bold black outlines,
> purple section banners, simple icons, and obvious left-to-right path. Don't copy
> the publisher branding or their exact layout.

**Candidate routing expectation**

`technical-diagram` should activate.

**Behavioural checks**

- extracts style variables rather than cloning layout or brand marks;
- preserves the order pipeline's own semantics and object count;
- keeps the requested warm/editorial visual language consistent;
- no copied logo, mascot, publisher name, or decorative branded element appears;
- visual reference does not override the target system's required reading path.

### TD-E6 — prose orientation near-miss

**Prompt**

> ELI5 distributed caches. I know what a normal in-memory cache is but don't
> understand what makes one distributed. Give me the quick version.

**Candidate routing expectation**

`technical-diagram` should **not** steal the request. Route to `eli5`.

**Behavioural checks**

- primary response remains a concise verbal orientation;
- any visual is supporting rather than becoming the main deliverable;
- user's stated knowledge is respected;
- candidate introduces no unnecessary artifact ceremony relative to baseline.

This is the principal `eli5` anti-collision case.

### TD-E7 — code investigation near-miss

**Prompt**

> In this repository, how does checkout actually get from the HTTP endpoint to
> payment capture? Trace the current code and tell me where ownership changes. A
> diagram is fine if it helps, but I mainly need to understand the implementation.

**Candidate routing expectation**

`technical-diagram` should **not** activate as the primary workflow. Route to
`codebase-walkthrough`.

**Behavioural checks**

- repository evidence is inspected before architecture claims are made;
- current runtime/data flow and ownership are the primary output;
- a diagram, if produced, is subordinate to the evidence-backed walkthrough;
- no unsupported edge is invented merely to produce a polished visual.

This is the principal `codebase-walkthrough` anti-collision case.

### TD-E8 — trivial relationship, no forced diagram

**Prompt**

> Is Redis in-memory or on-disk? Just tell me which and one sentence of nuance.

**Candidate routing expectation**

`technical-diagram` should not activate merely because Redis is a technical
component.

**Behavioural checks**

- answers directly in prose;
- does not generate an infographic for a trivial factual distinction;
- candidate adds no material latency or ceremony relative to baseline.

## Visual grading rubric

For TD-E1 through TD-E5, score each artifact from 1–5 on these dimensions. Blind
condition labels when practical.

### A. Mechanism clarity

- **5** — main mechanism is obvious in seconds; details reinforce it.
- **3** — mechanism is understandable but requires deliberate tracing.
- **1** — reader must decode the picture or infer missing relationships.

### B. Semantic fidelity

- **5** — arrows, grouping, state, ownership, and terminology accurately encode
  the supplied system.
- **3** — mostly correct with one ambiguous visual implication.
- **1** — important relationships are invented, reversed, or conflated.

### C. Visual hierarchy

- **5** — title, primary path, boundaries, and secondary information have obvious
  priority.
- **3** — hierarchy exists but several elements compete.
- **1** — all elements have similar weight or attention is drawn to decoration.

### D. Legibility

- **5** — labels are concise, unclipped, and readable at target size.
- **3** — some crowding or wrapping but still usable.
- **1** — tiny/clipped text or dense paragraphs materially impair reading.

### E. Composition

- **5** — no unnecessary crossing, spacing is balanced, and the eye has an obvious
  route.
- **3** — a few awkward connectors or empty/crowded areas.
- **1** — hairball topology or unclear starting point.

### F. Style consistency

- **5** — palette, strokes, radii, typography, arrows, and icon abstraction form a
  coherent system.
- **3** — minor inconsistencies that do not harm comprehension.
- **1** — mixed visual languages or decorative effects distract from content.

### G. Reference adaptation, when applicable

- **5** — captures reusable style traits while remaining an original composition.
- **3** — style is recognisable but either too generic or unnecessarily close to
  the source layout.
- **1** — copies branding/layout directly or ignores the requested visual traits.

## Paired grading

Record separately:

1. **Activation** — selected `technical-diagram`, selected adjacent skill, or no
   relevant skill; use `not_verifiable` when discovery is hidden.
2. **Goal completion** — did the user get the requested visual outcome?
3. **Boundary correctness** — especially TD-E6, TD-E7, and TD-E8.
4. **Artifact integrity** — self-contained/offline, editable source retained,
   no external resources or unsafe interpolation.
5. **Visual rubric** — A–G where applicable.
6. **Regression** — unnecessary ceremony, unsupported claims, or extra artifact
   generation relative to baseline.
7. **Cost/latency** — record only when exposed by the harness.

## Minimum acceptance condition

The candidate is acceptable when:

- TD-E1 through TD-E5 route to `technical-diagram` when routing is observable;
- TD-E6 routes to `eli5`;
- TD-E7 routes to `codebase-walkthrough`;
- TD-E8 is answered directly without forcing a diagram;
- rendered artifacts are self-contained and avoid raw diagram code as the
  user-facing result;
- no visual case scores below `3` on semantic fidelity or legibility;
- the median visual score across mechanism clarity, hierarchy, composition, and
  style consistency is at least `4` for TD-E1, TD-E2, and TD-E5;
- the candidate introduces no material regression in adjacent-skill behaviour.

Run at least one complete matched pair per case for a routing/behaviour smoke test.
Use repeated pairs when model variance or description changes make the routing
conclusion consequential. Do not report behavioural evaluation as passed until
matched runs have actually been executed and preserved.
