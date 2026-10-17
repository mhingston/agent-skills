# Agent Observability Evaluation Scenarios

Use these portable cases when changing turn-aware trace reconstruction or
instruction-availability checks in `agent-observability`. Evaluate the owning
skill under the matched baseline/candidate procedure in
`../../skill-creator/references/evaluation.md`; this file is not a runtime
dependency or an assertion that a behavioural test has already been run.

## AO-E1 — skill-loading race versus legitimate parallel dispatch

**Prompt**

> Our agent loaded a search-guidance skill and performed two lookups, but the
> searches appear to ignore the skill's rules. Design the minimum
> provider-neutral instrumentation and checks needed to diagnose this without
> treating all concurrent tool calls as invalid.

**Fixture**

Supply a synthetic harness trace with observed dispatch and injection
boundaries:

- Assistant turn T1 dispatches a single batch containing `load_skill`,
  `search_docs`, and an independent `list_projects` lookup.
- `load_skill` returns a short launch acknowledgement in T1's tool results.
  The skill body first becomes available to the model in T2.
- `search_docs` is documented as depending on the skill's search rules.
  `list_projects` has no such dependency.
- A control trace dispatches `search_docs` from T3 after the body is available.
- A second control removes injection-time evidence, leaving only a flattened
  tool-call log and a final answer stating that the skill was loaded.

**Routing expectation**

`agent-observability` should activate for trace design and reconstruction,
not the application-debugging or generic readiness route.

**Feasibility**

`fixtureable` — requires only synthetic trace fixtures and an agent that can
assess a trace contract; no real skill loader or provider API is necessary
for this case definition.

**Outcome checks**

- preserves assistant-turn identity, same-batch membership, and the effective
  instruction-context or injection milestone when observable;
- identifies `search_docs` in T1 as dispatched before the rules were available,
  without claiming its subsequent content was governed by those rules;
- leaves `list_projects` concurrent dispatch valid because no instruction
  prerequisite was declared;
- distinguishes the T3 lookup as instruction-eligible without claiming this
  alone proves its answer quality;
- treats the flattened-only control as an evidence gap, not a race proved from
  a final narrative or presumed order;
- does not require storage of raw sensitive prompts, provider-specific event
  names, a new tracing system, or automatic blocking of every parallel call.
