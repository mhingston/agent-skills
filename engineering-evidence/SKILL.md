---
name: engineering-evidence
description: >
  Build an evidence-backed ledger of engineering outcomes, decisions,
  reliability work, reviews, mentoring contributions, and stakeholder impact.
  Use for recurring weekly or monthly impact capture, release retrospectives, or
  reconstructing factual work evidence. Do not use to score people, infer
  performance, rank contributors, or fabricate impact from activity counts.
---

# Engineering Evidence

Preserve useful engineering evidence while it is still easy to verify. Produce a
factual ledger that links work to outcomes and decisions without turning activity
into a performance judgement.

## Operating boundary

May:

- inspect accessible engineering and collaboration records;
- consolidate duplicate evidence;
- identify missing outcome or rationale context;
- maintain a private evidence ledger when explicitly permitted;
- draft a factual summary for human review.

Must not:

- rank people or teams;
- assign performance ratings;
- infer motivation, effort, credit, or blame;
- equate commits, lines changed, review count, or message volume with impact;
- disclose private or sensitive evidence beyond the configured audience;
- send summaries or update personnel systems without explicit approval.

## Relevant evidence

Use authoritative or attributable sources where available:

- merged changes and released behaviour;
- incidents, mitigations, remediation, and prevented recurrence;
- architectural and operational decisions with rationale;
- code reviews that changed risk, correctness, maintainability, or understanding;
- migrations, reliability improvements, cost reductions, and toil reduction;
- documentation, enablement, mentoring, and unblock evidence;
- customer or stakeholder feedback tied to an engineering outcome;
- follow-up work created from discovered risks or gaps.

An activity is not automatically an outcome. Distinguish:

- **activity** — something happened;
- **output** — an artefact was produced;
- **outcome** — behaviour, reliability, cost, risk, delivery, or understanding changed;
- **claim** — an interpretation requiring human confirmation.

## Workflow

### 1. Establish purpose and audience

Determine whether the ledger supports:

- personal recall;
- team status or retrospective preparation;
- release or incident review;
- leadership communication;
- promotion or performance evidence preparation.

When the audience is sensitive, default to a private factual ledger and require
human review before reuse.

### 2. Set the evidence window and scope

Define:

- time window;
- repositories, services, projects, and teams in scope;
- available sources;
- prior ledger or deduplication state;
- inclusion and privacy boundaries;
- desired level of detail.

Report source gaps and avoid claims beyond the inspected scope.

### 3. Extract candidate evidence

Look for candidates such as:

- shipped or released changes with observable behaviour;
- reliability, security, privacy, or data-integrity improvements;
- incidents resolved and follow-up risks reduced;
- significant technical decisions and rejected alternatives;
- reviews that identified or prevented a material problem;
- dependencies, migrations, or deprecations completed;
- documented unblock, enablement, or mentoring outcomes;
- stakeholder feedback linked to a delivered result.

Do not include routine activity merely to fill the report.

### 4. Link evidence to outcome

For each candidate, record:

- date or period;
- subject, project, service, or work item;
- factual contribution or decision;
- resulting output;
- observed or expected outcome;
- direct evidence;
- collaborators and attribution when evidenced;
- confidence and unresolved context.

Mark expected outcomes as expected. Do not rewrite them as observed results.

### 5. Falsify and deduplicate

Check for:

- duplicate records across pull requests, releases, and project updates;
- reverted, rolled-back, or superseded work;
- outcomes that did not materialise;
- work performed by another person or team;
- attribution ambiguity;
- sensitive information inappropriate for the audience;
- activity metrics presented as impact.

Preserve disagreement or uncertainty rather than manufacturing a clean narrative.

### 6. Maintain continuity

When prior state is available:

- use a stable identity for the underlying outcome or decision;
- update an existing entry when evidence improves;
- record reversals, supersession, and later-observed results;
- avoid repeating unchanged entries in incremental summaries;
- retain source links and capture dates;
- follow configured retention and deletion rules.

### 7. Summarise proportionately

Prefer a small number of well-supported entries over exhaustive activity.

Group by outcome type when useful:

- delivery and customer value;
- reliability, security, and risk reduction;
- technical direction and decisions;
- team enablement and knowledge transfer;
- follow-up opportunities.

Keep factual evidence separate from optional human-authored interpretation.

## Output

Return:

### Evidence captured

For each entry include:

- concise factual title;
- date or period;
- contribution or decision;
- output;
- observed outcome, expected outcome, or unresolved outcome;
- evidence links or source routes;
- collaborators or attribution notes;
- confidence;
- sensitivity or audience constraint when relevant.

### Updated outcomes

Previously recorded items whose result, status, attribution, or confidence changed.

### Missing context

Promising evidence that cannot yet be used because outcome, attribution, access,
or rationale is missing.

### Coverage and limitations

Inspected and unavailable sources, scope limits, and any privacy exclusions.

### Optional draft summary

Only when requested, provide a human-reviewable summary grounded entirely in the
ledger. Label unverified interpretation clearly.

## Validation checks

Before returning:

- every entry has attributable evidence;
- activity is not presented as impact without an outcome;
- observed and expected outcomes are distinct;
- duplicates, reversals, and supersession are handled;
- attribution is evidence-backed and non-exclusive when collaborative;
- private material respects the audience boundary;
- no rating, ranking, or performance judgement is produced.
