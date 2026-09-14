---
name: specialist-model-lab
description: Design and run bounded development of small, task-specific machine-learning models from task definition through dataset/model discovery, baseline training, controlled experiments, protected evaluation, Pareto selection, and packaging. Use when asked to find, train, improve, distil, quantize, or autonomously iterate a specialist model under explicit quality, latency, size, memory, or cost constraints. Do not use for ordinary LLM prompting, generic ML explanations, or one-off technical experiments whose primary outcome is evidence rather than a model.
compatibility: Requires access to a training runtime for execution, plus dataset/model registries or local data when discovery is needed. The planning path can run without training access.
---

# Specialist Model Lab

Develop the smallest well-supported specialist model that satisfies an explicit
contract. Treat model architecture, data, training recipe, compression, and the
research loop itself as hypotheses to test rather than predetermined answers.

The outcome is not "a model trained successfully". It is a reproducible evidence
package showing what was tried, what passed protected evaluation, where the
Pareto frontier lies, and whether any candidate is good enough to promote.

## Use when

Use this skill when the requested outcome is a bounded task-specific model such
as a classifier, ranker, retriever, token classifier, embedding model, anomaly
detector, or other compact specialist model, especially when the work may include:

- discovering suitable public or local datasets;
- comparing existing checkpoints and simpler non-neural baselines;
- fine-tuning, distillation, pruning, quantization, or architecture changes;
- repeated agent-driven experiments under a compute budget;
- failure-driven data improvement or synthetic-data generation;
- selecting among quality, latency, memory, size, and cost trade-offs.

## Avoid when

Do not use this skill when:

- the user primarily needs an explanation of ML concepts rather than a model;
- the task is prompt/tool/harness optimization for a general-purpose LLM;
- the question is whether one uncertain technical claim is true, with no model
  development outcome; use a bounded technical-research workflow instead;
- there is no lawful, authorised path to use the required data;
- success cannot yet be expressed as an observable task metric or deployment
  constraint;
- the requested work would expose protected evaluation examples to the optimizer.

## Core invariants

1. **Define the objective before optimizing.** Record primary metrics, hard
   constraints, tie-breakers, and budget before running experiments.
2. **Search data before committing to an architecture.** Dataset availability,
   label quality, licence, provenance, and domain fit can change the right model
   family entirely.
3. **Keep an independent protected evaluation boundary.** The optimizer may
   receive metrics and failure categories, but must not read protected examples or
   alter the oracle to improve its score.
4. **Always establish a cheap baseline.** Include a simple heuristic, linear,
   embedding, classical-ML, or small pretrained baseline when it can answer the
   task. A transformer is not automatically the default.
5. **Change one material causal hypothesis at a time when practical.** Preserve
   enough experiment identity to explain why a candidate changed.
6. **Retain negative results.** Failed experiments constrain the search space and
   must not disappear from the evidence ledger.
7. **Promote on evidence, not best-seed luck.** Confirm material gains across
   seeds, slices, or repeated runs proportionate to variance and decision impact.
8. **Prefer Pareto improvement to one scalar score.** Quality gains that violate
   deployment constraints are not wins.
9. **Bound autonomous search.** Compute, wall-clock, monetary, storage, iteration,
   and side-effect limits must be explicit.
10. **Do not claim recursive self-improvement merely because an agent iterates.**
    Reserve that claim for experiments that separately show the improvement
    process itself becomes more effective across held-out tasks.

## 1. Define the model contract

Before searching data or models, capture:

- task and input/output schema;
- intended domain, languages, populations, and operating conditions;
- primary quality metric and any class/slice-specific minimums;
- hard deployment constraints: size, memory, p95 latency, throughput, hardware,
  offline/online execution, quantization format, and dependency limits;
- acceptable training/runtime cost;
- data-handling, privacy, licensing, redistribution, and governance constraints;
- minimum evidence required to promote a candidate;
- experiment budget and stop rules.

If these are not all known, distinguish **hard constraints**, **working
assumptions**, and **unknowns**. Do not silently turn a guess into a gate.

Prefer a contract such as:

```text
Task: classify support tickets into six routing intents
Primary: macro-F1 >= 0.91 on protected evaluation
Slices: recall >= 0.85 for every production-critical class
Deployment: <= 50 MB, <= 15 ms p95 on target CPU, <= 150 MB peak RAM
Budget: <= 40 training runs or <= £25 equivalent compute
Promotion: repeated gain outside observed run-to-run noise, no hard-gate regressions
```

## 2. Discover and qualify datasets

Search appropriate sources before deciding how to train. Typical sources include:

- Hugging Face datasets and benchmark repositories;
- Kaggle and OpenML;
- task-specific academic or industry datasets;
- approved local/user-provided data;
- weakly labelled, synthetic, or programmatically generated data when justified.

For any non-trivial search or merge, read
[references/data-and-model-discovery.md](references/data-and-model-discovery.md).

For each serious candidate record at least:

- source and stable identifier/version when available;
- task and domain fit;
- example count and label distribution;
- label provenance and known quality limitations;
- licence and redistribution/training constraints;
- language, temporal, geographic, or population coverage that may matter;
- duplication, contamination, PII, safety, or benchmark-leakage risks;
- access requirements and download/processing cost.

Rank datasets by fitness for the declared contract, not popularity. If no dataset
is adequate, return a data-acquisition plan rather than forcing model training.
That plan may combine human-labelled seeds, approved local data, weak supervision,
active learning, or synthetic data, but must preserve an independently sourced or
human-verified evaluation boundary.

## 3. Establish the evaluation boundary

Before optimizing, define:

- train split;
- development/validation split visible to the experiment loop;
- protected evaluation split unavailable to the optimizer except through bounded
  metrics or predeclared aggregate failure categories;
- contamination/duplicate checks across splits;
- task metrics, slice metrics, calibration/threshold metrics when relevant;
- target-device latency, memory, package-size, and throughput measurements;
- repeated-run or seed policy when stochastic variance can change the decision.

Do not synthesize the protected set from the same generator used to produce
training data unless an independent source demonstrates that this is valid for
this task. Do not tune thresholds, labels, exclusions, or metrics after seeing a
candidate's protected results merely to make the candidate pass.

Use [references/model-evaluation.md](references/model-evaluation.md) when defining
splits, promotion gates, robustness slices, variance treatment, or Pareto
selection.

## 4. Discover candidate solution families

Search existing model registries and known lightweight approaches. Include both
pretrained specialists and general foundations that can be adapted, but do not
assume an encoder or transformer is required.

Candidate families may include:

- rules or deterministic recognizers;
- linear/classical models over lexical, n-gram, or engineered features;
- embedding plus nearest-neighbour or shallow classifier;
- compact CNN/RNN architectures where appropriate;
- small encoder models such as ModernBERT-, DeBERTa-, MiniLM-, or similar
  families;
- existing task-specific checkpoints with compatible licences;
- small generative models only when the output contract actually requires
  generation.

Record model licence, parameter count, context/input limits, expected deployment
format, hardware fit, training artefact availability, and whether the published
checkpoint is actually suitable for further training rather than inference only.

Prefer the simplest candidate that can plausibly meet the contract.

## 5. Establish baselines

Run the cheapest meaningful baselines before autonomous search. At minimum,
compare against:

- a trivial/majority/random baseline where informative;
- the strongest cheap non-neural or shallow baseline that fits the task;
- an off-the-shelf pretrained model without elaborate optimization when one is a
  credible candidate.

A sophisticated experiment earns its cost only if it can beat or materially
improve the trade-off against these baselines.

## 6. Run bounded experiments

For each experiment record:

- experiment ID and parent candidate/lineage;
- hypothesis;
- one primary change or intentionally coupled change set;
- code/config revision;
- dataset fingerprints and split identities;
- base model/checkpoint identity;
- random seed and dependency/runtime versions;
- hardware and precision;
- training budget and observed duration/cost;
- development and protected metrics that the boundary permits;
- target-device measurements;
- outcome: `promote`, `retain-on-frontier`, `reject`, `inconclusive`, or `blocked`;
- why the result changed the next experiment.

An autonomous loop may propose edits to data sampling, augmentation, loss,
hyperparameters, architecture, distillation, quantization, or training code, but
it may not alter protected evaluation examples or gates unless the model contract
is explicitly reopened by the accountable operator.

Use a bounded loop:

```text
observe frontier and failures
→ form one decision-bearing hypothesis
→ make the smallest experiment
→ train/evaluate
→ compare against baseline + frontier
→ retain evidence
→ promote, branch, or reject
→ stop when a declared bound is reached
```

Keep multiple useful lineages when different trade-offs may later become valuable.
Do not overwrite history with a single "latest" model.

## 7. Improve data from failures

When error analysis points to a data gap, classify it before adding examples:

- missing class/phenomenon coverage;
- domain or language mismatch;
- ambiguous or inconsistent labels;
- long-tail rarity;
- adversarial/robustness gap;
- temporal drift;
- preprocessing/tokenization failure;
- model-capacity or objective failure that more data is unlikely to fix.

Only then choose among retrieval of additional public data, human labelling,
active learning, weak supervision, augmentation, or synthetic generation.

Keep generated data marked as generated, preserve generator/prompt/version
provenance, deduplicate against protected data, and validate a sample independently
before allowing it to dominate training.

## 8. Select the Pareto frontier

Compare candidates on the dimensions that matter to the contract, typically:

- primary quality and critical-slice quality;
- calibration or confidence quality when operational decisions use probabilities;
- p50/p95 latency and throughput on target hardware;
- peak memory;
- package/model size;
- training and inference cost;
- robustness under declared perturbations or domain slices.

Retain non-dominated candidates rather than collapsing everything into one
arbitrary weighted score. Choose one default winner only when the contract gives a
clear ordering or an accountable operator chooses the trade-off.

## 9. Promotion and stop rules

Stop experimentation when any declared bound is reached, including:

- compute, money, wall-clock, storage, or experiment-count budget exhausted;
- a candidate satisfies all gates and additional optimization has low expected
  value;
- N consecutive experiments fail to improve the Pareto frontier;
- observed improvement is within measurement/run-to-run noise;
- required data cannot be licensed, accessed, or handled safely;
- protected evaluation or a critical slice materially regresses;
- improvement appears only on one seed/run and does not reproduce;
- the next experiment requires changing the product/task contract rather than the
  model.

Do not move a gate because the current model misses it. Reopen the contract as a
separate decision with the reason and owner visible.

## 10. Optional self-improvement research mode

Only after the ordinary loop is stable may the experiment examine whether the
**research process** itself can improve. Treat the research strategy, hypothesis
selection policy, curriculum generator, or experiment scheduler as another
candidate artefact.

To claim improvement of the improver:

- evaluate old versus new research policy on multiple held-out task instances or
  model-development problems;
- fix or independently govern the meta-evaluation budget and oracle;
- compare downstream frontier improvement, experiment efficiency, or success
  probability rather than eloquence of research notes;
- retain failed policy variants and test against benchmark/reward exploitation;
- avoid claiming recursive self-improvement from one successful lineage.

This mode is optional research, not required for useful specialist-model
development.

## Output contract

Return or persist a compact lab report containing:

1. **Status** — `Ready`, `Running`, `Candidate`, `No-go`, or `Blocked`.
2. **Model contract** — task, metrics, hard constraints, assumptions, budget, and
   stop rules.
3. **Data inventory** — ranked candidate datasets, provenance/licence risks, and
   selected training/evaluation sources.
4. **Evaluation contract** — split identities, protected boundary, metrics,
   slices, target hardware, and promotion criteria.
5. **Candidate inventory** — baselines and model families considered, including
   why apparently obvious choices were rejected.
6. **Experiment ledger** — reproducible run identities, hypotheses, changes,
   metrics, failures, cost, and disposition.
7. **Pareto frontier** — non-dominated candidates and their trade-offs.
8. **Recommendation** — promote one candidate, retain several variants, acquire
   better data, change the task contract, or stop.
9. **Reproduction package** — exact code/config revision, dataset/model
   identifiers, seeds, dependencies, commands or scripts, and exported artefacts
   required to rerun the selected result.

## Quality gate

Before declaring a candidate ready, verify that:

- success criteria and deployment constraints were declared before optimization;
- dataset/model discovery was not skipped merely because a preferred architecture
  was named up front;
- licences, provenance, privacy, and redistribution constraints are known enough
  for the intended use;
- a protected evaluation boundary exists and the optimizer could not inspect its
  examples;
- at least one cheap baseline was measured when applicable;
- the candidate improvement is reproducible at the strength required by observed
  variance;
- protected and critical-slice regressions are visible;
- target-device resource measurements were actually observed rather than inferred
  from parameter count;
- experiment lineage and negative results are preserved;
- the winner is Pareto-justified against the declared contract;
- stop rules prevented unbounded search;
- any self-improvement claim is narrower than the evidence and separately tests
  the improvement process itself.

When evaluating changes to this skill, use the behavioural cases in
[references/skill-evaluation.md](references/skill-evaluation.md) with the matched
baseline/candidate process owned by `skill-creator`.
