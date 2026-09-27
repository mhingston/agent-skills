---
name: review-calibration
description: Evaluate historical code-review evidence to determine whether review dimensions, thresholds, falsification, specialist routing, and reviewer topology are useful. Use when a team wants evidence-backed proposals for improving its AI-assisted review policy. Produce advisory calibration proposals only; never alter policy, approve changes, rank reviewers, or infer quality from finding counts alone.
---

# Review Calibration

Evaluate whether a review workflow is finding consequential risks efficiently and
routing them appropriately. Turn historical evidence into explicit proposals for
human-governed policy changes without silently tuning prompts, thresholds, models, or
approval rules.

Read [`references/calibration-contract.md`](references/calibration-contract.md) before
collecting evidence or producing proposals.

## Boundaries

- Remain read-only unless the user separately asks to publish an approved proposal.
- Do not change review policy, thresholds, required dimensions, model routing, branch
  protection, or repository settings.
- Do not infer reviewer competence, author quality, team performance, or individual
  productivity from review outcomes.
- Do not hard-code vendor-, harness-, or model-specific defect assumptions from external
  studies. Treat them only as hypotheses until compatible local revision-linked evidence
  supports a bounded review-policy experiment.
- Do not optimise for more findings. An empty, well-covered review can be correct.
- Do not treat a human rejection as proof that a finding was poor; inspect the stated
  rationale and later evidence.
- Do not treat a later defect as proof that a reviewer should have predicted it unless
  the reviewed evidence made the failure reasonably discoverable.
- Keep technical severity, confidence, policy threshold, human disposition, and later
  outcome separate.
- Report unavailable or incompatible evidence rather than fabricating metrics.

## Inputs

Resolve a bounded calibration window and collect the best available versions of:

- revision-bound review reports and risk maps;
- candidate-finding and falsification receipts, when recorded;
- human-verdict records and per-risk dispositions;
- pull-request revisions and material review comments;
- authoring harness/model provenance and defect taxonomy when those fields were captured
  deterministically for the exact revision rather than inferred from style or commit text;
- escaped defects, incidents, rollbacks, regressions, or support evidence that can be
  linked to an exact reviewed revision;
- specialist-review requests and their outcomes;
- measured review latency, model/tool usage, and cost where available;
- the current review policy, dimension definitions, thresholds, and routing rules.

Record repository, time window, included review versions, excluded records, linkage
method, retention constraints, and evidence limitations. Never join records by title,
author, date proximity, or model-generated similarity alone when an exact revision or
stable risk identifier is available.

## Workflow

### 1. State the calibration question

Choose one primary question, for example:

- Does each mandatory review dimension contribute unique validated risk evidence?
- Are current thresholds producing useful human attention rather than routine overrides?
- Does independent falsification suppress unsupported findings?
- When does a different model, specialist, or deterministic analyser change the risk map?
- Do additional workers materially improve discovery for high-consequence changes?
- Are architectural unknowns being redirected upstream rather than casually accepted?
- Do locally observed defect mechanisms vary by authoring harness or model enough to justify
  a bounded adaptive review lens or specialist trigger?
- Is the current verification portfolio buying sufficient independent evidence at proportionate
  cost, latency, and human-attention load, or are some checks redundant, mistimed, or missing?

Do not run an unbounded retrospective. Name the decision that the evidence should inform.

### 2. Validate evidence compatibility

For every review record require, where applicable:

- exact repository, base SHA, and head SHA;
- report and risk-map schema version;
- execution mode and review dimensions;
- reviewer provenance and known correlation limitations;
- finding, falsification, threshold, disposition, and human-verdict identifiers;
- outcome linkage that distinguishes confirmed causal relevance from temporal proximity.

Separate evidence into `compatible`, `partially-compatible`, and `excluded`. Do not merge
metrics across schema versions or workflows unless their fields have equivalent meanings.

### 3. Build the review-outcome ledger

Create one row per reviewed revision and preserve one row per risk when analysing risk
outcomes. Include only fields supported by evidence:

- consequence and comprehension risk;
- mandatory and adaptive dimensions selected;
- candidate, validated, falsified, inconclusive, and deduplicated finding counts;
- unique validated risks by dimension;
- compound risks and unresolved architectural redirects;
- severity, likelihood, confidence, policy threshold, and technical disposition;
- human disposition and rationale category;
- specialist escalation and result;
- later linked outcome and linkage confidence;
- measured latency, model/tool use, cost, and human-attention demand where observable;
- verifier/check identity, ordering, and unique evidence contribution when the calibration
  question concerns the verification portfolio;
- reviewer-provenance and correlation indicators;
- authoring harness/model identity and later defect category only when revision-linked and
  compatible enough for the calibration question.

Counts are diagnostic inputs, never quality scores.

### 4. Evaluate discovery effectiveness

Assess:

- **unique contribution** — validated risks found by one dimension that were not recovered
  by another dimension or deterministic check;
- **falsification value** — candidates suppressed or downgraded after an evidence-backed
  attempt to disprove them;
- **duplication** — findings consolidated into one root cause or compound risk;
- **material unknowns** — consequential questions that remained unresolved at handoff;
- **escape alignment** — later defects whose causal mechanism was discoverable within the
  reviewed scope and mapped to a missing or ineffective dimension;
- **marginal worker value** — whether another worker, model, specialist, or tool changed
  the final risk map rather than merely restating it;
- **cost and latency** — measured resource use relative to consequence risk and unique
  evidence produced.

Avoid precision unsupported by the sample. Prefer counts and ranges over percentages for
small cohorts.

#### Verification budget and marginal verifier value

Treat verification as a bounded evidence portfolio, not a count of checks. For an
equivalent consequence-risk cohort, ask what the smallest portfolio is that preserves
the evidence needed for the human-owned decision.

For each verifier, deterministic check, model review, specialist review, or runtime probe,
inspect:

- the concrete claim, failure mode, contract, or boundary it can establish or falsify;
- whether it contributes unique decision-relevant evidence beyond cheaper or earlier checks;
- evidence correlation with other verifiers, including shared models, prompts, fixtures,
  assumptions, or execution paths;
- measured compute/tool cost, critical-path latency, and human interpretation/attention
  when available;
- whether moving it earlier would fail faster or reduce wasted downstream work;
- whether reserving it for a narrower change/risk class would preserve consequence coverage;
- the harm of false negatives, false positives, or removing the check.

Prefer cheap deterministic, high-signal checks early when they can reject invalid work
without weakening evidence. Reserve expensive semantic, specialist, mutation, browser/E2E,
or runtime checks for changes whose consequence, uncertainty, or boundary exposure justifies
them. Remove or narrow a verifier only when evidence shows its marginal signal is redundant
or immaterial to the decision.

A verification budget is never permission to drop required safety evidence, weaken a
contract, or treat a cheaper correlated check as independent confirmation. When mandatory
evidence exceeds the available budget, surface the capacity/policy conflict rather than
silently lowering the bar.

### 5. Evaluate threshold and routing behaviour

For each policy threshold or technical disposition, inspect:

- how often it triggered;
- which severities, confidence levels, and dimensions triggered it;
- how humans disposed the associated risk and why;
- whether accepted or deferred risks were tracked and revisited;
- whether `rejected-as-unsupported` cases reveal weak evidence, policy mismatch, or missing
  specialist context;
- whether `redirect-to-design` cases produced an approved upstream decision before review
  resumed;
- whether specialist or model escalation produced decision-relevant evidence;
- whether the rule is routinely bypassed, mechanically obeyed, or genuinely informative.

A frequently overridden threshold may still be correct. Distinguish policy failure from
poor evidence, exceptional context, and missing authority.

### 6. Examine reviewer correlation

Use recorded provenance to identify shared assumptions:

- same model or model family;
- same prompt family or originating context;
- same immutable evidence packet;
- same tools, retrieval limits, or unavailable runtime evidence;
- authoring model reused as reviewer or falsifier;
- lack of independent specialist or deterministic evidence.

Do not call parallel contexts independent when they share material assumptions. Recommend
heterogeneous review only where consequence and evidence justify the additional cost.

### 7. Test authoring-pattern hypotheses

Use authoring provenance only when the calibration question requires it and the evidence is
compatible. External benchmarks, vendor reports, or anecdotes may suggest what to test, but
must not become a standing review rule by themselves.

For a candidate authoring-pattern hypothesis:

- require exact revision-linked authoring identity rather than guessing from code style;
- compare the same defect mechanism across sufficiently comparable change classes,
  repositories, consequence levels, and time windows;
- inspect causal failure categories such as injection, authorisation bypass, N+1 queries,
  schema drift, or retry/idempotency defects rather than aggregate finding counts;
- consider model/harness version drift and workflow changes as alternative explanations;
- distinguish a useful adaptive trigger from a reviewer confirmation-bias trap;
- propose only a bounded, reversible lens, specialist route, or deterministic check whose
  marginal value can be measured against the current review path.

Do not rank authors, models, or harnesses by overall quality. A locally supported recurring
failure pattern may justify extra attention for that mechanism, not a general presumption
that code from that source is unsafe.

### 8. Form calibration hypotheses

For each observed pattern, write:

1. evidence and sample size;
2. calibrated interpretation;
3. plausible alternative explanations;
4. proposed change;
5. expected benefit and possible harm;
6. bounded evaluation or rollback plan;
7. accountable human owner needed to approve it.

Prefer reversible experiments over permanent policy changes. Examples include changing one
threshold for one repository class, adding a specialist trigger for one boundary, removing
a low-yield adaptive dimension, moving a cheap deterministic verifier earlier, narrowing an
expensive low-yield verifier to the consequence classes where it changes decisions, or
testing a heterogeneous falsifier on high-consequence changes.

### 9. Produce the calibration report

Return:

1. **Scope and evidence quality** — window, repositories, schema versions, exclusions,
   linkage confidence, and limitations.
2. **Current policy snapshot** — dimensions, thresholds, routing, reviewer topology, and
   authority boundaries.
3. **Discovery and verification-budget findings** — unique contribution, falsification,
   duplication, unknowns, marginal worker/verifier value, escapes, and measured
   cost/latency/human-attention load.
4. **Threshold and routing findings** — trigger and human-disposition patterns without
   treating either as an automatic verdict.
5. **Correlation and authoring-pattern findings** — shared assumptions, limits on
   independence, and any locally supported source-specific failure hypotheses without
   turning them into quality rankings.
6. **Calibration proposals** — structured according to the reference contract.
7. **Evaluation plan** — cohort, duration or sample target, success and harm measures,
   rollback condition, and owner.
8. **No-change conclusions** — mechanisms that should remain unchanged and the supporting
   evidence.

Lead with the highest-confidence actionable proposal, not the most dramatic metric.

## Stop conditions

Stop or narrow the conclusion when:

- revision identity cannot be established;
- review, verdict, and later-outcome records cannot be linked reliably;
- sample size is too small for the proposed generalisation;
- schema or workflow changes make cohorts materially incomparable;
- required policy, authority, or retention rules are unavailable;
- the request asks for individual performance ranking or employment judgement;
- the proposed change cannot be evaluated or reversed safely.

When evidence is insufficient, return the missing instrumentation or record fields needed
for a future calibration run. Do not recommend automatic policy changes.