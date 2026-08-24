# Run record

- Case: `PC-E3`
- Condition: `candidate`
- Prompt: Define a small ontology for services, APIs, databases, and ownership in this monorepo so our retrieval layer can traverse dependencies.
- Expected routing: `repository-ontology`
- Loaded skills observed in Codex events: `repository-ontology`
- Agent-reported selection (not a native harness event): `repository-ontology`
- Final response:

The minimum sufficient model is a `typed-concept-model`: enough structure for dependency traversal, without RDF/OWL complexity.

The repository currently contains no service manifests, API specifications, database schemas, deployment definitions, or `CODEOWNERS`, so this defines the ontology schema—not repository instances. Any populated relationships must remain `observed` or `inferred` until an owner confirms them.

## Purpose

- Consumer: retrieval/indexing layer and engineering agents
- Workflow: traverse runtime dependencies and route components to owners
- Evidence scope: repository manifests, OpenAPI specs, database configuration, deployment files, and ownership metadata
- Maintainer: currently unknown; ideally the platform/architecture team
- Refresh trigger: changes to any contributing source file

## Competency questions

| ID | Question | Acceptance test |
|---|---|---|
| CQ-1 | Which services depend directly or transitively on a service? | Traverse `dependsOn` in either direction. |
| CQ-2 | Which APIs does a service provide or consume? | Traverse `providesAPI` and `consumesAPI`. |
| CQ-3 | Which databases can be affected by a service or API? | Traverse service/API edges to `readsFrom` or `writesTo`. |
| CQ-4 | Who owns an affected component? | Every component resolves through `ownedBy` to at least one owner or an explicit unknown-owner state. |
| CQ-5 | What evidence supports an answer? | Every node and edge returns source path, revision, status, and observation time. |

## Concepts

```yaml
ontology:
  id: monorepo-architecture
  version: 0.1.0

concepts:
  Component:
    abstract: true
    definition: An independently identifiable architectural element.
    required: [id, name, sourceRefs]

  Service:
    extends: Component
    definition: A deployable runtime process with an independently observable lifecycle.
    identity: Explicit manifest ID; otherwise deployment name plus repository scope.

  API:
    extends: Component
    definition: A versioned interface exposed for use by another component.
    identity: Explicit API ID or canonical specification location plus version.

  Database:
    extends: Component
    definition: A persistent data store addressed as one operational dependency.
    identity: Explicit datastore ID, never a credential or connection string.
    optional: [engine, environmentScope]

  Owner:
    definition: An accountable team or organisational unit responsible for a component.
    identity: Stable team or group ID.
```

A library, package, controller, database table, API operation, queue, or cache is not automatically one of these concepts. Add those types only when a competency question requires them.

## Relationships

| Edge | Source → target | Meaning |
|---|---|---|
| `dependsOn` | Service → Service | Source requires the target for runtime behaviour. |
| `providesAPI` | Service → API | Service implements and exposes the API. |
| `consumesAPI` | Service → API | Service invokes the API as a client. |
| `readsFrom` | Service or API → Database | Component can retrieve persistent data. |
| `writesTo` | Service or API → Database | Component can create, modify, or delete persistent data. |
| `ownedBy` | Component → Owner | Owner is accountable for the component. |
| `supersedes` | Component → Component | Source replaces an older component identity. |

Do not derive `dependsOn` merely because two services share a database. That may indicate coupling, but it is not evidence of a direct service dependency.

`API → Database` edges should be recorded only when evidence binds database access to that particular API surface. Otherwise attach the edge to the service.

## Assertion envelope

Every relationship should carry its own evidence and uncertainty:

```yaml
assertion:
  subject: service.orders
  predicate: consumesAPI
  object: api.payments.v1

  status: observed       # observed | inferred | ambiguous | confirmed |
                         # disputed | deprecated
  confidence: high       # high | medium | low

  evidence:
    - path: services/orders/config.yaml
      location: dependencies.payments
      revision: "<git-sha>"
      kind: configuration

  ruleVersion: MAP-SERVICE-API@1
  observedAt: "<rfc3339>"
  reviewedBy: null
  validFrom: null
  validTo: null
```

Traversal should default to `observed` and `confirmed` assertions. Inferred edges may be included only when the caller explicitly requests them.

## Stable identifiers

Use semantic IDs without replacing source-native names:

```text
service.<stable-name>
api.<stable-name>.<major-version>
database.<stable-name>
owner.<stable-team-id>
```

Examples:

```text
service.orders
api.payments.v1
database.orders-primary
owner.commerce-platform
```

Renames preserve the previous ID as an alias. Merges and splits require human review; the indexer must not guess identity continuity.

## Source mapping priority

Use explicit metadata before heuristics:

1. Dedicated architecture/component manifest
2. OpenAPI or other API specification
3. Deployment or infrastructure configuration
4. Database migration/configuration evidence
5. `CODEOWNERS` or another designated ownership registry
6. Source imports, client construction, or naming conventions

Evidence from level 6 produces `inferred`, never `confirmed`, assertions.

A compact component manifest could look like:

```yaml
id: service.orders
type: Service
name: Orders
owner: owner.commerce-platform

providesApis:
  - api.orders.v1
consumesApis:
  - api.payments.v1

databases:
  reads:
    - database.catalog-primary
  writes:
    - database.orders-primary
```

## Retrieval representation

Index one document per component, preserving edges as structured fields:

```json
{
  "id": "service.orders",
  "type": "Service",
  "name": "Orders",
  "edges": [
    {
      "predicate": "consumesAPI",
      "target": "api.payments.v1",
      "status": "observed"
    },
    {
      "predicate": "ownedBy",
      "target": "owner.commerce-platform",
      "status": "confirmed"
    }
  ],
  "lineage": {
    "repositoryRevision": "<git-sha>",
    "ontologyVersion": "0.1.0",
    "ruleVersions": ["MAP-COMPONENT-MANIFEST@1"]
  }
}
```

Keep this generated representation separate from source manifests. Invalidate affected component documents whenever their source, ontology version, or mapping-rule version changes.

## Current gaps

- No component inventory from which to create service instances.
- No authoritative API or database metadata.
- No machine-readable ownership source.
- No repository revision exists yet, so assertions cannot be revision-bound.
- The ontology maintainer and authorised reviewers are unknown.

The smallest next increment is to introduce one versioned component manifest format, nominate the ownership authority, and populate two representative services. Validate all five competency questions against those examples before broadening the ontology. No formal RDF/OWL model is warranted yet.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
