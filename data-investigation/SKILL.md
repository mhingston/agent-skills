---
name: data-investigation
description: Conduct reproducible, decision-relevant investigations of datasets through explicit analytical framing, qualified data semantics, appropriate descriptive, diagnostic, causal, predictive, or prescriptive methods, bounded iteration, and independent claim review. Use when the primary outcome is an evidence-backed conclusion or recommendation from data, including exploratory analysis, KPI changes, experiment interpretation, causal-impact questions, or predictive evidence. Do not use when the primary outcome is a trained or adapted model (`model-lab`), an isolated software/runtime claim (`code-research`), a concrete defect diagnosis (`fault-isolation`), broad cross-system organisational synthesis (`organisational-intelligence`), or validated customer-journey friction across mixed customer and operational evidence (`customer-friction-radar`).
---

# Data Investigation

Turn a consequential question about data into a reproducible investigation whose
claims another analyst or agent can inspect, rerun, and challenge.

The outcome is not a persuasive notebook or a collection of plots. It is a
decision-relevant conclusion calibrated to the available evidence, together with
the analytical trail needed to determine why that conclusion should be trusted.

## Core invariants

1. **Frame the decision before choosing a method.** Record the question, intended
   use, population, outcome, constraints, and evidence required before optimising
   an analysis.
2. **Preserve the possibility of an inconclusive result.** Never reinterpret the
   assignment as finding an effect, a useful segment, or a winning model.
3. **Qualify meaning before calculation.** Establish source authority, grain,
   eligibility, time semantics, availability, joins, and material limitations.
4. **Do not silently change the question.** Changes to the population, target,
   metric, observation window, exclusions, or intended use require an explicit
   brief revision.
5. **Match validation to intended use.** A random split, convenient metric, or
   aggregate result is not valid merely because it produces a strong score.
6. **Keep evaluation independent from optimisation.** The investigator may use
   development feedback, but must not read protected examples, weaken the oracle,
   or repeatedly probe a final holdout.
7. **Separate association, prediction, and causation.** Predictive usefulness does
   not establish a causal mechanism or intervention effect.
8. **Retain negative evidence.** Failed hypotheses, unsuitable analyses, rejected
   specifications, and contradictory diagnostics constrain the conclusion.
9. **Preserve human judgement.** An agent can explore, analyse, and challenge; an
   accountable person owns consequential interpretation and action.
10. **Respect data authority and access.** Use only authorised data and tools,
    minimise sensitive exposure, and do not infer permission from technical reach.

## Route adjacent work

Use this skill when the requested outcome is a supported analytical claim,
comparison, explanation, or recommendation.

Prefer another workflow when the primary outcome is:

- a task-specific model, fine-tuned checkpoint, deployment candidate, or Pareto
  model selection: use `model-lab`;
- one falsifiable engineering claim about a runtime, library, compatibility, or
  performance property: use `code-research`;
- the causal mechanism of a concrete software defect or regression: use
  `fault-isolation`;
- a decision brief assembled from policies, tickets, conversations, architecture,
  telemetry, and other heterogeneous organisational evidence: use
  `organisational-intelligence`;
- identifying, validating, or explaining customer-journey friction across
  reviews, complaints, assisted-service interactions, digital telemetry, and
  operational signals: use `customer-friction-radar`;
- a deterministic transformation, lookup, or already-specified report with no
  material analytical judgement: execute it directly with the appropriate data
  or spreadsheet tool.

If an investigation shows that building a model is the next outcome, hand the
qualified task, data constraints, baselines, and evaluation contract to
`model-lab`. Do not silently turn exploratory evidence into a production model.

A bounded statistical question may support a customer-friction investigation,
but `data-investigation` does not own the journey-level theme, triangulation, or
friction brief.

## 1. Establish the analytical brief

Agree the smallest useful brief before substantial exploration:

- question and decision or action the answer could inform;
- intended user and operational use;
- unit of analysis, target population, eligibility, geography, and time window;
- outcome, exposure, treatment, prediction target, or KPI as applicable;
- important slices, error costs, harms, or constraints;
- information available at the time the real decision would be made;
- what the investigator may choose and what requires escalation;
- deliverables, evidence strength, budget, and stop condition;
- conditions under which `inconclusive` or `blocked` is the correct result.

Distinguish supplied facts, working assumptions, and unresolved decisions. Ask
only questions that can materially change the estimand, method, validity, or use
of the result. If the available evidence cannot answer the question, say so rather
than quietly substituting an easier one.

## 2. Qualify the data and its meaning

Create compact data notes covering each material source:

- stable identity, version, snapshot, query, or retrieval time;
- authoritative owner and what the source can or cannot establish;
- table/file grain, keys, cardinality, and expected row counts;
- population construction, eligibility rules, filters, and exclusions;
- timestamp meaning, event order, latency, and information-availability time;
- target/label provenance and whether it can contain outcome-derived information;
- join logic, duplicate handling, missingness, censoring, and survivorship risks;
- definition or instrumentation changes over the analysis window;
- privacy, consent, licensing, retention, residency, and access constraints;
- unresolved semantic or quality questions and their likely effect.

Inspect actual distributions and join results rather than trusting column names or
schemas alone. Treat unexplained row loss, many-to-many expansion, post-outcome
features, and unknown metric definitions as validity risks. Block or qualify the
claim when the missing meaning could reverse it.

## 3. Select the investigation mode

Classify the question before selecting methods:

- **descriptive** — what happened or what is present;
- **diagnostic** — which explanations are consistent with the observations;
- **causal** — what effect an intervention or exposure had or would have;
- **predictive** — what can be forecast or classified at a defined decision time;
- **prescriptive** — which action is preferable under explicit objectives and
  constraints.

Read [references/investigation-modes.md](references/investigation-modes.md) for the
selected mode. Use more than one mode only when the handoff between them is
explicit. Do not let descriptive exploration inherit predictive or causal claims.

## 4. Define the analysis and verification contract

Before a long or adaptive investigation, record:

- claims or competing explanations under consideration;
- baseline, counterfactual, comparator, or null expectation;
- primary and secondary metrics, uncertainty treatment, and important slices;
- sampling, split, preprocessing, exclusion, and multiple-comparison rules;
- diagnostics, negative controls, sensitivity checks, or falsifiers;
- what the agent may change during iteration;
- fixed evaluator or review criteria it may not change;
- development versus final-confirmation evidence;
- compute, time, attempt, query, and cost budgets;
- escalation and stop rules.

Predeclare consequential choices where practical. If a material rule changes
after results are observed, preserve the original result and label the revised
analysis as exploratory or a new comparison epoch.

Use an actual access boundary for protected data when unbiased confirmation
matters. A different directory, branch, notebook, or fresh prompt is not by itself
protection if the investigator can still read the data or prior result.

## 5. Rehearse the evidence path

Run the cheapest end-to-end baseline before authorising extensive exploration:

1. load the approved data snapshot;
2. reproduce population and row-count checks;
3. execute the simplest valid baseline analysis;
4. verify time ordering, feature availability, splits, and preprocessing;
5. produce at least one required slice or diagnostic;
6. confirm that code, environment, outputs, and assumptions are preservable.

Distinguish setup failure, data-semantic failure, and analytical failure. Resolve
the evidence path before spending a larger experiment budget.

## 6. Execute a bounded investigation

Choose the loop that fits the question:

- For exploratory descriptive work, answer one decision-relevant question or
  render one interpretable view at a time, inspect it, then choose the next step.
- For predictive optimisation, use a bounded hypothesis -> change -> development
  evaluation -> keep/reject loop against a fixed contract.
- For diagnostic or causal work, compare plausible explanations or specifications
  and require discriminating diagnostics rather than selecting the most appealing
  narrative.
- For prescriptive work, keep predictions, causal assumptions, utilities, costs,
  constraints, and decision authority separate.

For every material attempt record:

- attempt ID and hypothesis;
- data snapshot, code/config revision, environment, and seed where relevant;
- change from the baseline or parent attempt;
- metrics, uncertainty, slices, and diagnostics;
- anomalies, failed checks, and contradictory evidence;
- disposition: `retain`, `reject`, `inconclusive`, or `blocked`;
- why the result changes or does not change the next step.

Stop when the brief is answered strongly enough for its intended decision, a
declared budget is exhausted, evidence is irreducibly ambiguous, validity fails,
or the next step requires a human-owned decision. More analysis is not stronger
evidence when it repeatedly searches the same noise.

## 7. Review the claim independently

Freeze the selected analysis before final confirmation. Read
[references/independent-review.md](references/independent-review.md) when the
conclusion is consequential, iteration was adaptive, causality is claimed, or an
independent reviewer is requested.

At minimum, verify that:

- the conclusion answers the agreed question and population;
- decisive computations and diagnostics rerun from recorded inputs;
- preprocessing and feature availability respect decision time;
- the evaluation design matches intended use;
- uncertainty, slice failures, negative evidence, and alternative explanations
  remain visible;
- the final claim is no stronger than the evidence;
- any untouched or protected final evaluation is run once against the frozen
  candidate and reported without post-hoc gate changes.

Reviewer agreement is not independent evidence unless the reviewer inspects or
reruns the material artefacts.

## 8. Conclude and preserve the evidence

Return a result with one of these statuses:

- `Supported` — evidence supports the bounded claim for the stated use;
- `Qualified` — useful evidence exists, but material limitations constrain use;
- `Inconclusive` — available evidence does not discriminate sufficiently;
- `Blocked` — missing data, meaning, authority, access, or validity prevents the
  investigation.

The evidence package must include:

1. analytical brief and any explicit revisions;
2. data identities, semantics, lineage, and access limitations;
3. analysis/evaluation contract;
4. baseline and experiment or analysis ledger;
5. code, environment, commands, and generated artefacts required to rerun;
6. decisive results, uncertainty, slices, and diagnostics;
7. failed alternatives and unresolved contradictions;
8. independent-review or final-confirmation evidence when performed;
9. conclusion, limits, operational implications, and accountable next decision.

Prefer runnable artefacts over a transcript describing what the agent says it did.
Do not persist sensitive data merely to make the package self-contained; preserve
authorised stable references and reproduction instructions instead.

## 9. Carry lessons forward selectively

Keep assignment-specific definitions and exceptions in the project context. A
recurring, reviewed methodological failure may become a scoped skill rule or
evaluation case only after evidence shows that it generalises.

Record the triggering context, observed failure, desired invariant, scope, and a
case that can test the behaviour. Route longitudinal qualification and skill
change through the appropriate learning and skill-authoring workflows. Do not let
the investigating agent rewrite its own guidance or evaluator as proof of
improvement.

## Quality gate

Before returning, verify that:

- the question, intended use, population, and decision time are explicit;
- material data meaning and provenance are established or reported as blockers;
- the selected mode and validation design match the question;
- target, temporal, group, preprocessing, and synthetic-family leakage were
  considered where relevant;
- causal language is supported by a causal design rather than association alone;
- adaptive iteration is bounded and final confirmation is independent;
- failed analyses and negative diagnostics remain visible;
- the result can be rerun from stable identities and instructions;
- status and confidence do not exceed the evidence;
- the skill did not deploy a model, change policy, or take the downstream
  operational decision.

Use [references/evaluation-suite.md](references/evaluation-suite.md) when changing
this skill's trigger, boundaries, investigation modes, or evidence contract.
