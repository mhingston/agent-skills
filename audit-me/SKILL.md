---
name: audit-me
description: >
  Audit the user's work surfaces and recurring workflows to identify dropped
  commitments, fragmented context, repetitive coordination work, stale work,
  missed deadlines, and other automation opportunities. Use when asked what
  work could be automated, how to reduce operational overhead, how to design
  scheduled agents, or how to turn recurring friction into reliable workflows.
---

# Workflow Automation Auditor

Identify valuable automation opportunities and turn them into safe, precise,
testable, and harness-agnostic automation specifications.

Do not merely produce a generic list of ideas. Ground recommendations in the
user's actual responsibilities, tools, recurring work, evidence, and failure
modes.

## Core principle

Automate the scaffolding around human work, not the human responsibility itself.

Good automation:

- assembles context;
- detects forgotten commitments;
- surfaces anomalies and stale work;
- tracks deadlines and dependencies;
- records evidence of completed work;
- drafts or recommends next actions;
- removes repetitive information gathering.

Do not automate:

- sensitive personnel decisions;
- performance judgements;
- emotionally significant communication;
- irreversible actions without explicit approval;
- decisions requiring accountability, empathy, or organisational authority.

## When invoked

Determine which work surfaces are available or relevant, such as:

- repositories, issues, pull requests, reviews, and notifications;
- email, calendar, meetings, and messages;
- project-management systems;
- documents, decision records, and meeting notes;
- CI/CD, monitoring, incident, release, and security systems.

Do not require every surface to be connected. Work with the available evidence
and identify blind spots explicitly.

## Audit workflow

### 1. Establish the responsibility model

Infer or determine:

- outcomes for which the user is accountable;
- recurring activities and review cadences;
- people or teams depending on the user;
- deadlines or service expectations;
- systems where relevant information lives;
- tasks that require repeated context reconstruction;
- mistakes or omissions that damage trust.

Focus on responsibilities rather than merely enumerating tools.

### 2. Search for friction patterns

Look for:

- **Fragmented context** — one task requires reconstruction across several systems.
- **Dropped commitments** — a promise, assignment, or action item is not tracked.
- **Stale work** — work exists but progress, ownership, or escalation has stopped.
- **Repetitive surveillance** — multiple systems are repeatedly checked for change.
- **Evidence loss** — useful outcomes or decisions are hard to reconstruct later.
- **Administrative friction** — low-judgement coordination repeatedly consumes attention.

Treat phrases such as "I'll", "let me", "I'll take a look", "action", and
"follow up" as commitment candidates, not proof of an obligation. Verify the
speaker, context, expected outcome, and evidence of completion.

### 3. Choose the implementation form

For every candidate classify the lightest reliable delivery mechanism:

- scheduled prompt only;
- scheduled prompt invoking an existing skill;
- new reusable skill plus one or more scheduled invocations;
- deterministic script, query, CI check, or ordinary workflow;
- event-driven automation rather than a scheduled run;
- not suitable for automation.

Prefer a prompt prototype when the logic is narrow and still changing. Recommend
a reusable skill when the procedure, evidence rules, boundaries, or evaluation
criteria recur across multiple invocations. Prefer deterministic code when the
decision can be expressed and verified mechanically.

Do not assume a particular scheduler, manifest format, agent harness, state
store, or configuration schema.

### 4. Classify the time model

Classify each candidate as:

- **Fast signal** — recent events and current operational state.
- **Slow model** — patterns learned over weeks or months.
- **Hybrid** — a durable baseline combined with a recent delta.

State the recent window, historical window, refresh expectations, freshness
requirements, and behaviour when the slow model or live sources are unavailable.

### 5. Define context and state

For every candidate specify the context it may need, such as:

- responsibility and ownership model;
- active projects and current priorities;
- repository or service relationships;
- release and deadline context;
- known exceptions and intentional waiting periods;
- historical cadence baseline;
- previous-run findings and feedback.

Define a state contract without prescribing a storage technology or serialization
format. Include when relevant:

- stable identity for each finding;
- first-seen, last-seen, and last-source-activity times;
- previous and current classification;
- resolution evidence;
- dismissal or snooze status;
- source coverage and last successful scan;
- retention, sensitivity, and deletion expectations.

A repeated search is not stateful merely because the harness retains a chat.

### 6. Generate candidate automations

Create narrowly scoped candidates rather than one omniscient agent.

For each candidate provide:

- **Name**
- **Problem**
- **Evidence**
- **Who benefits**
- **Data sources**
- **Implementation form**
- **Time model**
- **Trigger or schedule**
- **Detection logic**
- **Required context**
- **State contract**
- **Output**
- **Permitted actions**
- **Actions requiring approval**
- **Failure and uncertainty behaviour**
- **Privacy or security concerns**
- **Operational budget**
- **Success metric**
- **Evaluation fixtures**

The operational budget should cover maximum findings, run frequency, acceptable
noise, cost or execution limits, silence policy, and an automatic pause condition.

Evaluation fixtures should include:

- positive cases that must be surfaced;
- negative cases that must remain silent;
- ambiguous cases that must report uncertainty;
- regression cases from known false positives or misses.

### 7. Prioritise candidates

Score each candidate from 1–5 on:

- frequency;
- time or attention consumed;
- cost of omission;
- predictability of the decision;
- availability and reliability of input data;
- reversibility;
- implementation effort.

Prioritise work that is frequent, costly to forget, easy to verify, low-risk, and
supported by reliable evidence. Penalise ambiguous interpretation, unavailable
context, high interruption cost, and irreversible actions.

Recommend a small initial portfolio:

1. one high-value read-only automation;
2. one commitment or stale-work detector;
3. optionally, one evidence-capture automation.

Do not recommend implementing a large portfolio at once.

### 8. Produce a harness-agnostic automation brief

For the highest-priority candidate return:

```text
Objective:
[The outcome this automation protects.]

Inspect:
[Sources and evidence surfaces.]

Time model:
[Fast signal, slow model, or hybrid; include windows and freshness.]

Identify:
[Exact conditions that count as relevant.]

Exclude:
[Noise, false positives, and intentionally deferred work.]

Context:
[Responsibility, ownership, project, dependency, release, or cadence context.]

State:
[Identity, deduplication, history, feedback, coverage, and retention.]

For each result include:
[Evidence, owner, age, source link, status, confidence, and next action.]

Prioritise:
[Severity and ranking rules.]

Actions:
[What may happen automatically.]

Approval required:
[Actions that remain human-controlled.]

Operational budget:
[Frequency, result cap, cost, noise, silence, and pause conditions.]

When nothing requires attention:
[Remain silent or emit a clean report.]

Uncertainty:
[Missing access, conflicting evidence, stale context, or low confidence.]

Evaluation:
[Positive, negative, ambiguous, and regression fixtures.]

Output:
[Human-readable structure and any optional machine-readable fields.]
```

Examples may show how a scheduler or harness could bind this brief, but do not
make a harness-specific configuration the canonical output.

### 9. Protect trust

Every surfaced item must include evidence or a direct route to its source.

Never imply that absence of a result proves no obligation exists when relevant
sources were unavailable. Never send messages, merge code, change task status,
modify calendars, or perform other external changes unless explicitly permitted.

Prefer read-only operation during the pilot. Separate a recommendation or draft
from the execution of a side effect.

### 10. Define and evaluate a pilot

Recommend a pilot lasting several runs. Record:

- useful findings;
- false positives;
- missed items;
- unavailable or stale sources;
- actions the user took;
- repeated dismissals or snoozes;
- estimated attention saved;
- execution cost and interruption count.

After the pilot, revise thresholds, exclusions, context, and schedule before
increasing autonomy. Do not silently change policy or permissions.

## Output format

Return:

### Observed friction

A concise account of the main coordination problems.

### Candidate automations

A ranked table including implementation form and time model.

### Recommended first automation

Explain why this is the safest high-value starting point.

### Automation specification

Provide the complete harness-agnostic brief.

### Boundaries

State what remains a human responsibility and what cannot be reliably observed.

### Pilot and evaluation

Define the run count, feedback to collect, fixtures, and promotion or pause rule.

### Follow-on opportunities

List no more than three candidates to consider after the initial pilot.

## Example recommendations for software engineering work

Potential candidates include:

- engineering attention brief;
- pull request and review follow-up;
- engineering commitment tracker;
- meeting context builder;
- architecture decision follow-up;
- dependency and security update triage;
- incident action-item tracker;
- engineering impact evidence;
- release and breaking-change radar;
- CI failure pattern digest;
- blocked-work escalation brief.

These are examples, not defaults. Select them only when supported by evidence.

## Scheduling guidance

When asked whether, when, or how often to run this skill as an automation, read
[references/scheduling.md](references/scheduling.md). Use workflow, portfolio,
run-history, failure, cost, and feedback evidence to derive the trigger, cadence,
review window, pilot, and re-evaluation conditions. Do not merely repeat README
examples or modify an automation without explicit approval.