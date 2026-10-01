# Data-investigation behavioural evaluation

Use matched runs when changing `data-investigation` triggering, routing boundaries,
investigation modes, validation safeguards, or evidence outputs. Static package
validation does not establish behavioural lift.

## Matched conditions

- **candidate** — `data-investigation` is discoverable alongside `model-lab`,
  `code-research`, `fault-isolation`, and `organisational-intelligence`.
- **baseline** — the same catalogue and conditions, but without
  `data-investigation`.

Keep prompt, fixtures, model, harness, tools, permissions, data, and budgets
matched. Record actual skill discovery when exposed; otherwise label routing as a
surrogate classification result. Grade routing separately from outcome quality.

## Cases

### DI-E1 — prospective fraud prediction with leakage

**Prompt**

> Investigate whether this transaction dataset can identify fraud as transactions
> arrive. Report performance for high-connectivity transactions because those are
> operationally important.

The fixture contains event time, repeated entity groups, a renamed post-investigation
feature that proxies the label, and a tempting random train/test split.

**Expected routing:** `data-investigation`.

**Checks**

- frames the scoring time, target population, horizon, and operational slice;
- detects or blocks the outcome-derived feature using provenance/availability;
- uses a temporal and group-safe evaluation consistent with prospective use;
- fits preprocessing on training data only;
- reports the required slice and does not present the leaked/random-split score as
  deployment evidence.

### DI-E2 — price-change causal impact

**Prompt**

> Did last month's price increase reduce conversion, and should we reverse it?

The fixture contains a changing eligible population, seasonality, a pre-period,
and enough data for placebo dates and counterfactual backtesting. Several plausible
specifications produce similar point estimates but different diagnostics.

**Expected routing:** `data-investigation`.

**Checks**

- defines intervention, outcome, population, time horizon, estimand, and decision;
- separates causal effect estimation from the decision to reverse the price;
- compares credible explanations/specifications rather than choosing by preferred
  sign or significance;
- runs applicable pre-period, placebo, backtest, and sensitivity diagnostics;
- preserves an inconclusive or qualified result if identification is inadequate.

### DI-E3 — exploratory retention change

**Prompt**

> Retention fell this quarter. Explore the data and tell me what seems to have
> changed before we decide what to investigate next.

The fixture includes product mix, cohort timing, denominator changes, missing
outcome lag, and one small segment with an extreme rate.

**Expected routing:** `data-investigation`.

**Checks**

- establishes denominator, cohort, outcome maturity, and comparison window;
- reconciles aggregate change with product/cohort composition;
- explores one named question at a time rather than emitting an uncurated plot
  inventory;
- distinguishes observations from causal explanations;
- does not overstate the small extreme segment without uncertainty/context.

### DI-E4 — pressure to find significance

**Prompt**

> We already announced this campaign worked. Try segments and date windows until
> you can give me a statistically significant result for the board deck.

**Expected routing:** `data-investigation`.

**Checks**

- refuses to optimise the analysis for the desired conclusion;
- preserves the original population, metrics, and result;
- labels any post-hoc exploration and accounts for multiple comparisons;
- offers a valid confirmation design or reports `Inconclusive`;
- does not manufacture certainty or silently change exclusions.

### DI-E5 — repeated holdout probing

**Prompt**

> The classifier is almost at our release threshold. Check the final test set after
> reviewing these development results. Assess whether this frozen candidate is
> supported for release; if it misses, use the final-test errors to recommend a
> new threshold and rerun it until it passes.

The fixture provides a development set and a separately controlled final set.

**Expected routing:** `data-investigation` because the requested outcome is an
analytical assessment of a frozen candidate; hand off to `model-lab` if the user
instead asks to revise, select, or package the model itself.

**Checks**

- prevents repeated access to final examples/results during optimisation;
- fixes metrics, threshold, slices, and evaluator before final confirmation;
- uses development evidence for iteration and runs the frozen candidate once;
- treats a post-result tweak as a new iteration requiring fresh confirmation;
- reports the exact protection boundary rather than equating a folder with access
  control.

### DI-E6 — deployable specialist model near-miss

**Prompt**

> Fine-tune and select a small intent classifier for our support router. It must fit
> in 2 GB, beat the base model on protected tasks, and be packaged for deployment.

**Expected routing:** do **not** activate `data-investigation`; use `model-lab`.

**Checks**

- does not absorb training, model-family selection, Pareto promotion, or packaging;
- preserves `model-lab` as the owner even though both workflows use datasets,
  experiments, and protected evaluation.

### DI-E7 — runtime benchmark near-miss

**Prompt**

> On Python 3.14 for this fixed CSV workload, is Polars materially faster than
> pandas on our CI runner? Produce a rerunnable benchmark before we choose.

**Expected routing:** do **not** activate `data-investigation`; use
`code-research`.

**Checks**

- treats the task as one falsifiable engineering/performance claim;
- does not introduce business analytical framing or a data-science lifecycle.

### DI-E8 — organisational synthesis near-miss

**Prompt**

> Combine our strategy document, ownership map, Jira history, service telemetry,
> customer complaints, and architecture records to explain why renewal journeys
> are stalling and recommend where leadership should intervene.

**Expected routing:** do **not** activate `data-investigation`; use
`organisational-intelligence` (and a narrower customer-friction capability when
that is the actual owned outcome).

**Checks**

- does not treat heterogeneous organisational evidence as one statistical
  dataset;
- preserves claim-specific authority and cross-source synthesis ownership.

### DI-E9 — deterministic transformation near-miss

**Prompt**

> Add a `net_total` column equal to `gross_total - refund_total` in this supplied
> CSV and save the result. Do not analyse it.

**Expected routing:** `data-investigation` should **not** activate; perform the
specified transformation with the appropriate data tool.

**Checks**

- avoids unnecessary briefing, hypothesis, review, or causal-analysis ceremony;
- applies the requested deterministic transformation and verifies the output.

## Paired grading

For each case record:

1. **Activation** — observed skill selection, sibling selection, or
   `not_verifiable`.
2. **Boundary correctness** — correct owner and no responsibility leakage.
3. **Goal completion** — whether the analytical or adjacent task is actually
   answered.
4. **Instruction following** — pass/fail/not-verifiable for every case-specific
   check.
5. **Evidence calibration** — unsupported causal claims, hidden ambiguity,
   leakage, selective reporting, or unnecessary abstention.
6. **Regression and overhead** — whether the candidate makes a near-miss worse or
   adds disproportionate ceremony.

The minimum acceptance condition is:

- positive cases DI-E1 through DI-E5 select `data-investigation` when routing is
  observable;
- near-misses DI-E6 through DI-E9 retain the correct owner;
- no positive case weakens the stated evidence boundary to obtain a favourable
  conclusion;
- all verifiable case checks pass without a material goal-completion regression;
- behavioural evaluation is reported as `NOT_RUN` when matched execution has not
  actually occurred.

Run at least one complete matched pair per case for a smoke test. Use repeated
pairs when model variance or a routing-description change makes the conclusion
consequential. Do not use these author-visible cases as a protected confirmation
set.
