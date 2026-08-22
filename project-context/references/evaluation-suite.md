# Project-context evaluation suite

Use matched runs when changing `project-context` triggering, routing, or workflow
semantics. Compare the candidate skill against no skill or the previous version
using the same model, harness, repository fixture, and verifier.

The goal is correct task completion and routing, not whether the response mentions
project context terminology.

## Core cases

### 1. Long-running fragmented project — should trigger

Prompt:

> We have architecture docs in the repo, product decisions in Confluence, tickets
> in Jira, and generated summaries in agent sessions. Different agents keep
> rediscovering which source is current. Design the minimum durable project-context
> model and tell me what should remain authoritative.

Expected behaviour:

- classifies a dedicated project-context substrate as justified;
- inventories claim-specific authority before proposing structure;
- separates current truth, future intent, history/evidence, and scratch;
- avoids declaring Confluence, Jira, or the repository globally authoritative;
- proposes the thinnest machine-readable layer that removes reconstruction;
- defines an orientation packet and explicit conflict handling;
- does not jump into implementation without authorisation.

Failure signals:

- creates another documentation repository without first checking existing homes;
- treats the newest or most convenient source as canonical;
- proposes a broad knowledge graph without operational need;
- recommends copying all sources into prompts on every session.

### 2. Routine implementation plan — should route elsewhere

Prompt:

> Plan how to add an idempotency key to this existing POST endpoint. The repo has
> a clear architecture doc, ADRs, tests, and a ready ticket.

Expected behaviour:

- does not establish or audit a project-context record;
- routes to an ordinary software-planning workflow;
- may consume existing durable context as evidence without redesigning it.

Failure signal:

- introduces a context index, new documentation taxonomy, or lifecycle hooks for
  an otherwise bounded planning request.

### 3. Repository ontology request — should route elsewhere

Prompt:

> Define a small ontology for services, APIs, databases, and ownership in this
> monorepo so our retrieval layer can traverse dependencies.

Expected behaviour:

- routes to repository ontology / semantic-model work;
- does not redefine the task as project-context governance merely because both
  use typed relationships.

### 4. Shared organisational memory — should route elsewhere

Prompt:

> Capture the deployment workaround we just learned into our configured Confluence
> memory so future teams can recall it.

Expected behaviour:

- routes to memory capture;
- does not create project-record history or a context index unless the user asks
  for project-local governance too.

### 5. Context-as-code audit — should trigger

Prompt:

> Assess whether this multi-agent project has enough durable context for a fresh
> agent to resume work safely. Check whether trackers and generated status have
> become competing sources of truth and whether readiness can be derived from
> evidence.

Expected behaviour:

- assesses source authority, role coverage, machine-interface gaps, orientation,
  projections, and derived state;
- distinguishes missing evidence from failure;
- recommends the smallest next slice rather than a wholesale rewrite.

### 6. Machine-interface design — should trigger

Prompt:

> Agents can find our docs, but they still have to read twenty files to determine
> what is ready, what is blocked, and whether Jira disagrees with the project
> record. What deterministic interface should we add?

Expected behaviour:

- proposes bounded machine questions and structured outputs;
- preserves one owner for each field replicated externally;
- separates preview/plan from consequential apply operations;
- recommends deterministic validation and precise repair findings;
- avoids delegating relationship validation back to an LLM.

## Validator fixture cases

The bundled validator should be tested independently from model behaviour.
Representative fixtures should cover:

1. a valid index with resolvable references;
2. duplicate identities;
3. missing local paths;
4. path traversal outside the configured root;
5. a canonical scratch record;
6. a superseded/archived record still marked canonical;
7. an unresolved reference;
8. invalid schema-version and enum values.

The validator is deliberately structural. Do not add semantic prose scoring to it;
semantic freshness and correctness require authoritative evidence and, where
necessary, human or model judgement.
