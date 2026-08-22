# Dynamic-workflows behavioural evaluation

Use this reference when changing the skill description, applicability boundaries,
or routing behaviour. The purpose is to test that `dynamic-workflows` activates
for executable Mastra work without stealing runtime-neutral workflow-design tasks
from `agent-workflow-design`.

## Matched conditions

Run each case as a matched pair in fresh contexts with the same model, harness,
tools, permissions, repository state, and user prompt.

- **candidate** — `dynamic-workflows` and `agent-workflow-design` are both
  discoverable.
- **baseline** — `agent-workflow-design` remains discoverable but
  `dynamic-workflows` is absent.

For this new skill, the baseline measures the pre-skill catalogue rather than a
previous `dynamic-workflows` revision. Do not remove the sibling skill from the
baseline: doing so would fail to test the routing boundary that matters.

Record the harness and model. When the harness exposes skill discovery/loading,
record the selected skill directly. If it does not, label any classification
exercise as a routing surrogate rather than an end-to-end routing result.

## Cases

### DW-E1 — adaptive Mastra workflow

**Prompt**

> Build a Mastra dynamic workflow for coding tasks where the decomposition can
> change per request. I want a planner to propose a bounded graph, validate it,
> require approval before repository mutation, then execute it and preserve a run
> receipt.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Behavioural checks**

- selects adaptive rather than deterministic mode;
- treats planner output as untrusted structured data;
- uses a plan -> validate -> approve -> execute boundary;
- keeps orchestration in Mastra rather than a supervisor model conversation;
- does not grant planner output authority to invent tools, roots, credentials, or
  permissions.

### DW-E2 — deterministic Mastra workflow

**Prompt**

> Implement a Mastra workflow that always runs lint, tests, a read-only review,
> and then publishes a verification report in that fixed order. The topology is
> known and should be repeatable.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Behavioural checks**

- selects deterministic mode;
- does not add a planning model merely to restate known sequencing;
- represents ordering and data flow in the executable Mastra graph;
- keeps retries/loops bounded if introduced.

### DW-E3 — runtime-neutral workflow design near-miss

**Prompt**

> Design a durable agent workflow for a review-and-remediation process. I need the
> state machine, authority boundaries, retry semantics, resumability, and
> verification model, but do not choose or implement a runtime yet.

**Candidate routing expectation**

`dynamic-workflows` should **not** activate. Route to `agent-workflow-design`.

**Behavioural checks**

- does not force Mastra, ACP, stored workflows, or any runtime-specific API;
- preserves the runtime-neutral design task;
- candidate behaviour should be no worse than baseline on the sibling skill's
  existing workflow-design contract.

This is the principal anti-collision case.

### DW-E4 — coding workflow using ACP

**Prompt**

> Build a Mastra workflow that sends repository implementation tasks to an ACP
> coding agent, then runs an independent review step. Keep the coding harness
> swappable rather than hard-coding one vendor.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Behavioural checks**

- uses ACP because repository-capable coding work is required;
- treats Mastra as the ACP client and the spawned coding harness as the ACP agent;
- does not invent a fixed supported-harness allowlist;
- preserves explicit repository/workflow state rather than relying on hidden ACP
  chat history;
- defaults overlapping repository mutation to sequential or isolated execution.

### DW-E5 — non-coding Mastra workflow using ordinary tools

**Prompt**

> Build a Mastra dynamic workflow that fetches data from two registered APIs in
> parallel, combines the results, applies a deterministic threshold, and sends a
> notification. There is no repository or coding-agent work involved.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Behavioural checks**

- uses ordinary registered Mastra tools/agents;
- does **not** introduce ACP merely because the skill supports it;
- uses explicit fan-out/fan-in and deterministic aggregation where appropriate;
- keeps authority and external-effect policy in the application/Mastra
  integration layer rather than attributing it to a coding worker.

## Paired grading

For each case record, separately:

1. **Activation** — selected `dynamic-workflows`, selected the sibling skill, or no
   relevant skill; use `not_verifiable` if the harness hides discovery.
2. **Boundary correctness** — did the candidate route DW-E3 away from
   `dynamic-workflows` and avoid ACP in DW-E5?
3. **Outcome behaviour** — pass/fail/not-verifiable for every case-specific check.
4. **Regression** — did the candidate reduce correctness or add unnecessary
   ceremony relative to baseline?
5. **Cost/latency** — record only if exposed by the harness.

The minimum acceptance condition is:

- DW-E1, DW-E2, DW-E4 and DW-E5 route to `dynamic-workflows` when routing is
  observable;
- DW-E3 routes to `agent-workflow-design`;
- all verifiable behavioural checks pass;
- candidate introduces no routing regression on the runtime-neutral case;
- ACP is used in DW-E4 and not used in DW-E5.

Run at least one complete matched pair per case for a routing smoke test. Use
three or more paired trials when model variance or a description change makes the
routing conclusion consequential. Do not claim a behavioural pass until the
matched runs have actually been executed and preserved.