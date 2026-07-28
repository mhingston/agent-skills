# Schema and Ontology Changes

Use this reference only when the task materially changes a machine-readable schema, ontology, taxonomy, controlled vocabulary, semantic model, or artifacts generated from one. Keep the plan tool-neutral unless repository evidence selects a tool.

## Establish authority and topology

Inspect and record:

- the authoritative editable source and any imports, profiles, overlays, or extensions;
- which artifacts are generated, by which pinned tool and configuration, and whether generated files are committed;
- the data producers, consumers, APIs, queries, code generators, agents, documentation, and operational processes that depend on each representation;
- identifier, namespace, prefix, mapping, versioning, compatibility, deprecation, and release policies;
- representative valid, invalid, boundary, legacy, and mixed-version instances;
- existing deterministic validation, generation, reasoning, and consumer-contract commands.

Do not edit a generated representation directly. Plan a source change, deterministic regeneration, and consumer verification unless repository evidence identifies that representation as authoritative.

## Separate the validation claims

Define what “valid,” “consistent,” or “compatible” means for the task. Map each material claim to the narrowest check that can falsify it.

| Layer | Claim | Useful evidence |
| --- | --- | --- |
| Schema well-formedness | The source conforms to its schema language or metamodel | Parser or metamodel validation |
| Schema quality | The model follows adopted naming, documentation, identifier, and modeling rules | Configured lint or policy checks |
| Instance conformance | Data obeys declared shapes, cardinalities, ranges, and constraints | Positive, negative, boundary, and representative legacy fixtures |
| Vocabulary integrity | Referenced terms, identifiers, prefixes, mappings, bindings, labels, and deprecations are valid | Term-resolution and binding checks against authoritative vocabularies |
| Generated-artifact consistency | Derived schemas, code, documentation, shapes, or ontology renderings match the authoritative source | Reproducible generation plus clean-diff or snapshot checks |
| Consumer compatibility | Supported producers and consumers continue to interoperate | Contract, round-trip, query, generated-client, and mixed-version tests |
| Formal semantic consistency | Required logical properties such as satisfiability or entailment hold | A suitable reasoner or domain-specific semantic checker |
| Domain adequacy | The model means what domain owners intend and covers required cases | Owner review after deterministic checks, supported by competency questions and counterexamples |

One passing layer does not prove another. In particular, syntactic or instance validation does not prove formal logical consistency or domain correctness.

## Challenge the model and transition

For each consequential modeling decision:

- clarify overloaded terms and distinguish identity, type, role, state, and relationship where confusion would affect consumers;
- expose assumptions about closed- versus open-world interpretation, uniqueness, absence, inheritance, cardinality, and identifier stability;
- seek counterexamples, invalid fixtures, boundary values, deprecated terms, cycles, contradictions, and ambiguous mappings;
- trace the consequences for current data, queries, generated artifacts, APIs, agents, and mixed versions;
- state which observation, fixture, or owner decision would overturn the proposed model.

Prefer additive evolution, stable identifiers, explicit deprecation, and a bounded compatibility window. Separate source expansion, regeneration, consumer migration, authority change, and destructive cleanup when they cannot be verified safely as one slice.

## LinkML when repository evidence selects it

Treat LinkML as a schema language and potential authoritative source, not as proof that an ontology is logically consistent. Discover the repository's pinned version, project configuration, imports, generators, and commands before naming exact execution steps.

Plan the relevant subset of this validation chain:

1. Validate the LinkML schema against the LinkML metamodel.
2. Run the configured LinkML linter for adopted quality rules.
3. Validate positive, negative, boundary, legacy, and representative data instances against the schema.
4. When external ontology terms or binding constraints are material, use the repository's adopted term-validation mechanism; `linkml-term-validator` is one available option, not a universal dependency.
5. Regenerate derived JSON Schema, SHACL, OWL, code, documentation, or other outputs from the authoritative LinkML source and prove reproducibility.
6. Validate each derived artifact in the environment that consumes it.
7. If formal OWL semantics are a requirement, run the selected reasoner and explicit satisfiability or entailment checks on the generated OWL. Generation alone is not that evidence.

Current LinkML CLI roles include `linkml validate schema.yaml` for metamodel validation, `linkml validate -s schema.yaml data.yaml` for instance validation, and `linkml lint schema.yaml` for metamodel plus configurable quality checks. Treat these as illustrative until the repository's installed version and commands are observed.

Primary references:

- [LinkML `validate` CLI](https://linkml.io/linkml/cli/validate.html)
- [LinkML `lint` CLI](https://linkml.io/linkml/cli/lint.html)
- [LinkML data validation strategies](https://linkml.io/linkml/data/validating-data.html)
- [LinkML OWL generation and semantic limits](https://linkml.io/linkml/generators/owl.html)
- [LinkML SHACL generation](https://linkml.io/linkml/generators/shacl.html)
- [`linkml-term-validator`](https://github.com/linkml/linkml-term-validator)

## Replan gates

Replan rather than silently expand scope when:

- the claimed source of truth conflicts with generated or deployed artifacts;
- a change alters a stable identifier, namespace, mapping, or public semantic contract;
- existing instances fail for reasons not covered by the approved migration policy;
- generator output changes beyond the intended model delta;
- a required validation layer has no credible checker or owner;
- reasoner results, competency questions, or consumer tests contradict the proposed semantics;
- supported producers and consumers cannot coexist through the intended transition.
