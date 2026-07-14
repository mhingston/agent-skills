---
name: session-lessons
description: Analyse multiple recent agent sessions to identify recurring friction, discoveries, workflow gaps, explicit user directives, and effective patterns that may deserve durable codification. Clusters evidence across distinct sessions, checks existing coverage, and recommends updates to agent instructions, repository documentation, user directives, existing skills, new skills, tracked work items, or no action. Use for periodic learning reviews, knowledge-base health checks, and evidence gathering before changing agent behaviour. Analysis-only by default.
---

# Session Lessons

Analyse experience across multiple sessions and turn recurring patterns into evidence-backed codification recommendations.

This skill examines available session history, including raw conversations, summaries, checkpoints, retrospectives, and structured observations when available. It does not depend on a particular end-of-session process.

> **Longitudinal analysis, not single-session reflection.**
>
> A single session can provide supporting evidence, but recurring recommendations
> should normally be based on multiple independent sessions and contexts.

**Announce at start:**

> I'm using the session-lessons skill to analyse patterns across recent sessions.

## Behavioural Boundary

This skill is analysis-first.

By default, it does not:

- modify repository files;
- create or edit skills;
- create tracked work items;
- update user directives;
- promote findings into persistent instructions or memory.

It produces recommendations and supporting evidence for operator review.

Only perform a recommended action when the operator explicitly requests it.

## When to Use

Use this skill when:

- reviewing recurring friction across recent sessions;
- performing a periodic agent-harness or knowledge-base health check;
- checking whether repeated operator guidance should become a durable directive;
- identifying undocumented conventions or recurring troubleshooting knowledge;
- deciding whether an existing skill needs refinement;
- gathering evidence before creating a new skill;
- identifying patterns that are not visible from one task, pull request, or session;
- checking whether previous codification changes reduced recurring friction.

## When Not to Use

Do not use this skill as a substitute for:

- a retrospective focused on one specific pull request, incident, or session;
- a promotion workflow that writes already-approved lessons into durable files;
- a skill-authoring workflow used after a new skill has been approved;
- a general-purpose transcript summariser.

## Inputs

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `repo` | No | Current repository | Repository or project scope |
| `window` | No | `30d` | Look-back period |
| `theme` | No | — | Optional topic or workflow filter |
| `min_sessions` | No | `3` | Minimum distinct sessions for a recurring candidate |
| `include_singletons` | No | `false` | Include single-session observations in the watchlist |
| `include_noop` | No | `false` | Include adequately covered or rejected candidates |
| `include_resolved` | No | `false` | Include previously promoted or resolved candidates |
| `sources` | No | All available | Structured observations, checkpoints, summaries, retrospectives, and raw turns |
| `since` | No | Derived from window | Optional timestamp or previous analysis cursor |

Natural-language equivalents are acceptable.

Examples:

```text
Analyse session lessons for this repository over the last 30 days.

Analyse the last 90 days, focused on database migrations.

Show single-session observations as a watchlist but do not recommend actions.

Check whether our recent agent-hook problems justify a new skill.
```

## Evidence Sources

Use the highest-quality available evidence in this order:

1. structured observations;
2. checkpoint or retrospective notes;
3. session summaries;
4. raw user and assistant turns.

Structured observations improve precision but are not required.

When several sources describe the same event in the same session, count them as one occurrence.

Do not treat each transcript turn as an independent occurrence.

## Observation Categories

Extract atomic observations using these categories.

### Discovery

Previously undocumented information about:

- the codebase;
- architecture;
- tools;
- environments;
- APIs;
- workflows;
- conventions;
- operational behaviour.

### Friction

A task that was slower, more confusing, or more repetitive than expected.

Examples include:

- repeated explanation from the user;
- unnecessary clarification loops;
- incorrect tool selection;
- failed retries;
- manual workarounds;
- missing context;
- avoidable validation failures.

### Skill Gap

Evidence that:

- a skill failed to trigger;
- a skill triggered incorrectly;
- instructions were incomplete;
- an edge case was missing;
- an existing skill lacked an example or decision rule;
- a reusable workflow had no skill.

### Documentation Gap

Information that would have prevented confusion if it had already existed in:

- agent instruction files such as `AGENTS.md`;
- repository documentation;
- architecture or decision records;
- inline developer documentation;
- operational runbooks.

### Explicit User Directive

A behavioural preference or convention explicitly stated by the user.

Do not infer user preferences from behaviour alone.

### Effective Pattern

A tool sequence, workflow, convention, prompt, validation loop, or division of labour that repeatedly worked well.

### Contradictory Evidence

Evidence that a proposed lesson:

- did not generalise;
- was rejected by the user;
- was only needed in one unusual context;
- is already handled successfully in other sessions;
- would conflict with an existing convention.

## Unit of Evidence

The normal evidence unit is:

> One independently observed pattern in one session.

Multiple turns, retries, summaries, or evidence-source copies from the same session do not increase the session count.

A session may contribute more than one occurrence to a cluster only when the occurrences are genuinely independent and have distinct causes. Treat this as exceptional and explain it.

## Default Qualification Threshold

A recurring candidate normally requires:

- evidence from at least **3 distinct sessions**; and
- evidence from at least **2 distinct contexts**, such as branches, tasks, authors, services, repositories, or workflows.

A candidate may qualify with 2 sessions when at least one strong signal is present:

- an explicit user directive repeated in both sessions;
- a production-impacting or safety-critical failure;
- the same deterministic tool or skill failure;
- repeated incorrect behaviour despite existing guidance;
- a high-cost failure mode.

Single-session findings belong in the watchlist unless the operator explicitly requests single-session recommendations.

## Correlated Evidence

Do not inflate confidence when sessions are highly correlated.

Examples:

- several sessions working on the same task or ticket;
- retries of the same failed workflow;
- sessions created from the same branch or incident;
- copied prompts producing the same outcome;
- parent and child agent executions for one task;
- multiple observations derived from one summary.

Record correlated evidence, but count it as one context when assessing diversity.

## Confidence and Priority

Keep **confidence** and **priority** separate.

### Confidence

Confidence describes how strongly the evidence supports the proposed pattern.

| Confidence | Meaning |
| --- | --- |
| `HIGH` | Repeated across independent contexts with clear causal evidence and little contradiction |
| `MEDIUM` | Repeated, but evidence is partly correlated, incomplete, or open to another explanation |
| `LOW` | Plausible pattern with limited, weak, or mostly single-context evidence |

### Priority

Priority describes the cost of leaving the pattern unresolved.

| Priority | Meaning |
| --- | --- |
| `P1` | Causes repeated failure, unsafe behaviour, significant rework, or blocks common workflows |
| `P2` | Causes recurring friction or meaningful inefficiency |
| `P3` | Useful improvement with limited operational impact |
| `WATCH` | Evidence is not yet sufficient for codification |

High confidence does not automatically mean high priority.

## Candidate Lifecycle

Each candidate should have a stable identifier and lifecycle status.

Suggested statuses:

```text
watch
proposed
approved
promoted
rejected
resolved
superseded
```

Use a stable candidate ID derived from the normalised pattern and scope, for example:

```text
skill-trigger-misses:repo-wide
cosmos-emulator-startup:payments-service
explicit-preference-no-browser-automation:user
```

Before emitting a candidate, check previous session-lessons reports or the project's learning registry when available.

Do not repeatedly recommend candidates that are:

- already promoted;
- explicitly rejected;
- resolved by a later change;
- superseded by a broader candidate.

A rejected or resolved candidate may be resurfaced only when materially new evidence appears. Explain what changed.

## Recommended Destinations

Each mature candidate should be routed to one primary destination:

- `agent instructions`;
- `repo docs`;
- `user directives`;
- `existing skill`;
- `new skill`;
- `tracked work item`;
- `no-op`.

Use the repository's existing conventions and available tooling when naming the specific destination.

A tracked work item might become an issue, ticket, task, backlog item, or project card depending on the environment.

## Output Contract

Produce four sections:

1. **Run summary**
2. **Recommended candidates**
3. **Watchlist**
4. **Suppressed or resolved candidates**, only when requested or materially relevant

### Run Summary

Include:

- repository or project scope;
- analysis window;
- number of sessions examined;
- number of sessions with usable evidence;
- evidence sources used;
- theme filter, if any;
- limitations or missing data.

### Candidate Fields

| Field | Description |
| --- | --- |
| `candidate_id` | Stable identifier for tracking the candidate over time |
| `pattern` | Short human-readable pattern label |
| `category` | Discovery, friction, skill gap, documentation gap, user directive, or effective pattern |
| `first_seen` | Earliest supporting session timestamp |
| `last_seen` | Most recent supporting session timestamp |
| `occurrence_count` | Deduplicated atomic observations |
| `session_count` | Distinct supporting sessions |
| `context_count` | Distinct branches, tasks, services, authors, repositories, or workflows |
| `trend` | `new`, `growing`, `stable`, `declining`, `stale`, or `resolved` |
| `supporting_evidence` | Brief evidence summaries with session references |
| `contradictory_evidence` | Relevant counterexamples, rejections, or successful cases |
| `current_coverage` | `absent`, `partial`, `adequate`, or `conflicting` |
| `recommended_destination` | Durable destination or `no-op` |
| `destination_detail` | Proposed path, skill, directive, or work-item summary |
| `recommended_change` | Concrete description of what should change |
| `validation_follow_up` | Test, eval, or observation that would verify the improvement |
| `confidence` | `HIGH`, `MEDIUM`, or `LOW` |
| `priority` | `P1`, `P2`, `P3`, or `WATCH` |
| `reason` | Concise rationale combining evidence, coverage, and impact |

Sort recommendations by:

1. priority;
2. confidence;
3. distinct session count;
4. most recent occurrence.

Do not sort by raw turn or message count.

## Evidence Presentation

For each recommendation:

- provide two or three representative evidence summaries;
- reference the contributing sessions;
- explain whether the sessions are independent or correlated;
- mention meaningful contradictory evidence;
- avoid dumping full transcripts;
- redact credentials, secrets, personal data, and irrelevant content.

A candidate must be understandable without opening every source session.

## Promotion Gate

Recommend immediate codification only when:

- the pattern satisfies the evidence threshold;
- the proposed destination is clear;
- existing coverage is absent, partial, or conflicting;
- the recommendation is actionable;
- contradictory evidence does not undermine the conclusion.

Otherwise:

- place the candidate in the watchlist;
- state what additional evidence would raise confidence;
- avoid proposing speculative file changes.

## Common Workflows

### Periodic Learning Review

Analyse the default 30-day window without a theme.

Use this to find recurring problems and successful patterns across normal work.

### Theme-Focused Review

Limit extraction and clustering to a topic such as:

```text
database migrations
coding-agent hooks
merge conflict resolution
test flakiness
deployment approvals
```

Discard unrelated clusters even when they meet the global evidence threshold.

### Pre-Skill Evidence Check

Before creating a skill:

1. search existing skill coverage;
2. gather evidence across independent sessions;
3. verify the workflow has stable triggers, inputs, steps, and outputs;
4. prefer extending an existing skill when the workflow belongs to the same decision domain;
5. recommend a new skill only when it has a distinct reusable contract.

### Effectiveness Review

After a lesson has been promoted:

1. compare sessions before and after the change;
2. look for reduced friction or failure frequency;
3. mark the candidate `resolved` when evidence supports improvement;
4. reopen it when the problem continues despite the codification.

## Workflow and Routing

Detailed process:

- [references/workflow.md](references/workflow.md)
- [references/routing.md](references/routing.md)

## Invariants

- Analyse multiple sessions by default.
- Count distinct sessions, not repeated turns.
- Keep confidence separate from priority.
- Search existing coverage before recommending new material.
- Include contradictory evidence.
- Do not infer user directives.
- Prefer updating existing guidance over creating parallel guidance.
- Do not write files, skills, directives, or work items without explicit approval.
- Track candidate lifecycle to avoid repeatedly surfacing resolved or rejected recommendations.
