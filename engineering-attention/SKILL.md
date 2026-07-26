---
name: engineering-attention
description: >
  Produce an evidence-backed engineering attention brief by correlating recent
  repository, review, CI, release, incident, dependency, and commitment signals
  with durable ownership and project context. Use for recurring prioritisation,
  stale-work detection, blocker review, or deciding what engineering work needs
  attention now. Do not use to approve, merge, deploy, judge performance, or
  contact people without explicit permission.
---

# Engineering Attention

Identify the smallest set of engineering items that deserve attention now.
Optimise for prevented delay, avoided operational risk, honoured commitments, and
reduced context reconstruction rather than activity volume.

## Operating boundary

Default to read-only analysis.

May:

- inspect accessible work surfaces;
- correlate and deduplicate evidence;
- update internal finding state when a safe state location is available;
- recommend next actions;
- prepare drafts when explicitly requested.

Must not, without explicit approval:

- send messages or comments;
- change assignees, labels, issue state, or project status;
- rerun CI;
- push commits or open pull requests;
- merge, deploy, roll back, or change production state;
- infer performance, motivation, or blame.

## Inputs and coverage

Use only sources available in the current environment. Relevant sources may
include:

- pull requests, reviews, issues, branches, commits, and code ownership;
- CI checks, deployments, releases, feature flags, and migrations;
- incidents, alerts, security findings, and dependency updates;
- project records, deadlines, decision records, and meeting action items;
- messages or email containing explicit engineering commitments.

Report inaccessible, stale, or conflicting sources. Do not treat missing access
as evidence that no attention item exists.

## Time models

Choose the lightest useful mode:

- **Fast** — inspect a recent window for urgent changes and new blockers.
- **Slow** — refresh historical cadence, ownership, recurring-failure, or project
  context without generating routine notifications.
- **Hybrid** — rank recent signals against a durable baseline.

Use hybrid mode when judging staleness, anomaly, or relative urgency. A fixed age
threshold is a fallback, not a universal definition of stale work.

## Workflow

### 1. Establish the attention contract

Determine:

- the user or team whose attention is being protected;
- repositories, services, projects, and responsibilities in scope;
- deadlines, release windows, and service expectations;
- output destination and maximum result count;
- silence policy and permitted actions;
- available historical context and previous-run state.

When the responsibility model is incomplete, limit claims and explain the gap.

### 2. Collect current and durable context

For fast signals, inspect recent activity and authoritative current state.

For slow context, use available evidence about:

- ownership and collaborators;
- active projects and dependencies;
- normal review and delivery cadence;
- recurring CI or incident patterns;
- intentional waiting periods and known exceptions;
- previous priorities, dismissals, and resolution evidence.

Verify actionable findings against current source state before reporting them.

### 3. Generate candidates

Look for candidates in these categories.

#### Blocking and dependency risk

Surface work when the subject is blocking another person, team, release, migration,
or customer outcome, or when an external blocker now requires escalation or a
decision.

#### Explicit commitments

Treat a commitment as a candidate only when evidence identifies:

- who committed;
- the expected action or outcome;
- the counterparty or dependent work;
- a reasonable due time or age;
- whether completion evidence exists.

Do not convert casual intent, brainstorming, or quoted text into an obligation.

#### Pull request and review follow-up

Consider:

- requested reviews without meaningful response;
- unresolved review threads after a revision;
- authored changes waiting unexpectedly;
- drafts with no meaningful activity;
- merge-ready work waiting on a clear administrative action.

Account for weekends, documented holds, repository cadence, and review complexity.

#### CI, release, and operational risk

Consider:

- newly failing or persistently failing critical checks;
- likely regressions separated from known flaky failures;
- missing release, migration, rollback, observability, or compatibility evidence;
- active incident actions without ownership or progress;
- security or dependency findings with plausible exposure.

Do not report routine successful runs or bot churn without a decision to make.

#### Stale work and decisions

Use historical cadence when available. Distinguish:

- intentionally waiting;
- blocked with an owner;
- abandoned or forgotten;
- awaiting a decision;
- stale source data.

### 4. Falsify each candidate

Before surfacing an item, seek disconfirming evidence:

- completion in another system;
- explicit deferral or accepted wait;
- superseding work;
- duplicate or bot-generated activity;
- changed ownership;
- resolved incident or released version;
- an unavailable source that makes the conclusion unsafe.

Downgrade confidence or omit the item when evidence does not support action.

### 5. Normalize finding state

Assign a stable finding identity derived from the underlying work item and
attention reason, not the wording of the report.

When state is available, track:

- first seen and last seen;
- last meaningful source activity;
- previous and current priority;
- evidence changes;
- resolution evidence;
- dismissal or snooze;
- source coverage;
- last successful scan.

Do not repeatedly notify unchanged findings unless the schedule explicitly asks
for a full report. Highlight new, materially changed, escalated, or newly resolved
items.

### 6. Rank attention

Prefer this default ordering unless the local responsibility model says otherwise:

1. active production, security, privacy, or data-integrity risk;
2. work where the subject is blocking others;
3. time-sensitive customer, release, or migration commitments;
4. explicit commitments without completion evidence;
5. stale work with a concrete, low-cost next action;
6. informational watch items whose status materially changed.

Rank by evidence and consequence, not seniority, message volume, or author
popularity.

### 7. Respect the operational budget

Apply configured limits. When no limits are provided:

- return at most five `Now` items;
- return at most five `Soon` items;
- include `Watching` only for changed or likely-to-escalate items;
- omit routine clean checks;
- remain silent when there is no material change if the harness supports silence.

Prefer one useful interruption over a complete activity digest.

## Output

Return:

### Now

Items requiring action or a decision in the current working period.

### Soon

Items likely to require attention before the next normal review window.

### Watching

Only materially changed items that are not yet actionable.

For every item include:

- priority and concise reason it matters now;
- repository, service, project, or work item;
- owner and relevant collaborators when evidenced;
- age and last meaningful activity;
- direct evidence or source route;
- current status and blocker;
- recommended next action;
- confidence;
- `new`, `changed`, `escalated`, `unchanged`, or `resolved` when state exists.

### Coverage

List inspected, unavailable, stale, and conflicting sources. State whether slow
context and previous-run state were available.

When nothing requires attention, follow the configured silence policy. Otherwise
return: `No material engineering attention items.`

## Validation checks

Before returning:

- every finding has evidence;
- every priority has a consequence-based reason;
- duplicate manifestations of one problem are consolidated;
- unavailable context is visible;
- unchanged findings follow the notification policy;
- no side effect occurred without permission;
- no statement implies performance judgement or blame.
