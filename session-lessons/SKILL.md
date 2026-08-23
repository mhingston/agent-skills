---
name: session-lessons
description: Analyse multiple recent agent sessions to identify recurring friction, discoveries, workflow gaps, explicit user directives, and effective patterns that may deserve durable codification. Clusters evidence across distinct sessions and revision-bound pull-request lifecycles, checks existing coverage, and recommends updates to agent instructions, repository documentation, user directives, existing skills, new skills, tracked work items, or no action. Use for periodic learning reviews, knowledge-base health checks, and evidence gathering before changing agent behaviour. Analysis-only by default.
---

# Session Lessons

Analyse experience across multiple sessions and revision-bound pull-request lifecycles, then turn recurring patterns into evidence-backed codification recommendations.

This skill can use raw conversations, summaries, checkpoints, retrospectives, structured observations, and—when repository access is available—review → remediation → re-review → merge evidence. It does not depend on a particular end-of-session process.

> **Longitudinal analysis, not single-session reflection.**
>
> One session or pull request can provide supporting evidence, but recurring
> recommendations should normally be based on multiple independent evidence units
> and contexts.

**Announce at start:**

> I'm using the session-lessons skill to analyse patterns across recent sessions.

## Behavioural Boundary

This skill is analysis-first. By default, it does not:

- modify repository files;
- create or edit skills;
- create tracked work items;
- update user directives;
- promote findings into persistent instructions or memory.

It produces recommendations and supporting evidence for operator review. Only perform a recommended action when the operator explicitly requests it.

## When to Use

Use this skill when:

- reviewing recurring friction across recent sessions or pull requests;
- performing a periodic agent-harness or knowledge-base health check;
- checking whether repeated operator guidance should become durable guidance;
- identifying undocumented conventions or recurring troubleshooting knowledge;
- deciding whether an existing skill needs refinement;
- gathering evidence before creating a new skill;
- identifying patterns not visible from one task, pull request, or session;
- checking whether previous codification reduced recurring friction.

Do not use it as a substitute for a retrospective focused on one PR, incident, or session; a promotion workflow that writes approved lessons; a skill-authoring workflow after approval; or a general-purpose transcript summariser.

## Inputs

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `repo` | No | Current repository | Repository or project scope |
| `window` | No | `30d` | Look-back period |
| `theme` | No | — | Optional topic or workflow filter |
| `min_sessions` | No | `3` | Minimum distinct session evidence units when session history is the source |
| `include_pr_lifecycle` | No | `true` when repository evidence is available | Include revision-bound PR lifecycle evidence |
| `include_singletons` | No | `false` | Include single-evidence-unit observations in the watchlist |
| `include_noop` | No | `false` | Include adequately covered or rejected candidates |
| `include_resolved` | No | `false` | Include previously promoted or resolved candidates |
| `sources` | No | All available | Structured observations, PR lifecycle evidence, checkpoints, summaries, retrospectives, raw turns |
| `since` | No | Derived from window | Optional timestamp or previous analysis cursor |

Natural-language equivalents are acceptable.

## Evidence Sources

Use the highest-quality available evidence in this order:

1. structured observations with stable run, task, or revision identity;
2. revision-bound PR lifecycle evidence linking a validated finding to remediation and fresh re-review;
3. checkpoint or retrospective notes;
4. session summaries;
5. raw user and assistant turns.

Prefer records that preserve originating session or run, relevant task or revision identity, observed event, supporting evidence, and consequence. Treat an agent's interpretation as a claim to corroborate; command results, user corrections, validated review findings, revision-bound remediation, and other observable evidence carry more weight.

When several sources describe the same underlying event, count it once. Do not treat transcript turns, review comments, remediation commits, or re-review rounds as independent occurrences by themselves.

### Pull-request lifecycle evidence

Use PR lifecycle evidence only when it can be tied to exact revisions. Reconstruct validated finding → reviewed revision → remediation → fresh re-review → outcome, preserve canonical `AC-N` / `NG-N` references when available, and treat merge as an outcome rather than proof.

Read [references/pr-lifecycle-evidence.md](references/pr-lifecycle-evidence.md) before extracting or qualifying PR-derived observations.

## Observation Categories

Extract atomic observations using these categories.

### Discovery

Previously undocumented information about code, architecture, tools, environments, APIs, workflows, conventions, or operational behaviour.

### Friction

Work that was slower, more confusing, or more repetitive than expected, including repeated explanation, unnecessary clarification, incorrect tool selection, failed retries, manual workarounds, missing context, or avoidable validation failure.

### Skill Gap

Evidence that a skill failed to trigger, triggered incorrectly, lacked instructions or an edge case, lacked a useful example or decision rule, or that a reusable workflow had no suitable skill.

### Documentation Gap

Information that would have prevented confusion if it already existed in agent instructions, repository docs, architecture or decision records, developer documentation, or runbooks.

### Explicit User Directive

A behavioural preference or convention explicitly stated by the user. Do not infer directives from behaviour alone.

### Effective Pattern

A tool sequence, workflow, convention, prompt, validation loop, or division of labour that repeatedly worked well.

### Contradictory Evidence

Evidence that a proposed lesson did not generalise, was rejected, was unusual, is already handled successfully elsewhere, conflicts with an existing convention, or originated in a review finding later falsified or shown not to require the proposed remediation.

## Unit of Evidence

The normal evidence unit is:

> One independently observed pattern in one session, or one root-cause pattern
> reconstructed from one revision-bound pull-request lifecycle.

Multiple turns, retries, summaries, evidence-source copies, review comments, remediation commits, or re-review rounds from the same underlying event do not increase the evidence-unit count.

A session or PR may contribute more than one occurrence to a cluster only when the occurrences are genuinely independent and have distinct causes. Treat this as exceptional and explain it.

## Default Qualification Threshold

A recurring candidate normally requires:

- at least **3 distinct evidence units**; and
- at least **2 distinct contexts**, such as branches, tasks, pull requests, authors, services, repositories, or workflows.

When only session history is available, this normally means at least 3 distinct sessions. A candidate may qualify with 2 evidence units when at least one strong signal exists:

- repeated explicit user directive;
- production-impacting or safety-critical failure;
- same deterministic tool or skill failure;
- repeated incorrect behaviour despite existing guidance;
- same validated must-fix review failure across independent PRs;
- high-cost failure mode.

Single-evidence-unit findings belong in the watchlist unless the operator explicitly requests singleton recommendations.

### Escaped-defect evaluation fast path

A single escaped defect, production incident, unsafe agent action, or agent-missed
failure may justify an immediate `eval_seed` before it satisfies the recurrence
threshold for durable codification. Use this fast path only when:

- the failure is linked to an exact run, task, revision, or other stable evidence
  identity;
- available evidence supports the relevant failure mechanism rather than merely
  showing that the incident happened after agent involvement;
- the behaviour is reproducible or can be represented by a faithful fixture;
- an independent verifier can distinguish the escaped failure from the desired
  outcome;
- sensitive data and task-specific answer keys can be removed without destroying
  the mechanism being tested.

This exception bypasses recurrence only for **evaluation coverage**. It does not
qualify a skill change, instruction update, policy change, or automatic
self-modification. Keep the candidate in the watchlist or mark it as an
evaluation-only proposal until ordinary evidence supports a durable change.

The seed should capture the trigger, validated failure mechanism, desired
invariant, strongest verifier, exact source references, and a sibling or near-miss
shape when practical. A later `skill-creator` evaluation decides whether any
proposed skill revision improves that regression without degrading broader cases.

## Correlated Evidence

Do not inflate confidence when evidence units are highly correlated. Examples include:

- several sessions on the same task, branch, or incident;
- retries of the same failed workflow;
- copied prompts;
- parent and child executions for one task;
- multiple observations from one summary;
- several review comments or remediation rounds on one PR;
- sibling PRs from one decomposed task sharing the same cause.

Record correlated evidence, but count it as one context when assessing diversity.

## Confidence and Priority

Keep confidence and priority separate.

| Confidence | Meaning |
| --- | --- |
| `HIGH` | Repeated across independent contexts with clear causal evidence and little contradiction |
| `MEDIUM` | Repeated, but evidence is partly correlated, incomplete, or open to another explanation |
| `LOW` | Plausible pattern with limited, weak, or mostly single-context evidence |

| Priority | Meaning |
| --- | --- |
| `P1` | Causes repeated failure, unsafe behaviour, significant rework, or blocks common workflows |
| `P2` | Causes recurring friction or meaningful inefficiency |
| `P3` | Useful improvement with limited operational impact |
| `WATCH` | Evidence is not yet sufficient for codification |

High confidence does not automatically mean high priority.

## Candidate Lifecycle

Each candidate should have a stable identifier and lifecycle status:

```text
watch
proposed
approved
promoted
rejected
resolved
superseded
```

Derive candidate IDs from the normalised pattern and scope, for example:

```text
skill-trigger-misses:repo-wide
cosmos-emulator-startup:payments-service
explicit-preference-no-browser-automation:user
```

Before emitting a candidate, check prior session-lessons reports or the project's learning registry when available. Do not repeatedly recommend promoted, rejected, resolved, or superseded candidates unless materially new evidence appears; explain what changed.

## Recommended Destinations

Route each mature candidate to one primary destination:

- `agent instructions`;
- `repo docs`;
- `user directives`;
- `existing skill`;
- `new skill`;
- `tracked work item`;
- `no-op`.

Use existing repository conventions and available tooling when naming the specific destination. Prefer updating existing guidance over creating parallel guidance.

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
- sessions examined and sessions with usable evidence;
- PRs examined and PRs with usable revision-bound evidence when enabled;
- total deduplicated evidence units;
- evidence sources used;
- theme filter, if any;
- limitations or missing data.

### Candidate Fields

| Field | Description |
| --- | --- |
| `candidate_id` | Stable identifier |
| `pattern` | Short human-readable pattern |
| `category` | Discovery, friction, skill gap, documentation gap, user directive, effective pattern, or contradictory evidence |
| `first_seen` | Earliest supporting evidence timestamp |
| `last_seen` | Most recent supporting evidence timestamp |
| `occurrence_count` | Deduplicated atomic observations |
| `evidence_unit_count` | Distinct supporting session or PR-lifecycle units |
| `session_count` | Distinct supporting sessions |
| `pr_count` | Distinct supporting PR lifecycles |
| `context_count` | Distinct branches, tasks, PRs, services, authors, repositories, or workflows |
| `trend` | `new`, `growing`, `stable`, `declining`, `stale`, or `resolved` |
| `supporting_evidence` | Brief evidence summaries with source references |
| `contract_refs` | Canonical `AC-N` / `NG-N` references when applicable |
| `contradictory_evidence` | Counterexamples, rejections, falsified findings, or successful cases |
| `current_coverage` | `absent`, `partial`, `adequate`, or `conflicting` |
| `recommended_destination` | Durable destination or `no-op` |
| `destination_detail` | Proposed path, skill, directive, or work-item summary |
| `recommended_change` | Concrete change |
| `validation_follow_up` | Test, eval, or observation that would verify improvement |
| `eval_seed` | Optional source-linked evaluation seed for skill changes |
| `confidence` | `HIGH`, `MEDIUM`, or `LOW` |
| `priority` | `P1`, `P2`, `P3`, or `WATCH` |
| `reason` | Concise rationale combining evidence, coverage, and impact |

Sort recommendations by priority, confidence, distinct evidence-unit count, then recency. Do not sort by raw turn, review-comment, or commit count.

## Evidence Presentation

For each recommendation:

- provide two or three representative evidence summaries;
- reference contributing sessions and PR lifecycles;
- for PR evidence, include the validated finding and relevant reviewed/remediated revisions rather than only the merge commit;
- explain whether evidence units are independent or correlated;
- mention meaningful contradictory evidence;
- preserve canonical contract references when they connect repeated failures or remediations;
- avoid dumping full transcripts, diffs, or review threads;
- redact credentials, secrets, personal data, and irrelevant content.

A candidate must be understandable without opening every source.

## Promotion Gate

Recommend immediate codification only when:

- the pattern satisfies the evidence threshold;
- the proposed destination is clear;
- existing coverage is absent, partial, or conflicting;
- the recommendation is actionable;
- contradictory evidence does not undermine it.

Otherwise place it in the watchlist, state what additional evidence would raise confidence, and avoid speculative file changes. An escaped-defect fast-path `eval_seed` may be emitted from the watchlist without treating the candidate as qualified for codification.

## Common Workflows

### Periodic Learning Review

Analyse the default 30-day window. When repository access is available, include usable revision-bound PR lifecycle evidence by default rather than treating merged review history as disposable.

### Theme-Focused Review

Limit extraction and clustering to the supplied topic. Keep enough surrounding evidence to identify root cause; discard incidental keyword matches.

### Pre-Skill Evidence Check

Before recommending a new or changed skill:

1. search existing skill coverage;
2. gather evidence across independent sessions and relevant PR lifecycles;
3. verify stable triggers, inputs, steps, and outputs;
4. prefer extending an existing skill in the same decision domain;
5. recommend a new skill only when it has a distinct reusable contract.

When evidence is concrete enough, include an `eval_seed` containing a representative trigger, observed failure or validated finding, desired invariant, useful near miss or counterexample, strongest verifier or re-review result, and contributing source references. Keep it free of secrets, task-specific answer keys, and unverifiable model rationale.

For an escaped-defect fast-path seed, preserve its evaluation-only status and the evidence that established reproducibility and the failure mechanism. Do not present a proposed skill edit as qualified merely because the incident was severe.

### Effectiveness Review

After a lesson is promoted:

1. compare sessions and relevant PR lifecycle evidence before and after the change;
2. look for reduced friction or failure frequency;
3. mark the candidate `resolved` when evidence supports improvement;
4. reopen it when the problem persists.

## Workflow and Routing

Detailed process:

- [references/workflow.md](references/workflow.md)
- [references/routing.md](references/routing.md)
- [references/pr-lifecycle-evidence.md](references/pr-lifecycle-evidence.md)

## Invariants

- Analyse multiple independent evidence units by default.
- Count distinct sessions or PR root-cause lifecycles, not repeated turns, comments, commits, or review rounds.
- Keep confidence separate from priority.
- Search existing coverage before recommending new material.
- Include contradictory evidence and falsified review findings.
- Do not infer user directives.
- Prefer updating existing guidance over creating parallel guidance.
- Treat structured self-reports as evidence-bearing claims, not unquestioned truth.
- Treat merge as an outcome, not proof that a review finding was valid or resolved.
- Preserve revision identity and canonical contract references for PR-derived learning evidence when available.
- Keep skill eval seeds source-linked and free of task-specific answer keys.
- Let a validated escaped defect accelerate regression coverage, never automatic codification or self-modification.
- Do not write files, skills, directives, or work items without explicit approval.
- Track candidate lifecycle to avoid repeatedly surfacing resolved or rejected recommendations.