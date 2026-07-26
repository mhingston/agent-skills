# Scheduling `engineering-attention`

Use this reference when asked whether, when, or how often to run
`engineering-attention`. Read the skill and README first, then derive a schedule
from the target workflow and evidence. Do not merely copy an example cadence.

## Choose the trigger type

Prefer:

- **scheduled** runs when several sources must be reconciled and no single event
  represents the attention decision;
- **event-driven** runs when a trustworthy event requires low-latency detection,
  such as a critical CI failure, production incident, or release-state change;
- **hybrid** operation when events provide rapid detection but a periodic run is
  needed to reconcile missed events, commitments, stale work, and cross-source
  context;
- **on demand** runs for expensive, uncommon, or highly judgement-dependent
  investigations;
- **lifecycle-triggered** runs around release windows, migrations, incidents, or
  project milestones.

Do not poll frequently for conditions that an authoritative event can surface
reliably. Do not rely only on events when the skill must compare several sources,
find missing activity, or detect stale work.

## Evidence to inspect

Use available evidence about:

- how quickly blockers, review requests, commitments, CI failures, release risks,
  and incident actions become costly;
- the arrival rate of materially new or changed findings;
- the normal review, delivery, and issue cadence for the work in scope;
- working hours, time zones, stand-ups, planning meetings, and release windows;
- how often previous runs produced only unchanged findings;
- duplicate-alert, dismissal, snooze, and false-positive rates;
- known misses and how long they existed before detection;
- source freshness, event reliability, runtime, and access cost;
- whether state can distinguish new, changed, escalated, resolved, and unchanged
  findings;
- whether the run is silent context refresh or a user interruption.

State which evidence was unavailable. Fixed age thresholds are a fallback when
historical cadence cannot be established, not proof of universal staleness.

## Choose the time model and windows

- Use **fast** mode for recent changes whose value decays quickly.
- Use **slow** mode to refresh ownership, project, dependency, cadence, and
  recurring-failure context without routine notification.
- Use **hybrid** mode for prioritisation, anomaly detection, and stale-work review.

Set separate windows for recent evidence and historical baseline. The historical
window should cover enough representative work cycles to distinguish normal delay
from anomalous inactivity without retaining unnecessary sensitive data.

## Choose a starting cadence

Balance:

1. **Acceptable detection delay** — how long a finding can wait before its omission
   becomes materially more costly.
2. **Meaningful change rate** — how often a run discovers a new, changed,
   escalated, or resolved item.
3. **Action window** — when the recipient can use the result, such as before a
   working day, stand-up, review block, or release decision.
4. **Interruption cost** — whether each run notifies a person or remains silent.
5. **Deduplication quality** — whether unchanged findings can be suppressed.
6. **Source and execution cost** — the expense and reliability of inspecting all
   required surfaces.

Prefer the lowest frequency that still meets the acceptable detection delay.
Increase frequency temporarily during releases or incidents rather than making an
exceptional cadence permanent.

## Common starting hypotheses

These require local evidence before adoption:

- one hybrid brief near the start of each working day;
- one fast blocker or commitment check late in the working day;
- one or two fast review-follow-up checks per working day;
- one hybrid stale-work review near the start of the working week;
- a silent incremental slow-context refresh overnight and a fuller refresh weekly;
- event-driven critical-risk detection plus periodic reconciliation;
- temporarily increased hybrid frequency during a release or migration window.

## Recommend a pilot

Return:

```text
Recommended trigger:
[scheduled, event-driven, hybrid, on demand, or lifecycle-triggered]

Starting cadence:
[human-readable recommendation]

Why:
[evidence about acceptable delay, change rate, action window, and interruption cost]

Time model:
[fast, slow, or hybrid]

Windows:
- Recent evidence:
- Historical baseline:

Notification behaviour:
[always report, changes only, or silent when clean]

Alternative:
[a lower-cost or less interruptive configuration]

Pilot:
[minimum runs and representative period]

Increase frequency when:
[evidence-backed conditions]

Decrease or pause when:
[evidence-backed conditions]

Unknowns:
[missing evidence that could materially change the recommendation]
```

During the pilot, record useful findings, correct silence, duplicates, false
positives, misses, source coverage, runtime, cost, interruptions, and actions
actually taken. Do not modify the schedule or permissions without separate human
approval.