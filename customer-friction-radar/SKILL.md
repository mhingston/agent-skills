---
name: customer-friction-radar
description: Analyse customer-friction evidence across public reviews, app reviews, complaints, call transcripts, digital telemetry, and operational signals. Use when asked to identify, validate, compare, or explain customer-journey friction, connect digital self-service failures to assisted-service demand, or produce a friction brief. Use persistence or ontology-maintenance workflows only when explicitly requested. Do not use for generic sentiment reporting, support-case handling, or automatic backlog prioritisation without corroborating evidence.
compatibility: Requires access to relevant public or internal customer evidence. Internal correlation requires access to the relevant telemetry, transcript, complaint, or operational sources.
---

# Customer Friction Radar

Turn noisy customer feedback into a small set of traceable, testable customer-journey friction themes. Treat public reviews as sensors, not prevalence estimates.

## Core principles

### Start from customer effort, not sentiment

Identify:

1. what the customer was trying to do;
2. where the journey broke down;
3. what extra effort followed;
4. what consequence resulted.

Positive or negative sentiment is supporting context only.

Prefer questions such as:

- Which self-service journeys are leaking into avoidable assisted contact?
- Where do customers have to repeat information or re-establish context?
- Which operational states create uncertainty or repeated status checking?
- Which product or organisational boundaries are visible to customers?
- Which recurring complaints can be corroborated by internal evidence?
- Which friction theme is sufficiently evidenced to justify a bounded experiment?

### Separate signals from prevalence

Public reviews, app-store feedback, and complaints are selection-biased evidence. They can establish that a failure mode exists and may indicate recurrence or change within the observed sample. They do not establish population prevalence by themselves.

Never translate review counts into population statements without a valid denominator from an authoritative internal source.

### Preserve the journey

For every material observation capture:

- member/customer intent;
- product or service;
- journey stage;
- channel;
- observed friction;
- extra effort;
- consequence;
- source evidence and date;
- confidence and limitations.

Prefer journey-level explanations over isolated interface defects.

### Triangulate before recommending material change

Treat an external theme as a hypothesis until it is corroborated or challenged by another evidence type when reasonably accessible.

Useful internal evidence includes:

- call transcripts and transcript-derived measures;
- contact reasons and dispositions;
- repeat-contact rates;
- portal funnel abandonment;
- authentication/API failures;
- digital-to-assisted handoff rates;
- complaints and escalation records;
- CSAT/NPS free text;
- cancellation/retention outcomes;
- operational incidents, queues, dispatch and service state.

If internal evidence is unavailable, state `external-signal-only` in the theme's limitations and name the smallest query needed to test it.

### Preserve evidence and uncertainty

Use these statuses precisely:

- `observed` — directly present in source evidence;
- `inferred` — model interpretation from observations;
- `corroborated` — supported by an independent evidence type;
- `contradicted` — meaningful evidence argues against the interpretation;
- `confirmed` — accepted by an authorised human owner;
- `stale` — no longer fresh enough for the intended decision.

Never promote an inference to `confirmed` because a model is confident.

### Keep the ontology small and operational

The ontology exists to improve consistent classification, cross-source correlation, trend comparison and decision continuity. It is not an enterprise knowledge-graph programme.

Add or change a concept only when:

- recurring evidence cannot be classified clearly;
- a competency question cannot be answered;
- inconsistent terminology is materially affecting analysis.

When persistence or controlled-vocabulary work is requested, read [references/customer-friction-ontology.md](references/customer-friction-ontology.md) before creating or changing ontology terms or persistent structure.

### Do not automate product decisions

The skill may surface and rank evidence, propose hypotheses, and recommend a bounded investigation or experiment. It must not silently:

- create product commitments;
- convert a review into a bug;
- assign blame to a team or individual;
- infer customer intent beyond evidence;
- declare root cause from correlation;
- rewrite canonical ontology terms without preserving history;
- treat a theme as resolved because review volume temporarily falls.

## Modes

Choose the lightest mode that satisfies the request:

- **Scan** — inspect recent evidence and identify candidate signals.
- **Validate** — test one or more themes against independent evidence.
- **Brief** — produce a friction brief when requested.
- **Ontology/persistence** — optionally establish, evolve, or save the analysis in a governed system when explicitly requested.
- **Investigate** — perform a bounded multi-source analysis of one selected theme.

Do not default to full multi-source investigation when a small scan is sufficient.

## Workflow

### 1. Establish scope and stop condition

Identify:

- organisation/product/service scope;
- time window;
- customer journey or question, when known;
- evidence sources available;
- intended decision owner or consumer;
- target repository or destination only if the user requests persistence;
- maximum useful scope;
- stop condition.

Do not assume that any particular source, system, organisation, or internal
vocabulary is available.

Prefer one journey or a small number of candidate themes.

A good stop condition:

> Stop when the leading theme is supported by two independent evidence types, its main alternative explanation has been tested, and one bounded next action is clear.

### 2. Inspect prior material only when relevant

When the user asks to use existing knowledge or save the result, inspect the authorised destination for:

- customer-friction root material;
- ontology and controlled vocabulary;
- source register;
- theme registry;
- recent friction briefs;
- existing theme pages relevant to the current evidence.

Reuse stable IDs and canonical labels. Search before create.

If the structure does not exist and ontology maintenance is requested, bootstrap the minimal structure in `references/customer-friction-ontology.md`.

### 3. Build a source/authority map

Treat source authority as claim-specific.

Start with the sources named or supplied by the user. Add other sources only
when they answer a specific unresolved question; there is no mandatory source
list. Potentially relevant sources may include public or app reviews,
membership or service journeys, contact reasons, call/chat transcripts,
digital funnel and handoff telemetry, complaints, dispatch/ETA/service-state
data, and retention or cancellation outcomes—but only query sources that are
actually available and in scope.

| Source | Strong for | Weak for |
| --- | --- | --- |
| Public reviews | Existence, examples, recurring language, perceived effort | Population prevalence, root cause |
| App reviews | Digital defects, usability, authentication/device symptoms | End-to-end operational cause |
| Complaints | Material failures, escalation paths, harm | Population prevalence |
| Call transcripts | Customer effort, repetition, handoffs, assisted-service context | Digital events not spoken aloud |
| Portal telemetry | Observable digital behaviour and failures | Customer interpretation/emotion |
| Contact reasons | Demand shape and broad intent | Detailed mechanism |
| Operational data | Queue, dispatch, service and incident state | Customer understanding of state |

### 4. Collect evidence minimally

Prefer first-party APIs, licensed feeds, official review/app pages and internal systems.

Do not bypass access controls or violate source terms.

For public sources:

- retain only the minimum useful customer content;
- avoid unnecessary personal data;
- deduplicate repeated/syndicated reviews;
- record observed sample size and source coverage.

### 5. Extract structured observations

For each relevant item capture the fields in `references/customer-friction-ontology.md`.

Ground every classification in evidence. Keep a short excerpt or faithful paraphrase sufficient for human verification.

Do not force an observation into an existing theme when the mechanism differs. Use `candidate-theme` until resolved.

### 6. Cluster by failure mechanism

Prefer mechanisms such as:

- self-service submission appears complete but does not progress;
- digital context is lost during handoff to an agent;
- customer must repeat information already supplied;
- status is available but operational uncertainty remains;
- product boundary creates inconsistent identity, entitlement or offer context;
- promised post-interaction information is not durably accessible.

Avoid broad clusters such as `bad service`, `app issue`, `communication` or `expensive` unless evidence cannot yet support a more discriminating concept.

### 7. Compare with existing themes

For each cluster decide:

- `new`;
- `reinforces`;
- `broadens`;
- `splits`;
- `contradicts`;
- `resolves`;
- `no-change`.

Preserve stable IDs. Split or supersede rather than silently redefining a theme.

### 8. Triangulate material themes

For leading themes identify the smallest internal query that could confirm or falsify the interpretation.

Examples:

- digital submission complaint → compare `submitted`, `acknowledged` and downstream workflow events; measure assisted contact shortly afterwards;
- repeated-information complaint → search transcripts for repetition indicators and compare with prior digital/contact context;
- uncertain ETA complaint → compare operational state transitions, ETA changes, status-page checks and status-related calls;
- renewal negotiation complaint → compare initial offer, digital behaviour, assisted contact, final offer and retain/cancel outcome.

Keep separate:

1. external signal;
2. internal behavioural evidence;
3. operational mechanism;
4. causal hypothesis.

### 9. Assess evidence strength and decision priority

Use ordinal assessments rather than false-precision scoring.

Evidence strength:

- `weak` — isolated/single-source evidence with plausible alternatives;
- `moderate` — recurring evidence or one strong internal signal;
- `strong` — recurrence plus independent corroboration with limited contradiction.

Decision priority:

- `urgent` — credible safety, vulnerability, regulatory or severe service risk;
- `high` — recurring material effort/outcome impact with a plausible bounded intervention;
- `medium` — meaningful but weakly corroborated or lower-impact friction;
- `watch` — early signal requiring more evidence.

Never infer priority from star rating alone.

### 10. Persist the analysis when requested

Only perform this step when the user explicitly asks to save, update, or maintain the analysis in an authorised destination:

1. fetch current page before edit;
2. update existing theme pages before creating new ones;
3. append new evidence without deleting contrary evidence;
4. update trend, evidence strength, status and last-seen date;
5. add corroboration and contradiction links;
6. record ontology changes separately from theme evidence;
7. preserve human-authored decisions and accepted terminology;
8. create new ontology terms as `proposed` unless confirmed by an authorised source/reviewer;
9. mark superseded terms explicitly instead of reusing identifiers;
10. use dedicated skill-managed pages or clearly marked managed sections.

Do not overwrite unrelated human-authored content.

### 11. Produce the friction brief when requested

Read [references/friction-brief.md](references/friction-brief.md) when the user asks for a brief.

Rank only themes that changed, became decision-relevant or need attention.

For each material theme include:

- theme ID and canonical label;
- member/customer intent;
- failure mechanism;
- affected journey/product/channel;
- observed sample evidence;
- trend within the observed evidence;
- corroborating/contradicting internal evidence;
- leading and competing hypotheses;
- evidence strength;
- decision priority;
- smallest next investigation or experiment;
- owner when known;
- confidence and limitations.

### 12. Recommend one bounded next action

Prefer the smallest action capable of changing the decision state, for example:

- instrument one missing state transition;
- compare digital submissions with calls within a defined time window;
- label a sample of transcripts for repeated-information friction;
- inspect one failed handoff path;
- test a contextual callback/handoff flow;
- add one missing canonical ontology concept.

Do not broaden the solution space when the evidence already points to a testable vertical slice.

## Optional persistence operating rules

- search before create;
- fetch the current record or document before edit;
- preserve stable IDs and hierarchy;
- preserve human-authored decisions/comments/accepted definitions;
- make updates idempotent where practical;
- add dates and evidence links to material updates;
- do not duplicate briefs for the same reporting window;
- do not delete evidence because a theme is downgraded or resolved;
- do not promote proposed ontology terms without human or authoritative confirmation;
- fail visibly if the destination or record cannot be resolved safely.

If multiple plausible destinations exist and the target cannot be resolved, ask rather than writing to an arbitrary location.

## Quality checks

Before returning or publishing verify:

- every material finding traces to inspectable evidence;
- observed sample size and source coverage are stated;
- review evidence is not presented as population prevalence;
- external signal, internal corroboration and causal hypothesis remain distinct;
- duplicate themes were checked before adding a new theme;
- ontology terms have stable IDs and explicit status;
- contradictory evidence remains visible;
- priority follows impact and evidence, not negativity alone;
- the recommendation is bounded;
- if persistence is requested, changes preserve human decisions/history;
- sensitive internal evidence is not copied to a less-restricted page.

## Failure and stop conditions

Stop or narrow when:

- source access is too partial for an observed-sample statement;
- evidence is duplicated, stale or non-attributable;
- a theme cannot be distinguished from a generic complaint category;
- required internal evidence is unavailable;
- the relevant journey cannot be identified;
- ontology changes would encode an unverified root cause or mutable policy as canonical truth;
- a requested persistence destination cannot be resolved safely;
- further collection is repetitive rather than decision-relevant;
- the proposed intervention is broader than the evidence supports.

Return the missing evidence and the smallest recovery action.

## Resources

- [Customer friction ontology](references/customer-friction-ontology.md)
- [Friction brief contract](references/friction-brief.md)
