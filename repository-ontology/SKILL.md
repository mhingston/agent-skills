---
name: repository-ontology
description: Evaluate, establish, validate, or evolve an ontology for a software repository. Use when asked to identify repository or domain concepts, create a shared vocabulary, model architectural or business relationships, assess an existing ontology, improve semantic grounding for agents, or determine whether a repository would benefit from an ontology or knowledge graph.
compatibility: Requires read access to relevant repository evidence. Formal RDF, OWL, SHACL, or reasoner validation also requires suitable ontology tooling.
---

# Repository Ontology

Establish the smallest evidence-backed semantic model that helps a named consumer
answer concrete questions or control behaviour. Do not create an ontology merely
to document every file, class, table, or dependency.

## Modes

- **Assess** — determine whether existing semantic assets are sufficient.
- **Establish** — create an initial glossary, taxonomy, typed model, graph, or
  formal ontology.
- **Evolve** — propose controlled changes to an existing model.

Always assess before establishing or evolving.

### Glossary-first active evolution

When the current verdict is `glossary-sufficient` and the primary problem is
shared language rather than graph traversal or formal validation, use a lightweight
active evolution path instead of escalating to a richer ontology.

Work from the term currently causing ambiguity or model drift:

1. locate its current definition, aliases, examples, and authoritative sources;
2. identify the competing meanings or the fuzzy boundary that matters;
3. test proposed wording with concrete examples, counterexamples, and edge-case
   scenarios that force the distinction to become observable;
4. compare the proposed meaning with current code, schemas, tests, and accepted
   domain/architecture decisions without treating implementation prevalence as
   semantic authority;
5. resolve the term only when authoritative evidence or an accountable reviewer
   discriminates between the alternatives; otherwise preserve `ambiguous` or
   `disputed` status;
6. update only the minimum glossary/model surface needed to make the resolved
   meaning durable and check downstream aliases/mappings for drift.

Prefer doing this while the ambiguous term is actively affecting a design,
refinement, review, or investigation rather than creating a large vocabulary
workshop detached from a concrete consumer need.

When resolving terminology exposes a durable decision, recommend a separate ADR
or decision record only when all three are true:

- the choice is materially costly to reverse;
- a future maintainer could reasonably be surprised by it without the rationale;
- the result reflects a real trade-off between credible alternatives.

Otherwise keep the decision local to the glossary/model evidence. Do not create an
ADR for every naming clarification or obvious implementation consequence.

## Core principles

### Prefer the minimum sufficient model

Choose the least expressive representation that answers the competency questions:

1. glossary for consistent terminology;
2. taxonomy for categorisation and broader/narrower relationships;
3. typed concept model for explicit entities, relationships, and constraints;
4. RDF or JSON-LD graph for global identifiers, graph queries, or interoperability;
5. OWL for formal semantics and inference;
6. SHACL or equivalent for validating operational graph data.

Do not select a formalism because it appears sophisticated.

### Ground every material assertion

A repository identifier is not automatically a domain concept. Do not infer
canonical meaning from filenames, class names, database tables, routes, comments,
directory layout, generated documentation, or one isolated implementation.

Prefer maintained authoritative sources and multiple independent evidence types.
Treat ambiguous interpretations as hypotheses requiring review.

### Keep semantic layers distinct

Classify concepts as one or more of:

- domain;
- architecture;
- implementation;
- delivery;
- governance;
- agent operation.

Do not collapse a domain concept into its current class, table, service, or file.

### Keep authority and delivery artefacts distinct

Distinguish:

1. **source evidence** — repository and authoritative external sources;
2. **ontology or meaning model** — governed concepts, definitions, and relations;
3. **semantic layer** — identifiers, mappings, assertions, transformations, and
   instances that apply the meaning model to sources;
4. **delivery representations** — generated documents, graph projections, indexes,
   embeddings, caches, or APIs prepared for consumers.

An ontology does not replace its evidence. A generated graph, document, or index
is not authoritative merely because consumers query it. Preserve lineage across
all layers.

### Preserve provenance and uncertainty

For each material assertion record source, repository location, revision when
relevant, evidence type, confidence, status, and reviewer when confirmed.

Use these statuses precisely:

- `observed` — directly present in evidence;
- `inferred` — reasoned from observations;
- `ambiguous` — two or more materially different interpretations remain
  consistent with the available evidence and the evidence does not discriminate
  between them;
- `confirmed` — accepted by an authorised human or authoritative source;
- `disputed` — authoritative or attributable meanings or evidence conflict;
- `deprecated` — retained for compatibility but no longer preferred.

`ambiguous` and `disputed` are not synonyms. Use `ambiguous` when several
interpretations fit the evidence without an authoritative conflict; use `disputed`
when sources or authorities positively disagree. Never present an inferred or
ambiguous assertion as confirmed.

## Evidence inputs

Use relevant maintained evidence such as:

- README, contributor, architecture, domain, and decision documentation;
- glossaries, taxonomies, diagrams, and existing ontology assets;
- public types, interfaces, APIs, messages, events, and schemas;
- database schemas and migrations;
- tests, fixtures, and acceptance scenarios;
- configuration, deployment, package, ownership, and governance files;
- version-control, issue, and pull-request history when materially useful.

Treat generated, duplicated, and historical sources as lower authority unless the
repository explicitly designates them as canonical.

## Core workflow

### 1. Establish purpose and ownership

Identify:

- the decision, workflow, retrieval task, validation, or agent behaviour the model
  must support;
- the human or software consumer;
- the maintainer and update trigger;
- success criteria and acceptable maintenance cost.

Examples include mapping capabilities to code, tracing requirements to tests,
identifying event relationships, routing agents, validating action preconditions,
or preserving canonical vocabulary.

If no concrete consumer or use case exists, recommend against a formal ontology.

### 2. Inventory existing semantic assets and gaps

Search for existing glossaries, schemas, type systems, domain models, architecture
models, metadata vocabularies, knowledge graphs, policy definitions, and generated
documentation.

Determine whether the repository already has a sufficient implicit or distributed
model. The absence of RDF or OWL does not mean no ontology exists; a dependency
graph alone is not an ontology.

Identify bounded semantic gaps or Knowledge Debt relevant to the intended use:

- opaque, overloaded, unstable, or conflicting identifiers;
- undocumented codes, flags, states, units, or abbreviations;
- relationships represented only by joins, conventions, or human knowledge;
- rules embedded only in code, queries, pipelines, or procedures;
- missing ownership, source authority, provenance, or lineage;
- stale generated representations or retrieval indexes;
- retrieval units that require substantial runtime reconstruction.

Rank gaps by competency-question relevance, interpretation risk, consumer value,
evidence availability, and maintenance cost. Treat this as a remediation backlog,
not justification to model the entire repository.

### 3. Define competency questions

Write bounded questions the model must answer. For each question record:

- intended consumer;
- why the answer matters;
- required concepts and relationships;
- example answer;
- expected supporting evidence;
- acceptance test.

Reject questions too broad to test. Prefer questions such as:

- Which service implements this business capability?
- Which events can change this aggregate's state?
- Which tests validate this requirement or invariant?
- Which source is authoritative for this concept?
- Which action may an agent perform on this artefact, under what preconditions?
- Which assertions are confirmed, inferred, ambiguous, disputed, or stale?

### 4. Decide whether an ontology is warranted

Return one verdict:

- `not-needed`;
- `glossary-sufficient`;
- `taxonomy-sufficient`;
- `typed-concept-model`;
- `semantic-graph`;
- `formal-ontology`;
- `operational-ontology`.

Base the verdict on competency questions and consumers, not repository size or
novelty. Explain why simpler alternatives such as documentation, JSON Schema,
OpenAPI, static analysis, or a dependency graph are or are not sufficient.

When the verdict is `glossary-sufficient`, prefer the active glossary evolution
path above for concrete terminology problems instead of continuing through graph
or formal-model steps that do not serve the consumer.

### 5. Reuse before inventing

Before defining a new canonical concept or property, inspect applicable,
maintained standards and vocabularies.

For every candidate external term decide whether to:

- reuse directly;
- specialise locally;
- map as equivalent, broader, narrower, or related;
- use only as an interchange mapping;
- reject because its meaning, scope, licence, or governance does not fit.

Record the vocabulary name, namespace, version, maintenance status, licence, and
material semantic differences. Do not import an entire external ontology when a
small reviewed subset or mapping is sufficient.

### 6. Build an evidence-backed term inventory

For each candidate term record:

- identifier and preferred label;
- discriminating definition;
- semantic layer;
- status, confidence, and provenance;
- synonyms, homonyms, deprecated terms, ambiguities, and conflicts;
- examples and counterexamples;
- implementation-specific names that must not become canonical terminology.

For a material `ambiguous` term or relationship, record the plausible
interpretations, evidence compatible with each, why choosing between them matters,
and the smallest evidence or accountable review that would discriminate between
them.

Stress-test proposed definitions with concrete scenarios when a term's boundary is
still fuzzy. Prefer examples that force neighbouring concepts apart: lifecycle
edges, partial/whole operations, ownership changes, identity collisions, empty or
error states, and other cases where two plausible definitions produce different
answers. A definition that only works for the happy-path example is not yet
sufficiently discriminating.

Cross-check resolved language against implementation evidence to reveal drift, but
do not let the dominant class/table/function name establish canonical meaning by
frequency. When code and the proposed model disagree, classify whether the code,
model, mapping, or evidence is wrong before changing the term.

Avoid circular definitions. Resolve terminology conflicts or ambiguity only when
authoritative evidence supports the choice; otherwise preserve the alternatives
or disagreement.

### 7. Construct the minimum conceptual model

Model only concepts and relationships required by the competency questions.

For each concept define identity criteria, lifecycle or state when relevant,
required and optional properties, broader concept, provenance requirements,
examples, and counterexamples.

For each relationship define source, target, direction, meaning, justified
cardinality, temporal characteristics, evidence, examples, and counterexamples.
Prefer precise relationships such as `implements`, `owns`, `publishes`,
`consumes`, `dependsOn`, `validates`, `governedBy`, `authorisedBy`,
`derivedFrom`, and `supersedes`. Avoid vague `relatedTo` edges.

Use top-down and bottom-up modelling as reciprocal checks:

- top-down definitions establish intended meaning, scope, identity, and invariants;
- bottom-up repository evidence tests those definitions and exposes missing terms,
  aliases, exceptions, and drift.

Classify mismatches as a source defect, model defect, mapping-rule defect,
legitimate exception, or unresolved disagreement. Do not let observed frequency
establish canonical meaning automatically, and do not accept an expert model that
cannot classify representative evidence or answer its competency questions.

When the verdict requires RDF, JSON-LD, OWL, SHACL, formal axioms, or operational
agent constraints, read
[`references/formal-modeling.md`](references/formal-modeling.md) before
formalisation.

When the model will be populated from repository evidence or published through an
agent, semantic API, knowledge graph, search index, vector store, cache, or
generated semantic representation, read
[`references/semantic-operationalisation.md`](references/semantic-operationalisation.md).

When the model will validate or govern proposed tool calls, intermediate results,
or resulting state inside a live agent workflow, read
[`references/runtime-agent-validation.md`](references/runtime-agent-validation.md).

### 8. Validate usefulness and correctness

Test every competency question against the proposed model. Check:

- coverage — required concepts and relations exist;
- answerability — the model can produce the expected answer;
- evidence — answers trace to repository sources;
- ambiguity — materially different interpretations remain visible until evidence
  or authorised review discriminates between them;
- conflict — authoritative disagreements remain visible rather than being
  smoothed into a single answer;
- consistency — identifiers and constraints do not contradict each other;
- minimality — removing an element would break a competency question;
- maintenance — ownership and refresh triggers are explicit;
- agent safety — permissions, evidence, and mutable policy are not confused with
  domain truth.

For formal models, run parser, schema, constraint, and reasoner checks appropriate
to the chosen language. Report unavailable tooling rather than claiming formal
validation.

For AI-facing or indexed representations, test competency questions against the
published consumer representation as well as the conceptual model. Verify
identity resolution, evidence lineage, freshness filtering, access enforcement,
update visibility, and behaviour when evidence conflicts, is ambiguous, or is
missing.

For runtime action governance, validate the complete proposal-to-effect path:
typed boundaries, semantic reasoning, operational constraints, authority,
transactional preconditions, side-effect execution, and postcondition
verification. A reasoner or validator result is not an enforcement guarantee
unless the side-effecting boundary consumes it and fails closed.

### 9. Review with domain and operational owners

Ask authorised reviewers to confirm definitions, ambiguous or disputed terms,
external vocabulary mappings, authority, constraints, conversion rules,
publication controls, runtime enforcement boundaries, and maintenance ownership.
Record decisions and rejected alternatives. Human confirmation changes status;
model confidence does not.

When a terminology/model resolution creates a lasting decision record candidate,
apply the three-part ADR test from the glossary-first path. Record a separate ADR
only for a hard-to-reverse, non-obvious, real trade-off; do not turn glossary
maintenance into a stream of ceremonial decisions.

### 10. Publish incrementally

Prefer a small versioned model plus provenance over a large speculative graph.
For large repositories, partition by competency question, domain boundary, or
semantic layer; reconcile identifiers and conflicts before adding cross-boundary
relationships.

Keep schema, instances, validation constraints, mutable policy, conversion rules,
runtime enforcement, and consumer delivery representations in distinct artefacts
or clearly separated sections.

Do not publish semantic data to agents, graphs, APIs, indexes, embeddings, or
caches without source and rule lineage, refresh and invalidation paths, sensitivity
controls, and a way to suppress or explicitly represent ambiguous, disputed, or
stale assertions.

### 11. Repair preventable ambiguity at the source

When analysis reveals ambiguity that can be corrected safely and cheaply in the
repository, recommend the smallest source-level improvement, such as clearer
names, descriptions for codes and fields, machine-readable ownership, stable
identifiers, deprecation links, provenance hooks, or canonical-source declarations.

Do not create a permanent ontology workaround when a compatible source change
would remove the ambiguity for every consumer.

## Output contract

Return:

1. purpose, consumer, maintainer, and evidence scope;
2. competency questions and acceptance tests;
3. verdict and rejected simpler or more complex alternatives;
4. external-vocabulary reuse and mapping decisions;
5. evidence-backed term inventory, unresolved ambiguities, and conflicts;
6. prioritised semantic gaps relevant to the competency questions;
7. minimum conceptual model;
8. provenance, status, and confidence register;
9. validation results and limitations;
10. maintenance and review plan;
11. semantic operationalisation plan when derived or AI-facing representations are
    in scope;
12. runtime validation and enforcement plan when live agent actions are in scope;
13. recommended next increment or `no further formalisation`.

For `glossary-sufficient` evolution, keep this output proportionate: a compact term
diff, examples/counterexamples, unresolved ambiguity, provenance, reviewer need,
and downstream mapping impact can replace the heavier model sections that are not
applicable.

Read
[`references/output-contracts.md`](references/output-contracts.md) when producing
machine-readable inventories, concept models, formalisation proposals, semantic
conversion artefacts, runtime validation artefacts, or audit reports.

## Failure and stop conditions

Stop or downgrade the verdict when:

- no concrete consumer or competency questions can be established;
- repository evidence is insufficient, materially ambiguous, or contradictory for
  a required conclusion;
- a simpler maintained artefact already answers the questions;
- no owner can review or maintain the model;
- formal validation is required but unavailable;
- proposed semantics would encode mutable policy as timeless domain truth;
- the model cannot answer its own acceptance tests;
- source identities cannot be reconciled safely for the intended use;
- conversion rules cannot be explicit, versioned, and reviewed;
- an AI-facing delivery mechanism cannot preserve lineage, enforce required access
  controls, or support refresh and invalidation;
- a live action cannot be separated into a proposal and controlled execution;
- mandatory runtime validation, authority, transactional enforcement, or
  postcondition observation cannot be performed for the action's risk.

Report the missing evidence, unresolved interpretations, conflict, or decision and
the smallest recovery action. Do not fill gaps with plausible terminology,
generated axioms, opaque conversion prompts, or inferred authority.
