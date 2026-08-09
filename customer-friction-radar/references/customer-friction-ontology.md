# Customer Friction Ontology

Use this reference when establishing, reading, or evolving the Customer Friction
Radar model in Confluence.

The ontology is intentionally lightweight. It is a controlled vocabulary and
relationship model for recurring customer-friction analysis, not a full enterprise
knowledge graph.

## Competency questions

The model should help answer:

1. What was the customer trying to do?
2. At which journey stage and channel did friction occur?
3. What failure mechanism created extra effort or a poor outcome?
4. Which products, services, systems, or operational processes are implicated by
   evidence?
5. Which evidence supports or contradicts the theme?
6. Is the signal new, recurring, strengthening, weakening, or resolved?
7. Which internal measure could corroborate or falsify the interpretation?
8. Which owner or team should investigate the journey without assigning blame?
9. What bounded experiment or instrumentation change could reduce uncertainty?

If a proposed ontology element does not help answer one of these questions, do not
add it by default.

## Confluence structure

Prefer this minimal page tree in the chosen space:

```text
Customer Friction Radar
├── Operating Model
├── Ontology and Controlled Vocabulary
├── Source Register
├── Theme Registry
│   ├── CF-001 <canonical theme label>
│   ├── CF-002 <canonical theme label>
│   └── ...
└── Friction Briefs
    ├── 2026-08-03 to 2026-08-09
    └── ...
```

Create only the pages required by the current use case. A separate page per theme
is useful once the theme has enough evidence or history to justify one; early
candidate themes may remain in the registry table.

Keep decision records or product commitments in their existing authoritative
system. Link to them from a theme page rather than turning the friction ontology
into a replacement backlog or ADR system.

## Stable identifiers

Use identifiers with stable prefixes:

- `CF-###` — Customer Friction Theme
- `FO-###` — Friction Observation when durable observation IDs are useful
- `CQ-###` — Competency Question when explicitly tracked
- `FC-###` — Controlled vocabulary concept when a stable concept ID is needed

Do not reuse identifiers. When a concept or theme is replaced, retain the old ID
and mark it `superseded` or `deprecated` with a link to the replacement.

## Core entity types

### CustomerFrictionTheme

A recurring failure mechanism or customer-effort pattern that can manifest across
one or more pieces of evidence.

Required fields:

- `theme_id`
- `canonical_label`
- `definition`
- `status`
- `first_seen`
- `last_seen`
- `evidence_strength`
- `decision_priority`
- `products_or_services`
- `journey_stages`
- `channels`
- `member_intents`
- `failure_mechanisms`
- `consequences`
- `evidence_observations`
- `corroborating_signals`
- `contradicting_signals`
- `hypotheses`
- `owner` when known
- `next_test`
- `limitations`

Recommended theme statuses:

- `candidate` — early signal; mechanism not yet stable;
- `emerging` — recurring or strengthening evidence but not yet well corroborated;
- `established` — recurring and sufficiently corroborated to treat as a durable
  friction theme;
- `watch` — known theme without current decision urgency;
- `improving` — evidence suggests reduction, but closure criteria are not met;
- `resolved` — agreed closure criteria are met for the intended scope;
- `disputed` — material evidence or stakeholders disagree about the mechanism;
- `superseded` — replaced by one or more better-defined themes;
- `deprecated` — retained for history but no longer used for classification.

Do not use `resolved` to mean "not observed this week".

### FrictionObservation

One attributable piece of evidence that a customer journey contained friction.

Fields:

- `observation_id` when persisted individually
- `source_type`
- `source_name`
- `source_url_or_identifier`
- `published_or_event_date`
- `retrieved_at`
- `evidence_status`
- `evidence_excerpt_or_paraphrase`
- `member_intent`
- `product_or_service`
- `journey_stage`
- `channel`
- `failure_mechanism`
- `extra_effort`
- `consequence`
- `theme_id` or `candidate-theme`
- `classification_confidence`
- `limitations`

Avoid storing reviewer names or unnecessary personal data.

### MemberIntent

What the customer or member was trying to accomplish.

Examples should be organisation-specific and evidence-backed, such as:

- report a breakdown;
- understand status or ETA;
- renew a membership or policy;
- change personal or vehicle details;
- retrieve documents;
- cancel or change a service;
- understand a price or offer;
- resolve a failed transaction.

Do not create a new intent merely because a source uses different wording.

### JourneyStage

A durable stage in the customer's attempt to achieve an intent.

Start with a minimal generic vocabulary and specialise only when needed:

- discover or understand;
- identify or authenticate;
- initiate;
- submit;
- wait or track;
- fulfil or receive service;
- handoff or escalate;
- resolve;
- follow-up;
- renew, retain, cancel, or leave.

Organisation-specific journeys may add precise stages when ambiguity affects
analysis.

### Channel

Where the interaction or handoff occurs.

Typical values:

- web portal;
- mobile app;
- telephone;
- chat or messaging;
- email;
- roadside or field service;
- third-party partner;
- cross-channel handoff.

Keep the distinction between `channel` and the underlying system or supplier.

### FailureMechanism

The smallest reusable explanation of what failed from the customer's perspective,
without asserting an unverified technical root cause.

Good examples:

- submission appears complete but downstream progress is absent;
- authentication prevents access to an otherwise valid journey;
- context is lost during handoff;
- customer repeats information already supplied;
- status or ETA changes without enough explanation;
- product or entitlement context is inconsistent across channels;
- promised information is not durably available after the interaction;
- self-service path lacks an effective assisted-service escape hatch.

Poor examples:

- bad service;
- app problem;
- customer unhappy;
- agent error;
- API bug, unless directly established by technical evidence.

### ExtraEffort

Additional work imposed on the customer because the intended journey did not
complete smoothly.

Typical values:

- repeated contact;
- repeated information;
- channel switching;
- manual re-entry;
- waiting without useful state information;
- repeated status checks;
- escalation;
- re-authentication;
- workaround outside the expected journey.

### Consequence

Observable or customer-reported result of the friction.

Typical values:

- delay;
- unresolved need;
- repeat contact;
- complaint or escalation;
- cancellation or churn risk;
- failed or reversed transaction;
- safety or vulnerability concern;
- distrust or perceived unfairness;
- additional operational handling.

Do not infer a consequence that the source or internal evidence does not support.

### OperationalSignal

An internal measure that can corroborate, contradict, or contextualise a friction
theme.

Examples:

- digital-to-assisted contact rate;
- repeat-contact rate;
- funnel abandonment;
- authentication failure rate;
- workflow state-transition failure;
- ETA revision frequency;
- status-page repeat checks;
- transfer rate;
- handle time for a named intent;
- cancellation or retention outcome;
- incident or queue state.

Record the source system, metric definition, time window, denominator, and owner
when available. Do not compare metrics whose definitions differ without stating
the mismatch.

### Hypothesis

A testable explanation connecting observations to a possible mechanism.

Fields:

- `statement`
- `supporting_evidence`
- `contradicting_evidence`
- `assumptions`
- `falsifying_observation`
- `status`: `open`, `supported`, `weakened`, `rejected`, or `confirmed-by-owner`

Avoid naming a specific technical root cause until evidence supports it.

### Intervention

A proposed bounded change or experiment intended to reduce uncertainty or customer
effort.

Fields:

- `intervention`
- `theme_id`
- `mechanism_of_action`
- `leading_measure`
- `lagging_measure`
- `risk_or_tradeoff`
- `reversibility`
- `owner`
- `status`

A proposed intervention is not a backlog commitment.

## Relationships

Prefer explicit relationships:

- `observationSupportsTheme`
- `observationContradictsTheme`
- `themeAffectsJourneyStage`
- `themeAffectsChannel`
- `themeAffectsProductOrService`
- `themeOccursDuringIntent`
- `themeCreatesExtraEffort`
- `themeCanLeadToConsequence`
- `operationalSignalCorroboratesTheme`
- `operationalSignalContradictsTheme`
- `hypothesisExplainsTheme`
- `interventionTestsHypothesis`
- `interventionTargetsTheme`
- `themeOwnedBy`
- `themeSupersedesTheme`

Avoid a generic `relatedTo` relationship when a meaningful typed relationship is
available.

## Theme identity rules

Two observations belong to the same theme when the customer-effort mechanism is
materially the same even if:

- the source platform differs;
- the wording differs;
- the product differs;
- the exact UI or system differs.

Split themes when combining them would hide materially different mechanisms or
lead to different investigations.

Examples:

- `cannot log in` and `submitted breakdown but dispatch did not progress` are
  different mechanisms even though both are digital failures;
- `had to repeat details after transfer` and `portal form lost entered data during
  validation` may both involve repetition but belong to different mechanisms if
  they require different interventions;
- `unclear ETA` and `long wait` should not automatically be one theme: elapsed
  service time and uncertainty about operational state can be independently
  measurable.

## Trend semantics

Use trend labels only relative to a defined observed sample and comparable source
coverage:

- `rising`
- `stable`
- `falling`
- `new`
- `insufficient-comparable-data`

Always state the comparison window and sample counts. Do not compare two periods
when source coverage materially changed without qualification.

## Evidence strength

Use:

- `weak`
- `moderate`
- `strong`

Record why. Typical reasons include recurrence, independent corroboration,
contradiction, freshness, source authority, and sample limitations.

## Decision priority

Use:

- `urgent`
- `high`
- `medium`
- `watch`

Priority is a decision aid, not a performance score. Consider customer harm,
severity, recurrence, strategic relevance, operational cost, evidence strength,
and whether a bounded intervention exists.

## Ontology governance

Every controlled-vocabulary term should have:

- stable ID where persistence matters;
- preferred label;
- definition;
- aliases where useful;
- examples and counterexamples when ambiguity is likely;
- status: `proposed`, `confirmed`, `disputed`, `deprecated`, or `superseded`;
- evidence or authoritative source;
- reviewer or owner when confirmed;
- last reviewed date.

When evidence exposes ambiguity:

1. search for an existing concept or alias;
2. determine whether the problem is classification, wording, or genuinely missing
   semantics;
3. prefer an alias or definition refinement over a new concept when identity is
   unchanged;
4. create a `proposed` concept only when a new distinction is decision-relevant;
5. preserve the previous definition and identifier when superseding;
6. request human confirmation for canonical terminology that affects cross-team
   interpretation.

Do not encode temporary operational thresholds, mutable product policy, or an
unverified causal explanation as timeless ontology truth.

## Confluence page templates

### Theme page

```text
# CF-### Canonical theme label

## Definition
<failure mechanism from the customer perspective>

## Status
- Theme status:
- Evidence strength:
- Decision priority:
- First seen:
- Last seen:
- Owner:

## Customer journey
- Member intent:
- Product/service:
- Journey stage:
- Channel:
- Extra effort:
- Consequence:

## Evidence
### Supporting observations
<dated, attributable observations>

### Corroborating operational signals
<metrics or internal evidence with definitions>

### Contradicting evidence
<keep visible>

## Hypotheses
<leading and competing explanations>

## Next test
<smallest query, instrumentation change, or experiment>

## Decisions and experiments
<link to authoritative decision or delivery systems; do not duplicate ownership>

## History
<material status, definition, split, merge, or supersession events>
```

### Source register

Track:

- source name;
- source type;
- access method;
- what claims it can establish;
- known bias or limitations;
- expected freshness;
- owner or steward;
- sensitivity classification;
- last successfully accessed.

### Ontology change log

For every material change record:

- date;
- changed concept or relationship;
- previous state;
- new state;
- reason;
- supporting evidence;
- authoring agent or person;
- human reviewer when applicable.
