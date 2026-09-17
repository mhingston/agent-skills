# Exploration substrates and authority-bearing capabilities

Use this reference when a model phase is primarily exploratory or analytical and the design choice is between a prescriptive chain of specialist agents/tools and a more general sandboxed workspace with familiar file/shell primitives.

The objective is not to prefer a filesystem agent universally. It is to separate two concerns that are easy to conflate:

1. **How the model explores and maintains working context.**
2. **What the system is actually authorised to read, mutate, or commit.**

A broad exploratory interface can be effective without granting broad authority when the sandbox, credentials, network policy, external capability layer, and workflow coordinator enforce the real boundary.

## Prefer empirical topology selection

Do not assume that more specialised agents, more handoffs, or more bespoke tools improve quality. Every handoff can discard local context, force lossy summarisation, and make recovery from an earlier mistaken assumption harder.

For an exploratory model phase, consider a single bounded worker that can plan, inspect, iterate, execute safe local analysis, and revise its approach inside one persistent workspace when:

- the substeps depend heavily on shared local context;
- errors are best repaired by revisiting earlier evidence;
- no independent judgement boundary is required between the substeps;
- permissions and effect authority are the same throughout the phase;
- the coordinator can still validate the phase result independently.

Split into separate workers when the split buys something concrete: different authority, independent verification, materially different context, isolation, specialist model requirements, separate acceptance contracts, or parallelism that survives the coordination overhead.

Treat the topology as an empirical design decision. Compare representative tasks rather than inferring quality from architecture alone.

### Match topology to knowledge-work structure

Open-ended knowledge work often starts from an intent rather than a pre-decomposed task. When the answer depends on several independently searchable evidence dimensions, consider a coordinator pattern such as:

`intent -> decomposition -> bounded evidence workers -> compact evidence packets -> synthesis -> verification`

Use this pattern only when decomposition reduces search ambiguity or context pressure enough to justify the extra coordination. Each evidence worker should receive a distinct question or evidence responsibility, preserve source/provenance handles, and return the smallest finding set needed by the synthesising worker rather than a transcript-sized dump.

Prefer a single exploratory worker instead when the evidence dimensions are tightly coupled, later findings frequently invalidate earlier assumptions, or the worker needs to revisit shared context repeatedly. Prefer deterministic batching or programmatic tool calling when the apparent "research workers" would only perform predictable fan-out, filtering, joining, or aggregation with no independent semantic judgement.

Do not copy human organisational charts mechanically. A legal-firm, research-team, or analyst-assistant pattern is useful only when the information-flow boundary is real: distinct evidence responsibilities, bounded context, useful parallelism, or independent judgement. Agent count is not evidence of better knowledge work.

## Familiar primitives can be a useful exploration interface

Models are often strong at familiar operations such as listing, reading, searching, writing local scratch files, and using a shell to compose deterministic utilities. Inside an adequately isolated workspace, these primitives can be a better exploration substrate than a large forest of narrowly wrapped tools.

That does **not** make shell or filesystem access a safe authority boundary. Enforce separately:

- filesystem roots and protected paths;
- network destinations;
- credential scope;
- process/resource limits;
- external service permissions;
- write and effect boundaries;
- approval requirements;
- immutable workflow/evaluator/control-plane state.

Use domain-specific capabilities where they provide stable semantics, independently enforced policy, constrained external access, idempotency/reconciliation, or durable receipts. In particular, consequential database, payment, deployment, messaging, or production operations should not become ambient shell credentials merely to make the agent interface feel simpler.

A useful default distinction is:

- **general-purpose primitives for local exploration and transformation**;
- **typed domain capabilities for authoritative reads and consequential effects**.

## Materialise domain context when it improves progressive exploration

Large system prompts are not the only way to give an agent company- or domain-specific knowledge. When the runtime supports an isolated workspace, consider materialising a scoped snapshot of relevant context as versioned, read-only files that the worker can search progressively.

Suitable material can include:

- schemas and semantic-layer definitions;
- architecture or domain documentation;
- approved skills and procedures;
- generated indexes or catalogues;
- source-linked examples and conventions.

Preserve for each materialised snapshot:

- source identity and version;
- generation time and freshness policy;
- scope and exclusions;
- redaction or sensitivity policy;
- whether the file is canonical source, a derived view, or untrusted evidence.

Materialised prose or generated context still does not become executable authority. A policy described in a file may inform a proposal; permission to perform a consequential effect must remain separately enforced.

## Compare the complete end-to-end behaviour

When evaluating two agent topologies, keep the task set, model, permissions, source snapshot, verification, and effect boundary matched. Measure dimensions separately rather than collapsing them into one score:

- task success against independent outcome checks;
- unsupported claims or policy violations;
- recovery from an incorrect intermediate assumption;
- context-loss or handoff failures;
- number of model/tool steps;
- end-to-end latency;
- model/tool cost where comparable;
- retries and downstream remediation;
- operator intervention;
- failure containment.

A topology that uses fewer agents or fewer bespoke tools is not better merely because it is simpler. A more prescriptive pipeline is not better merely because its phases are explicit. Prefer the smallest structure that demonstrates better or equivalent outcome quality while preserving the required authority, verification, observability, and recovery properties.

### Diagnose retrieval ceilings with an oracle-context control

When a knowledge workflow fails, do not assume the model is the limiting component. For representative tasks where the correct supporting evidence is known, run a matched diagnostic:

1. **Oracle-context condition** — provide the correct evidence directly to the reasoning/synthesis stage.
2. **Real-retrieval condition** — require the workflow to find the evidence through its normal tools and orchestration.

Keep the model, synthesis instructions, verifier, permissions, answer contract, and non-retrieval budgets matched where possible.

Interpret the comparison conservatively:

- oracle succeeds while retrieval fails: investigate retrieval coverage, query/tool selection, decomposition, ranking, or handoff loss before changing the reasoning model;
- both fail: the limiting factor may be reasoning, instructions, answer construction, or the task/evaluation contract rather than retrieval alone;
- both succeed but one route uses materially fewer searches, model resumptions, tokens, or latency: treat the difference as an efficiency result, not hidden quality lift;
- oracle evidence itself is ambiguous, incomplete, or evaluator-dependent: do not report a clean retrieval gap.

The diagnostic does not prove one root cause by itself. Use traces and failure analysis to localise the remaining gap, and keep search/tool budgets explicit so extra exploration is not mistaken for architectural improvement.

## Calibration case — analytical data agent

Suppose an analytics agent currently uses separate query-understanding, schema-planning, SQL-generation, execution, and reporting agents. Each worker receives a summary from the previous worker. The system often fails after a bad join because the SQL worker cannot revisit the schema evidence that led to the plan.

A second design proposes one bounded exploratory worker with a persistent sandbox containing a versioned read-only semantic layer, schemas, and documentation. It can list/read/search files and use local shell utilities. Actual warehouse execution remains behind a typed read-only query capability with query limits, cost controls, provenance, and receipts.

A sound design should:

- recognise the context-loss and recovery cost of the sequential handoffs;
- consider the single-workspace worker as a candidate rather than assuming the existing specialisation is inherently superior;
- keep authoritative warehouse access outside ambient shell credentials;
- preserve source/version provenance for the materialised semantic layer;
- keep workflow acceptance and query safety independently enforced;
- compare the two topologies on representative historical and held-out questions, including recovery cases, before claiming improvement.

Do not infer from one successful demo that the filesystem-oriented topology generalises. Retain failures as regression fixtures and re-evaluate when the model, context substrate, or tool surface materially changes.
