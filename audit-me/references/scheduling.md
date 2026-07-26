# Scheduling `audit-me`

Use this reference when asked whether, when, or how often to run `audit-me` as an
automation. Derive the recommendation from the target workflow and available
evidence. Do not merely repeat the example cadences in the README.

## Decide whether scheduling is appropriate

Prefer:

- **on demand** when the automation portfolio is small, stable, or rarely changes;
- **scheduled review** when recurring friction and automation outcomes accumulate
  across several systems without a reliable event trigger;
- **event-triggered review** after a material role, tool, source, permission, or
  responsibility change;
- **threshold-triggered review** after repeated false positives, misses,
  dismissals, unavailable-source runs, or unexpected side effects;
- **hybrid review** when a periodic portfolio audit should be supplemented by
  material-change or safety triggers.

Do not schedule `audit-me` merely because a scheduler is available. A review that
cannot inspect recent work, automation definitions, run history, and feedback is
likely to produce generic recommendations.

## Evidence to inspect

Use available evidence about:

- changes to responsibilities, repositories, teams, tools, and connected sources;
- repeated manual checks or context-reconstruction work;
- dropped commitments, stale work, evidence loss, and coordination failures;
- the number and age of active automations;
- useful findings, correct silence, false positives, duplicates, and known misses;
- source-coverage gaps, execution failures, cost, and interruption burden;
- recent schedule, permission, threshold, or implementation changes;
- when the previous portfolio audit occurred and which recommendations were acted on.

State which evidence was unavailable. Do not treat a lack of recorded problems as
proof that no friction exists when feedback or work surfaces were not inspected.

## Choose a starting trigger and cadence

Balance:

1. **Rate of change** — how frequently responsibilities, sources, and automations
   materially change.
2. **Cost of omission** — how damaging it is to leave recurring friction or a poor
   automation unreviewed.
3. **Evidence accumulation** — how many representative runs or work cycles are
   needed before conclusions are useful.
4. **Review cost** — source-access cost, execution cost, and human attention needed
   to evaluate recommendations.
5. **Actionability** — whether the review occurs early enough to influence the
   next planning, delivery, or portfolio decision.

Use a calendar cadence only when it produces enough new evidence to justify the
review. Prefer a minimum run count or lifecycle trigger when evidence accumulates
irregularly.

## Common starting points

Treat these as hypotheses, not defaults:

- initial audit after relevant work surfaces are connected;
- monthly review for an actively changing portfolio with sufficient run history;
- quarterly review for a stable, low-noise portfolio;
- immediate review after an unauthorised or surprising side effect;
- review after several repeated dismissals, misses, or source failures;
- review after a material role, team, tool, or responsibility change.

## Recommend a pilot

Return:

```text
Recommended trigger:
[on demand, scheduled, event-driven, threshold-triggered, lifecycle-triggered, or hybrid]

Starting cadence:
[human-readable recommendation]

Evidence:
[observed rate of change, portfolio history, failure patterns, and review cost]

Review window:
[time period, minimum run count, or lifecycle events to inspect]

Notification behaviour:
[always report, report recommendations only, or remain silent when unchanged]

Alternative:
[a lower-cost or less frequent configuration]

Pilot:
[minimum reviews or representative period]

Increase frequency when:
[evidence-backed conditions]

Decrease or pause when:
[evidence-backed conditions]

Unknowns:
[missing evidence that could materially change the recommendation]
```

Do not create, reschedule, enable, disable, or modify an automation unless the
user separately authorises that action.