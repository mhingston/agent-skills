# engineering-attention

`engineering-attention` produces a small, evidence-backed brief of engineering
work that needs attention now. It supports fast, slow, and hybrid runs without
requiring a particular scheduler, manifest format, state store, or coding-agent
harness.

## Suggested automations

| Purpose | Suggested cadence | Time model | Typical output |
| --- | --- | --- | --- |
| Morning attention brief | Once each working morning | Hybrid | Up to five items requiring action today. |
| Blocker and commitment check | Once late in the working day | Fast | New blockers, escalations, and unfulfilled commitments. |
| Review follow-up | One or two times per working day | Fast or hybrid | Reviews owed, unresolved threads, and unexpectedly idle pull requests. |
| Weekly stale-work review | Once near the start of the working week | Hybrid | Work whose inactivity is abnormal for its context. |
| Context refresh | Nightly incremental or weekly full refresh | Slow | Updated baselines; usually no user notification. |
| Release-period radar | More frequently during an active release window | Hybrid | Changed release, migration, rollback, or compatibility risk. |

These are starting points. Reduce frequency when findings rarely change or the
interruption cost exceeds the omission risk.

## Evidence-based schedule selection

When choosing a trigger, cadence, time model, or evidence window, read
[references/scheduling.md](references/scheduling.md). It defines how to derive a
scheduled, event-driven, hybrid, lifecycle-triggered, or on-demand configuration
from acceptable detection delay, meaningful change rate, work cadence, action
windows, interruption cost, deduplication quality, source reliability, and prior
run evidence. Do not merely copy the table above.

A harness can ask:

```text
Read this skill, its README, and its scheduling reference. Use available workflow
and run evidence to recommend when engineering-attention should run. Provide the
trigger, starting cadence, fast and slow windows, notification policy, lower-cost
alternative, pilot, re-evaluation conditions, and material unknowns. Do not create
or modify an automation.
```

## Thin invocation: morning brief

```text
Use the engineering-attention skill.

Scope the run to my active engineering responsibilities and the accessible
repositories, project records, CI, release, incident, and commitment sources.

Use recent activity as the fast window and available historical cadence,
ownership, project, and previous-run context as the slow baseline.

Return no more than five Now items and five Soon items. Report only new,
materially changed, escalated, or newly resolved findings. Perform no external
write actions. Remain silent when no material attention item exists.
```

## Thin invocation: review follow-up

```text
Use the engineering-attention skill in fast mode, with historical review cadence
when available.

Focus on requested reviews I owe, unresolved threads after revisions, authored
pull requests waiting unexpectedly, and merge-ready work blocked by a clear
administrative action.

Exclude documented holds, weekends, bot-only activity, known long-running work,
and items already acknowledged until a future date.

Do not comment, rerun checks, change metadata, or modify code. Return direct
evidence and a recommended next action for each finding.
```

## Thin invocation: weekly stale work

```text
Use the engineering-attention skill in hybrid mode.

Compare open engineering work with its repository, project, and work-type
cadence. Identify abandoned work, blocked work without escalation, decisions
without owners, and commitments without completion evidence.

Do not use one universal age threshold when historical cadence is available.
Separate intentional waiting from forgotten work. Return at most ten findings,
ranked by consequence and ease of recovery.
```

## Schedule configuration checklist

Use the native scheduling and automation mechanism of the chosen harness. Define:

- subject or team whose attention is protected;
- repositories, services, projects, and source systems in scope;
- recent and historical windows;
- working days, timezone, and release-period overrides;
- result caps and silence policy;
- permitted actions and approval gates;
- state location and retention policy;
- exclusions, snoozes, and intentional waiting periods;
- output destination;
- cost, runtime, and automatic-pause limits.

This checklist is deliberately not a canonical schema. Translate it into cron,
a hosted automation, a CI workflow, a local task runner, or another scheduler as
appropriate.

## State guidance

Persist only the minimum data needed for deduplication, change detection, source
coverage, and feedback. Do not rely on chat history alone. Keep sensitive message
content and credentials out of version control.