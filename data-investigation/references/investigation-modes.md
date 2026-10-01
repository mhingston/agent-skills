# Investigation modes

Use only the sections relevant to the analytical brief. These modes define
different evidence contracts; they are not interchangeable labels for the same
workflow.

## Descriptive and exploratory work

Use descriptive work to establish distributions, counts, changes, segments,
relationships, and data-quality facts without claiming why they occurred.

Require:

- an explicit population, denominator, time window, and comparison basis;
- reconciled totals and row-count transitions;
- appropriate uncertainty when sampling or noisy measurement is involved;
- plots and tables whose scales, aggregation, missingness, and exclusions are
  visible;
- one question per analytical step when human interpretation determines what to
  inspect next;
- a distinction between observations discovered as planned analysis and patterns
  found through open-ended exploration.

Avoid automated plot dumps. Each view should answer a named question or test a
data-quality assumption. Treat a discovered pattern as a lead until it survives
an appropriate confirmation step.

## Diagnostic work

Diagnostic analysis asks which explanations remain plausible, not merely which
variables correlate with an outcome.

Require:

- at least one credible competing explanation when the decision is consequential;
- an observation or diagnostic that could discriminate between explanations;
- explicit treatment of timing, selection, measurement changes, reverse
  causality, common causes, and operational process changes where relevant;
- preservation of explanations the evidence cannot distinguish;
- a stop condition that permits `Inconclusive`.

Do not convert the leading narrative into a causal claim merely because it fits
the observed series or has a plausible mechanism.

## Causal work

Define the causal question before choosing an estimator:

- intervention or exposure;
- outcome;
- target population and time horizon;
- estimand, including whose effect is sought;
- assignment or exposure process;
- counterfactual and identification assumptions;
- pre-treatment covariates and prohibited post-treatment information;
- interference, anticipation, spillover, and attrition risks where material.

Choose a design from the actual assignment mechanism and data, not from method
familiarity. Depending on the case, credible evidence may use randomisation,
natural experiments, difference-in-differences, interrupted time series,
synthetic controls, matching/weighting, regression discontinuity, instrumental
variables, or a transparent statement that identification is unavailable.

Require applicable checks such as:

- pre-trend or pre-period fit;
- placebo interventions or outcomes;
- backtesting and out-of-sample counterfactual performance;
- covariate balance and overlap;
- robustness across defensible windows/specifications;
- negative controls;
- sensitivity to unmeasured confounding or alternative measurement;
- heterogeneous effects for operationally important groups.

Comparing several specifications is useful only when their assumptions and
diagnostics are visible. Do not select the specification with the preferred sign
or smallest p-value.

## Predictive work

Define the real scoring event and reproduce it in evaluation:

- what entity is scored and when;
- what information exists at that moment;
- prediction horizon and label-availability delay;
- how cases arrive over time and how repeated entities are grouped;
- who acts on the prediction and the costs of different errors.

Protect against:

- target or label proxies unavailable at scoring time;
- random splits that mix future and past when deployment is prospective;
- the same user, account, site, conversation, template, or related entity crossing
  train and evaluation boundaries;
- preprocessing, feature selection, imputation, or threshold choice fitted on
  evaluation data;
- repeated tuning against the final holdout;
- aggregate gains that conceal failure on a required slice;
- synthetic or augmented variants crossing split families.

Start with the simplest valid baseline. Report discrimination, calibration,
decision-threshold behaviour, important slice errors, uncertainty, and operational
costs appropriate to the intended use. Model development becomes `model-lab` when
the primary outcome shifts from analytical evidence to producing and selecting a
model artefact.

## Prescriptive work

Prescriptive analysis combines evidence with objectives and constraints. Keep
these layers separate:

1. observed data and descriptive facts;
2. forecasts or estimated causal effects;
3. utilities, costs, risks, fairness or policy constraints;
4. optimisation or decision rule;
5. accountable human or system authority to act.

Test a proposed policy through an appropriate simulation, off-policy evaluation,
controlled experiment, or limited pilot when historical outcomes do not establish
what the new policy will do. Report sensitivity to uncertain utilities and effect
estimates. An analytically preferred action is a recommendation, not permission to
execute it.

## Mixed investigations and mode changes

Many investigations begin descriptively and later become diagnostic, predictive,
or causal. When the mode changes:

- revise the analytical brief;
- identify the new claim and evidence contract;
- freeze exploratory findings that influenced the new hypothesis;
- create fresh confirmation evidence where needed;
- do not reuse a convenient exploratory split or specification as unbiased final
  confirmation.

If the new mode requires materially different data, authority, expertise, or
verification, stop and hand off rather than continuing under the original brief.

## Mechanism lineage

This routing and evidence model adapts mechanisms from Hugo Bowne-Anderson, Luca
Fiaschi, and Thomas Wiecki, “The Agentic Data Science Playbook,” O'Reilly Radar,
30 September 2026:
https://www.oreilly.com/radar/the-agentic-data-science-playbook/

The source is an illustrative playbook rather than causal evidence that every
mechanism transfers. This skill narrows those mechanisms to the catalogue's
existing evidence, authority, evaluation, and model-development boundaries.
