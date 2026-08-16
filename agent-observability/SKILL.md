---
name: agent-observability
description: Design, assess, or improve provider-neutral observability for coding-agent and multi-agent workflows using correlated traces, revision-bound evidence, redaction, and deterministic trace fitness checks. Use when instrumenting agent runs, tool calls, model calls, handoffs, evaluators, retries, costs, checkpoints, or termination reasons, or when diagnosing why agent behaviour cannot be reconstructed reliably. Do not use as a readiness score, application APM replacement, or permission to archive raw prompts and sensitive payloads.
---

# Agent Observability

Make agent behaviour reconstructable from structured evidence rather than conversation memory. Model the run as a correlated trace whose events identify what acted, what it touched, what evidence it produced, why control moved, and how the run terminated.

Observability is a control and learning surface. It does not establish correctness, confer approval, or create authority that the workflow did not already have.

## Boundaries

- Instrument the harness, orchestrator, tool boundary, or workflow controller rather than relying on the model to narrate its own history.
- Preserve missing telemetry as a gap. Never ask a model to invent events, costs, tool results, identities, timestamps, revisions, or approvals that were not captured.
- Prefer metadata, hashes, immutable references, and redacted summaries to raw prompts, responses, source files, environment values, credentials, or customer data.
- Keep application telemetry and agent-run telemetry distinct even when they share correlation IDs. Application traces describe product/runtime behaviour; agent traces describe the automation that reasoned and acted.
- Do not treat a valid trace schema, low cost, few retries, or a successful termination code as proof that the result is correct.
- Do not turn observability into unrestricted surveillance of engineers or performance ranking. Instrument workflows and technical controls, not personal productivity.
- Do not make merge, deploy, security, compliance, or risk decisions from telemetry unless a separately owned policy explicitly defines that gate.

## Route adjacent work

Use this skill to design or evaluate the telemetry and trace contract around agents. Prefer another workflow when the primary task is:

- deciding whether a repository is ready for a given autonomy level: use an agent-readiness assessment;
- reviewing one code change: use technical review;
- analysing recurring lessons across multiple sessions: use a longitudinal session-learning workflow;
- debugging an application failure without a material agent-control question: use ordinary application diagnostics;
- defining business KPIs or general service observability: use the relevant product/SRE practice.

## 1. Define the observability contract

Establish:

- workflow or agent system in scope;
- decisions the telemetry must support, such as diagnosis, recovery, cost control, reviewer independence, auditability, or learning;
- actors and execution boundaries;
- required revision, task, source, and external-operation identities;
- environments and data classifications involved;
- retention and access constraints;
- acceptable instrumentation overhead;
- existing tracing, logging, metrics, or event infrastructure that should be reused.

Start from concrete reconstruction questions, for example:

- Which model and instructions produced this change?
- Which tools ran, with what result and latency?
- Did a reviewer inspect the same revision the implementer produced?
- Why did the loop retry or stop?
- Which state was last known-good before recovery?
- Did a human actually approve the consequential action?

If a field does not help answer a real control, diagnosis, recovery, or learning question, do not collect it merely because it is available.

## 2. Model stable identities first

Use stable correlation fields consistently across events. A typical minimum is:

- `trace_id` — one end-to-end workflow or agent run;
- `span_id` — one event or bounded operation;
- `parent_span_id` — causal parent when applicable;
- `run_id` — one concrete execution attempt;
- `session_id` — optional conversational or harness session identity;
- `task_id` — canonical work item or research/task identity when available;
- `producer_id` — agent, model role, tool, or human actor identity at the level the harness can actually prove;
- `base_revision` and `head_revision`, or an equivalent deterministic state fingerprint for uncommitted work;
- `source_version` — ticket, specification, policy, prompt bundle, or other authoritative input version when material.

Do not use a commit SHA to identify uncommitted product state. Record a deterministic working-state fingerprint or mark the state identity unavailable.

Do not guess hidden model, user, tool, or reviewer identity. Use `unknown` or omit an optional field when the harness cannot expose it reliably.

## 3. Define event types and required evidence

Keep the event vocabulary small enough to stay consistent. Common event classes are:

### Agent run

Capture:

- goal or task reference;
- producer/harness identity;
- repository or workspace identity;
- start and end state identities;
- status and termination reason;
- duration;
- summary or evidence reference rather than a self-certified correctness claim.

### Model call

Capture when available:

- model/provider/profile identity;
- instruction or prompt-bundle version/reference;
- input/output token counts;
- cost or billing unit;
- latency and status;
- redacted request/response hash or immutable artefact reference when justified.

Do not require raw prompt retention merely to make a model call observable.

### Tool call

Capture:

- tool name and version or endpoint identity when material;
- operation class such as read, write, execute, message, deploy, or external side effect;
- redacted input/output references or hashes;
- exit/status code;
- latency;
- retry/idempotency identity when relevant;
- changed external state or receipt identity for consequential writes.

### Handoff or delegation

Capture:

- source and target actor;
- reason for handoff;
- task/scope contract;
- exact state or revision handed off;
- evidence packet reference;
- requested next action;
- returned status and unresolved items when the child completes.

### Evaluation or review

Capture:

- producer under evaluation;
- evaluator identity and execution context when known;
- exact revision/state inspected;
- evaluation method or check reference;
- result and evidence reference;
- known correlation limits, such as shared model family, prompt family, source context, or tools.

Do not label a reviewer independent merely because it was a different subagent. Independence is an evidence property, not a process name.

### Error, retry, checkpoint, or recovery

Capture:

- failing parent span;
- error class and safe message/reference;
- retryability classification and attempt count;
- retry or recovery reason;
- previous and resulting state identity;
- last known-good state when available;
- stop, stall, divergence, budget, timeout, or policy reason when control terminates.

### Human decision

When consequential human judgement is part of the workflow, capture only what the system can prove:

- decision type;
- actor identity from the authoritative approval surface;
- revision/state and evidence presented;
- decision value;
- timestamp and source receipt/reference.

A model-written note saying “approved by human” is not a human-decision event.

## 4. Separate payloads from trace metadata

Keep the trace compact and durable by storing references rather than sensitive or high-volume payloads.

Prefer:

```text
trace event -> immutable/redacted artefact reference -> protected payload store
```

over embedding full prompts, source files, logs, transcripts, or tool payloads directly in every event.

For each referenced artefact, preserve enough metadata to detect drift or substitution, such as content hash, revision, capture time, producer, and retention class.

Apply explicit redaction before persistence. At minimum consider:

- credentials, tokens, cookies, authorization headers, signing material;
- environment variables and secret-bearing command arguments;
- customer/member/user personal data;
- proprietary source or document content not required for the trace consumer;
- unrestricted raw model prompts/responses;
- external tool payloads with broader access than the observability audience.

Hashing a secret does not automatically make retaining it appropriate. Collect less before relying on redaction.

## 5. Instrument outside the model loop

Prefer deterministic instrumentation at boundaries the model cannot silently bypass:

- orchestrator state transitions;
- model client wrappers;
- MCP/tool dispatch;
- shell/executor wrappers;
- delegation interfaces;
- review/evaluation runners;
- approval connectors;
- git/revision checkpoints;
- external write/read-back receipts.

When the harness exposes native trace hooks, map them into the common event contract instead of building a competing parallel recorder.

Do not ask the agent to remember to emit critical security, authorization, cost, or completion events when the harness can capture them mechanically.

## 6. Add deterministic trace fitness checks

Validate trace structure separately from semantic outcome quality. Useful checks include:

- required fields exist for each event type;
- trace/span IDs are unique and parent references resolve;
- no impossible cycles exist in parentage;
- timestamps and durations are internally coherent within known clock limits;
- a completion state has an explicit termination reason;
- revision-sensitive review/evaluation events name the exact state inspected;
- write events have a receipt or explicit unknown-result state;
- retries do not exceed configured bounds;
- cost/token/latency totals reconcile with observable child events;
- evaluator and producer identities are not silently conflated;
- redaction rules reject prohibited fields or payload classes;
- unknown or missing fields remain gaps rather than fabricated defaults.

A trace that passes these checks is structurally trustworthy enough to analyse. It is not proof that the agent made the right decision.

## 7. Define useful derived metrics

Derive metrics only from captured events and state what they mean. Common examples include:

- end-to-end duration and active model/tool time;
- model calls, tool calls, retries, handoffs, and remediation rounds;
- token and cost totals by stage or model profile;
- failed-tool and retry rates;
- time to first deterministic failure signal;
- no-progress/stall termination frequency;
- reviewer/evaluator coverage by exact revision;
- recovery frequency and distance from last known-good state;
- completion versus blocked/stale/policy-stop rates;
- repeated correction categories suitable for later session-learning analysis.

Do not convert activity volume into developer performance, or optimization metrics into task-quality metrics. Fewer calls and lower cost are not improvements if evidence coverage or correctness declines.

## 8. Design retention and access

Define:

- event and artefact retention periods;
- who can access metadata versus referenced payloads;
- deletion and legal/privacy requirements;
- whether traces cross repository, team, tenant, or environment boundaries;
- encryption and storage controls appropriate to the data;
- sampling policy for high-volume non-control events;
- events that must never be sampled away, such as consequential writes, approvals, security denials, termination reasons, and recovery checkpoints.

Prefer retaining compact control metadata longer than raw payloads. Do not let observability become a second uncontrolled data lake.

## 9. Evaluate reconstruction quality

Test the design with realistic traces. Given only the retained evidence, an independent operator should be able to answer the intended reconstruction questions without relying on the original conversation.

Include failure cases such as:

1. a tool call fails and retries;
2. the agent modifies uncommitted state before review;
3. review runs against an obsolete revision;
4. context compaction or process restart occurs;
5. an external write times out with uncertain outcome;
6. a model or harness version changes mid-workflow;
7. an approval is claimed in prose but no authoritative receipt exists;
8. a sensitive value appears in a tool argument and must be rejected or redacted.

Treat any answer that requires guessing as an observability gap.

## Output contract

Return the smallest design or assessment that preserves these semantics:

1. **Scope and reconstruction goals** — workflows, actors, decisions, risks, and data boundaries.
2. **Identity model** — trace, run, task, actor, source, revision/state, and artefact identities.
3. **Event contract** — event types with required and optional fields.
4. **Instrumentation map** — where each event is captured and which boundary owns it.
5. **Privacy and retention** — prohibited payloads, redaction, references, access, sampling, and retention.
6. **Trace fitness checks** — deterministic structural validations and failure behaviour.
7. **Derived metrics** — only metrics tied to a stated diagnosis, control, cost, or learning question.
8. **Reconstruction tests** — representative normal and failure scenarios.
9. **Gaps and next action** — missing instrumentation, unknown identities, or the smallest implementation/evaluation step that would close the highest-value gap.

For an assessment, label each material field or control `Supported`, `Partial`, `Unsupported`, or `Unknown` and cite the observed instrumentation or trace evidence. For an implementation request, preserve the existing telemetry stack and add the smallest compatible instrumentation rather than introducing a new platform by default.

## Quality gate

Before returning, verify that:

- every collected field supports an explicit reconstruction, control, diagnosis, cost, recovery, or learning question;
- state and revision identities are strong enough for revision-sensitive claims;
- critical events are captured outside model self-report where practical;
- model, tool, handoff, evaluation, error, retry, recovery, and human-decision evidence remain distinguishable;
- reviewer independence is not inferred from labels alone;
- application and agent telemetry are not conflated;
- raw sensitive payload retention is minimized and redaction occurs before persistence;
- missing telemetry remains visible rather than reconstructed by a model;
- deterministic trace fitness is not confused with semantic correctness;
- observability did not create new approval or operational authority.
