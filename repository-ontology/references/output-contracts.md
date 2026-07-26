# Output contracts

Use these structures when the ontology task requires durable or machine-readable
artefacts. Omit fields that genuinely do not apply; never invent values to make a
template look complete.

## Assessment report

```yaml
scope:
  repository: owner/repository
  revision: <commit-or-null>
  evidence_window: <scope>
purpose:
  consumer: <human-or-system>
  decision_or_workflow: <what-it-supports>
  maintainer: <owner-or-unknown>
competency_questions:
  - id: CQ-001
    question: Which service implements a given business capability?
    acceptance_test: <query-or-review-check>
verdict: typed-concept-model
rationale: <why-this-is-the-minimum-sufficient-model>
alternatives:
  - option: glossary-sufficient
    rejected_because: <reason>
limitations: []
```

## External vocabulary decision

```yaml
vocabulary_decisions:
  - vocabulary: <name>
    namespace: <iri-or-prefix>
    version: <version-or-date>
    maintenance_status: active # active | inactive | unknown
    licence: <licence-or-unknown>
    candidate_term: <external-term>
    local_term: <local-term-or-null>
    decision: reuse-directly
    # reuse-directly | specialise | equivalent | broader | narrower |
    # related | interchange-only | reject
    semantic_differences: []
    imported_scope: [<reviewed-term-or-module>]
    evidence: []
    reviewed_by: <reviewer-or-null>
```

Do not declare equivalence merely because labels match. Prefer a small reviewed
mapping over importing an entire external ontology.

## Semantic-gap backlog

```yaml
semantic_gaps:
  - id: GAP-001
    description: Deployment service names cannot be reliably mapped to projects.
    affected_competency_questions: [CQ-001]
    evidence:
      - path: deploy/services.yaml
        revision: <sha>
    interpretation_risk: high
    consumer_value: high
    evidence_availability: partial
    maintenance_cost: medium
    priority: high
    smallest_recovery_action: Add an explicit project identifier to each service.
    owner: <owner-or-unknown>
    status: open # open | accepted | remediated | deferred
```

Record only gaps relevant to the intended use. Do not turn this into a general
repository-quality backlog.

## Term inventory

```yaml
terms:
  - id: policy
    preferred_label: Policy
    definition: A contract defining cover, parties, limits, and validity.
    layers: [domain]
    status: inferred
    confidence: medium
    evidence:
      - path: docs/domain-model.md
        location: Policy
        revision: <sha>
        kind: documentation
    synonyms: [InsurancePolicy]
    homonyms:
      - label: Policy
        meaning: Retry policy used by the billing subsystem.
    deprecated_terms: []
    examples: []
    counterexamples: []
    conflicts: []
```

## Concept model

```yaml
concepts:
  - id: service
    preferred_label: Service
    definition: <definition>
    layers: [architecture]
    identity_criteria: <criteria>
    broader: null
    required_properties: []
    optional_properties: []
    lifecycle: null
    provenance_required: true
relationships:
  - id: implements
    label: implements
    definition: <definition>
    source: service
    target: business-capability
    direction: source-to-target
    cardinality: unknown
    temporal: current-at-revision
    evidence: []
    examples: []
    counterexamples: []
```

## Property semantics

```yaml
properties:
  - id: lifecycle-status
    definition: The governed operational lifecycle of the component.
    applies_to: Component
    datatype: controlled-term
    cardinality: zero-or-one
    null_semantics: unknown
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
    permitted_use: [agent-retrieval, architecture-analysis]
    provenance_required: true
    refresh_trigger: source-change
```

## Identifier mapping

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
    collision_status: clear # clear | ambiguous | disputed
    rename_policy: preserve-old-as-alias
    merge_policy: human-review-required
    split_policy: human-review-required
    status: confirmed
    confidence: high
    reviewed_by: <reviewer>
    observed_at: <rfc3339>
```

Never overwrite source identifiers. Keep the crosswalk versioned and traceable.

## Provenance register

```yaml
assertions:
  - id: AS-001
    subject: payments-service
    predicate: implements
    object: take-payment
    status: observed
    confidence: high
    sources:
      - path: docs/capabilities.md
        location: Payments
        revision: <sha>
        kind: documentation
    ontology_version: <version-or-null>
    rule_versions: []
    reviewed_by: null
    observed_at: <rfc3339>
    valid_from: null
    valid_to: null
    supersedes: null
```

## Semantic conversion rule

```yaml
semantic_rules:
  - id: MAP-APPLICATION-OWNER-001
    version: 2
    rule_kind: relationship-mapping
    purpose: Derive confirmed application ownership from active CODEOWNERS entries.
    affected_competency_questions: [CQ-002]
    source_pattern:
      artefact: CODEOWNERS
      path_pattern: /src/Claims.Intake/**
    source_authority:
      required: true
      designation: repository-governance
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
    effective_to: null
    owner: <rule-owner>
    approved_by: <reviewer>
    validation:
      - no unmatched owners
      - no conflicting authoritative ownership source
    escalation:
      - conflicting ownership sources
      - owner cannot be resolved
    rollback: Revert generated assertions to the previous accepted rule version.
```

Generated assertions must record the exact rule version that produced them.

## AI-facing semantic instance

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
    confidence: high
    owner: team.claims-platform
    sensitivity: internal
    permitted_use: [agent-retrieval]
    generated_at: <rfc3339>
    last_validated_at: <rfc3339>
  lifecycle:
    freshness_status: current
    invalidation_reason: null
    retirement_status: active
```

Treat this as a derived delivery representation, not a system of record.

## Publication-readiness report

```yaml
publication_readiness:
  consumer: <agent-search-api-or-graph>
  representation: <path-or-service>
  status: pass # pass | conditional | fail
  checks:
    source_authority_retained: pass
    identifier_mapping_complete: pass
    ontology_version_recorded: pass
    rule_versions_recorded: pass
    required_relationships_validated: pass
    stale_and_disputed_filtering: pass
    sensitivity_enforcement: pass
    refresh_and_invalidation_defined: pass
    deletion_and_retirement_defined: pass
    competency_questions_tested_on_delivery: pass
    rollback_or_suppression_available: pass
  limitations: []
  approved_by: <reviewer-or-null>
  assessed_at: <rfc3339>
```

A model may be semantically valid while its delivery representation is unsafe or
operationally incomplete.

## Lifecycle record

```yaml
lifecycle:
  artefact: <semantic-instance-index-or-graph-projection>
  source_revision: <sha>
  ontology_version: <version>
  rule_versions: [MAP-001@2]
  generated_at: <rfc3339>
  last_validated_at: <rfc3339>
  refresh_trigger: repository-change
  freshness_status: current # current | stale | disputed | retired
  invalidation_reason: null
  retirement_status: active
  deletion_propagation: <mechanism>
  owner: <owner>
```

## Runtime action validation

```yaml
action_validation:
  proposal_id: ACT-REFUND-001
  action: IssueRefund
  actor:
    id: <agent-or-user-id>
    delegated_authority: <authority-reference>
  risk:
    level: high
    reversible: false
  proposal:
    order: order.123
    amount: 25.00
    currency: GBP
    recipient: customer.456
  pinned_context:
    source_revision: <sha>
    current_state_observed_at: <rfc3339>
    ontology_version: <version>
    constraint_version: <version>
    mapping_rule_versions: [MAP-001@2]
    policy_version: <version>
    tool_schema_version: <version>
  preconditions:
    - order is refundable
    - no accepted refund already covers this amount
    - recipient is the entitled customer
  expected_effects:
    - refund.refersTo = order.123
    - refund.recipient = customer.456
    - order.refundedAmount increases by 25.00
  observed_effects: []
  checks:
    structural: pass
    semantic_reasoning: pass
    operational_constraints: pass
    authority: pass
    transactional_preconditions: pass
    postconditions: not-run
  commit:
    status: not-run # not-run | committed | failed | partial
    idempotency_key: <key-or-null>
    authoritative_receipt: null
  containment:
    rollback: <mechanism-or-null>
    compensation: <mechanism-or-null>
    escalation: <route>
```

Keep the proposal, validation, commit receipt, and postcondition observations
separate. A valid proposal is not proof that execution succeeded.

## Runtime validation result

```yaml
validation_result:
  proposal_id: ACT-REFUND-001
  status: indeterminate
  # pass | reject | indeterminate | unavailable
  risk: high
  pinned_context:
    source_revision: <sha>
    ontology_version: <version>
    constraint_version: <version>
    mapping_rule_versions: [MAP-001@2]
    policy_version: <version>
    tool_schema_version: <version>
  validators:
    - kind: structural
      implementation: <name-and-version>
    - kind: semantic-reasoner
      implementation: <name-and-version>
    - kind: authority
      implementation: <name-and-version>
  checks:
    structural: pass
    semantic_reasoning: pass
    operational_constraints: indeterminate
    authority: not-run
    transactional_preconditions: not-run
  violations: []
  unresolved:
    - Customer identity cannot be reconciled with the payment recipient.
  evidence: []
  retryable: false
  required_next_action: human-review
  attempt: 1
  budgets:
    max_attempts: 3
    max_elapsed_seconds: <limit>
    max_cost: <limit-or-null>
```

Runtime-validation status is distinct from assertion status, competency-question
status, and publication-readiness status. Do not convert `indeterminate` into
`pass` through model confidence. Pin and revalidate the context before commit if
any source, ontology, rule, policy, identity, state, or tool-schema input changes.

## Competency-question validation

```yaml
validation:
  - competency_question: CQ-001
    status: pass # pass | partial | fail | not-run
    validation_surface: conceptual-model # conceptual-model | published-representation
    query_or_method: <query-command-or-review-procedure>
    expected: <expected-answer-shape>
    actual: <actual-result>
    evidence_coverage: <summary>
    ambiguity: []
    limitation: <what-this-does-not-establish>
```

For AI-facing work, validate both the conceptual model and the exact published
representation consumed by the agent or retrieval system.

## Evolution proposal

```yaml
change:
  id: ONT-CHANGE-001
  version_from: <version>
  proposed_version: <version>
  purpose: <competency-question-or-defect>
  additions: []
  modifications: []
  deprecations: []
  migrations: []
  expected_inferences: []
  potential_unintended_inferences: []
  affected_queries: []
  affected_rules: []
  affected_delivery_representations: []
  affected_runtime_validators: []
  affected_policies: []
  affected_transactional_controls: []
  evidence: []
  reviewers_required: []
  validation_plan: []
  regeneration_plan: []
  runtime_migration_plan: []
  rollback: <reversal-plan>
```

## Human-readable final report

Use this order:

1. **Executive verdict** — whether a model is needed and the minimum form.
2. **Purpose and consumer** — decision or workflow supported.
3. **Evidence scope and authority** — canonical sources, revision, and gaps.
4. **Competency questions** — acceptance tests and results.
5. **Existing semantic assets** — what already works and what is missing.
6. **External vocabulary decisions** — reuse, mapping, rejection, and differences.
7. **Semantic gaps** — prioritised ambiguity or lineage problems relevant to use.
8. **Term inventory** — preferred terms, conflicts, and uncertain meanings.
9. **Conceptual model** — only concepts and relationships required by the questions.
10. **Provenance and confidence** — observed, inferred, confirmed, disputed, deprecated.
11. **Operationalisation** — identities, conversion rules, delivery artefacts, and controls.
12. **Runtime enforcement** — validation layers, authority, transactions, effects, and loops.
13. **Validation** — exact checks, outcomes, and unavailable tooling.
14. **Maintenance** — owner, update triggers, versioning, drift, and review cadence.
15. **Recommendation** — next smallest increment or no further formalisation.

## Audit checks

Before delivering any artefact, confirm:

- every competency question has an acceptance test;
- every material concept or relation has evidence and status;
- definitions distinguish adjacent concepts and avoid circularity;
- external vocabulary decisions record versions and semantic differences;
- equivalent mappings are not inferred from matching labels alone;
- domain, architecture, implementation, delivery, governance, and agent-operation
  layers are not silently collapsed;
- source evidence, ontology, semantic layer, and delivery representations are
  distinguishable;
- schema, instances, constraints, and policy are distinguishable;
- disputed and stale assertions remain visible;
- no inferred assertion is labelled confirmed;
- source identifiers are preserved and semantic mappings are versioned;
- generated assertions identify applicable ontology and rule versions;
- no formal validation is claimed without an exact tool result;
- AI-facing representations retain lineage, freshness, sensitivity, and permitted
  use metadata;
- publication controls include refresh, invalidation, deletion, retirement, and
  suppression of stale or disputed assertions;
- competency questions are tested against the actual published representation when
  one exists;
- runtime structural, semantic, policy, transactional, and postcondition checks are
  distinguishable;
- runtime-validation outcomes use `pass`, `reject`, `indeterminate`, or
  `unavailable` without confusing them with assertion status;
- high-risk actions fail closed when mandatory checks are rejected, indeterminate,
  or unavailable;
- the side-effecting boundary actually consumes validation results;
- proposal, commit receipt, and observed effects remain separate and traceable;
- runtime retries have explicit attempt, time, token, or cost budgets as applicable;
- the model is no larger than needed to answer the competency questions;
- ownership and refresh triggers are explicit.