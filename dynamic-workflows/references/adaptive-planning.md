# Adaptive planning contract

Use this reference when a model generates the workflow topology for the current
run rather than executing a graph authored in advance.

Adaptive mode means **runtime graph generation**, not a supervisor improvising
turn by turn and not merely saving model-produced JSON.

The lifecycle is:

```text
understand task
  -> propose structured plan + graph
  -> validate schema and policy
  -> approve when required
  -> persist exact accepted graph
  -> execute
  -> verify
  -> record receipt
```

## Planner boundary

The planner may decide:

- decomposition;
- sequencing and dependencies;
- safe read-only fan-out;
- candidate worker roles from registered IDs;
- bounded loops/repeated checks;
- aggregation shape;
- estimated worker/token/cost budget;
- proposed mutation scopes from allowed roots.

The planner may **not**:

- create or install tools/ACP agents;
- invent an executable command or arbitrary code primitive;
- widen filesystem, network, credential or environment scope;
- change permission policy;
- approve its own plan;
- bypass workflow limits;
- mutate the target repository while planning;
- silently replace a rejected/invalid graph with a simpler one.

Treat planner output as untrusted data.

## Structured envelope

Require structured output rather than prose another agent must reinterpret. The
exact schema can vary, but should preserve:

```json
{
  "objective": "...",
  "assumptions": [],
  "steps": [],
  "stopConditions": [],
  "maxRetries": 0,
  "estimatedAgents": 0,
  "estimatedTokenBudget": 0,
  "graph": []
}
```

Each planned worker step should identify enough policy-relevant information to
validate it mechanically, for example:

- stable step ID;
- kind/type;
- registered primitive ID;
- dependencies;
- read-only vs mutating status;
- permitted scope;
- optional concurrency group;
- task/prompt intent;
- expected structured result when control flow depends on it.

Do not require fields that the runtime/policy cannot use. The purpose is to make
material planning decisions inspectable and enforceable.

## Deterministic validation

Validate the envelope and executable graph separately.

At minimum check:

- JSON/schema validity;
- known graph entry types for the installed Mastra version;
- registered/allowed primitive IDs;
- stable unique step IDs;
- valid dependency references and no accidental cycles;
- valid mappings and schema flow;
- allowed filesystem/resource roots;
- maximum agents/tasks and concurrency;
- maximum retry/round counts;
- token/cost ceilings where the environment exposes them;
- bounded loops and explicit stop/no-progress conditions;
- mutation scopes and concurrent-write safety;
- no executable code/command injection through planner-controlled fields.

A syntactically valid graph is not automatically policy-valid.

## Mutation and concurrency

Prefer adaptive fan-out for independent analysis, search, review, classification,
or other read-mostly work.

For repository mutation, default to one sequential mutation lane. A planner may
propose parallel writers only when deterministic validation can establish
disjoint mutable scopes or the runtime provides isolated workspaces plus an
explicit integration phase.

If safe independence cannot be established, rewrite/reject the concurrency plan;
do not rely on the planner's assertion that edits will not conflict.

## Approval boundary

Require preview/approval before execution when the accepted plan introduces
material mutation, external effects, elevated permissions, unfamiliar resource
scope, or material cost/parallelism.

Approval should cover the things that actually determine blast radius:

- objective and material assumptions;
- exact graph identity/digest;
- registered workers/tools;
- mutation/resource scope;
- permissions/effects;
- concurrency;
- agent/task/retry/token/cost budget;
- stop conditions.

Approval of only the original natural-language request is not approval of an
arbitrarily generated execution graph.

A read-only, low-cost plan may auto-run only when existing policy or explicit user
authorization permits it.

## Persistence and replan semantics

Persist the exact approved graph and a stable identity/digest with the run.

Resume means continue/replay the **same approved graph** under the runtime's actual
resume semantics. Replanning is a new proposal with a new graph identity that
must pass validation and any required approval again.

Do not overwrite the prior graph and call the result a resume.

If source state, branch revision, permissions, policy, registered primitives, or
other material preconditions changed, revalidate before continuing and invalidate
prior evidence where necessary.

## Repair policy

If planner output is malformed or fails a correctable structural constraint, one
bounded repair attempt may be appropriate. Return the concrete validation errors
and require a complete replacement proposal.

Do not repair around:

- missing authority;
- forbidden scope;
- unavailable required capability;
- unsafe parallel mutation that cannot be isolated;
- a budget the task inherently exceeds without human acceptance;
- stale source assumptions that require fresh investigation.

Those conditions require a blocked/replanned decision, not prompt persistence.

## Run receipt

Record enough to inspect and reproduce what happened:

- task/objective;
- plan/graph identity and digest;
- material assumptions;
- validation result and policy version/settings;
- approval decision when applicable;
- actual started/completed/failed steps;
- worker/runtime versions where available;
- token/cost/concurrency observations where available;
- repository/source revision before and after;
- deterministic verification evidence;
- termination reason;
- whether the run is resumable, requires replan, or is terminal.

Do not fabricate lifecycle guarantees the installed Mastra version does not
provide.
