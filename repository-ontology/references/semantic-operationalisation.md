# Semantic operationalisation reference

Read this reference when the semantic model will be populated from repository
sources, exposed through a knowledge graph or semantic API, or used by agents,
enterprise search, retrieval-augmented generation, indexes, or generated semantic
representations.

The ontology defines governed meaning. It does not by itself define how source
evidence becomes maintained, consumer-ready semantic data.

## Keep authority and delivery layers distinct

Distinguish four artefact layers:

1. **Source evidence** — repository files, schemas, code, documentation, history,
   and authoritative external sources.
2. **Ontology or meaning model** — governed concepts, definitions,
   classifications, relationships, and interpretation rules.
3. **Semantic layer** — identifiers, mappings, assertions, transformations,
   constraints, and instances that operationalise the meaning model over source
   evidence.
4. **Delivery representations** — generated documents, graph projections,
   indexes, embeddings, caches, or APIs prepared for specific consumers.

The repository remains the source of evidence unless an authoritative source is
explicitly designated elsewhere. A graph, generated document, vector index, or
cache is not authoritative merely because consumers query it directly.

Preserve lineage from every delivery representation through semantic rules and
assertions to the source revision that supports it.

## Assess semantic readiness

Before building a semantic conversion pipeline, identify bounded semantic gaps or
Knowledge Debt relevant to the competency questions:

- opaque, overloaded, unstable, or conflicting identifiers;
- undocumented abbreviations, codes, flags, states, or units;
- conflicting or circular definitions;
- relationships represented only by joins, naming conventions, directory layout,
  deployment configuration, or human knowledge;
- rules embedded only in code, queries, pipelines, or operational procedures;
- missing source authority, ownership, provenance, or lineage;
- stale generated representations or indexes;
- retrieval units that require substantial runtime reconstruction or guesswork;
- concepts whose meaning depends on one unavailable expert.

Rank each gap by:

- relevance to competency questions;
- risk of incorrect interpretation or action;
- expected consumer value;
- evidence and reviewer availability;
- remediation and ongoing maintenance cost.

Treat the result as a bounded remediation backlog. Do not use semantic debt as a
reason to model the entire repository.

## Preserve source identifiers and add semantic identities

Do not overwrite repository, database, API, package, deployment, or external
identifiers. Introduce a stable semantic identity only when multiple source names
must be reconciled or consumers require identity across representations.

For every semantic identity record:

- semantic identifier and concept type;
- preferred label and aliases;
- source identifiers with source kind and revision;
- collision and ambiguity status;
- rename, merge, split, alias, and deprecation behaviour;
- evidence, status, confidence, reviewer, and observation time.

Example:

```yaml
identifier_mappings:
  - semantic_id: application.claims-intake
    concept: application
    preferred_label: Claims Intake
    source_identifiers:
      - source: repository
        revision: <sha>
        kind: project
        value: src/Claims.Intake/Claims.Intake.csproj
      - source: deployment
        revision: <deployment-revision>
        kind: service-name
        value: claims-intake-api
    aliases: [Claims.Intake, claims-intake-api]
    collision_status: clear
    status: confirmed
    reviewed_by: <reviewer>
    observed_at: <rfc3339>
```

Do not impose one universal semantic-identifier syntax. Define and version the
convention used by the target model.

## Define property semantics explicitly

For every material property, code, state, flag, or measurement required by the
competency questions, define:

- identifier and discriminating definition;
- applicable concept or relationship;
- datatype, cardinality, and null or unknown semantics;
- controlled values and source-to-semantic mappings;
- unit and conversion rule when relevant;
- whether the value is observed or derived;
- derivation rule and dependencies;
- temporal meaning and validity interval;
- sensitivity, access, or permitted-use constraints;
- provenance and refresh requirements.

Example:

```yaml
properties:
  - id: lifecycle-status
    definition: The governed operational lifecycle of the component.
    applies_to: Component
    datatype: controlled-term
    allowed_values: [active, deprecated, retired]
    source_mappings:
      - source_value: prod
        semantic_value: active
      - source_value: decom
        semantic_value: retired
    unit: null
    derived: false
    derivation_rule: null
    temporal_semantics: current-at-revision
    sensitivity: internal
    provenance_required: true
```

Do not assume that a source value is self-explanatory because it is syntactically
valid or consistently used.

## Make conversion rules first-class artefacts

The ontology defines meaning. Versioned semantic rules define how repository
evidence is discovered, interpreted, mapped, validated, published, refreshed,
and retired.

Rule families may include:

- source discovery and selection;
- source-authority resolution;
- interpretation and classification;
- identifier and alias mapping;
- attribute, code, state, and unit mapping;
- relationship and predicate selection;
- derivation and aggregation;
- validation and rejection;
- lineage and evidence capture;
- sensitivity, access, and permitted use;
- publication and consumer projection;
- refresh, invalidation, and deletion;
- drift detection;
- conflict escalation and exception handling;
- retirement and supersession.

For every rule record:

- stable rule identifier and version;
- purpose and applicable competency questions;
- source pattern and authority requirements;
- interpretation or transformation;
- expected output shape;
- evidence and confidence requirements;
- validation checks;
- conflict and escalation behaviour;
- effective period, owner, and approver;
- affected artefacts and rollback behaviour.

Example:

```yaml
semantic_rules:
  - id: MAP-APPLICATION-OWNER-001
    version: 2
    rule_kind: relationship-mapping
    source_pattern:
      artefact: CODEOWNERS
      path_pattern: /src/Claims.Intake/**
    interpretation:
      subject_type: Application
      predicate: ownedBy
      object_type: Team
    output_pattern:
      subject_from: matched_project.semantic_id
      object_from: matched_owner.semantic_id
    evidence_requirements:
      - CODEOWNERS entry is active at the assessed revision
      - owner resolves to a confirmed team identity
    confidence: high
    effective_from: <rfc3339>
    approved_by: <reviewer>
    validation:
      - no unmatched owners
      - no conflicting authoritative ownership source
    escalation:
      - conflicting ownership sources
      - owner cannot be resolved
```

Generated assertions must identify the exact rule version and source records that
produced them. Do not hide semantic conversion inside an unversioned prompt.

## Prepare AI-facing semantic representations only when justified

When an agent or retrieval system would otherwise need to reconstruct a material
instance from many disconnected sources at query time, create a coherent derived
representation for that instance.

Include only information required by competency questions:

- stable semantic identity, type, label, and concise definition;
- material attributes and relationships;
- source lineage and revision;
- assertion status, confidence, freshness, and reviewer state;
- sensitivity, access, and permitted-use metadata;
- ontology and semantic-rule versions;
- generation and last-validation times.

Example:

```yaml
semantic_instance:
  semantic_id: application.claims-intake
  type: Application
  label: Claims Intake
  description: >-
    Customer-facing application responsible for receiving and validating
    insurance claims.
  attributes:
    lifecycle_status: active
  relationships:
    - predicate: implements
      object: capability.submit-claim
    - predicate: ownedBy
      object: team.claims-platform
  lineage:
    repository: owner/repository
    revision: <sha>
    source_paths:
      - src/Claims.Intake/Claims.Intake.csproj
      - docs/claims-architecture.md
    ontology_version: <version>
    rule_versions: [MAP-APPLICATION-OWNER-001@2]
  governance:
    status: confirmed
    owner: team.claims-platform
    generated_at: <rfc3339>
    last_validated_at: <rfc3339>
```

These representations are derived delivery artefacts, not systems of record.
Split oversized representations into linked retrieval units instead of producing
one comprehensive document.

## Apply a publication-readiness gate

Before exposing semantic representations through an agent, graph, API, search
index, vector store, cache, or generated documentation, verify:

- intended consumer, use case, and permitted use are explicit;
- source authority and exact revision are retained;
- semantic identities and source mappings are complete enough for the use case;
- applicable ontology and semantic-rule versions are recorded;
- required properties and relationships passed validation;
- disputed, stale, inferred, and unapproved assertions can be distinguished and
  filtered;
- sensitivity and access constraints can be enforced by the delivery mechanism;
- refresh, invalidation, deletion, and retirement paths exist;
- competency questions pass against the published representation, not only the
  conceptual model;
- rollback or suppression is possible when source evidence or rules are wrong.

Do not index or embed opaque source material first and claim semantic readiness
later. Indexing can improve retrieval while amplifying unresolved ambiguity.

## Validate retrieval and agent use

For AI-facing representations, test the complete consumer path:

- identity resolution and alias handling;
- retrieval precision and recall for competency questions;
- relationship traversal and evidence citation;
- filtering by freshness, status, sensitivity, and authority;
- behaviour when evidence conflicts or is missing;
- protection against generated or untrusted content overriding canonical meaning;
- update visibility after source, ontology, or rule changes;
- deletion and retirement propagation;
- unsupported inference and hallucination rates;
- whether the semantic representation improves outcomes over direct source
  retrieval or a simpler maintained artefact.

Use representative negative and adversarial cases. Do not assume that a coherent
semantic document automatically improves retrieval or agent decisions.

## Manage refresh, drift, and retirement

Define concrete invalidation triggers, including:

- repository revisions affecting cited evidence;
- file move, deletion, rename, or schema change;
- symbol, API, event, or deployment identifier change;
- owner or authority change;
- ontology or mapping-rule version change;
- instance merge, split, deprecation, or retirement;
- failed competency-question regression;
- evidence ageing beyond an agreed threshold.

Every generated artefact should record:

```yaml
lifecycle:
  source_revision: <sha>
  ontology_version: <version>
  rule_versions: [MAP-001@2]
  generated_at: <rfc3339>
  last_validated_at: <rfc3339>
  refresh_trigger: repository-change
  freshness_status: current # current | stale | disputed | retired
  invalidation_reason: null
  retirement_status: active
```

Prefer deterministic regeneration from sources and versioned rules. Do not allow
a generated semantic layer or index to become a stale parallel source of truth.

## Feed preventable ambiguity back to the source

When semantic analysis reveals ambiguity that can be corrected safely and cheaply
in the repository, recommend the smallest source-level improvement, such as:

- clearer schema, symbol, event, or API names;
- explicit descriptions for fields, states, flags, and codes;
- machine-readable ownership and authority metadata;
- stable identifiers and aliases;
- documented deprecation and replacement links;
- provenance or generated-metadata hooks;
- explicit canonical-source declarations.

Do not create a permanent ontology workaround when a source improvement would
remove the ambiguity for every consumer. Preserve compatibility and human review
requirements when proposing source changes.

## Stop conditions

Stop or reduce scope when:

- source authority cannot be established;
- semantic identities cannot be reconciled safely;
- conversion rules cannot be made explicit and reviewable;
- the delivery mechanism cannot enforce required sensitivity or access controls;
- refresh and invalidation cannot be operated;
- published representations cannot retain source, ontology, and rule lineage;
- the semantic representation does not improve the named competency questions;
- a simpler maintained representation provides equivalent value.

Report the smallest missing capability, evidence item, owner, or source correction
needed to resume.