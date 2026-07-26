# automation-reviewer

`automation-reviewer` evaluates whether scheduled prompts, reusable skills, and
other agent automations are useful, quiet, safe, and worth their operational
cost. It proposes changes but does not apply them.

## Suggested automations

| Purpose | Suggested cadence | Minimum useful evidence |
| --- | --- | --- |
| Pilot review | After several representative runs | Findings, feedback, misses, coverage, and cost. |
| Monthly portfolio review | Monthly | Run history across normal and failure-prone periods. |
| Noise review | After repeated dismissals or duplicate alerts | Examples of unnecessary interruptions. |
| Safety review | Immediately after an unauthorised or surprising side effect | Exact action, authority, and resulting state. |
| Promotion review | Before giving an automation write permissions | Read-only pilot evidence and postcondition design. |
| Portability review | Before moving to another harness | Behavioural fixtures and adapter differences. |

Avoid reviewing after every run unless the automation is in an active safety
investigation.

## Thin invocation: pilot review

```text
Use the automation-reviewer skill.

Review the selected automation across the available pilot runs. Inspect its
purpose, definition, skill or prompt version, schedule, scope, source coverage,
finding history, user feedback, known misses, cost, interruptions, and side
effects.

Classify useful findings, correct silence, false positives, duplicates, misses,
indeterminate runs, and failures. Recommend one reversible change and a measured
follow-up pilot.

Do not modify the automation, its permissions, schedule, thresholds, or state.
```

## Thin invocation: monthly portfolio review

```text
Use the automation-reviewer skill to inspect the current automation portfolio.

Rank automations by omission prevention, evidence quality, noise, cost, source
coverage, and permission risk. Identify at most one automation to tune, one to
pause or simplify, and one prompt whose repeated logic may justify a reusable
skill.

Propose changes only. Preserve harness-agnostic canonical skills and keep adapter
concerns separate.
```

## Schedule configuration checklist

Use the native scheduler and define:

- automations or portfolio in scope;
- review window or minimum run count;
- location of definitions, run history, state, and feedback;
- known-miss and false-positive sources;
- cost and interruption data;
- report destination;
- maximum recommendations;
- whether critical safety findings should bypass normal silence;
- approval route for any proposed change.

This is a checklist, not a required schema.

## Promotion rule

Do not promote a prompt into a reusable skill merely because it runs on a
schedule. Promotion is justified when multiple invocations repeat stable
procedural logic, evidence requirements, state semantics, safety boundaries, or
evaluation criteria.
