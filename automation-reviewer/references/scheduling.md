# Scheduling `automation-reviewer`

Use this reference when asked whether, when, or how often to run
`automation-reviewer`. Read the skill and README first, then derive the review
trigger from available run evidence and risk. Do not merely copy an example
cadence.

## Choose the trigger type

Prefer:

- **after a minimum run count** when review quality depends on representative pilot
  evidence;
- **scheduled portfolio review** when several mature automations need periodic
  comparison and governance;
- **threshold-triggered review** after repeated dismissals, duplicates, misses,
  source failures, cost overruns, or interruption-budget breaches;
- **immediate safety review** after an unauthorised, surprising, or poorly verified
  side effect;
- **lifecycle-triggered review** before increasing permissions, moving harnesses,
  changing important sources, or promoting a repeated prompt into a skill;
- **hybrid review** when periodic governance should be supplemented by safety and
  quality thresholds.

Avoid reviewing after every successful run unless an active safety investigation
requires it. A single run rarely supports reliable tuning conclusions.

## Evidence to inspect

Use available evidence about:

- the number of representative runs and whether they cover normal and
  failure-prone periods;
- useful findings, correct silence, false positives, duplicate notifications,
  known misses, indeterminate runs, and execution failures;
- dismissals, snoozes, feedback, and actions users actually took;
- source coverage, freshness, and unavailable-source patterns;
- runtime, token, compute, financial, and interruption cost;
- permission compliance, external effects, and postcondition evidence;
- recent changes to prompts, skills, models, tools, sources, schedules, thresholds,
  policies, state, or harness adapters;
- the consequence of leaving a poor automation unchanged.

Do not compare materially different automation versions as one homogeneous sample.
State where feedback, known-miss data, cost, or side-effect evidence is incomplete.

## Choose a review window

Use a window long enough to include representative conditions but short enough that
the automation contract and implementation remain comparable. Prefer:

- a minimum run count for low-frequency automations;
- a representative calendar period for daily or intra-day automations;
- one or more lifecycle events for release, incident, or project automations;
- immediate bounded evidence for safety incidents;
- a portfolio window that includes recent changes and the previous review decision.

Version the automation definition, skill or prompt, model, tools, sources, policy,
and schedule when possible.

## Choose a starting cadence

Balance:

1. **Evidence sufficiency** — enough runs, feedback, and known outcomes to support a
   conclusion.
2. **Risk exposure** — permission level, reversibility, and consequence of misses or
   unexpected effects.
3. **Change rate** — how frequently the automation or its environment changes.
4. **Operational burden** — noise, cost, runtime, and human review effort.
5. **Decision horizon** — when a tuning, promotion, pause, or permission decision
   must be made.

Use threshold and lifecycle triggers when they provide stronger evidence than a
calendar date. Increase review frequency before and after expanding autonomy.

## Common starting hypotheses

Treat these as evidence-gathering candidates, not defaults:

- pilot review after several representative runs;
- monthly portfolio review for actively used automations;
- review after repeated duplicate alerts or dismissals;
- immediate review after an unauthorised or surprising side effect;
- review before adding write permissions;
- review before moving an automation to another harness;
- review when repeated prompt logic may justify a reusable skill.

## Recommend a pilot

Return:

```text
Recommended trigger:
[minimum-run, scheduled, threshold-triggered, safety-triggered, lifecycle-triggered, or hybrid]

Starting cadence or threshold:
[human-readable recommendation]

Why:
[evidence about sample sufficiency, risk, change rate, and review cost]

Review window:
[runs, dates, lifecycle events, and comparable versions]

Critical bypass:
[conditions that should trigger immediate review]

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

Do not modify schedules, permissions, thresholds, prompts, skills, state, or
harness configuration unless the user separately authorises that action.