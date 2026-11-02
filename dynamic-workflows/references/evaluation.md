# Dynamic-workflows behavioural evaluation

Use this reference when changing the skill description, applicability boundaries,
routing behaviour **or material execution guidance**. Routing checks establish
that `dynamic-workflows` activates for executable Mastra work without stealing
runtime-neutral design tasks from `agent-workflow-design`. Outcome checks test
whether new operational safeguards affect the implementation the skill produces.

## Matched conditions

Run each case as a matched pair in fresh contexts with the same model, harness,
tools, permissions, repository state, and user prompt.

- **Initial introduction / routing baseline** — `agent-workflow-design` remains
  discoverable but `dynamic-workflows` is absent; compare with a candidate
  exposing both skills. This measures the *pre-skill catalogue*, not a previous
  revision, and protects the runtime-neutral near-miss.
- **Subsequent behaviour revision baseline** — the exact base-commit revision
  of `dynamic-workflows` (with the sibling skill still discoverable); compare
  with the exact candidate revision under review. This is required for the
  operational cases DW-E7–DW-E10 and other material instruction changes. Do
  not remove the changed skill from the baseline to manufacture a gain.

Record base/candidate SHA, evaluation suite revision, verifier, harness/model,
fixtures, observed activation, outcome and cost where exposed. When a harness
hides skill discovery, label a classification exercise a routing surrogate,
not an end-to-end result. Unexecuted comparisons are `NOT_RUN` with a blocker,
not passes; rerun if the candidate or evaluator changes materially.

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

### DW-E6 — durable run lifecycle and cumulative limits

**Prompt**

> Implement a Mastra dynamic workflow with per-run concurrency, worker, retry,
> time, and token/cost limits. It can suspend and resume, and the stored workflow
> definition may be updated while a run is paused. Show how the resumed run keeps
> its definition, progress, and consumed budget.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Behavioural checks**

- binds the run to an explicit workflow definition identity/digest and policy
  settings rather than resolving whatever definition is current at resume time;
- treats a workflow-definition update as affecting future runs, not silently
  mutating an already suspended run;
- keeps worker/task, retry/round, and observed token/cost usage cumulative across
  suspend/resume instead of resetting the budget;
- lets per-run limits tighten deployment hard caps but not widen them;
- claims paused-time exclusion from an active-time limit only when the installed
  runtime/integration can actually measure active versus paused time;
- exposes critical lifecycle progress from runtime-owned state/snapshots/tracing
  rather than worker self-report;
- recommends a narrow representative calibration run before raising poorly
  evidenced concurrency or cost limits.

### DW-E7 — replay-safe trigger identity and deletion

**Prompt**

> Implement a Mastra workflow that sends a notification on signed webhook
> delivery or scheduled occurrence. Each may be retried, even after the
> workflow's 30-day run retention has expired. The runtime may restart.
> Show exactly how retries, old deliveries and operator re-runs behave.

**Setup / fixture**

- One tenant; a verified webhook delivery and trusted schedule occurrence with
  timestamps and immutable source event IDs; inject a duplicate concurrently.
- Stub a notification side effect with an observable invocation counter.
- Advance a controlled clock across completion, run purge, replay-window expiry
  and tombstone deletion; include an event with no trusted event timestamp.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Observable outcome checks**

- uses one trusted CLI/schedule/webhook/chat entry policy, authenticates
  source/tenant and checks approval before side effects;
- atomically claims source- and tenant-scoped keys, so concurrent retries start
  only one run and effect; deliberate re-runs require a new authorised event;
- retained retries return the existing run ID; after run deletion a minimal
  tombstone rejects duplicates without reconstructing a deleted outcome;
- after tombstone expiry, trusted stale-event rejection still blocks replay;
  missing/untrusted event time is rejected unless another bounded replay
  strategy is explicitly implemented;
- tombstone lifetime matches the accepted replay window, and it contains no
  payload, token or unneeded personal identifiers.

### DW-E8 — generated definition retention and approval expiry

**Prompt**

> Build an adaptive Mastra plan-approve-execute workflow. Persist the approved
> graph, pause a run for approval, and delete expired run records without losing
> reusable published workflows. What gets deleted and when?

**Setup / fixture**

- Create one per-run generated graph, one explicitly published reusable graph,
  and a second live run sharing one immutable definition revision.
- Advance a controlled clock beyond suspended-idle TTL and terminal TTL; inject
  a late approval and a legal-hold override.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Observable outcome checks**

- 30-day terminal and suspended-idle defaults (or explicitly authorised
  override), expiry revocation and denial of late resume/approval;
- deletions include plan, approval, receipt, worker artifacts, checkpoint and
  external traces, without removing definitions still referenced by live runs;
- per-run generated definitions are removed with their last retained run;
  stored/approved does not implicitly mean published;
- explicitly reusable definitions remain until retirement, and promotion from
  run-scoped to reusable needs a separate authorised publication/version;
- expiry cannot be deferred or widened by planner text.

### DW-E9 — pre-write redaction and correlated telemetry

**Prompt**

> Implement a Mastra workflow with ACP worker output, stored plans and
> receipts, approval decisions and exported OpenTelemetry spans. An ACP
> worker writes a nested error containing an API key and authorization header.
> Prove neither the database nor the collector receives the secrets.

**Setup / fixture**

- Inject a distinctive canary secret into nested planner fields, stdout/stderr,
  exceptions and tool output; use a fake durable storage writer and OTLP sink.
- Include an approval that occurs after suspension/restart.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Observable outcome checks**

- redacts *before* every snapshot, log, approval, receipt and trace write,
  including nested and unstructured payloads; blocks uncontrolled raw capture;
- verifies absence of the canary in both storage and exported spans rather
  than claiming that `SensitiveDataFilter` covers all destinations;
- models run, step-attempt, worker and approval spans correlated by run ID and
  definition digest; step/worker include pinned step digest;
- preserves/links trace context across restart without inventing native ACP
  internals instrumentation; uses the installed-version-verified export path.

### DW-E10 — backend contract and immutable step revisions

**Prompt**

> Implement a durable Mastra workflow with a reusable registered worker step.
> Change the worker implementation while the workflow is suspended and switch
> from LibSQL to a different storage adapter. Prove that resume cannot execute
> changed step code and that approvals/receipts remain queryable.

**Setup / fixture**

- Version A and B of the same primitive ID with different digests, identical
  graph topology, one suspended approved run; fake adapter missing an approval
  domain; process restart before resume.
- Pre-record original graph+step digest and run ID; then register version B.

**Candidate routing expectation**

`dynamic-workflows` should activate.

**Observable outcome checks**

- workflow digest includes canonical graph *and* resolved immutable step manifest;
  changing A to B changes the workflow digest even with unchanged topology;
- suspended run resumes on A or blocks/replans and requires fresh approval;
  it never silently adopts B;
- LibSQL is retained as local default, but effective backend must durably
  support definitions, runs/checkpoints, approvals, receipts and lookup by run ID
  across process restart;
- missing adapter capabilities are implemented in a durable integration store
  rather than assumed to exist in Mastra storage;
- orchestration remains in Mastra; ACP workers retain only task execution.

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

- DW-E1, DW-E2, DW-E4, DW-E5, DW-E6 and DW-E7–DW-E10 route to
  `dynamic-workflows` when routing is observable;
- DW-E3 routes to `agent-workflow-design`;
- all verifiable behavioural checks pass;
- candidate introduces no routing regression on the runtime-neutral case;
- ACP is used in DW-E4 and not used in DW-E5;
- in the operational suite (DW-E7–DW-E10), each verifiable safeguard has
  explicit observed evidence (or is marked `not_verifiable`) against the base
  revision, not inferred solely from a plausible implementation plan.

Run at least one matched pair per affected case for an outcome smoke test, and
one complete pair per routing case when routing changes. Use three or more paired
trials when model variance or a description change makes the routing conclusion
consequential. Preserve outputs, assertions, run IDs and verifier results.
Static documentation inspection and green CI do not count as runtime behaviour.
Do not claim a behavioural pass until the matched runs are executed and preserved.