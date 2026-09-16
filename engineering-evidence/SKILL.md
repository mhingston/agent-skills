---
name: engineering-evidence
description: >
  Proactively discover, correlate, and substantiate evidence of engineering and
  business impact attributable to the user across available read-only tools and
  records. Use for weekly, monthly, quarterly, project, release, or review-period
  impact capture; reconstructing forgotten contributions; finding measurable
  outcomes; or preparing evidence for retrospectives, leadership updates, CVs,
  portfolios, promotion, or performance-review discussions. Distinguish activity,
  output, observed impact, supported contribution, expected impact, and candidate
  impact. Use `engineering-attention` instead when the primary question is what
  engineering work needs action now. Do not score people, rank contributors,
  infer performance, or manufacture impact from activity counts.
---

# Engineering Evidence

Recover useful evidence of what the user changed, enabled, prevented, or improved
while that evidence is still accessible. Build an evidence-backed impact ledger,
not a favourable narrative or activity report.

The goal is to distinguish demonstrated impact from plausible or still-emerging
impact and make attribution, uncertainty, collaborators, and missing evidence
visible.

## Operating boundary

May:

- inspect accessible engineering, delivery, collaboration, incident,
  documentation, and analytics records;
- discover candidate contributions and outcomes across connected systems;
- correlate evidence across systems when it materially strengthens or falsifies
  a claim;
- consolidate duplicate evidence;
- identify missing outcome, attribution, or rationale context;
- maintain a private evidence ledger when explicitly permitted;
- transform the ledger into factual material for human review when requested.

Must not:

- rank people or teams;
- assign performance ratings or promotion recommendations;
- infer motivation, effort, credit, or blame beyond the evidence;
- equate commits, lines changed, PR count, review count, story points, velocity,
  or message volume with impact;
- claim exclusive ownership for collaborative outcomes;
- manufacture financial value or causality;
- suppress contradictory evidence;
- disclose private or sensitive evidence beyond the configured audience;
- send summaries or update personnel systems without explicit approval;
- act as the authoritative active decision register or reconcile a current
  proposal against prior decisions; use a decision-continuity workflow for that
  purpose.

Discovery should be read-only by default. A missing or inaccessible source is a
coverage limitation, not evidence that no contribution occurred.

## Core attribution principle

Capture both:

- outcomes directly produced by the user; and
- broader team, project, or organisational outcomes where evidence shows the
  user materially contributed.

Do not require the user to be solely responsible for an outcome.

For every finding distinguish:

- the user's evidenced contribution;
- the broader outcome;
- relevant collaborators;
- uncertainty about attribution;
- whether the evidence supports observed impact, supported contribution,
  expected impact, or only a candidate hypothesis.

Never imply exclusive ownership where the work was collaborative.

## Discover available evidence

At the beginning of a run:

1. Establish the requested time period, scope, projects, and intended audience.
2. Determine which relevant tools and data sources can actually be inspected.
3. Search those sources for candidate contributions and outcomes.
4. Correlate evidence across systems when doing so materially strengthens or
   falsifies a claim.
5. Report important evidence surfaces that were unavailable.
6. Never treat lack of evidence from an inaccessible source as evidence that no
   contribution occurred.

The skill is harness-agnostic and should use whatever relevant integrations are
available rather than requiring a fixed toolset.

Potential sources include:

- GitHub/GitLab: PRs, issues, reviews, discussions, releases, commits, CI, and
  deployment evidence;
- Jira/Linear/Azure DevOps: work items, initiatives, delivery history, cycle
  time, lead time, blocked time, throughput, and rework;
- Slack/Teams/email: attributable stakeholder feedback, recognition, decisions,
  unblock evidence, and initiative history;
- incident and observability systems: incidents, mitigations, reliability
  changes, remediation, and recurrence;
- documentation systems: ADRs, proposals, technical strategy, onboarding
  material, and knowledge improvements;
- product or business analytics: adoption, conversion, support load, cost,
  latency, quality, and other relevant outcome measures.

Do not require every source to be connected.

## Activity, output, outcome, and claim

Do not confuse activity with impact.

Examples:

- "12 PRs merged" is activity.
- "Introduced automated deployment validation" is an output.
- "Failed deployments decreased from X to Y after rollout over comparable
  periods" is an observed outcome.
- "This increased engineering velocity" remains a claim unless the evidence
  supports it.

Use activity metrics as discovery signals, not evidence of value by themselves.

## Impact areas

Search for attributable evidence across areas such as:

- customer or business value;
- delivery flow and reduced time-to-value;
- reliability and resilience;
- security, privacy, and compliance;
- cost or resource reduction;
- developer productivity and reduced toil;
- quality and defect reduction;
- architectural or technical direction;
- simplification and removal of unnecessary complexity;
- team enablement and knowledge transfer;
- mentoring and reviewing;
- cross-team coordination and unblocking;
- risk identification or prevention;
- initiatives originated or materially advanced;
- stakeholder or customer recognition tied to specific work.

Do not force every contribution into a financial metric.

## Invisible and leverage-heavy work

Actively search for valuable work that simple activity reports often miss:

- ideas or initiatives originated by the user;
- proposals or prototypes that shaped subsequent implementation;
- risks identified before they became incidents;
- architectural or technical decisions;
- recommendations adopted by others;
- reviews that materially improved correctness, safety, or design;
- mentoring or knowledge transfer;
- cross-team unblocking;
- documentation and onboarding improvements;
- removal of recurring manual work;
- simplification;
- projects deliberately stopped after evidence showed they were not worthwhile.

A merged PR is not required for a contribution to matter.

## Quantitative evidence

Where suitable data exists, investigate comparisons such as:

- cycle time;
- lead time;
- blocked or waiting time;
- deployment frequency;
- change failure rate;
- incident frequency or duration;
- defect or rework rate;
- manual effort or toil;
- infrastructure, model, or API cost;
- latency and throughput;
- customer or product measures.

Avoid using velocity or story points as an individual productivity measure.

Before attributing a metric change to the user's work, consider where possible:

- comparable populations and time windows;
- other simultaneous changes;
- workload or seasonality;
- changes to measurement definitions;
- sample size;
- whether the contribution has a credible mechanism for influencing the measure.

Distinguish correlation from causality.

## Evidence strength

Classify each finding using a small evidence model.

### Observed impact

Direct evidence shows that the relevant outcome occurred and the user's
contribution can reasonably be linked to it.

### Supported contribution

The wider outcome occurred and evidence shows that the user materially
contributed, but exclusive causality cannot be established.

### Expected impact

The work has shipped, been adopted, or changed behaviour, but the intended
downstream result has not yet had enough time or measurement to be observed.

### Candidate impact

There is plausible evidence of value, but material context, attribution,
measurement, or validation is missing.

Never silently convert expected or candidate impact into observed impact.

## Emerging impact

Maintain an explicit set of contributions worth revisiting later.

For each one capture:

- the contribution;
- expected outcome;
- evidence available now;
- what additional evidence would strengthen or falsify the claim;
- an appropriate observation window where one can reasonably be inferred.

Example:

> Introduced automated PR validation. Expected impact: reduced review rework and
> shorter cycle time. Revisit after enough comparable work has passed through
> the workflow.

Do not invent a measurement period when there is insufficient evidence to choose
one.

## Praise and stakeholder signals

Treat attributable praise, recognition, and positive feedback as useful
supporting evidence, not automatic proof of business impact.

Capture:

- what work or behaviour the feedback referred to;
- the relevant outcome or project;
- who supplied the feedback where appropriate;
- a source route;
- whether there is corroborating outcome evidence.

Prefer a concise factual note and source link over retaining large message bodies.
Avoid turning popularity, message frequency, or praise volume into a score.

## Workflow

### 1. Establish purpose, audience, and scope

Determine the requested period and whether the ledger supports:

- personal recall;
- team status or retrospective preparation;
- release or incident review;
- leadership communication;
- project or quarterly summaries;
- CV or portfolio preparation;
- promotion or performance-review evidence preparation.

Define repositories, services, projects, teams, privacy boundaries, prior ledger
state, and desired level of detail. When the audience is sensitive, default to a
private factual ledger and require human review before reuse.

### 2. Discover candidate contributions

Search accessible evidence surfaces for work attributable to the user and for
team or project outcomes plausibly linked to that work.

Start broad enough to recover forgotten or invisible contributions, then narrow
to candidates with meaningful outcomes. Routine activity may guide discovery but
should not be included merely to fill the report.

### 3. Link contribution to outcome

For each candidate, record:

- date or period;
- subject, project, service, or work item;
- user's factual contribution or decision;
- resulting output where relevant;
- broader observed or expected outcome;
- why the outcome mattered;
- direct evidence and source routes;
- quantitative evidence where meaningful;
- collaborators and attribution;
- evidence strength;
- unresolved context or caveats.

### 4. Correlate across systems

Where materially useful, connect evidence such as:

- a PR or ADR to a release or deployment;
- a delivery change to cycle-time or blocked-time data;
- a remediation to incident recurrence or reliability data;
- an automation to manual-effort or cost evidence;
- a proposal or review to later implementation by others;
- stakeholder praise to the specific work or outcome it referenced.

Do not correlate sources merely to make a claim appear stronger.

### 5. Falsify promising claims

Actively attempt to weaken strong-looking findings before presenting them.

Check for evidence that:

- work was reverted or superseded;
- the supposed outcome predates the contribution;
- another simultaneous change better explains the result;
- attribution primarily belongs elsewhere;
- an estimated saving was never measured;
- stakeholder praise referred to different work;
- a local improvement caused worse downstream outcomes;
- greater throughput coincided with greater rework or failure;
- the expected outcome never materialised.

Preserve contradictory evidence and uncertainty.

### 6. Deduplicate and maintain continuity

When prior state is available:

- use a stable identity for the underlying contribution or outcome;
- update an existing entry when evidence improves;
- record reversals, supersession, and later-observed results;
- avoid repeating unchanged entries in incremental summaries;
- retain source links and capture dates;
- follow configured retention and deletion rules.

### 7. Summarise proportionately

Prefer a small number of meaningful findings over exhaustive activity statistics.
Five well-supported impacts are better than fifty weak activity signals.

Keep evidence separate from optional human interpretation.

## Output

Return an evidence-backed impact report.

### Strongest evidenced impacts

For each include:

- outcome;
- user's attributable contribution;
- why the outcome mattered;
- relevant quantitative evidence;
- supporting source routes;
- collaborators and attribution;
- evidence strength;
- caveats or contradictory evidence.

### Additional contributions

Meaningful contributions with less measurable or more indirect downstream impact.

### Stakeholder signals

Relevant attributable praise, recognition, or feedback linked to specific work.

### Emerging impact

Recent contributions with outcomes worth evaluating later.

### Missing evidence

Potentially valuable claims where another measurement, source, or observation
period would materially improve confidence.

### Coverage and limitations

Include:

- period and scope;
- sources inspected;
- unavailable sources;
- material privacy exclusions;
- important attribution or measurement limitations.

## Optional reuse modes

When explicitly requested, transform the evidence ledger into factual material
suitable for:

- retrospectives;
- project or quarterly summaries;
- leadership updates;
- CV or portfolio preparation;
- promotion or performance-review preparation.

These are presentation modes over the evidence, not separate evidence standards.

For performance-review or promotion preparation:

- surface relevant evidence;
- organise it around the requested framework where one is supplied;
- distinguish evidence from interpretation;
- leave rating, promotion, compensation, and performance judgement to humans.

Do not independently assess whether the user deserves a promotion, rating, or
reward.

## Validation checks

Before returning:

- every reported impact has attributable evidence;
- activity is not presented as impact without an outcome;
- observed, supported, expected, and candidate impact are distinct;
- attribution is evidence-backed and non-exclusive when collaborative;
- quantitative comparisons use reasonably comparable populations and periods;
- contradictory evidence, reversals, and supersession are preserved;
- praise is tied to specific work rather than treated as a score;
- inaccessible sources are reported as coverage gaps rather than negative
  evidence;
- private material respects the audience boundary;
- no rating, ranking, promotion judgement, or manufactured financial value is
  produced.

## Scheduling guidance

When asked whether, when, or how often to run this skill as an automation, read
[references/scheduling.md](references/scheduling.md). Derive the trigger, cadence,
capture, observation and consolidation windows, output behaviour, pilot, and
re-evaluation conditions from evidence half-life, lifecycle rhythm,
prior-ledger evidence, and privacy constraints. Do not merely repeat README
examples or modify an automation without explicit approval.
