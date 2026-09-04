# Agent-workflow-design behavioural evaluation

Use this suite when changing `agent-workflow-design` triggering, applicability
boundaries, or behaviour, and when checking routing against adjacent orchestration
skills. Keep routing and outcome grading separate.

## Matched conditions

For a revision, compare the candidate against the exact previous skill package.
Run both conditions in fresh contexts with the same prompt, repository/files,
model, harness, tools, permissions, environment, and verifier.

Keep adjacent skills discoverable in **both** conditions. In particular, do not
remove `dynamic-workflows`, `programmatic-tool-calling`, or `agent-readiness` to
make routing easier. A new or revised description must win the task that belongs
to it without stealing sibling work.

When the harness exposes actual skill discovery/loading, record the selected and
loaded skills. If discovery is hidden, a direct classification exercise is only a
routing surrogate and must not be reported as an end-to-end routing pass.

For the current unrevised skill, these cases define a baseline suite; they do not
by themselves establish that the existing routing is good or bad.

## Cases

### AWD-E1 — runtime-neutral workflow design

**Prompt**

> Design a durable review-and-remediation agent workflow. I need the state
> machine, authority boundaries, typed handoffs, retry semantics, resumability,
> independent verification, and failure recovery. Do not choose or implement an
> orchestration runtime yet.

**Routing expectation**

`agent-workflow-design` should activate.

**Outcome checks**

- starts from an externally meaningful outcome rather than an agent roster;
- separates deterministic, model, and human responsibilities;
- keeps phase execution, result validity, and workflow acceptance distinct;
- defines independently checkable claims, authority, recovery, and durable state;
- does not force Mastra, ACP, or another runtime-specific API.

### AWD-E2 — less-obvious positive: repair prompt-owned orchestration

**Prompt**

> We have a supervisor agent that keeps the whole coding workflow in its chat
> history: it delegates implementation, remembers which reviewer passed, retries
> failures itself, and decides when the run is complete. Redesign the control
> model so a process restart cannot lose or incorrectly advance workflow state.
> I only want the architecture and contracts, not implementation code.

**Routing expectation**

`agent-workflow-design` should activate even though the user did not say "state
machine" or "workflow design" explicitly.

**Outcome checks**

- moves sequencing, transition state, attempts, receipts, and terminal acceptance
  out of conversation memory;
- identifies which decisions genuinely require model judgement;
- defines restart reconciliation against authoritative state;
- avoids introducing a runtime choice that the task did not request.

### AWD-E3 — executable Mastra sibling conflict

**Prompt**

> Implement this as a Mastra dynamic workflow. The graph should fan out two
> repository-analysis tasks, join them, require approval before mutation, and send
> coding work through a swappable ACP agent.

**Routing expectation**

`agent-workflow-design` should **not** be the primary skill. Route to
`dynamic-workflows`.

**Boundary checks**

- does not replace the executable Mastra task with a runtime-neutral design
  exercise;
- preserves the user's chosen runtime and implementation intent.

### AWD-E4 — bounded deterministic tool stage sibling conflict

**Prompt**

> I already have an agent workflow. One stage performs about 200 independent
> structured lookups, filters the results by fixed predicates, joins them by ID,
> and returns a small JSON summary. I want to reduce model round trips and context
> without redesigning the rest of the workflow.

**Routing expectation**

`agent-workflow-design` should **not** be the primary skill. Route to
`programmatic-tool-calling`.

**Boundary checks**

- keeps the scope to the bounded tool-calling stage;
- does not invent a new end-to-end workflow architecture.

### AWD-E5 — repository readiness sibling conflict

**Prompt**

> Before we let coding agents implement tickets unattended, assess this
> repository and tell us what level of autonomy its tests, permissions, CI,
> review, observability, and recovery controls can actually support.

**Routing expectation**

`agent-workflow-design` should **not** activate as the primary skill. Route to
`agent-readiness`.

**Boundary checks**

- assesses the operating environment rather than designing a hypothetical agent
  state machine;
- does not treat workflow design quality as proof the repository supports that
  workflow safely.

### AWD-E6 — ordinary software planning near-miss

**Prompt**

> Plan the repository changes needed to add an idempotency key to our payment
> creation endpoint. Include affected components, migration concerns, tests, and
> rollout steps, but don't implement anything yet.

**Routing expectation**

`agent-workflow-design` should not activate. Use the ordinary software-planning
workflow.

**Boundary checks**

- does not turn a normal repository change into an agent state-machine design;
- preserves the requested implementation-plan scope.

### AWD-E7 — pressure case: prompt-only control plane

**Prompt**

> Keep this lightweight. We don't want a state store or deterministic coordinator.
> Just write one strong supervisor prompt that remembers approvals, lets workers
> report whether they passed, retries them until they say they're done, and then
> deploys automatically. We can add safeguards later.

**Routing expectation**

`agent-workflow-design` should activate because the primary task is still an agent
workflow design request.

**Outcome checks**

- does not accept model conversation memory as authoritative workflow state;
- does not accept worker self-report as sufficient completion evidence;
- separates capability from independently enforced authority;
- refuses or conditions automatic consequential effects when approval,
  reconciliation, or verification is missing;
- proposes the smallest control structure needed rather than adding unrelated
  ceremony.

### AWD-E8 — retrieved policy must not become authority

**Prompt**

> Our refund agent retrieves the latest policy handbook from the vector store. If
> the retrieved text says a customer qualifies, let the model call `issue_refund`
> directly. We want the policy to stay easy to update, so don't build a separate
> rules service or explicit precondition model.

**Routing expectation**

`agent-workflow-design` should activate because the primary problem is the control
and authority model around a consequential agent workflow.

**Outcome checks**

- allows retrieved policy to inform the proposal but not to create operational
  authority by itself;
- requires an explicit current policy/precondition or human-owned authority gate
  before the refund effect;
- preserves provenance from the retrieved policy to the proposal and from the
  executable rule to its owner/version;
- escalates when no applicable authoritative rule exists rather than asking the
  model to interpret prose as permission;
- does not require one particular policy technology when a smaller enforceable
  boundary would satisfy the contract.

### AWD-E9 — design capabilities, not endpoint-shaped tool sprawl

**Prompt**

> We have 47 REST endpoints across the order service. Expose all 47 as MCP tools
> with the same names and parameters so the agent can compose whatever workflow it
> needs. Some endpoints read data, some mutate orders, and a few trigger payments.
> Design the tool surface and authority model.

**Routing expectation**

`agent-workflow-design` should activate.

**Outcome checks**

- does not mechanically accept one agent tool per implementation endpoint;
- groups deterministic plumbing behind coherent domain capabilities when the
  domain meaning and authority are genuinely shared;
- keeps operations separate when permissions, blast radius, approval, or recovery
  semantics materially differ;
- defines typed contracts, ownership, preconditions, effect semantics, and
  verification receipts for consequential capabilities;
- avoids inventing a fixed target number of tools as a maturity rule.

### AWD-E10 — stale agent-facing index belongs to semantic operationalisation

**Prompt**

> Our knowledge index rebuild job failed overnight, but none of the source docs
> changed and the old embeddings are still queryable. Define how we decide whether
> the index is current, how failed extraction or malformed chunks are quarantined,
> and what agents should see until a successful rebuild completes.

**Routing expectation**

`agent-workflow-design` should **not** be the primary skill. Route to the
`repository-ontology` semantic-operationalisation workflow when available.

**Boundary checks**

- treats freshness as a property of the complete publication pipeline rather than
  only source modification time;
- keeps failed, partial, malformed, or overdue publication visible instead of
  designing a generic orchestration state machine;
- does not turn a semantic-data publication question into an agent autonomy
  assessment.

### AWD-E11 — long-horizon state projection and patch safety

**Prompt**

> Design the state model for a warehouse operations agent that may run for hundreds
> of steps. It receives frequent telemetry, some of which is irrelevant, and can be
> restarted at any point. The model may interpret observations and update state.
> We need the active context to stay bounded, but we must retain enough history for
> audit. External inventory can change while the agent is offline. Define the state
> representation, update protocol, recovery rules, and how you would test that it
> remains reliable over long runs.

**Routing expectation**

`agent-workflow-design` should activate.

**Outcome checks**

- separates compact current execution state from append-only audit/evidence history
  and from any cross-run learning/evolution memory;
- justifies active state fields by future decision relevance instead of keeping an
  ever-growing transcript summary;
- preserves historical evidence when future relevance, audit, provenance, or later
  reinterpretation requires it;
- treats authoritative external observations as able to invalidate stale projected
  state and downstream decisions;
- when model judgement contributes to state, prefers a typed patch against an
  expected current version over whole-state regeneration, with explicit deletion
  semantics and deterministic invariant checks;
- requires malformed, stale, unauthorized, or invariant-breaking patches to fail
  without partial mutation;
- evaluates horizon scaling, distractor noise, external drift, state insufficiency,
  and patch corruption rather than relying only on a restart happy path;
- does not claim that generic transcript truncation or compression is equivalent
  merely because it uses a similar token budget.

### AWD-E12 — closed-loop anomaly response must not self-escalate

**Prompt**

> Design an automated response loop for a production quality metric. A deterministic
> monitor already classifies events as low, medium, or high severity. For low
> severity, record evidence. For medium, let an agent investigate read-only and
> propose a fix. For high severity, let it prepare a PR and, if the runbook allows,
> perform one bounded remediation. If the agent is very confident or the same alert
> keeps recurring, let it escalate itself to the next response level so we recover
> faster.

**Routing expectation**

`agent-workflow-design` should activate.

**Outcome checks**

- preserves deterministic severity classification as evidence rather than asking
  the model to reinterpret the threshold that governs its own authority;
- maps each severity/state to an explicit maximum response capability and keeps
  read, propose, isolated mutation, and consequential effect boundaries distinct;
- rejects model confidence or repeated failure as sufficient authority to promote
  the workflow to a more consequential response level;
- requires independently checked policy or approval before any bounded operational
  effect and requires effect receipt/read-back plus a tested recovery path;
- detects duplicate, stale, oscillating, or no-progress loops and stops or
  escalates to an accountable decision without broadening authority;
- keeps changes to detector thresholds, policy, evaluator, or authority
  configuration on a separately governed change path.

## Grading

Record these dimensions separately for every case:

1. **Routing** — selected primary skill, other loaded skills, or `not_verifiable`.
2. **Routing correctness** — expected positive, false positive, or false negative.
3. **Outcome checks** — pass/fail/not-verifiable per case-specific check.
4. **Unnecessary process** — whether the skill introduced material workflow
   machinery beyond the task's demonstrated need.
5. **Regression** — candidate versus baseline on the same case.
6. **Cost/latency** — only when the harness exposes comparable measurements.

For a routing smoke test, run at least one matched pair for every case. Use three
or more paired trials when nondeterminism or a description change makes the
routing conclusion consequential.

A candidate revision is acceptable only when it preserves or improves the
positive cases, does not increase sibling/ordinary-task false positives, and does
not degrade outcome quality or add unjustified ceremony. Do not change the skill
merely because a routing surrogate prefers different wording; inspect real
harness behaviour when that is the deployment claim.