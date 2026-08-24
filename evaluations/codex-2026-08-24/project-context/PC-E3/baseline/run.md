# Run record

- Case: `PC-E3`
- Condition: `baseline`
- Prompt: Define a small ontology for services, APIs, databases, and ownership in this monorepo so our retrieval layer can traverse dependencies.
- Expected routing: `repository-ontology`
- Loaded skills observed in Codex events: `repository-ontology, implement-ticket, plan, decision-continuity, memory-recall, memory-capture, memory-maintenance`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Verdict: `typed-concept-model`

The repo does not currently contain explicit service/API/database inventories or ownership manifests, so a full semantic graph would be overkill. The smallest useful model for dependency traversal is a typed concept model with a few stable relationship predicates and provenance/status fields.

```yaml
scope:
  repository: agent-skills-monorepo
  revision: null
  evidence_window: README.md and repository-local ontology skill references
purpose:
  consumer: retrieval layer
  decision_or_workflow: traverse dependencies across services, APIs, databases, and ownership
  maintainer: repo maintainers / skill authors

competency_questions:
  - id: CQ-001
    question: Which service or skill owns this capability?
    acceptance_test: Given a capability or module, return the owning service or owning agent/module with provenance.
  - id: CQ-002
    question: Which APIs does this service expose or consume?
    acceptance_test: Return first-order API dependencies without reconstructing them from filenames alone.
  - id: CQ-003
    question: Which databases does this service read from or write to?
    acceptance_test: Return storage dependencies and directionality when available.
  - id: CQ-004
    question: What is the dependency path from one repo entity to another?
    acceptance_test: Traverse service -> API -> database -> owner edges with source-backed provenance.

verdict: typed-concept-model
rationale: >
  The repo needs a small governed vocabulary for traversal and retrieval, not a
  formal OWL/RDF system. The source evidence is sparse and mostly architectural
  guidance in README.md; the model should stay lightweight, provenance-aware, and
  extensible.

concepts:
  - id: service
    preferred_label: Service
    definition: A deployable or operationally addressable unit that provides capabilities to other repo entities.
    layers: [architecture]
    identity_criteria: Stable operational boundary with a name used for dependency traversal.
    broader: null
    required_properties: [name, status]
    optional_properties: [description, owner, exposes_api, depends_on_api, reads_database, writes_database]
    lifecycle: [active, deprecated, retired]
    provenance_required: true

  - id: api
    preferred_label: API
    definition: A callable interface exposed by a service, module, or external integration boundary.
    layers: [architecture, implementation]
    identity_criteria: Stable interface boundary with a name, version, or route group.
    broader: null
    required_properties: [name, status]
    optional_properties: [version, owner, exposed_by, consumed_by]
    lifecycle: [active, deprecated, retired]
    provenance_required: true

  - id: database
    preferred_label: Database
    definition: A persistent storage system or schema that is materially depended on by a service.
    layers: [architecture, implementation]
    identity_criteria: Stable persistent data store or logical database/schema name.
    broader: null
    required_properties: [name, status]
    optional_properties: [type, owner, read_by, written_by]
    lifecycle: [active, deprecated, retired]
    provenance_required: true

  - id: owner
    preferred_label: Owner
    definition: The accountable human, team, agent, or module responsible for a concept.
    layers: [governance, agent operation]
    identity_criteria: The accountable party named in authoritative repository evidence.
    broader: null
    required_properties: [name, owner_type, status]
    optional_properties: [contact, steward_of]
    lifecycle: [active, inactive]
    provenance_required: true

relationships:
  - id: exposes_api
    label: exposes API
    definition: A service provides an API boundary.
    source: service
    target: api
    direction: source-to-target
    cardinality: zero-or-many
    temporal: current-at-revision

  - id: consumes_api
    label: consumes API
    definition: A service depends on an API exposed by another service or external system.
    source: service
    target: api
    direction: source-to-target
    cardinality: zero-or-many
    temporal: current-at-revision

  - id: reads_database
    label: reads database
    definition: A service performs read operations against a database.
    source: service
    target: database
    direction: source-to-target
    cardinality: zero-or-many
    temporal: current-at-revision

  - id: writes_database
    label: writes database
    definition: A service performs write operations against a database.
    source: service
    target: database
    direction: source-to-target
    cardinality: zero-or-many
    temporal: current-at-revision

  - id: owned_by
    label: owned by
    definition: A concept has an accountable owner.
    source: service
    target: owner
    direction: source-to-target
    cardinality: zero-or-one
    temporal: current-at-revision

  - id: owns
    label: owns
    definition: The inverse of owned_by, used for traversal.
    source: owner
    target: service
    direction: source-to-target
    cardinality: zero-or-many
    temporal: current-at-revision

properties:
  - id: name
    definition: Human-readable canonical label for the concept.
    applies_to: [service, api, database, owner]
    datatype: string
    cardinality: one
    null_semantics: not-allowed
    derived: false
    temporal_semantics: current-at-revision
    provenance_required: true

  - id: status
    definition: Lifecycle state used by retrieval and traversal logic.
    applies_to: [service, api, database, owner]
    datatype: controlled-term
    cardinality: one
    null_semantics: not-allowed
    allowed_values: [active, deprecated, retired, inactive]
    derived: false
    temporal_semantics: current-at-revision
    provenance_required: true

  - id: source_kind
    definition: The evidence class that supports a statement.
    applies_to: all assertions
    datatype: controlled-term
    cardinality: one
    allowed_values: [readme, code, schema, config, docs, decision, human-confirmed]
    derived: false
    temporal_semantics: assertion-time
    provenance_required: true

assertion_statuses:
  - observed
  - inferred
  - ambiguous
  - confirmed
  - disputed
  - deprecated

source_evidence:
  - path: README.md
    kind: documentation
    observations:
      - The repository is a catalogue of reusable Agent Skills and orchestrating agent definitions.
      - Skills are self-contained directories with `SKILL.md` entry points.
      - Internal workflow modules have owning agents.
      - The repository distinguishes source evidence, ontology/meaning model, semantic layer, and delivery representations.
  - path: .codex/skills/repository-ontology/references/semantic-operationalisation.md
    kind: guidance
    observations:
      - Preserve authority and delivery layers distinctly.
      - Preserve provenance, confidence, and source revision for generated semantic assertions.

minimal_semantic_rules:
  - id: MAP-OWNER-001
    purpose: Derive owned_by from explicit repository statements or module metadata.
    source_patterns: [README.md, skill frontmatter, agent metadata, CODEOWNERS when present]
    output: service -> owner
    status: proposed

  - id: MAP-API-001
    purpose: Derive API boundaries from explicit interfaces, route groups, or documented integration points.
    source_patterns: [OpenAPI, route definitions, interface declarations, docs]
    output: service -> api
    status: proposed

  - id: MAP-DB-001
    purpose: Derive database dependencies from schemas, migration files, connection configs, or documented ownership.
    source_patterns: [schema files, migrations, ORM models, config]
    output: service -> database
    status: proposed
```

Notes:
- In this repo, `service`, `api`, and `database` are currently mostly **inferred** concept types, not fully observed entities.
- `owner` is the strongest repository-native concept because the README explicitly states owning agents/modules and responsibility boundaries.
- For traversal, keep the graph shallow: `service -> api -> database -> owner`, with provenance attached to every edge.

If you want, I can turn this into one of these next:
1. a machine-readable `ontology.yaml` for the repo,
2. SHACL-style validation rules for the retrieval layer,
3. a small JSON-LD/RDF graph projection.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
