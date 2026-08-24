# Run record

- Case: `PC-E3`
- Condition: `candidate`
- Prompt: Define a small ontology for services, APIs, databases, and ownership in this monorepo so our retrieval layer can traverse dependencies.
- Expected routing: `repository-ontology`
- Loaded skills observed in Codex events: `repository-ontology`
- Agent-reported selection (not a native harness event): `none`
- Final response:

**Verdict:** `typed-concept-model`

The repository does not show an existing ontology or schema for service/API/database ownership, so the lightest model that supports dependency traversal is a small typed concept model. A glossary or taxonomy would not be enough because your retrieval layer needs explicit edges.

**Scope**
This model should answer four questions:

1. What is this thing?
2. What does it depend on?
3. Who owns it?
4. What should retrieval traverse next?

**Core Concepts**

1. `Service`
- Definition: a deployable or logically bounded runtime component in the monorepo.
- Examples: web app, worker, job runner, backend service.
- Status: `observed` if declared in repo metadata; otherwise `inferred` from package/config boundaries.

2. `API`
- Definition: a contract exposed by a service or package for other components to call.
- Subtypes:
  - `HTTP_API`
  - `RPC_API`
  - `GraphQL_API`
  - `Internal_API`
- Status: `observed` when defined in route/schema/client files; otherwise `inferred`.

3. `Database`
- Definition: a persistent data store used by one or more services.
- Subtypes:
  - `Relational_Database`
  - `Document_Database`
  - `KeyValue_Store`
  - `Queue_or_Storage` if the repo treats it operationally as persistence
- Status: `observed` when declared in config/migrations; otherwise `inferred`.

4. `Owner`
- Definition: accountable human, team, or agent-managed stewardship unit for a service/API/database.
- Status: `observed` when explicitly declared; otherwise `ambiguous` unless confirmed by an authoritative source.

5. `Component`
- Definition: a generic retrieval node for anything the graph needs to traverse, including service, API, database, library, and package.
- Use this as the superclass so the traversal graph stays uniform.

**Core Relations**

1. `owns`
- Domain: `Owner -> Component`
- Meaning: accountability boundary, not code authorship.
- Use for routing questions like “who can change this?”

2. `implements`
- Domain: `Service -> API`
- Meaning: the service serves the API contract.

3. `depends_on`
- Domain: `Component -> Component`
- Meaning: runtime, compile-time, or operational dependency.
- Use this for traversal.
- Record dependency kind as an attribute:
  - `runtime`
  - `build`
  - `data`
  - `network`
  - `operational`

4. `reads_from`
- Domain: `Service -> Database`
- Meaning: service consumes persisted state.

5. `writes_to`
- Domain: `Service -> Database`
- Meaning: service mutates persisted state.

6. `exposes`
- Domain: `Service -> API`
- Meaning: externally visible surface.
- `implements` and `exposes` can be the same edge if you want the model smaller.

7. `backed_by`
- Domain: `API -> Service`
- Meaning: reverse traversal convenience.

8. `canonical_source_for`
- Domain: `Component -> Concept`
- Meaning: the source of truth for a business/domain concept if you later extend retrieval beyond infrastructure.

**Minimal Type Model**

```text
Component
  ├─ Service
  ├─ API
  ├─ Database
  ├─ Package
  ├─ Queue
  └─ Owner

Service
  ├─ exposes -> API
  ├─ depends_on -> Component
  ├─ reads_from -> Database
  ├─ writes_to -> Database
  └─ owned_by -> Owner

API
  ├─ backed_by -> Service
  └─ depends_on -> Component

Database
  └─ owned_by -> Owner

Owner
  └─ owns -> Component
```

**Attributes to Store**

For each node:

- `id`
- `label`
- `type`
- `repo_path`
- `status` (`observed`, `inferred`, `ambiguous`, `confirmed`, `disputed`, `deprecated`)
- `confidence`
- `source_refs`
- `revision`
- `owner_id` or `owner_ref` if available

For each edge:

- `predicate`
- `source_id`
- `target_id`
- `kind`
- `status`
- `confidence`
- `source_refs`

**Traversal Rules for Retrieval**

1. Start from the matched node.
2. Expand `depends_on` edges first.
3. Expand `owns` edges if the query is about accountability, incidents, or change routing.
4. Expand `reads_from` and `writes_to` edges if the query is about data impact.
5. Expand `implements` / `exposes` / `backed_by` edges if the query is about contracts or endpoints.
6. Stop at a configurable depth, usually 2 to 3 hops.
7. Prefer `observed` over `inferred`, and `confirmed` over both.
8. Do not collapse `ambiguous` ownership into a single owner.

**Evidence Policy**

Use only maintained sources from the repo, for example:

- `README.md`
- package manifests
- service configs
- migration files
- API schema files
- ownership files if present

Do not infer ownership from folder names alone unless nothing else exists, and then mark it `inferred`.

**Recommended Status Semantics**

- `observed`: directly stated in a source
- `inferred`: derived from structure or config
- `ambiguous`: more than one plausible interpretation
- `confirmed`: explicitly accepted by a maintained source or human
- `disputed`: sources conflict
- `deprecated`: still present, not preferred

**What I would not include yet**

- full RDF/OWL
- formal reasoning rules
- domain business concepts
- every package/module/file as a first-class concept

Those are likely overhead unless retrieval needs deeper semantic joins.

If you want, I can turn this into one of two concrete next steps:

1. a JSON Schema for the graph records, or
2. a short ontology document you can check into the repo.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
