# Run record

- Case: `PC-E3`
- Condition: `baseline`
- Prompt: Define a small ontology for services, APIs, databases, and ownership in this monorepo so our retrieval layer can traverse dependencies.
- Expected routing: `repository-ontology`
- Loaded skills observed in Codex events: `repository-ontology`
- Agent-reported selection (not a native harness event): `repository-ontology`
- Final response:

The minimum useful ontology is a small semantic graph with four entity types—`Service`, `API`, `Database`, and `Team`—plus five authoritative edge types. The repository currently has no service, API, database, deployment, or ownership metadata, so this defines the schema but deliberately does not invent instances.

## Scope and verdict

- Purpose: let the retrieval layer answer dependency and ownership questions through graph traversal.
- Consumer: repository search/RAG and engineering agents.
- Evidence inspected: [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-2e1_eam6/repo/README.md); no committed revision exists.
- Maintainer: unresolved; preferably the platform/developer-experience team, with individual asset owners reviewing their records.
- Verdict: `semantic-graph`.
- Why: documentation or a glossary cannot support multi-hop traversal. OWL/RDF reasoning is unnecessary; a typed property graph or JSON-LD projection is sufficient.

## Competency questions

| ID | Question | Acceptance test |
|---|---|---|
| CQ-1 | What does service X depend on? | Traverse `consumesAPI`, `readsFrom`, and `writesTo`; return targets with evidence. |
| CQ-2 | Which services are affected if API or database X changes? | Traverse the corresponding edges in reverse, transitively if requested. |
| CQ-3 | Who owns an affected asset? | Follow its direct `ownedBy` edge to a `Team`; do not infer ownership from neighbouring assets. |
| CQ-4 | Which service provides API X? | Reverse-traverse `providesAPI`. |
| CQ-5 | What path connects service A to service B? | Find a path through APIs and databases, reporting every edge’s source and confidence. |

## Concept model

```yaml
ontology_version: 0.1.0

concepts:
  Service:
    definition: Independently deployable software that performs runtime behavior.
    identity: Stable repository-qualified service ID, not a display or deployment name.
    required: [id, name, lifecycle, provenance]
    optional: [aliases, repository_path, runtime_names]

  API:
    definition: A versioned machine-consumable interface contract exposed to consumers.
    identity: Stable repository-qualified API ID plus contract/version identity.
    required: [id, name, protocol, lifecycle, provenance]
    optional: [aliases, specification_path, version]
    counterexample: An individual HTTP route is not normally a separate API.

  Database:
    definition: A logical persistent datastore whose contents services read or modify.
    identity: Stable logical datastore ID, independent of a particular host or replica.
    required: [id, name, lifecycle, provenance]
    optional: [aliases, engine, schema_paths, deployment_names]
    counterexample: A transient in-process cache is not a Database.

  Team:
    definition: An accountable organizational group capable of maintaining an asset.
    identity: Stable identifier from the authoritative organizational directory.
    required: [id, name, provenance]
    optional: [aliases, contact]
    counterexample: A repository username or recent contributor is not automatically a Team.
```

### Authoritative relationships

| Relationship | Source → target | Meaning |
|---|---|---|
| `providesAPI` | `Service → API` | The service hosts an implementation of the API contract. |
| `consumesAPI` | `Service → API` | Correct operation of the service requires calling the API. |
| `readsFrom` | `Service → Database` | The service reads persistent application data from the database. |
| `writesTo` | `Service → Database` | The service creates, changes, or deletes persistent data in the database. |
| `ownedBy` | `Service/API/Database → Team` | The team bears ultimate maintenance and incident-routing responsibility. |

All relationships are directional, revision-sensitive, and require provenance. Reverse edges such as `apiProvidedBy` or `ownerOf` should be generated in the delivery graph rather than separately maintained.

`dependsOn` should be a derived query relation:

```text
Service dependsOn API      if Service consumesAPI API
Service dependsOn Database if Service readsFrom or writesTo Database
Service A dependsOn Service B
  if A consumesAPI API and B providesAPI API
```

Do not derive ownership through dependencies. An API or database can have a different owner from its providing or consuming service.

## Minimal graph record

```yaml
id: service:<namespace>/<name>
type: Service
name: Example
lifecycle: active
aliases: []
relationships:
  - predicate: consumesAPI
    target: api:<namespace>/<name>
    assertion:
      status: observed
      confidence: high
      evidence:
        path: path/to/source
        revision: "<git-sha>"
        kind: openapi-client-config
      observed_at: "<rfc3339>"
  - predicate: ownedBy
    target: team:<directory-namespace>/<team>
    assertion:
      status: confirmed
      confidence: high
      evidence:
        path: path/to/ownership-metadata
        revision: "<git-sha>"
        kind: ownership-declaration
      reviewed_by: "<accountable-reviewer>"
```

Recommended IDs are `<type>:<namespace>/<stable-name>`. Preserve deployment names, package names, URLs, and historical names as source identifiers or aliases; never overwrite them during reconciliation.

## External vocabulary mapping

Use a narrow Backstage-compatible mapping rather than inventing interchange terms:

- `Service` specializes Backstage `Component` with `spec.type: service`.
- `API` maps directly to Backstage `API`.
- `Database` specializes Backstage `Resource` with `spec.type: database`.
- `Team` maps to Backstage `Group`.
- Reuse `ownedBy`, `providesApi`, `consumesApi`, and `dependsOn` for interchange.
- Keep local `readsFrom` and `writesTo`; Backstage’s generic `dependsOn` loses the read/write distinction.

Backstage explicitly models components, APIs, infrastructure resources, organizational groups, ownership, and API dependencies, making it a close—but not fully equivalent—interchange model. [Backstage system model](https://backstage.io/docs/features/software-catalog/system-model/), [well-known relations](https://backstage.io/docs/features/software-catalog/well-known-relations/).

## Evidence and uncertainty policy

Each assertion must carry:

```yaml
status: observed | inferred | ambiguous | confirmed | disputed | deprecated
confidence: low | medium | high
evidence:
  path: repository-relative-path
  revision: git-sha
  kind: manifest | api-spec | schema | configuration | ownership-declaration
rule_version: mapping-rule-id@version
observed_at: rfc3339
reviewed_by: null
```

Suggested source precedence:

1. Explicit asset catalogue or ownership manifest.
2. API specifications and database schemas.
3. Deployment/service manifests.
4. Runtime configuration and typed clients.
5. Code imports or naming conventions.

CODEOWNERS alone proves responsibility for repository paths, not necessarily operational ownership. Such a mapping should remain `inferred` until an authorized owner confirms it.

## Current semantic gaps

1. No machine-readable component inventory: service identities cannot be established.
2. No API specifications or consumer declarations: provider/consumer edges cannot be populated.
3. No database schemas or datastore declarations: read/write dependencies are unknown.
4. No ownership source: `ownedBy` edges cannot be established.
5. No Git revision: provenance cannot yet be bound to a stable repository state.

The smallest recovery action is to introduce one reviewed catalogue file per asset—or Backstage-compatible `catalog-info.yaml` files—containing stable IDs, aliases, lifecycle, ownership, and explicit dependency references.

## Operationalisation

Generate the retrieval graph deterministically from reviewed source metadata. Every generated node and edge should retain source revision, ontology version, and mapping-rule version. Regenerate when manifests, API specifications, schemas, ownership metadata, or aliases change.

Before publishing:

- reject dangling identifiers;
- distinguish missing ownership from confirmed ownership;
- expose ambiguous and disputed assertions rather than collapsing them;
- test all five competency questions against the generated graph;
- suppress stale records after source deletion or rename;
- enforce repository access controls before indexing source descriptions.

Publication readiness is currently `fail` because there are no instances, authoritative mappings, refresh rules, or stable revision. The next increment should be a five-asset pilot—two services, one API, one database, and one team—reviewed by the responsible engineering owner before wider indexing.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
