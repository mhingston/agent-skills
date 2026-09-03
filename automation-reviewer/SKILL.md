---
name: automation-reviewer
description: >
  Evaluate an existing recurring agent automation using run history, findings,
  user feedback, source coverage, cost, noise, misses, and side-effect evidence.
  Use after the automation has run, to tune, pause, split, simplify, or promote
  scheduled prompts and reusable skills after a pilot or during periodic portfolio
  review. Use `audit-me` to discover or design automation opportunities, and the
  underlying operational skill to produce the findings being evaluated. Do not
  silently change schedules, permissions, policies, or automation definitions.
---

# Automation Reviewer

Review whether an automation earns its operational cost and trust. Recommend
small, reversible changes grounded in run evidence.

## Operating boundary

Default to read-only review.

May:

- inspect automation definitions, prompts, skills, run history, state, and feedback;
- classify findings and failure patterns;
- recommend experiments, threshold changes, or implementation changes;
- draft revised prompts or skill changes when requested.

Must not, without explicit approval:

- enable, disable, reschedule, or delete automations;
- expand permissions or source access;
- change policy, thresholds, or state-retention rules;
- execute an automation's side effects;
- conceal misses, unavailable data, or adverse outcomes.

## Inputs

Use available evidence such as:

- automation purpose and current definition;
- skill or prompt versions;
- schedule and scope;
- run timestamps and completion status;
- findings and their evidence;
- user actions, dismissals, snoozes, and feedback;
- known missed items;
- source coverage and freshness;
- token, compute, runtime, or financial cost;
- interruptions or notifications;
- external side effects and postcondition evidence.

Do not infer success from run completion alone.

## Workflow

### 1. Reconstruct the automation contract

State:

- protected outcome;
- intended users;
- implementation form;
- time model;
- sources and context;
- schedule or trigger;
- permitted and approval-gated actions;
- output and silence policy;
- operational budget;
- success and pause criteria.

When the contract is unclear, identify the ambiguity before evaluating results.

### 2. Establish the review window

Prefer several representative runs rather than a single execution. Include both
normal and failure-prone periods when possible.

Record definition, prompt, skill, model, tool, source, and policy versions when
available. Do not compare runs as equivalent when material inputs changed.

### 3. Classify run outcomes

Classify evidence into:

- **Useful finding** — led to a justified action or prevented meaningful omission.
- **Correct silence** — no material finding and adequate source coverage.
- **False positive** — surfaced but should have remained silent.
- **Duplicate or stale notification** — correct fact, unnecessary interruption.
- **Miss** — known relevant item was not surfaced.
- **Indeterminate** — insufficient evidence or source coverage.
- **Execution failure** — automation failed to complete reliably.
- **Unsafe or unauthorised effect** — side effect exceeded the contract.

Preserve examples and source evidence for each material class.

### 4. Evaluate quality dimensions

Assess:

- usefulness and omission prevention;
- precision and false-positive burden;
- recall against known misses;
- evidence quality and source traceability;
- deduplication and change detection;
- coverage and graceful degradation;
- timeliness;
- cost and runtime;
- interruption burden;
- permission compliance;
- state retention and privacy;
- portability across intended harnesses.

Avoid false precision when sample sizes are small or feedback is incomplete.

### 5. Diagnose the failure layer

Locate the smallest likely cause:

- scope or responsibility model;
- source access or freshness;
- retrieval or parsing;
- identity resolution and deduplication;
- historical baseline;
- detection rule;
- ranking or threshold;
- schedule;
- output design;
- state handling;
- skill guidance;
- harness adapter;
- permission or postcondition control.

Do not respond to every false positive by adding more prompt text.

### 6. Choose the lightest change

Recommend one of:

- retain unchanged;
- narrow or broaden scope;
- tune schedule or notification policy;
- adjust a threshold or exclusion;
- repair source coverage or state;
- add a regression fixture;
- simplify a reusable skill;
- extract repeated logic from prompts into a skill;
- move deterministic logic into code or CI;
- split an overloaded automation;
- combine duplicate automations;
- pause or retire;
- require a new pilot before increased autonomy.

Keep proposed changes harness-agnostic unless reviewing a harness-specific adapter.

### 7. Define a reversible experiment

For each recommended change specify:

- hypothesis;
- exact change;
- unchanged boundaries;
- pilot duration or run count;
- positive, negative, ambiguous, and regression fixtures;
- metrics and evidence to collect;
- success, rollback, and pause conditions;
- approval required.

Do not silently apply the experiment.

## Output

Return:

### Automation reviewed

Purpose, implementation form, time model, scope, schedule, permissions, and
review window.

### Evidence summary

Counts or qualitative evidence for useful findings, correct silence, false
positives, duplicates, misses, indeterminate runs, failures, and side effects.
State limitations clearly.

### Diagnosis

The smallest supported failure layer and the evidence for it.

### Recommended change

One primary change, expected benefit, risk, and why simpler alternatives are
insufficient or preferable.

### Experiment

A bounded pilot with fixtures, measurements, success criteria, rollback, and
approval requirements.

### Keep unchanged

Important boundaries or mechanisms that should not change.

### Portfolio follow-ups

At most three lower-priority observations. Do not let these displace the primary
recommendation.

## Validation checks

Before returning:

- conclusions are tied to run evidence;
- unavailable coverage is visible;
- correct silence is not counted when coverage was inadequate;
- small samples are not presented with false certainty;
- prompt complexity is not the default remedy;
- no schedule, permission, or definition was changed;
- the recommendation is reversible and has a measurable pilot.

## Scheduling guidance

When asked whether, when, or how often to run this skill as an automation, read
[references/scheduling.md](references/scheduling.md). Derive the trigger, cadence
or threshold, review window, critical bypass, pilot, and re-evaluation conditions
from sample sufficiency, failure evidence, risk, change rate, cost, and pending
governance decisions. Do not merely repeat README examples or modify an
automation without explicit approval.