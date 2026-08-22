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

For adaptive runs, persist the exact approved definition with an immutable
identity or digest and the policy settings that validated it. Replanning produces
a new graph identity and a new validation/approval decision.

Do not claim cross-process/session resumability merely because a workflow can be
stored. Verify the installed run lifecycle, suspension/resume semantics and
persistence guarantees for the actual runtime version.

## Completion test

Static file generation is not sufficient evidence of success. When the environment
allows it:

1. instantiate/configure Mastra;
2. validate or register/upsert the definition;
3. load the stored workflow;
4. invoke the narrowest representative input;
5. inspect real workflow/worker output and repository state;
6. run the relevant deterministic checker or acceptance check.

If live ACP authentication or network access prevents step 4+, validate Mastra's
configuration/definition separately and report the exact remaining blocker.