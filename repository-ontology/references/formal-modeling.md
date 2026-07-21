# Formal modelling reference

Read this reference only after the core workflow selects `semantic-graph`,
`formal-ontology`, or `operational-ontology`.

## Keep knowledge kinds separate

Classify every material statement as one of:

- **Schema knowledge (TBox)** — classes, properties, hierarchies, and general
  restrictions.
- **Instance knowledge (ABox)** — facts about concrete repository artefacts,
  systems, people, versions, or events.
- **Validation constraints** — conditions that graph or instance data must meet.
- **Operational policy** — mutable permissions, workflows, approvals, and
  organisational rules.

Do not generalise an observed instance into a universal axiom without
authoritative evidence. Do not treat a mutable policy or validation rule as an
essential domain truth.

## Select the formalism deliberately

### RDF or JSON-LD

Use when the primary need is globally identifiable resources, graph traversal,
linked data, or interoperability. Define stable IRIs, namespaces, versioning, and
provenance before publishing data.

### OWL

Use only when formal class semantics, inference, consistency checking, or
interoperable ontology reasoning is required. Declare the intended profile or
expressivity boundary. Permit only constructs required by competency questions.

### SHACL or equivalent

Use for validating operational graph data against explicit shapes, cardinalities,
datatypes, closed sets, or cross-property constraints. Keep shapes separate from
class definitions when the rule is operational rather than semantic.

## Candidate axiom workflow

Before generating axioms, declare:

- target ontology language and serialisation;
- namespace and identifier conventions;
- permitted axiom and expression families;
- expected ontology profile;
- whether the task concerns schema, instances, or both;
- validation and reasoner commands;
- evidence and human-review requirements.

Candidate constructs may include declarations, subclass relations, class and
property assertions, domains and ranges, disjointness, property hierarchies,
inverses, characteristics, and existential, universal, or cardinality
restrictions. Include only what competency questions require.

For every candidate axiom record:

```yaml
candidate_id: AX-001
knowledge_kind: schema
interpretation: Every service that publishes an event is an event publisher.
formal_expression: >-
  SubClassOf(
    ObjectIntersectionOf(Service ObjectSomeValuesFrom(publishes Event))
    EventPublisher
  )
evidence:
  - path: docs/eventing.md
    location: section 3
status: proposed
confidence: medium
expected_inferences:
  - A Service publishing an Event is classified as EventPublisher.
potential_unintended_inferences: []
```

Verify that every referenced entity already exists or is intentionally declared
as a new evidence-backed candidate. Do not invent cardinalities, inverses,
disjointness, property characteristics, or closed-world assumptions.

Separate generation from critique and validation. Use constrained structured
output and low-variance settings when available. Candidate axioms never modify
the canonical ontology directly.

## Model constraints separately

Distinguish:

- concept definitions;
- structural constraints;
- business invariants;
- architectural policy;
- agent permissions;
- workflow preconditions and effects;
- inferred rules.

Example operational action model:

```yaml
action: MergePullRequest
preconditions:
  - required_checks_passed
  - required_approvals_present
permission:
  required: repository.merge
effects:
  - pull_request.status becomes merged
risk:
  level: medium
reversible: false
policy_source: .github/branch-protection.md
```

The policy source and observation time are part of the assertion. A repository
policy may change without changing the meaning of `PullRequest`.

## Agent-facing ontology checks

When agents consume the model, represent only evidence-backed information needed
to constrain or validate behaviour:

- goals and completion conditions;
- actions, inputs, outputs, preconditions, and effects;
- tool capabilities and authority boundaries;
- permissions, approval requirements, risk, and reversibility;
- evidence, provenance, source authority, confidence, and freshness;
- stale or superseded assertions;
- human decisions and verdicts as attributed events, not model conclusions.

An agent-facing ontology must improve routing, validation, retrieval, or control;
additional prompt context alone is not sufficient justification.

## Formal validation

Run checks appropriate to the selected representation:

1. parse and serialisation validation;
2. namespace and identifier validation;
3. undefined-entity and duplicate-identifier checks;
4. ontology-profile or expressivity checks;
5. reasoner consistency and unsatisfiable-class checks;
6. SHACL or equivalent constraint validation;
7. expected-inference tests;
8. unintended-inference probes;
9. competency-question queries and expected answers;
10. provenance and revision-completeness checks.

Record exact tool versions, commands, outcomes, and limitations. A file that
parses is not necessarily logically consistent or useful.

## Incremental formalisation

For large scopes:

1. partition by competency question, domain boundary, or semantic layer;
2. extract terms and candidate assertions independently;
3. reconcile identifiers, homonyms, and disputed meanings;
4. establish a small upper model only when cross-boundary queries require it;
5. validate each module before adding mappings;
6. add bridge axioms conservatively and test unintended inferences;
7. version every accepted change and retain provenance.

Prefer human-authored formalisation when ambiguity remains. Consider fine-tuning
only when the formalism is stable, a large reviewed corpus exists, demand is
repeated, and measured evaluation shows constrained prompting is inadequate.
