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
    reviewed_by: null
    observed_at: <rfc3339>
    valid_from: null
    valid_to: null
    supersedes: null
```

## Competency-question validation

```yaml
validation:
  - competency_question: CQ-001
    status: pass # pass | partial | fail | not-run
    query_or_method: <query-command-or-review-procedure>
    expected: <expected-answer-shape>
    actual: <actual-result>
    evidence_coverage: <summary>
    ambiguity: []
    limitation: <what-this-does-not-establish>
```

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
  evidence: []
  reviewers_required: []
  validation_plan: []
  rollback: <reversal-plan>
```

## Human-readable final report

Use this order:

1. **Executive verdict** — whether a model is needed and the minimum form.
2. **Purpose and consumer** — decision or workflow supported.
3. **Evidence scope and authority** — canonical sources, revision, and gaps.
4. **Competency questions** — acceptance tests and results.
5. **Existing semantic assets** — what already works and what is missing.
6. **Term inventory** — preferred terms, conflicts, and uncertain meanings.
7. **Conceptual model** — only concepts and relationships required by the questions.
8. **Provenance and confidence** — observed, inferred, confirmed, disputed, deprecated.
9. **Validation** — exact checks, outcomes, and unavailable tooling.
10. **Maintenance** — owner, update triggers, versioning, and review cadence.
11. **Recommendation** — next smallest increment or no further formalisation.

## Audit checks

Before delivering any artefact, confirm:

- every competency question has an acceptance test;
- every material concept or relation has evidence and status;
- definitions distinguish adjacent concepts and avoid circularity;
- domain, architecture, implementation, delivery, governance, and agent-operation
  layers are not silently collapsed;
- schema, instances, constraints, and policy are distinguishable;
- disputed and stale assertions remain visible;
- no inferred assertion is labelled confirmed;
- no formal validation is claimed without an exact tool result;
- the model is no larger than needed to answer the competency questions;
- ownership and refresh triggers are explicit.
