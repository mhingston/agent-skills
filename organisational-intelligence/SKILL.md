---
name: organisational-intelligence
description: Investigate consequential organisational questions by combining authoritative internal evidence, explicit source precedence, semantic relationships where available, relevant external frameworks, competing explanations, and human-verifiable reasoning into a defensible decision brief. Use when work spans multiple organisational systems, sources disagree, tacit knowledge must be made explicit, or a decision needs traceable evidence rather than a retrieval dump.
compatibility: Requires read access to relevant organisational evidence. External framework research may require web access. Ontologies and knowledge graphs are optional inputs, not prerequisites.
---

# Organisational Intelligence

Turn fragmented organisational evidence into a bounded, traceable decision brief.
Do not treat retrieval volume, an ontology, a knowledge graph, or a single expert
framework as sufficient evidence of understanding.

## Core principles

### Start from the decision

Frame the work around a concrete decision, uncertainty, blockage, or competency
question. Reject open-ended requests to "understand the organisation" unless they
can be narrowed to an observable outcome.

Prefer questions such as:

- Why is this customer journey generating avoidable contact?
- Which capability is constrained by this process or dependency?
- Which source is authoritative when policy, implementation, and operational
  evidence disagree?
- Which intervention is best supported by current evidence?
- What organisational knowledge is missing before this decision can be made?

### Separate evidence, semantics, frameworks, and judgement

Keep these layers distinct:

1. **evidence** — what organisational sources say or show;
2. **source authority** — which source is authoritative for which type of claim;
3. **semantic context** — definitions, entity identities, relationships, and
   constraints from glossaries, ontologies, knowledge graphs, schemas, or other
   maintained meaning models;
4. **reasoning frameworks** — explicit external or internal models used to
   interpret evidence;
5. **analysis** — hypotheses, synthesis, trade-offs, and recommendations;
6. **human judgement** — accepted, rejected, deferred, or superseded decisions.

Do not let one layer silently substitute for another.

### Prefer the minimum sufficient evidence map

Do not ingest every system. Identify only the sources needed to answer the
question and assign each a role, authority, freshness expectation, and known
limitations.

Typical source roles include:

- strategy and policy;
- planning and execution;
- implementation and architecture;
- service or capability ownership;
- operational telemetry;
- customer evidence;
- financial or performance metrics;
- historical decisions and rationale.

### Treat source authority as claim-specific

Authority is contextual. A strategy document may be authoritative for intended
outcomes but not current runtime behaviour. Production telemetry may be
canonical for observed service state but not business policy.

For every material claim, record which source types can establish it and which
sources are only supporting or contradictory evidence.

### Use ontologies and knowledge graphs when they reduce interpretation risk

A semantic model may help resolve concepts, identities, ownership, dependencies,
customer journeys, processes, systems, metrics, or capabilities. It is an input to
organisational reasoning, not the end product.

Do not require a graph when a glossary, source map, or small typed concept model
is sufficient. Do not infer canonical meaning from graph connectivity alone.

### Apply explicit frameworks, not implicit taste

When interpreting evidence, select one to three relevant frameworks from trusted,
inspectable sources. Examples may include SRE, DORA, Team Topologies, domain-
driven design, queueing theory, service design, control theory, incident analysis,
or organisation-specific operating models.

For each framework record:

- why it applies;
- which assumptions must hold;
- which observed evidence supports or violates those assumptions;
- what the framework predicts or recommends;
- limitations and failure conditions.

Search for a competing framework, counterexample, or disconfirming condition when
that could materially change the recommendation.

### Preserve contradiction, ambiguity, and uncertainty

Do not reconcile conflicting or multiply interpretable evidence by averaging it
into a smooth narrative. Distinguish:

- **unknown** — required evidence is missing, inaccessible, or insufficient;
- **ambiguous** — two or more materially different interpretations remain
  consistent with the evidence and the evidence does not discriminate between
  them;
- **conflicting** — attributable or authoritative sources positively disagree.

Classify material contradictions and ambiguities such as:

- intended state versus observed state;
- documented ownership versus actual operational responsibility;
- policy versus implementation;
- aggregate metric versus customer-level evidence;
- stale source versus current source;
- competing definitions of the same organisational concept;
- one metric, identifier, or relationship supporting multiple plausible meanings;
- evidence that supports several causal explanations without discriminating
  between them.

Keep unresolved alternatives and contradictions visible and state what evidence
would resolve or discriminate between them.

## Core workflow

### 1. Frame the question and stop condition

Identify:

- the concrete decision, uncertainty, or blockage;
- the decision owner or intended consumer;
- why the answer matters now;
- the maximum useful scope;
- the smallest evidence set likely to resolve it;
- a stop condition for sufficient evidence.

A good stop condition is decision-oriented, for example: "stop when the leading
explanation is supported by two independent evidence types and the main competing
explanation has been tested."

If no decision or useful competency question can be established, return a bounded
question set instead of performing broad organisational discovery.

### 2. Build the evidence and authority map

Identify the minimum relevant systems and artefacts. For each source record:

- source name and type;
- claims it is authoritative for;
- claims it cannot establish;
- owner or steward when known;
- freshness or revision;
- access and sensitivity constraints;
- known duplication, lag, or quality issues.

Define precedence only where sources can conflict. Do not create one global
ranking for all evidence.

### 3. Retrieve minimally sufficient evidence

Query sources according to the evidence map. Preserve:

- exact identifiers or links;
- dates or revisions;
- attributable statements;
- quantitative observations;
- negative evidence and missing expected evidence;
- ambiguity and contradictions.

Prefer current authoritative material over generated summaries. Use summaries for
navigation, not as replacements for inspectable source evidence when the claim is
material.

### 4. Scan and resolve material ambiguity

Before synthesis, identify ambiguity whose resolution could change the decision,
explanation, scope, ownership, or recommendation. Check at least:

- terminology and entity identity;
- source scope and applicability;
- ownership, authority, and responsibility;
- temporal meaning and effective dates;
- metric, field, and aggregation semantics;
- causal interpretation;
- intended versus observed behaviour;
- requirement, policy, or process interpretation.

Use existing organisational definitions, schemas, glossaries, ontologies, or
knowledge graphs when available. Do not silently select the conventional,
simplest, or most coherent interpretation merely because it is plausible.

For each material unresolved ambiguity record:

- the ambiguous question;
- plausible interpretations;
- evidence compatible with or against each interpretation;
- why the distinction matters;
- the smallest evidence, experiment, or accountable human judgement that would
  discriminate between them.

For unresolved terms distinguish observed usage, inferred meaning, confirmed
canonical meaning, ambiguous meaning, and disputed meaning. If ambiguity does not
materially affect the current decision, note it proportionately and continue. If
it materially blocks the decision, recommend the smallest semantic or evidence
remediation rather than expanding the entire model.

### 5. Form competing hypotheses

State at least one leading explanation and one credible alternative when the
question is causal or diagnostic.

For each hypothesis record:

- supporting evidence;
- contradicting evidence;
- assumptions;
- evidence still needed;
- what observation would falsify it.

Do not move directly from correlation to intervention. When the same evidence is
compatible with several explanations, preserve that ambiguity until a
material discriminator is available.

### 6. Select applicable reasoning frameworks

Choose the smallest set of frameworks that add explanatory or decision value.
Prefer primary, standards-based, research-backed, or operator-authored sources.

Reject a framework when its assumptions do not fit the organisational context.
Do not use a framework merely because it is well known.

Where material, test whether a competing framework or known failure mode changes
the interpretation.

### 7. Synthesize by finding, not by source

Organise the analysis around material findings and decisions rather than producing
a sequence of source summaries.

For each finding include:

- claim;
- evidence;
- source authority;
- semantic interpretation when needed;
- applicable framework;
- ambiguity, contradiction, or uncertainty;
- confidence;
- decision relevance.

Keep factual evidence and model-generated interpretation visibly separate. If a
finding depends on choosing among unresolved interpretations, present the
conditional alternatives rather than collapsing them into one conclusion.

### 8. Evaluate interventions

For each viable intervention record:

- mechanism of action;
- evidence it addresses;
- assumptions;
- expected benefit;
- cost or organisational friction;
- risks and failure modes;
- reversibility;
- measurable leading and lagging indicators;
- smallest vertical slice that can test it.

Prefer a bounded experiment when evidence is insufficient or ambiguous enough to
make a broad organisational change speculative.

### 9. Produce a decision brief

Return:

1. decision or question;
2. evidence scope and source-authority map;
3. material findings;
4. material ambiguities, semantic relationships, and relevant ontology/graph
   relationships;
5. leading and competing hypotheses;
6. frameworks used and why they apply;
7. contradictions, missing evidence, and limitations;
8. options and trade-offs;
9. recommendation or `insufficient-evidence`;
10. confidence and what would change the conclusion;
11. smallest next action or vertical slice;
12. human verification required before action.

Cite material evidence and external framework sources directly.

### 10. Preserve accepted decisions separately

The analysis is not the decision record. When a human accepts, rejects, defers,
or supersedes a recommendation, preserve the resulting decision, rationale,
assumptions, rejected alternatives, owner, evidence, and revisit conditions in an
appropriate durable decision system.

Do not silently convert a recommendation into accepted organisational direction.

## Optional semantic integration

When a maintained ontology or knowledge graph exists, use it to improve:

- entity resolution;
- cross-system joins;
- capability-to-system mapping;
- ownership and dependency tracing;
- process and customer-journey reasoning;
- metric and policy interpretation;
- provenance and lineage.

Validate graph-derived claims against source evidence and freshness requirements.
The graph may accelerate discovery but does not create authority by itself.

When analysis exposes a recurring semantic gap, formulate a bounded competency
question and propose the smallest model extension needed to answer it.

## Failure and stop conditions

Stop or narrow the investigation when:

- no consequential question or decision owner can be identified;
- required evidence is inaccessible or too stale to support the conclusion;
- source authority cannot be established for a material claim;
- material ambiguity makes key evidence incomparable or leaves consequential
  alternatives observationally indistinguishable;
- a framework's assumptions do not hold;
- competing explanations cannot be discriminated with available evidence;
- the likely intervention is broader than the evidence supports;
- sensitive evidence cannot be handled within the required access boundaries;
- further retrieval is producing repetition rather than decision-relevant
  information.

Return the missing evidence, unresolved interpretations, unresolved decision, or
smallest recovery action. Do not fill gaps with plausible organisational lore.

## Quality bar

A strong result should let a reviewer answer:

- What decision is this helping us make?
- Which evidence is authoritative for each important claim?
- What do we know versus infer?
- Which materially different interpretations remain compatible with the evidence?
- What evidence would discriminate between those interpretations?
- Which semantic relationships materially affect the conclusion?
- Which framework shaped the reasoning, and why is it applicable?
- What credible alternative explanation was tested?
- What evidence contradicts the recommendation?
- What would change our mind?
- What is the smallest useful next action?

If those questions cannot be answered, the work is not yet organisational
intelligence; it is still information retrieval or ungrounded synthesis.
