# Mastra dynamic-workflow runtime

Use this reference when implementing, changing, validating, storing, or running a
Mastra dynamic workflow.

## Runtime role

Mastra is the orchestration runtime. A dynamic workflow is persisted as a
JSON-compatible graph that references registered agents, tools, workflows, and
control-flow primitives by stable IDs.

Keep these responsibilities separate:

- **Mastra**: graph execution, ordering, mappings, control flow, state, storage,
  validation, run lifecycle and registered primitive resolution.
- **Application/Mastra integration and policy layer**: approvals, authority,
  allowed primitive IDs, filesystem/network/resource scope, effect boundaries,
  and concurrency/cost limits supplied to or enforced around the runtime.
- **Adaptive planner, when used**: propose task decomposition and a graph only.
- **ACP worker**: repository reasoning, file changes, commands/tests, and other
  coding-agent capabilities permitted by its environment.
- **Filesystem / explicit state**: shared truth between separate worker calls.

Mastra executes workflow policy supplied by the application/integration layer; do
not attribute deployment-specific approval or authority policy to Mastra itself.
Do not insert a model-backed supervisor merely to coordinate a known graph.

## Version preflight

Before writing code:

1. inspect installed `@mastra/core`, `@mastra/acp`, and storage versions;
2. inspect the installed dynamic-workflow docs/types/source for the exact graph
   schema and APIs;
3. compare current remote docs only when useful;
4. upgrade related packages deliberately rather than mixing incompatible eras.

Dynamic workflows require `@mastra/core >= 1.58.0`. ACP support requires
`@mastra/core >= 1.34.0`. Treat these as minimum feature versions, not recommended
hard pins.

For a new local project the minimum shape commonly includes:

```bash
npm install @mastra/core @mastra/acp @mastra/libsql
```

Also install or make available the selected ACP executable/adapter if coding
workers are required.

## Storage and registry

Dynamic workflows are stored definitions, so configure Mastra storage. For a
local-only project, LibSQL is a reasonable default unless the user already has a
storage adapter or requests another one:

```ts
import { Mastra } from "@mastra/core/mastra";
import { LibSQLStore } from "@mastra/libsql";

export const mastra = new Mastra({
  storage: new LibSQLStore({
    id: "mastra-storage",
    url: "file:./mastra.db",
  }),
  tools: {
    // registered tools referenced by dynamic workflow toolId
  },
  agents: {
    // ordinary registered Mastra agents referenced by dynamic workflow agentId
  },
});
```

Use stable primitive IDs. A generated graph may reference only IDs already
registered and allowed by the application's policy layer.

### Minimal storage backend contract

Keep LibSQL as the default for local development. A deployment may select another
Mastra storage adapter or composite storage, but the **effective** backend (Mastra
storage plus application-owned records where needed) must:

1. Persist and retrieve versioned workflow definitions, their canonical digests
   and the immutable step-manifest resolved at registration.
2. Persist run IDs, definition digests, trigger provenance, effective policy,
   cumulative budgets and execution/checkpoint state across restart/resume.
3. Persist approval requests and decisions bound to actor, run, definition,
   policy, scope, expiry and decision timestamp; reject replay/stale grants.
4. Persist redacted receipts and permitted step/worker output references and
   retrieve all run-associated records by `runId` with tenant/actor scoping.
5. Support atomic or recoverably idempotent state transitions, access controls,
   and targeted expiry/deletion across its configured domains and related stores.

Check the adapter's actual domain support: Mastra separates workflow state,
observability and schedules, and it does **not** automatically own application
approval or receipt policy. If any required operation is missing, implement it in
a durable integration store before claiming this contract. A definition store alone
does not prove durable approvals or resumability. Test restart and deletion.


## ACP workers in a dynamic workflow

`@mastra/acp` exposes two relevant integration forms:

- `AcpAgent`: wraps an ACP process as a Mastra subagent with agent-style methods;
- `createACPTool()`: wraps an ACP process as a Mastra tool that accepts a task and
  returns output.

For a dynamic workflow that needs a direct coding worker **without a model
supervisor**, `createACPTool()` is the simplest stable conceptual boundary: the
workflow references a registered tool and the tool launches the ACP agent.

Example shape:

```ts
import { createACPTool } from "@mastra/acp";

export const coderTool = createACPTool({
  id: "coder",
  description: "ACP coding worker for repository tasks.",
  command: process.execPath,
  args: ["/absolute/path/to/the/acp-adapter.js"],
  cwd: repo,
});
```

Then register `coderTool` under `tools` and reference its registered ID from a
`tool` graph entry.

If the project deliberately uses a real Mastra supervisor `Agent`, an `AcpAgent`
may instead be attached as that agent's subagent. Do not add such a supervisor
solely to make the dynamic workflow work.

**Important:** exact registration support has changed across Mastra versions. A
historical tested combination had a failure when a bare `AcpAgent` was registered
directly in `new Mastra({ agents: ... })`. Check the installed current source
before relying on either that failure or a workaround. See
`references/troubleshooting.md` from the main skill when the issue actually
appears.

## Dynamic definition

A stored workflow definition includes, at minimum, an ID, input/output schema and
an executable graph. Optional state/request-context/metadata fields depend on the
current definition contract.

Use JSON Schema inside stored definitions. Verify the current supported graph
entry types from installed docs/source before authoring a non-trivial graph. The
set has included agent, tool, mapping, nested workflow, parallel, conditional,
foreach, loop and timing entries, but this reference is deliberately not the
source of truth for the installed version.

### Data-flow rules

- Give every call site a stable descriptive `id`.
- Map workflow input and prior results explicitly.
- Match mapping keys to the primitive actually invoked.
- Use structured output when branch/loop logic depends on semantic worker output.
- Keep control-flow inputs machine-evaluable rather than asking a later model to
  reinterpret prose.
- Keep mappings within the shapes the installed stored-workflow DSL supports.
- Treat repository state as authoritative for sequential code edits; prompt text
  is not a substitute for observing the actual working tree.

A `createACPTool()` worker and an agent-style primitive may expose different input
and output envelopes. Inspect the installed types/reference and build mappings to
that actual shape rather than assuming `prompt/text` or `task/output` from an
older release.

## Reusable step pinning

A stable call-site `id` is not a code revision. Each reusable step reference
**must** resolve to a registered implementation with an immutable version or
content digest before validation/approval. Record a manifest of `stepId`,
`primitiveId`, resolved version/digest and any nested workflow digest; resolve
installed tool/worker packages or executable artifacts to reproducible identities
where they materially affect behaviour.

Compute the **workflow definition digest** deterministically from the canonical
validated graph *and* this resolved step manifest (including nested references).
For example, hash a canonical JSON envelope containing the schema version,
ordered graph and sorted step manifest; explicitly define canonicalisation and
hash algorithm in the application. A mutable label such as `latest` alone is not
a pin. A planner cannot supply a trusted digest for unregistered code.

On execution and resume, verify that the resolved implementations still match
the approved manifest. Reject/block or explicitly replan/reapprove when a pinned
step is unavailable or differs; do not substitute a newer implementation within
the old run. Changing any step digest changes the workflow digest even if the
graph topology is unchanged.


## Validation

Before upsert/registration:

- validate JSON/schema structure;
- verify every referenced primitive ID exists and is permitted;
- verify mapping expressions and upstream/downstream schemas;
- reject unsupported graph types;
- reject unbounded loops/retries;
- enforce maximum fan-out/concurrency and cost/task budgets;
- reject unsafe overlapping mutations;
- ensure adaptive planner output cannot introduce code, commands, tools,
  permissions, roots or credentials through graph data.

Allow one bounded repair of malformed planner output only when the repair can be
validated deterministically. Never silently execute a different simplified graph.

## Start sources and approval policy

Support starts from `cli`, `schedule`, `webhook` and `chat` through one trusted
application entry boundary. For every accepted *new* execution, mint a unique
`runId` and persist `trigger.type`, trusted caller/tenant, source event ID,
idempotency key, received timestamp, requested definition digest and effective
policy/approval mode before any side effect.

| Source | Trusted idempotency event | Authority and approval |
| --- | --- | --- |
| CLI | Invoker + command invocation ID | Authenticated operator scope; interactive or queued approval |
| Schedule | Schedule ID + scheduled fire time / occurrence ID | Scheduler service identity; previously authorised policy scope only |
| Webhook | Verified issuer + delivery/event ID | Authenticate signature and tenant; external payload grants no authority |
| Chat | Conversation ID + message/turn ID | Authenticated speaker scope; chat text alone is not execution approval |

Retries of one event must return the existing `runId`/outcome, not create an
additional side-effecting run. An intentional manual re-run uses a new event ID.
Do not confuse a chat session, delivery ID or schedule definition ID with a run
ID. Persist the resolved trigger provenance for auditing and deduplication.

All starts **must** pass the same graph validation, limits, resource scope and
mutation/cost approval boundary. Unattended sources must suspend/queue when new
approval is required; they cannot implicitly auto-approve because they lack a UI.
Record the policy version and explicit grant used for any permitted auto-run.


## Run identity, limits, and progress

Keep run lifecycle policy explicit and outside worker discretion. A practical run
record should preserve, when relevant:

- a stable `runId`;
- workflow definition ID plus immutable digest/revision;
- source/repository state identity used by the run;
- applicable policy version;
- configured concurrency, worker/task, retry/round, time, and token/cost limits;
- cumulative usage counters;
- status, termination reason, and the last durable execution/checkpoint state;
- trusted trigger/idempotency origin, retention policy and deletion deadline;
- pinned reusable step manifest and correlated trace identity.

Treat effective limits as:

```text
deployment hard caps
  ∩ workflow defaults
  ∩ per-run requested limits
```

A run-level request may reduce an allowed budget but must not create authority to
raise a deployment cap. Enforce the effective values in deterministic
application/Mastra integration code, not in planner prose or worker instructions.

When a run suspends, persist cumulative resource usage with the run. Resuming must
not reset total workers/tasks started, retries/rounds already consumed, or
token/cost usage already observed. If the installed runtime distinguishes active
execution time from paused wall-clock time, that may be used for an active-time
budget; otherwise define the time budget using evidence the integration can
actually measure and do not claim pause-exclusion semantics.

Expose operator progress from authoritative runtime state: stored step results,
execution/checkpoint state, registered run status, or native tracing. Do not rely
on a worker saying which phase is active or how much budget remains. When broader
trace reconstruction is required, compose with the `agent-observability` skill
and map existing Mastra/native trace hooks into that contract rather than adding a
parallel source of truth.

When scale or cost is uncertain, first run the smallest representative calibration
case that exercises the real worker/runtime boundary. Use observed concurrency,
latency, retry and cost evidence to choose larger-run limits; do not extrapolate
from planner estimates alone.

## Retention and safe persistence

Require an explicit `retentionPolicy` on durable run records, with effective
settings bounded by deployment policy. Default to `terminalTtlDays: 30` from
terminal completion and `suspendedIdleTtlDays: 30` from the last trusted
activity. Active runs must not be deleted mid-execution. After a suspended
run exceeds its idle TTL, mark it `expired`/terminal, deny resumption, revoke
pending approvals, and start terminal retention. Any longer legal/audit hold or
shorter data-minimisation setting must be an explicit authorised policy.

Expiry **must** delete the run/checkpoints, proposed and approved plans,
redacted worker outputs, logs/traces (including external stores), approval
requests/decisions, receipts and attached artifacts/references according to
their policies. Keep immutable versioned definitions and step manifests while
they are referenced by live or retained runs; unreferenced retired definitions
default to 30 days before purge. Current published definitions are retained
until explicitly retired. Do not delete a referenced definition while a run
can resume. Expire tenant-scoped links and coordinate backup/export retention
with the same stated policy; record deletion failures for retry/escalation.

**Redact before every write or export**, including planner proposals and
validation errors, approved graph/metadata, run snapshots, structured logs,
worker stdout/stderr and tool results, error stacks, approvals, receipts,
artifacts and telemetry. Remove or mask API keys, bearer/basic auth, cookies,
connection strings, passwords, private keys, environment-file contents and
other policy-classified secrets or personal data. Prefer allowlisted structured
fields and opaque secret-manager references; apply field-based scrubbing plus
content scanning/truncation to unstructured text. Preserve safe digests/IDs,
status and counters instead of raw secret-bearing payloads.

Treat model and ACP outputs as untrusted: sanitize at the boundary *before*
Mastra storage, application databases, loggers, snapshots and observability
exporters can receive them. Mastra's `SensitiveDataFilter` (where available)
is defence in depth for spans, **not** a substitute for sanitising stored
workflow data and all log/export paths. If a storage or tracing integration
writes raw payloads before an interception point, disable that capture path
until it is controlled. Never persist a secret merely to resume a run: resolve
an opaque handle again at execution with current permissions. Test structured,
free-text and nested secret leakage, and verify actual deletion.

## Telemetry span and export contract

Capture one correlated logical span per run, step attempt, ACP/registered worker
invocation and approval decision. All four types **must** carry
`workflow.run_id` and `workflow.definition_digest`, plus trace/span-parent IDs,
name/type, start/end, status/error class and policy version. Step and worker
spans also carry `workflow.step_id`, pinned `workflow.step_digest` and
attempt number; approval spans carry request/decision IDs, result and approver
role (never credentials or sensitive identities). Record cumulative usage and
termination reason on the run span when known. Model prompts, raw outputs and
approval secrets are not required span attributes.

The run is the root; step attempts are children and worker calls children of
their step. Reuse/enrich Mastra's native workflow-run and workflow-step spans;
map native tool/agent or `createACPTool()` execution spans to worker calls.
The application approval gate must emit a correlated approval span/event; it
is **not** automatically instrumented just because Mastra traces workflow
steps. Across suspension/restart, persist trace context and correlate a new
approval decision span rather than assuming one in-memory span can stay open.
Do not duplicate native spans merely to rename them.

Configure the installed `@mastra/observability` package and map its current
trace/span hooks to these attributes, enriching at the integration boundary.
Export sanitised spans through the appropriate current Mastra-supported
OpenTelemetry-compatible exporter/bridge to an OTLP collector and then the
chosen backend; verify the exporter/package API in the installed version.
Keep `MastraStorageExporter` if local Studio traces are required, while
applying the same redaction and expiry rules to **every** destination.
Propagate context to ACP workers when supported, otherwise correlate the
wrapper span using the stable run/step IDs. Do not claim that ACP internals
are automatically traced.

Official source check (2026-11-02): Mastra's
[observability guide](https://mastra.ai/docs/observability/overview)
describes `Observability`, `MastraStorageExporter`, `SensitiveDataFilter`,
automatic workflow/step/tool spans and external provider support;
[storage guide](https://mastra.ai/docs/storage) describes domain-specific
storage. These are current-doc examples, not guarantees for an older installed
package. See [`remote-docs.md`](remote-docs.md) for version precedence.


## Persistence and execution

Mastra can persist dynamic workflow definitions and expose them through stored
workflow APIs/client operations. Use the project's existing route/client style.
Current Mastra documentation has exposed stored workflow management under
`/api/stored/workflows`, but that path is **version-sensitive guidance, not a
stable contract**. Before using or generating code for it, verify the exact route
and operation shape against the installed Mastra version's docs/types/source or,
when no version is installed yet, the current official documentation. Follow the
source-precedence and verification record in `references/remote-docs.md` rather
than hard-coding this path from the skill text alone.

Bind every durable run to the exact stored workflow definition identity/digest and
the policy settings it executes. For adaptive runs, also preserve the exact
approved definition and its validation/approval decision. Replanning produces a
new graph identity and a new validation/approval decision.

Updating a stored workflow definition must affect future runs only. A suspended
run must resume the definition it was already bound to; if the installed runtime
does not provide a trustworthy definition-pinning guarantee, snapshot/version the
definition in the integration layer and resume from that immutable identity
instead of silently adopting current workflow contents.

Do not claim cross-process/session resumability merely because a workflow can be
stored. Verify the installed run lifecycle, suspension/resume semantics,
definition pinning, cumulative-budget persistence, and storage guarantees for the
actual runtime version.

## Completion test

Static file generation is not sufficient evidence of success. When the environment
allows it:

1. instantiate/configure Mastra;
2. validate or register/upsert the definition;
3. load the stored workflow;
4. invoke the narrowest representative calibration input when runtime/cost limits
   are not already evidenced;
5. inspect real workflow/worker output, runtime progress/usage, and repository
   state;
6. run the relevant deterministic checker or acceptance check.

If live ACP authentication or network access prevents step 4+, validate Mastra's
configuration/definition separately and report the exact remaining blocker.