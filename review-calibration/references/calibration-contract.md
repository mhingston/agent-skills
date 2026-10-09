# Review calibration contract

## Principle

Calibration proposes bounded, evidence-backed policy experiments. It never changes policy
or converts historical correlations into approval rules.

## Minimum evidence ledger

Use one review-level record per exact head revision:

```json
{
  "repository": "owner/repository",
  "head_sha": "40-character SHA",
  "review_schema_version": 2,
  "task_family": null,
  "accepted_contract": null,
  "scoped_standards": [],
  "first_pass": null,
  "review_coverage": null,
  "reviewed_at": "RFC-3339 timestamp",
  "consequence_risk": "moderate",
  "comprehension_risk": "high",
  "dimensions": ["correctness", "security"],
  "reviewer_provenance": {
    "execution_mode": "parallel-independent-contexts",
    "models": ["model identifier when available"],
    "shared_prompt_family": true,
    "shared_evidence_packet": true,
    "independent_falsifier": true,
    "correlation_limitations": ["same model family"]
  },
  "calibration_receipt": {
    "candidate_findings": 8,
    "validated_findings": 3,
    "falsified_findings": 4,
    "inconclusive_findings": 1,
    "deduplicated_findings": 1,
    "measured_latency_seconds": null,
    "measured_cost": null
  },
  "risk_ids": ["RISK-1"],
  "design_redirect_ids": [],
  "verdict_record": "reference or null",
  "later_outcomes": []
}
```

Use `null` or omit optional measured fields when unavailable. Never estimate model cost,
latency, candidate counts, or outcome linkage merely to complete the structure.

### Optional upstream-prevention extensions

Use these review-level fields only when evaluating whether approved scoped
standards prevent mistakes before first independent review:

- `task_family`: evidence-backed comparable behavioural/contract class.
- `accepted_contract`: stable task/source ID, approved revision, scope, and
  independent acceptance oracle reference.
- `scoped_standards`: source ID/revision, independent authority evidence,
  effective-at-attempt scope, and discrepancies between worker/reviewer receipts.
- `first_pass`: first attempt/run ID, first-implementation and first-review
  exact SHAs, independent pass/fail/unknown result and evidence reference,
  oracle revision, and number of subsequent remediation rounds.
- `review_coverage`: effective review policy revision, selected dimensions,
  verifier identities and observation/instrumentation revision.

Illustrative values, not facts that may be filled from guesswork:

```json
{
  "task_family": "legacy API response compatibility",
  "accepted_contract": {
    "source_id": "PAY-123",
    "source_revision": "ticket-v5",
    "applicable_scope": "legacy callers",
    "oracle_ref": "contract-tests-v2"
  },
  "scoped_standards": [{
    "source_id": "docs/contracts/customer-api.md",
    "source_revision": "approved-v3",
    "authority_evidence": "owner approval at v3",
    "applicable_scope": "legacy callers",
    "effective_at_attempt": true
  }],
  "first_pass": {
    "attempt_id": "workflow run ID",
    "attempt_head_sha": "initial SHA",
    "reviewed_head_sha": "initial reviewed SHA",
    "independent_outcome": "fail",
    "outcome_evidence": "test or review receipt",
    "oracle_revision": "contract-tests-v2",
    "remediation_rounds": 1
  },
  "review_coverage": {
    "policy_revision": "review-v2",
    "dimensions": ["correctness", "security"],
    "verifier_profile": "tests-v3",
    "capture_revision": "log-v4"
  }
}
```

Link first attempts to reviews and subsequent remediation by stable run/task
identity **and exact revision**, never PR titles, authors, temporal proximity
or model similarity. Count one initial attempt per task, not each remediation
round. Confirm that standards were approved and effective at the time of that
attempt; candidate-edited approval metadata is not authority. Compare cohorts
only with compatible accepted intent, consequence/complexity, independent
oracles, and review/capture coverage. Report `pass`, `fail`, `unknown`,
and excluded counts and denominators. Do not silently drop missing outcomes.
Changed reviewers/checks/task mix can explain fewer comments without prevention;
when linkage is insufficient, report `indeterminate` and recommend a bounded
prospective matched evaluation instead of a causal historical conclusion.

Use one risk-level record when analysing thresholds and human dispositions:

```json
{
  "repository": "owner/repository",
  "head_sha": "40-character SHA",
  "risk_id": "RISK-1",
  "dimension": "data integrity and migration safety",
  "severity": "major",
  "likelihood": "medium",
  "confidence": "high",
  "policy_threshold": "major",
  "threshold_result": "exceeded",
  "technical_disposition": "remediate-before-merge",
  "human_disposition": "remediated",
  "human_rationale_category": "confirmed failure path",
  "specialist_review": null,
  "later_outcome": null,
  "outcome_linkage_confidence": "not-applicable"
}
```

Do not copy private human rationale into a broad calibration dataset when a bounded
category is sufficient.

## Metric definitions

### Candidate validation rate

`validated_findings / candidate_findings`

Use only when candidate collection was recorded consistently. A higher value is not
necessarily better: it may indicate weak falsification or conservative candidate creation.

### Falsification yield

`falsified_findings / candidate_findings`

Interpret with the evidence checked and candidate-generation policy. High yield may mean
valuable suppression or noisy originating passes.

### Unique dimension contribution

Count validated risk root causes attributable to a dimension that were not independently
recovered by another dimension or deterministic check. Do not count duplicate wording as
unique contribution.

### Human rejection pattern

Count risks disposed as `rejected-as-unsupported`, grouped by evidence failure, policy
mismatch, duplicate root cause, missing context, or other stated rationale. Do not assume
the human was correct without checking later evidence.

### Escape alignment

A later defect aligns to a review gap only when:

1. the exact shipped or reviewed revision is known;
2. the causal mechanism is established;
3. the relevant evidence was within review scope or reasonably obtainable;
4. the defect maps to a missing, ineffective, or unresolved review question.

Label weaker associations `temporal-only` or `plausible`, not confirmed.

### Marginal worker value

A worker, model, specialist, or tool contributes marginal value when removing its unique
validated evidence would materially change the final risk map, specialist routing,
design redirect, or named unknown. Restated findings do not count.

### Cost, latency, and human attention

Use measured values only. Compare them within equivalent consequence-risk cohorts and
workflow versions. Human-attention cost may be measured as review/interpretation time,
handoff count, or another explicitly observed burden; do not invent a proxy when it was
not captured. Do not trade away required safety evidence solely to reduce averages.

### Marginal verifier value

A verifier contributes marginal value when its removal would materially reduce
decision-relevant evidence for the same consequence-risk cohort: for example by losing a
unique failure mechanism, independent confirmation, specialist interpretation, runtime
observation, or a materially earlier fail-fast signal.

Evaluate a verifier against the rest of the portfolio, not in isolation. Record, when
available:

- verifier/check identity and stage;
- claim or failure class covered;
- unique evidence contribution;
- correlation with other evidence sources;
- measured cost and latency;
- observed human-attention demand;
- whether the verifier changed the risk map, disposition, named unknown, or time-to-failure.

Do not equate finding count with verifier value. A zero-finding check may still be
load-bearing evidence, while a noisy check that produces many restatements may have little
marginal value.

### Verification budget

A verification budget is an explicit envelope for cost, latency, and human attention used
to choose the smallest evidence portfolio that remains sufficient for the applicable
consequence, uncertainty, and policy requirements.

Calibration may propose reordering, narrowing, replacing, or removing verification only
when the experiment preserves mandatory evidence and names the expected signal retained.
If the required evidence cannot fit the available budget, report a capacity or policy
conflict; do not weaken the required evidence to make the budget pass.

## Proposal schema

Every proposal uses this shape:

```json
{
  "proposal_id": "CAL-1",
  "title": "Test heterogeneous falsification for high-consequence changes",
  "evidence": {
    "cohort": "24 high-consequence reviews",
    "observations": ["..."],
    "limitations": ["..."]
  },
  "interpretation": "Calibrated explanation",
  "alternatives": ["Another plausible explanation"],
  "change": {
    "policy_surface": "reviewer topology",
    "current": "same model family",
    "proposed": "different model family for falsification only",
    "scope": "high-consequence changes touching trust or persistence boundaries"
  },
  "expected_benefit": "More assumption diversity during finding challenge",
  "possible_harms": ["latency", "inconsistent tool access"],
  "evaluation": {
    "cohort_or_sample_target": "next 20 eligible reviews",
    "success_measures": ["unique invalidations", "changed risk-map outcomes"],
    "harm_measures": ["added latency", "unsupported contradictions"],
    "rollback_condition": "No material marginal value after target cohort"
  },
  "authority_required": "Named policy owner",
  "status": "proposed"
}
```

Allowed `status` values are `proposed`, `approved-for-experiment`, `rejected`, and
`adopted`. The calibration skill emits only `proposed` unless it is faithfully recording
an explicit human decision.

## Reporting rules

- Show counts and denominators together.
- State schema and workflow versions for every cohort.
- Separate confirmed outcome links from plausible or temporal associations.
- Include no-change conclusions where evidence supports the current mechanism.
- Name missing instrumentation instead of filling gaps with model judgement.
- Keep proposals reversible, scoped, measurable, and human-owned.