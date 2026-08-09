# Customer Friction Ontology

Use this reference when the user asks to establish, read, or evolve a persistent Customer Friction Radar model.

The ontology is intentionally lightweight: a governed controlled vocabulary and relationship model for recurring customer-friction analysis, not a full enterprise knowledge graph. Persistence is optional.

## Contents

- [Competency questions](#competency-questions)
- [Minimal persistent structure](#minimal-persistent-structure)
- [Core concepts](#core-concepts)
- [Relationships](#relationships)
- [Evidence and concept status](#evidence-and-concept-status)
- [Theme naming rules](#theme-naming-rules)
- [Theme page template](#theme-page-template)
- [Source register template](#source-register-template)
- [Ontology change record](#ontology-change-record)

## Competency questions

The model should help answer:

1. What was the customer trying to do?
2. At which journey stage and channel did friction occur?
3. What failure mechanism created extra effort or a poor outcome?
4. Which products, services, systems or operational processes are implicated by evidence?
5. Which evidence supports or contradicts the theme?
6. Is the signal new, recurring, strengthening, weakening or resolved?
7. Which internal measure could corroborate or falsify the interpretation?
8. Which owner/team should investigate the journey without assigning blame?
9. What bounded experiment or instrumentation change could reduce uncertainty?

If a proposed ontology element does not help answer one of these questions, do not add it by default.

## Minimal persistent structure

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
    ├── YYYY-MM-DD to YYYY-MM-DD
    └── ...
```

Prefer one page per durable friction theme. Evidence instances may remain in a theme page, child page, table, or linked source depending on volume and sensitivity.

## Core concepts

### CustomerFrictionTheme

A recurring, evidence-backed failure mechanism that creates avoidable customer effort, uncertainty, delay, loss of context, inconsistent outcomes, or inability to complete an intended journey.

Properties:

- `theme_id` — stable `CF-###`;
- `canonical_label`;
- `definition`;
- `status`;
- `first_seen`;
- `last_seen`;
- `trend`;
- `evidence_strength`;
- `decision_priority`;
- `affected_intents`;
- `journey_stages`;
- `channels`;
- `products_services`;
- `candidate_owners`;
- `leading_hypothesis`;
- `competing_hypotheses`;
- `corroborating_signals`;
- `contradicting_signals`;
- `next_test`;
- `reviewed_by`;
- `last_reviewed_at`.

Theme lifecycle:

- `candidate`;
- `active`;
- `watch`;
- `disputed`;
- `resolved`;
- `superseded`.

Do not reuse a retired theme ID for a new meaning.

### FrictionObservation

One attributable observation supporting or challenging a theme.

Properties:

- `observation_id`;
- `source_id`;
- `source_type`;
- `observed_at`;
- `retrieved_at`;
- `customer_intent`;
- `journey_stage`;
- `channel`;
- `product_service`;
- `friction_mechanism`;
- `extra_effort`;
- `consequence`;
- `evidence_excerpt_or_paraphrase`;
- `evidence_url_or_identifier`;
- `classification_confidence`;
- `evidence_status`;
- `linked_theme_ids`.

Avoid storing unnecessary personally identifying information.

### MemberIntent / CustomerIntent

What the customer is trying to accomplish.

Examples:

- join/purchase;
- authenticate;
- manage membership;
- report breakdown;
- check breakdown status;
- update details;
- access documents;
- renew;
- query renewal;
- claim;
- cancel;
- seek support;
- understand outcome.

Keep this taxonomy small. Add terms only when recurring evidence cannot be classified adequately.

### JourneyStage

Where in the journey friction occurs.

Suggested vocabulary:

- discover;
- authenticate;
- initiate;
- provide-information;
- confirm-submit;
- processing;
- wait;
- status-tracking;
- assisted-handoff;
- agent-interaction;
- fulfilment;
- post-interaction;
- renew;
- cancel;
- recover-from-failure.

### Channel

Examples:

- web;
- mobile app;
- phone;
- chat;
- email;
- roadside;
- third-party;
- cross-channel.

### FailureMechanism

The mechanism creating friction. Prefer mechanisms over symptoms.

Candidate vocabulary:

- submission-not-progressed;
- lost-context-during-handoff;
- repeated-information;
- unclear-operational-state;
- unstable-or-misleading-eta;
- authentication-failure;
- entitlement-or-product-context-mismatch;
- transfer-or-routing-friction;
- inaccessible-post-interaction-information;
- inconsistent-offer-context;
- broken-notification;
- avoidable-assisted-contact;
- unclear-next-action;
- duplicate-contact;
- unresolved-after-contact.

New mechanisms begin as `proposed`.

### ExtraEffort

Examples:

- repeat-information;
- retry-action;
- switch-channel;
- wait-without-state;
- contact-support;
- repeat-contact;
- negotiate;
- re-authenticate;
- provide-proof-again;
- chase-update.

### Consequence

Examples:

- delayed-service;
- failed-self-service;
- avoidable-contact;
- repeat-contact;
- unresolved-case;
- complaint;
- cancellation-risk;
- retention-risk;
- payment-impact;
- safety-or-vulnerability-risk;
- reduced-trust.

### OperationalSignal

An internal quantitative or event-based observation that may corroborate or contradict a customer-friction theme.

Examples:

- API error rate;
- failed workflow transition;
- queue duration;
- ETA revision count;
- abandoned funnel step;
- status-page recheck frequency;
- call within N minutes of digital attempt;
- repeat-contact rate;
- transfer count;
- cancellation outcome.

### Hypothesis

A falsifiable explanation for why a friction theme occurs.

Keep hypotheses separate from canonical ontology definitions.

Properties:

- `hypothesis_id`;
- `claim`;
- `supporting_evidence`;
- `contradicting_evidence`;
- `assumptions`;
- `falsifier`;
- `status` (`open`, `supported`, `weakened`, `rejected`, `confirmed-by-owner`);
- `reviewer`.

### Intervention

A bounded experiment, instrumentation change or product/process change proposed to test or reduce friction.

An intervention is not automatically a commitment.

Properties:

- `intervention_id`;
- `theme_id`;
- `mechanism_of_action`;
- `scope`;
- `expected_signal_change`;
- `leading_measure`;
- `lagging_measure`;
- `risks`;
- `reversibility`;
- `decision_owner`;
- `status`.

## Relationships

Use explicit relationships where helpful:

- `observation SUPPORTS theme`;
- `observation CONTRADICTS theme`;
- `theme AFFECTS intent`;
- `theme OCCURS_AT journey_stage`;
- `theme OCCURS_IN channel`;
- `theme AFFECTS product_service`;
- `theme CORROBORATED_BY operational_signal`;
- `theme EXPLAINED_BY hypothesis`;
- `hypothesis TESTED_BY intervention`;
- `theme SUPERSEDES theme`;
- `theme RELATED_TO theme` only as a last resort.

Avoid encoding causal edges unless evidence supports causality.

## Evidence and concept status

Ontology term status:

- `proposed`;
- `confirmed`;
- `disputed`;
- `deprecated`;
- `superseded`.

Evidence status:

- `observed`;
- `inferred`;
- `corroborated`;
- `contradicted`;
- `confirmed`;
- `stale`.

Human confirmation must be attributable.

## Theme naming rules

Name the mechanism, not the emotion.

Good:

- `Digital submission appears complete but does not progress`
- `Member context is lost during assisted handoff`
- `Operational state is not clear enough to prevent status-seeking contact`

Poor:

- `Bad app`
- `Communication problems`
- `Angry customers`
- `Poor service`

## Theme page template

```markdown
# CF-### — <canonical label>

## Definition
<one discriminating definition>

## Status
- Lifecycle:
- Evidence strength:
- Decision priority:
- Trend:
- First seen:
- Last seen:
- Last reviewed:

## Affected journey
- Customer intents:
- Journey stages:
- Channels:
- Products/services:

## Evidence
### Supporting
| Date | Source | Observation | Evidence status | Link |
| --- | --- | --- | --- | --- |

### Contradicting
| Date | Source | Observation | Evidence status | Link |
| --- | --- | --- | --- | --- |

## Internal signals
| Signal | Observation | Window | Interpretation | Link |
| --- | --- | --- | --- | --- |

## Hypotheses
### Leading
- Claim:
- Supporting evidence:
- Contradicting evidence:
- Falsifier:

### Alternatives
...

## Next bounded test
- Action:
- Owner:
- Success evidence:
- Stop/revisit condition:

## Decision history
| Date | Decision | Owner | Rationale | Evidence |
| --- | --- | --- | --- | --- |
```

## Source register template

```markdown
| Source ID | Source | Type | Strong for | Weak for | Freshness | Access/sensitivity | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

## Ontology change record

Every material vocabulary change should record:

- date;
- term/relationship;
- action: add/change/deprecate/supersede;
- previous meaning when applicable;
- proposed meaning;
- reason;
- supporting evidence;
- authoring agent/person;
- human reviewer when applicable.

Do not silently redefine accepted terms.
