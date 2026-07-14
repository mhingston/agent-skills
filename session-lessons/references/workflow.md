# Session Lessons — Longitudinal Analysis Workflow

This reference defines how to convert session history into evidence-backed codification recommendations.

## Overview

Run the analysis in nine stages:

```text
1. Establish scope
2. Collect sessions
3. Extract atomic observations
4. Normalise and deduplicate
5. Cluster across sessions
6. Evaluate evidence
7. Compare existing coverage
8. Route and prioritise
9. Emit recommendations and watchlist
```

Do not begin with destination selection. First establish what repeatedly happened and why.

## 1. Establish Scope

Resolve:

- repository or project;
- look-back window;
- optional theme;
- minimum session threshold;
- included evidence sources;
- whether single-session observations should be shown;
- whether resolved or rejected candidates should be reconsidered.

Record the resolved scope in the run summary.

When a previous analysis cursor or report exists, use it to distinguish:

- previously reviewed evidence;
- newly observed evidence;
- candidates whose trend or status has changed.

Do not exclude older supporting evidence merely because it predates the cursor. The cursor identifies new material, while the analysis window determines the full evidence set.

## 2. Collect Sessions

Prefer structured evidence sources in this order:

1. structured observations;
2. checkpoint or retrospective notes;
3. session summaries;
4. raw turns.

Collect enough metadata to evaluate independence:

```text
session_id
timestamp
repository
branch
task_reference
service_or_component
author_or_operator
source_type
session_outcome
```

The exact session-store query depends on the available schema.

A representative query might resemble:

```sql
SELECT
    s.id AS session_id,
    s.repository,
    s.branch,
    s.task_reference,
    s.summary,
    s.started_at,
    s.completed_at,
    t.id AS turn_id,
    t.user_message,
    t.assistant_response,
    t.timestamp
FROM sessions s
LEFT JOIN turns t ON t.session_id = s.id
WHERE s.repository = :repo
  AND COALESCE(t.timestamp, s.started_at) >= :window_start
ORDER BY COALESCE(t.timestamp, s.started_at) DESC;
```

Do not assume this schema exists unchanged. Adapt to the actual session source.

### Theme Filtering

When a theme is supplied:

1. use the theme to narrow retrieval;
2. include synonyms and repository terminology;
3. retain enough surrounding context to identify the root cause;
4. discard observations that mention the keyword only incidentally.

Do not rely exclusively on exact keyword matching.

## 3. Extract Atomic Observations

Extract zero or more observations from each session.

Each observation should describe one finding, friction point, gap, directive, effective pattern, or contradiction.

Recommended schema:

```yaml
observation_id: session-123:skill-trigger-01
session_id: session-123
observed_at: 2026-07-14T09:30:00Z
repo: owner/repo
branch: feature/example
task_reference: PROJ-123
category: skill-gap
signal_type: incorrect-trigger
summary: The deployment skill did not trigger when the user requested a dry-run release.
root_cause: The skill description only mentions production releases.
impact: The user had to name the skill explicitly.
outcome: Recovered after explicit invocation.
explicitness: observed
severity: medium
source_type: checkpoint
source_refs:
  - checkpoint-123
proposed_pattern: deployment-skill-trigger-gap
```

### Extraction Questions

#### Novel Findings

- Was previously undocumented repository, tool, environment, or workflow knowledge discovered?
- Was an edge case encountered without prior guidance?
- Was a better or faster method established?

#### Friction

- Did a routine task require unnecessary retries or clarification?
- Did the user repeat context or correct the agent?
- Was the wrong tool, skill, or workflow selected?
- Did incomplete guidance cause avoidable work?

#### Skill Gaps

- Should an existing skill have triggered?
- Did a skill trigger incorrectly?
- Were its instructions insufficient for the situation?
- Is there a reusable workflow with no skill contract?

#### Documentation Gaps

- Would a short repository-wide instruction have prevented the problem?
- Is detailed technical guidance missing?
- Is an architectural or operational decision undocumented?

#### Explicit User Directives

- Did the user explicitly state a durable preference or behavioural rule?
- Was the scope of the directive clear?
- Was it temporary, project-specific, or user-wide?

Do not convert inferred preferences into directives.

#### Effective Patterns

- Did a tool combination repeatedly work well?
- Did a validation loop prevent errors?
- Did a prompt or workflow reduce operator intervention?
- Did a division of labour consistently improve outcomes?

#### Contradictions

- Did another session succeed without the proposed change?
- Did the user reject or reverse the proposed rule?
- Was the observed failure caused by unusual local conditions?
- Would the proposed lesson conflict with another established convention?

### Avoid Outcome Bias

Do not label every successful workflow as a durable best practice.

Require evidence that the successful pattern contributed materially to the outcome and is reusable elsewhere.

## 4. Normalise and Deduplicate

Normalise observations before clustering.

### Canonicalise

Normalise:

- equivalent terminology;
- service aliases;
- tool names;
- skill names;
- error variants;
- singular and plural forms;
- user wording that describes the same underlying workflow.

Keep original wording in evidence references.

### Deduplicate Within a Session

Observations belong to the same occurrence when they:

- describe the same root cause;
- occur in the same task;
- arise from retries of the same action;
- are repeated in both a structured source and raw turns;
- appear in multiple summaries generated from the same session.

Count these once.

### Correlated Sessions

Mark sessions as correlated when they share:

- the same task or tracked work item;
- the same branch;
- the same incident;
- a copied workflow;
- an immediate retry;
- a parent and child agent execution for one task.

Correlated sessions may contribute supporting detail, but they should not be treated as fully independent contexts.

## 5. Cluster Across Sessions

Cluster observations by shared root cause and reusable lesson.

Do not cluster merely because observations mention the same technology.

Good cluster:

```text
migration-validation-missing
```

Supporting observations:

- migration generated without checking rollback SQL;
- schema update merged without validating backward compatibility;
- migration agent skipped the dry-run environment.

These share a reusable workflow gap.

Poor cluster:

```text
postgres-problems
```

This groups unrelated failures based only on technology.

### Cluster Naming

Use a concise stable pattern name:

- lowercase;
- kebab-case;
- no more than six words;
- based on the underlying lesson rather than one symptom.

Examples:

```text
skill-trigger-too-narrow
merge-conflict-markers-remain
missing-post-change-validation
user-prefers-managed-scraping
docs-lack-local-env-bootstrap
```

### Cluster Splitting

Split a cluster when:

- observations require different fixes;
- trigger conditions differ materially;
- one pattern is behavioural and another technical;
- one applies repository-wide and another to one component;
- contradictory evidence applies to only part of the cluster.

### Cluster Merging

Merge clusters when:

- they share the same root cause;
- the same change would address them;
- their apparent differences are surface symptoms;
- keeping them separate would produce duplicate recommendations.

## 6. Evaluate Evidence

Evaluate recurrence, independence, causal clarity, contradiction, and impact.

### Core Evidence Metrics

For each cluster calculate:

```text
occurrence_count
session_count
context_count
first_seen
last_seen
supporting_sources
contradiction_count
correlation_risk
```

### Qualification

Default recurring threshold:

```text
session_count >= 3
AND
context_count >= 2
```

Strong-signal exception:

```text
session_count >= 2
AND
at least one strong signal
```

Strong signals include:

- repeated explicit user directive;
- deterministic skill or tool failure;
- production or safety impact;
- repeated failure despite existing guidance;
- significant cost or rework.

Everything else remains in the watchlist.

### Confidence Assessment

Start at `MEDIUM`.

Raise to `HIGH` when most of the following are true:

- at least three independent sessions;
- multiple contexts;
- high-quality structured observations;
- clear causal relationship;
- little meaningful contradiction;
- consistent proposed remedy.

Lower to `LOW` when any of the following materially apply:

- evidence is mainly from one task or branch;
- session summaries are sparse;
- root cause is inferred rather than observed;
- the cluster depends on broad semantic similarity;
- contradictory evidence is substantial;
- the proposed remedy differs across sessions.

Confidence should not be calculated from occurrence count alone.

### Trend Assessment

Assign:

| Trend | Meaning |
| --- | --- |
| `new` | First appeared in the current analysis period |
| `growing` | Frequency or scope has increased |
| `stable` | Continues at a similar rate |
| `declining` | Still occurs, but less often |
| `stale` | No recent evidence and no confirmed resolution |
| `resolved` | Post-change evidence indicates the issue has materially improved |

Use previous reports when available. Do not infer a trend from one analysis window without comparison data.

## 7. Compare Existing Coverage

Search all applicable durable sources:

```text
AGENTS.md
nested AGENTS.md files
docs/**/*.md
README files
architecture and decision records
runbooks
user-directives.md
**/SKILL.md
skill references
skill examples
skill tests or eval manifests
previous session-lessons reports
open tracked work items
```

Check semantic coverage, not only keyword presence.

### Coverage States

#### `absent`

No durable guidance addresses the pattern.

#### `partial`

Relevant material exists, but it lacks one or more of:

- trigger coverage;
- actionable steps;
- edge-case handling;
- examples;
- validation;
- destination-specific detail;
- clear ownership.

#### `adequate`

Existing guidance directly addresses the observed situation and provides enough information to act correctly.

An adequately documented pattern may still indicate:

- a trigger problem;
- poor discoverability;
- stale instructions;
- missing enforcement;
- an implementation defect.

Do not automatically route every adequately documented pattern to `no-op`. First determine why agents still failed.

#### `conflicting`

Multiple sources provide inconsistent instructions, or current behaviour contradicts the documented rule.

Conflicting coverage is generally higher priority than absent coverage because it can produce nondeterministic behaviour.

### Coverage Verification Questions

- Would an agent following the existing text have avoided the observed issue?
- Was the relevant guidance likely to be loaded in that context?
- Are the trigger conditions broad enough?
- Does the guidance describe the actual edge case?
- Is the content current?
- Is the same rule duplicated elsewhere with different wording?
- Is a test or enforcement mechanism missing?

## 8. Route and Prioritise

Apply [routing.md](routing.md).

Select one primary destination.

When useful, include secondary follow-up actions such as:

- add or update a skill eval;
- add a regression test;
- remove conflicting guidance;
- link a skill to repository documentation;
- create or update a tracked work item;
- review effectiveness after a specified number of sessions.

### Priority Assessment

#### `P1`

Use when the pattern:

- repeatedly causes failed outcomes;
- creates unsafe or destructive behaviour;
- blocks a common workflow;
- causes substantial rework;
- affects many repositories or agents;
- persists despite existing guidance.

#### `P2`

Use when the pattern:

- causes recurring operator friction;
- requires repeated explanation;
- produces avoidable but recoverable errors;
- reduces speed or consistency.

#### `P3`

Use when the pattern:

- would improve discoverability or convenience;
- captures a useful convention;
- has limited blast radius;
- is beneficial but not urgent.

#### `WATCH`

Use when evidence is insufficient or contradictory.

## 9. Emit Results

Produce:

### Run Summary

State:

- scope;
- window;
- sessions examined;
- sessions with usable evidence;
- evidence sources;
- theme;
- notable limitations.

### Recommended Candidates

Include only candidates that pass the promotion gate.

For each candidate provide:

- candidate fields from the output contract;
- representative supporting evidence;
- independence or correlation notes;
- contradictions;
- coverage assessment;
- concrete proposed change;
- validation follow-up.

### Watchlist

Include candidates that are plausible but not mature.

For each watchlist item state:

- current evidence;
- why it is insufficient;
- what additional evidence would change the recommendation.

### Suppressed Candidates

Normally suppress:

- adequately covered observations;
- low-value noise;
- rejected candidates;
- resolved candidates;
- duplicate clusters.

Show them when:

- `include_noop` or `include_resolved` was requested;
- their suppression explains an important decision;
- materially new evidence was found.

## Recommended Output Shape

```markdown
# Session Lessons Report

## Run Summary

- Scope:
- Window:
- Sessions examined:
- Sessions with usable evidence:
- Evidence sources:
- Theme:
- Limitations:

## Recommended Candidates

### candidate-id

- Pattern:
- Category:
- Priority:
- Confidence:
- Trend:
- Sessions:
- Contexts:
- Current coverage:
- Recommended destination:
- Destination detail:
- Recommended change:
- Validation follow-up:

Supporting evidence:

1. ...
2. ...
3. ...

Contradictory evidence:

- ...

Reason:

...

## Watchlist

### candidate-id

- Current evidence:
- Missing evidence:
- Revisit when:

## Resolved or Suppressed

...
```

## No-Write Rule

Do not modify files, create tracked work items, author skills, or update directives during this workflow unless the operator explicitly requests the corresponding action.

End with a specific promotion recommendation rather than offering to promote every candidate indiscriminately.
