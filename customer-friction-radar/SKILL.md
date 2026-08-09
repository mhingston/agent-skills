---
name: customer-friction-radar
description: Detect, validate, and maintain evidence-backed customer-friction themes across public reviews, app reviews, complaints, call transcripts, digital telemetry, and operational signals. Use when asked to analyse recent customer experience problems, find emerging journey friction, connect digital self-service failures to assisted-service demand, maintain a customer-friction ontology in Confluence via Atlassian Rovo MCP, or produce a recurring friction brief. Do not use for generic sentiment reporting, one-off support cases, or automatic backlog prioritisation without corroborating evidence.
compatibility: Requires access to relevant public or internal customer evidence. Confluence ontology maintenance requires an Atlassian Rovo MCP with permission to search, create, and edit pages in the target space. Internal correlation requires access to the relevant telemetry, transcript, complaint, or operational sources.
---

# Customer Friction Radar

Turn noisy customer feedback into a small set of traceable, testable customer-
journey friction themes. Treat public reviews as sensors, not prevalence estimates,
and use Confluence as a governed semantic memory for recurring friction.

## Core principles

### Start from customer effort, not sentiment

Identify what the customer was trying to do, where the journey broke down, what
extra effort followed, and what consequence resulted. Positive or negative
sentiment is supporting context only.

Prefer questions such as:

- Which self-service journeys are leaking into avoidable assisted contact?
- Where do customers have to repeat information or re-establish context?
- Which operational states create uncertainty or repeated status checking?
- Which product or organisational boundaries are visible to customers?
- Which recurring complaints can be corroborated by internal evidence?
- Which friction theme is sufficiently evidenced to justify a bounded experiment?

### Separate signals from prevalence

Public reviews, app-store feedback, and complaints are selection-biased evidence.
They can establish that a failure mode exists and may indicate recurrence or
change within the observed sample. They do not establish population prevalence by
themselves.

Never translate review counts into statements such as "X% of customers experience
this" without a valid denominator from an authoritative internal source.

### Preserve the customer journey

For every material observation, capture:

1. customer or member intent;
2. product or service;
3. journey stage;
4. channel;
5. observed friction;
6. extra customer effort;
7. consequence;
8. source evidence and date;
9. confidence and limitations.

Prefer journey-level explanations over isolated interface defects.

### Triangulate before recommending material change

Treat an external theme as a hypothesis until it is corroborated or challenged by
another evidence type when that evidence is reasonably accessible.

Useful internal corroboration may include:

- call transcripts and transcript-derived measures;
- contact reasons and dispositions;
- repeat-contact rates;
- self-service funnel abandonment;
- authentication or API failures;
- digital-to-assisted handoff rates;
- complaints and escalation records;
- CSAT or NPS free text;
- cancellation or retention outcomes;
- operational incidents, queues, or service delays.

Do not invent internal evidence when it is unavailable. Mark the theme as
`external-signal-only` and state the smallest internal query that would test it.

### Preserve evidence and uncertainty

Keep source URL or identifier, source type, publication or event date, retrieved
at time, evidence excerpt or faithful paraphrase, product, journey context, and
classification confidence.

Use these evidence statuses precisely:

- `observed` — directly present in source evidence;
- `inferred` — model-generated interpretation from observations;
- `corroborated` — supported by an independent evidence type;
- `contradicted` — meaningful evidence argues against the interpretation;
- `confirmed` — accepted by an authorised human owner;
- `stale` — evidence is no longer fresh enough for the intended decision.

Never promote an inference to `confirmed` because a model is confident.

### Keep the ontology small and operational

The customer-friction ontology exists to improve consistent classification,
cross-source correlation, trend comparison, and decision continuity. It is not a
project to model the entire organisation.

Add or change a concept only when recurring evidence cannot be classified clearly,
a competency question cannot be answered, or inconsistent terminology is
materially affecting analysis.

Read [references/customer-friction-ontology.md](references/customer-friction-ontology.md)
before creating or changing ontology terms or the Confluence structure.

### Do not automate product decisions

The skill may surface and rank evidence, propose hypotheses, and recommend a
bounded investigation or experiment. It must not silently:

- create product commitments;
- convert a review into a bug report;
- assign blame to a team or individual;
- infer customer intent beyond the evidence;
- declare root cause from correlation;
- rewrite canonical ontology terms without preserving history;
- treat a theme as resolved because review volume temporarily falls.

## Modes

Choose the lightest mode that satisfies the request.

- **Scan** — inspect recent evidence and identify candidate friction signals.
- **Validate** — test one or more existing themes against independent evidence.
- **Brief** — produce a ranked periodic friction brief and update theme state.
- **Ontology** — establish or evolve the Confluence customer-friction ontology.
- **Investigate** — perform a bounded multi-source analysis of one selected theme.

Do not default to a full multi-source investigation when a small scan is enough.

## Core workflow

### 1. Establish scope and stop condition

Identify:

- organisation, product, or service scope;
- time window;
- customer journey or question when one is already known;
- evidence sources available;
- intended decision owner or consumer;
- Confluence space when ontology maintenance is in scope;
- maximum useful scope;
- stop condition.

Prefer one journey or a small number of candidate themes over organisation-wide
analysis.

A good stop condition is: "stop when the leading theme is supported by two
independent evidence types, its main alternative explanation has been tested, and
a bounded next action is clear."

### 2. Inspect the existing Confluence model first

When Confluence access is available, search the target space before analysis for:

- the Customer Friction Radar root page;
- ontology and controlled vocabulary;
- source register;
- theme registry;
- recent friction briefs;
- existing theme pages relevant to the current evidence.

Reuse stable identifiers and canonical labels. Do not create duplicate themes
because wording differs.

If the structure does not exist and ontology maintenance is requested, bootstrap
the minimal structure described in
[references/customer-friction-ontology.md](references/customer-friction-ontology.md).

### 3. Build a source and authority map

For each source record what it can and cannot establish.

Typical source roles:

| Source | Strong for | Weak for |
| --- | --- | --- |
| Public reviews | Existence, examples, recurring language, perceived effort | Population prevalence, root cause |
| App reviews | Digital defects, usability, authentication, device-specific symptoms | End-to-end operational cause |
| Complaints | Material failures, escalation paths, harm | Population prevalence |
| Call transcripts | Customer effort, repetition, handoffs, assisted-service context | Digital events not spoken aloud |
| Portal telemetry | Observable digital behaviour and failures | Customer interpretation or emotion |
| Contact reasons | Demand shape and broad intent | Detailed mechanism without validation |
| Operational data | Queue, dispatch, service, incident state | Customer understanding of that state |

Treat source authority as claim-specific rather than globally ranked.

### 4. Collect recent evidence minimally

Prefer first-party APIs, licensed feeds, official review pages, app stores, and
internal systems. Do not bypass access controls or rely on scraping methods that
violate the source's terms.

For public sources capture only the minimum useful customer content. Avoid
retaining reviewer names, avatars, precise locations, or other personal data unless
material and permitted.

Deduplicate syndicated or repeated reviews. Keep an explicit observed sample size
and source coverage statement.

### 5. Extract structured observations

For each relevant item capture the fields defined in
[references/customer-friction-ontology.md](references/customer-friction-ontology.md).

Ground every classification in source evidence. Keep an evidence excerpt or
faithful paraphrase sufficient for a human to verify the classification.

Do not force an observation into an existing theme when its mechanism differs.
Use `candidate-theme` until the distinction can be resolved.

### 6. Cluster by failure mechanism

Group evidence by the smallest useful mechanism, not merely shared sentiment or
keywords.

Prefer themes such as:

- self-service submission appears complete but does not progress;
- digital context is lost during handoff to an agent;
- customer must repeat information already supplied;
- status is technically available but operational uncertainty remains;
- product boundary creates inconsistent identity, entitlement, or offer context;
- promised post-interaction information is not durably accessible.

Avoid broad themes such as `bad service`, `app issue`, `communication`, or
`expensive` unless the evidence cannot yet support a more discriminating concept.

### 7. Compare with existing themes

For each cluster decide:

- `new` — no existing theme has the same mechanism;
- `reinforces` — new evidence supports an existing theme;
- `broadens` — evidence adds a new journey, channel, or product manifestation;
- `splits` — one existing theme contains materially different mechanisms;
- `contradicts` — new evidence weakens an existing interpretation;
- `resolves` — sustained evidence supports closure criteria;
- `no-change` — evidence adds no decision-relevant information.

Preserve stable theme IDs. Split or supersede rather than silently redefining a
theme.

### 8. Triangulate material themes

For the leading themes, identify the smallest internal queries that could confirm
or falsify the interpretation.

Examples:

- digital submission complaint -> compare `submitted`, `acknowledged`, and
  downstream workflow events, then measure assisted contacts shortly afterward;
- repeated-information complaint -> search transcripts for repetition indicators
  and compare with digital or previous-contact context;
- uncertain ETA complaint -> compare operational state transitions, ETA changes,
  status-page checks, and status-related calls;
- renewal negotiation complaint -> compare initial offer, digital behaviour,
  assisted contact, final offer, and retain/cancel outcome.

Distinguish:

- external signal;
- internal behavioural evidence;
- operational mechanism;
- causal hypothesis.

Do not collapse these into one claim.

### 9. Assess evidence strength and priority

Avoid false-precision scoring. Use ordinal assessments.

**Evidence strength**

- `weak` — isolated or single-source evidence with plausible alternatives;
- `moderate` — recurring evidence or one strong internal signal;
- `strong` — recurrence plus independent corroboration with limited contradiction.

**Decision priority**

- `urgent` — credible safety, vulnerability, regulatory, or severe service risk;
- `high` — recurring material effort or outcome impact with a plausible bounded
  intervention;
- `medium` — meaningful but weakly corroborated or lower-impact friction;
- `watch` — early signal requiring more evidence.

Explain the evidence behind the assessment. Never infer priority from star rating
alone.

### 10. Maintain the Confluence friction model

When authorised to edit the target Confluence space:

1. update existing theme pages before creating new ones;
2. add new evidence observations without deleting contrary evidence;
3. update trend, evidence strength, status, and last-seen date;
4. add cross-source corroboration and contradiction links;
5. record ontology changes separately from theme evidence;
6. preserve human-authored decisions and accepted terminology;
7. create new ontology terms as `proposed` unless an authorised source or reviewer
   confirms them;
8. mark superseded terms explicitly instead of reusing their identifiers.

Use dedicated skill-managed pages or clearly identified managed sections. Do not
overwrite unrelated human-authored Confluence content.

### 11. Produce the friction brief

Use [references/friction-brief.md](references/friction-brief.md) for the output
contract.

Rank only themes that changed, became decision-relevant, or need attention. Do not
fill a report with stable background noise.

For each material theme include:

- theme ID and canonical label;
- what customers are trying to do;
- failure mechanism;
- affected journey, product, and channel;
- observed sample evidence;
- trend within the observed evidence;
- corroborating or contradicting internal evidence;
- likely mechanism or competing hypotheses;
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
- test a contextual callback or handoff flow;
- add one missing canonical concept to the ontology.

Do not broaden the solution space when the evidence already points to a testable
vertical slice.

## Confluence operating rules

When using Atlassian Rovo MCP:

- search before create;
- fetch the current page before edit;
- preserve page identifiers and hierarchy;
- preserve human-authored decisions, comments, and accepted definitions;
- make edits idempotent where practical;
- add dates and evidence links to every material update;
- do not duplicate weekly briefs for the same reporting window;
- do not delete evidence because a theme is downgraded or resolved;
- do not promote proposed ontology terms without human or authoritative-source
  confirmation;
- fail visibly if the target space or page cannot be resolved safely.

If multiple plausible Confluence spaces exist and the correct target cannot be
resolved from context, ask rather than writing to an arbitrary space.

## Quality checks

Before returning or publishing, verify:

- every material finding traces to inspectable evidence;
- observed sample size and source coverage are stated;
- public-review evidence is not presented as population prevalence;
- external signal, internal corroboration, and causal hypothesis remain distinct;
- duplicate themes were checked before adding a new theme;
- ontology terms have stable IDs and explicit status;
- contradictory evidence remains visible;
- priority follows impact and evidence, not negativity alone;
- the recommendation is a bounded investigation or experiment;
- Confluence changes preserve existing human decisions and history;
- sensitive internal evidence is not copied into a less-restricted page.

## Failure and stop conditions

Stop or narrow the work when:

- source access is too partial to support even an observed-sample statement;
- the evidence is duplicated, stale, or non-attributable;
- a theme cannot be distinguished from a generic complaint category;
- internal evidence required for a material claim is unavailable;
- the relevant customer journey cannot be identified;
- ontology changes would encode an unverified root cause or mutable policy as
  canonical truth;
- the Confluence target cannot be resolved safely;
- further collection is producing repetition rather than decision-relevant
  evidence;
- the proposed intervention is broader than the evidence supports.

Return the missing evidence and the smallest recovery action. Do not manufacture a
complete narrative from weak signals.

## Resources

- [Customer friction ontology](references/customer-friction-ontology.md)
- [Friction brief contract](references/friction-brief.md)
