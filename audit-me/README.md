# audit-me

`audit-me` discovers recurring coordination problems and turns them into
harness-agnostic automation briefs. It is a design and review skill, not the
runtime implementation of every automation it recommends.

## Suggested invocation cadence

| Situation | Suggested invocation |
| --- | --- |
| Initial setup | Run on demand after connecting the work surfaces that matter. |
| Portfolio review | Run monthly or quarterly against recent work and automation history. |
| Role or tool change | Run after responsibilities, repositories, teams, or systems materially change. |
| Noisy automation | Run after repeated false positives, misses, or dismissals. |
| New recurring friction | Run when a repeated manual check or context-reconstruction task becomes visible. |

These are suggestions rather than a canonical schedule. Cadence should follow the
cost of omission, rate of change, source freshness, and interruption budget.

## Suggested scheduled invocation

```text
Use the audit-me skill to review the current automation portfolio and recent work
friction.

Inspect the available run history, user feedback, recurring manual checks,
dropped commitments, stale work, evidence loss, and source-coverage gaps.

Recommend at most three changes. For each, choose the lightest reliable
implementation form: prompt, reusable skill, deterministic workflow, event-driven
automation, or no automation.

Do not change schedules, permissions, or automation definitions. Return proposed
changes, evidence, expected benefit, risk, and a pilot plan.
```

## Configuration questions

Bind the skill to a scheduler or coding-agent harness using the native mechanism
for that environment. Decide explicitly:

- scope and available sources;
- lookback period;
- where run history and user feedback can be inspected;
- maximum recommendations;
- cost and interruption budget;
- destination for the report;
- whether no findings should produce silence;
- which changes always require human approval.

Do not introduce a repository-wide manifest format solely to schedule this skill.
A local team may use any suitable configuration representation.
