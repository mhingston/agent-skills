---
name: model-lab
description: Design and run bounded development, fine-tuning, and adaptation of task-specific machine-learning models, including large generative LLMs, from data discovery and training-data preparation through controlled experiments, protected evaluation, Pareto selection, and packaging. Use when asked to find, train, fine-tune, distil, align, quantize, or autonomously iterate a model under explicit quality, latency, size, memory, cost, or deployment constraints, including training from verified agent traces. Do not use for ordinary LLM prompting, generic ML explanations, or one-off technical experiments whose primary outcome is evidence rather than a model.
compatibility: Requires access to an appropriate local or managed training runtime for execution, plus dataset/model registries or local data when discovery is needed. The planning path can run without training access.
---

# Model Lab

Develop or adapt the simplest well-supported model that satisfies an explicit
contract. The right answer may be a small classifier, an encoder, a distilled
model, or a much larger generative LLM fine-tuned through a managed service.
Treat model family, data, training recipe, adaptation method, runtime, compression,
and the research loop itself as hypotheses to test rather than predetermined
answers.

The outcome is not "a model trained successfully". It is a reproducible evidence
package showing what was tried, what passed protected evaluation, where the
Pareto frontier lies, and whether any candidate is good enough to promote.

## Use when

Use this skill when the requested outcome is a bounded task-specific model or an
adapted foundation model, including:

- classifiers, rankers, retrievers, token classifiers, embedding models, anomaly
  detectors, and compact specialist models;
- generative language models that need supervised fine-tuning, preference
  optimization, reinforcement fine-tuning, distillation, or domain adaptation;
- models trained from approved conversation logs, tool-use transcripts, or agent
  execution traces;
- local training as well as managed cloud training such as Microsoft Foundry,
  Azure Machine Learning, or another provider;
- repeated agent-driven experiments under a compute or monetary budget;
- failure-driven data improvement, active learning, synthetic data, compression,
  quantization, or deployment optimization.

## Avoid when

Do not use this skill when:

- the user primarily needs an explanation of ML concepts rather than a model;
- the task is only prompt/tool/harness optimization for a general-purpose LLM;
- the question is whether one uncertain technical claim is true, with no model
  development outcome; use a bounded technical-research workflow instead;
- raw traces, logs, or corpora cannot lawfully or safely be used for training;
- success cannot yet be expressed as an observable task metric or deployment
  constraint;
- the requested work would expose protected evaluation examples to the optimizer.

## Core invariants

1. **Define the objective before optimizing.** Record primary metrics, hard
   constraints, tie-breakers, and budget before running experiments.
2. **Qualify training data before training.** Dataset availability, trace quality,
   label provenance, licence, privacy, contamination, and domain fit can change the
   appropriate training method or make training unjustified.
3. **Do not train blindly on raw agent traces.** Transform traces into explicit
   training examples, preference pairs, or reward-bearing trajectories using
   observable evidence about quality and outcome.
4. **Keep an independent protected evaluation boundary.** The optimizer may
   receive bounded metrics and failure categories, but must not read protected
   examples or alter the oracle to improve its score.
5. **Compare against an appropriate baseline.** For fine-tuning, the untouched base
   model with the same harness, tools, prompts, and budget is normally the minimum
   baseline. Include simpler model families where they can answer the task.
6. **Choose the adaptation method from the evidence.** SFT, DPO/preference
   optimization, reinforcement fine-tuning, PEFT/LoRA, full fine-tuning,
   distillation, continued pretraining, and no-training baselines solve different
   problems.
7. **Change one material causal hypothesis at a time when practical.** Preserve
   enough experiment identity to explain why a candidate changed.
8. **Retain negative results.** Failed experiments constrain the search space and
   must not disappear from the evidence ledger.
9. **Promote on evidence, not one lucky run.** Confirm material gains at a strength
   proportionate to training variance, evaluation noise, and decision impact.
10. **Bound autonomous search.** Compute, wall-clock, monetary, storage, iteration,
    and external side-effect limits must be explicit.
11. **Do not claim recursive self-improvement merely because an agent iterates.**
    Reserve that claim for experiments that separately show the improvement
    process itself becomes more effective across held-out tasks.

## 1. Define the model contract

Before searching data or selecting a training method, capture:

- task and input/output contract;
- intended domain, languages, users, environments, and operating conditions;
- base model or candidate-family constraints, if any;
- primary quality metric and task/slice-specific minimums;
- agentic metrics when relevant: task completion, tool-call validity, verifier
  pass rate, recovery behaviour, action efficiency, and policy compliance;
- hard deployment constraints: provider, region, data residency, model access,
  size, memory, latency, throughput, hardware, quantization, and dependency limits;
- acceptable training and inference cost;
- data-handling, privacy, licensing, retention, redistribution, and governance
  constraints;
- minimum evidence required to promote a candidate;
- experiment budget and stop rules.

If these are not all known, distinguish **hard constraints**, **working
assumptions**, and **unknowns**. Do not silently turn a guess into a gate.

For an LLM adaptation problem, prefer a contract such as:

```text
Task: improve coding-agent success on bounded repository tasks
Primary: protected task pass rate >= base model + declared meaningful delta
Safety: no regression on policy or secret-handling checks
Agent quality: tool schema validity >= threshold; no increase in destructive actions
Deployment: managed Azure-compatible endpoint; residency and quota constraints met
Budget: fixed training spend + fixed rollout/evaluation budget
Promotion: beats untouched base model under matched harness/tools/prompts
```

## 2. Discover and qualify data

Search appropriate sources before deciding how to train. Typical sources include:

- Hugging Face datasets and benchmark repositories;
- Kaggle and OpenML where appropriate;
- task-specific academic or industry datasets;
- approved local/user-provided data;
- conversation logs, tool-use transcripts, or agent traces;
- weakly labelled, synthetic, or programmatically generated data when justified.

For public/local dataset search and model discovery, read
[references/data-and-model-discovery.md](references/data-and-model-discovery.md).

When agent traces or conversational trajectories are a material source, also read
[references/trajectory-training.md](references/trajectory-training.md).

For every serious data source record at least:

- stable source/version and provenance;
- task and domain fit;
- example/run count and distribution;
- label, preference, reward, or outcome provenance;
- licence and training/redistribution constraints;
- privacy, secrets, PII, source-code, and confidential-content risks;
- duplication, contamination, benchmark leakage, and near-duplicate task risks;
- harness/model/skill/tool versions when examples came from agent execution;
- transformations used to create the training representation.

If no source is adequate, return a data-acquisition or trace-collection plan rather
than forcing training.

## 3. Establish the evaluation boundary

Before optimizing, define:

- train split;
- development/validation split visible to the experiment loop;
- protected evaluation tasks/examples unavailable to the optimizer except through
  bounded predeclared metrics;
- grouping rules so related traces, repository tasks, conversations, users, or
  generated variants cannot leak across train/protected boundaries;
- task metrics, critical slices, safety/policy checks, and calibration where
  relevant;
- for agents, a matched execution harness, tool surface, verifier, task budget,
  and termination rules;
- deployment measurements and provider/runtime constraints;
- repeated-run/seed policy where stochasticity could change the decision.

Do not use traces from protected tasks as training examples, preference pairs,
reward-model data, or synthetic-data seeds. Do not tune thresholds, exclusions,
rewards, or metrics after seeing a candidate's protected results merely to make it
pass.

Use [references/model-evaluation.md](references/model-evaluation.md) for split
integrity, stochastic/agent evaluation, promotion gates, and Pareto selection.

## 4. Discover candidate models and adaptation paths

Search existing checkpoints and available provider offerings before training from
scratch. Do not assume either a tiny local model or a frontier-scale LLM is
required.

Candidate paths may include:

- rules, classical models, embeddings, or compact encoders for bounded tasks;
- existing specialist checkpoints;
- open-weight generative models that can be adapted locally or on rented compute;
- managed proprietary or open models that support fine-tuning;
- distillation from a stronger teacher into a smaller model;
- leaving weights unchanged and improving data retrieval, prompting, skills, or
  harness behaviour when this better satisfies the contract.

Record model/checkpoint revision, licence/terms, context limits, modalities,
training-method support, deployment/runtime availability, data-residency impact,
expected training cost, and whether trainable weights or a provider fine-tuning
interface actually exist.

Provider capabilities change. Before starting managed training, verify the live
provider documentation for supported models, methods, regions, quotas, RBAC,
pricing, data handling, and deployment constraints. Do not encode a stale model
matrix as repository policy.

## 5. Choose the training method

Choose the lightest method that targets the observed gap.

- **SFT** — use when there are trusted examples of desired responses/actions or
  verified successful trajectories worth imitating.
- **Preference optimization / DPO** — use when comparable chosen/rejected outputs
  can be justified by human preference or independent outcome evidence.
- **Reinforcement fine-tuning / agent RL** — use when the environment can generate
  fresh rollouts and a sufficiently reliable reward/verifier reflects the desired
  outcome without obvious shortcuts.
- **Distillation** — use when a stronger model can generate or label examples and
  a smaller/cheaper target is part of the contract.
- **Continued/domain pretraining** — use when the primary gap is domain-language
  modelling rather than following examples of the desired behaviour.
- **PEFT/LoRA or full fine-tuning** — choose according to model access, provider
  support, data scale, compute budget, and expected degree of adaptation.

Do not select a method merely because the training platform exposes it.

## 6. Transform traces into training data when applicable

Raw traces are evidence, not automatically examples to imitate. Preserve the raw
immutable source, then derive versioned training views.

Potential derivations include:

```text
verified state + desired next action           -> SFT example
same/similar state + better/worse actions      -> preference pair
trajectory + independent task outcome/reward   -> RL/RFT experience
strong-model trajectory + verified outcome     -> distillation candidate
```

Prefer observable state, messages, tool calls, tool results, environment state,
public rationale when present, and outcome evidence. Do not require or attempt to
recover hidden chain-of-thought.

Never infer that a successful final outcome makes every action in the trace good.
Remove or down-weight leakage, accidental success, policy violations, redundant
loops, test tampering, unsupported destructive actions, and traces whose outcome
cannot be attributed confidently.

The detailed contract for trajectory qualification, segmentation, preference
construction, reward provenance, and managed-training export lives in
[references/trajectory-training.md](references/trajectory-training.md).

## 7. Establish baselines

Before fine-tuning, measure at least the untouched base model under the same:

- system/task instructions;
- skills/context retrieval;
- tool schemas and permissions;
- inference budget and sampling policy;
- evaluator/verifier;
- protected tasks.

Where useful, also compare against prompt/harness improvements or a smaller model.
A fine-tuned model only earns promotion if weight adaptation adds value beyond
those cheaper interventions or satisfies another explicit constraint.

## 8. Run bounded experiments

For each experiment record:

- experiment ID and parent lineage;
- hypothesis and training method;
- code/config/provider job revision;
- training-data view version and fingerprints;
- source trace/dataset lineage without exposing protected content;
- base model/checkpoint/provider model identity;
- hyperparameters, adapter configuration, seed where applicable;
- harness, skill, tool-schema, and evaluator versions for agent experiments;
- provider/region/hardware/precision and relevant quota settings;
- training tokens/examples, budget, duration, and observed cost;
- development and permitted protected metrics;
- deployment measurements;
- outcome: `promote`, `retain-on-frontier`, `reject`, `inconclusive`, or `blocked`;
- why the result changes the next experiment.

A managed provider is an execution backend, not the source of truth for experiment
quality. Preserve enough local metadata and exported metrics to reconstruct what
was trained and why it was selected.

Use a bounded loop:

```text
observe baseline/frontier and failures
-> form one decision-bearing hypothesis
-> derive or revise training data/method
-> train candidate
-> evaluate in matched protected harness
-> compare against base + frontier
-> retain evidence
-> promote, branch, or reject
-> stop when a declared bound is reached
```

## 9. Improve data from failures

When error analysis points to a data gap, classify it before adding examples:

- missing class/phenomenon/task coverage;
- domain/language mismatch;
- ambiguous or inconsistent labels/preferences/rewards;
- long-tail rarity;
- tool-use or environment-state coverage gap;
- adversarial/robustness gap;
- temporal drift;
- preprocessing/tokenization/template failure;
- model-capacity/objective failure that more examples are unlikely to fix.

Only then choose among additional trace collection, retrieval of lawful public
data, human labelling, preference annotation, active learning, weak supervision,
augmentation, synthetic generation, or new online rollouts.

Keep generated and teacher-produced data marked as such, preserve generator/model
and prompt/version provenance, and validate a sample independently before allowing
it to dominate training.

## 10. Select the Pareto frontier

Compare candidates on the dimensions that matter to the contract, typically:

- task and critical-slice quality;
- agent task-completion and verifier pass rate;
- policy/safety regressions;
- tool-call validity and recovery behaviour;
- latency, throughput, peak memory, or hosted inference cost;
- training cost and data requirements;
- model/package size where relevant;
- robustness and generalisation to fresh tasks/environments.

Retain non-dominated candidates rather than collapsing everything into one
arbitrary weighted score. Choose a default winner only when the contract gives a
clear ordering or an accountable operator chooses the trade-off.

## 11. Promotion and stop rules

Stop experimentation when any declared bound is reached, including:

- compute, money, wall-clock, storage, provider quota, or experiment-count budget
  exhausted;
- a candidate satisfies all gates and additional optimization has low expected
  value;
- N consecutive experiments fail to improve the Pareto frontier;
- observed improvement is within measurement or rollout noise;
- required data cannot be licensed, accessed, transferred, or handled safely;
- protected evaluation, safety, or a critical slice materially regresses;
- gains vanish under a matched fresh-task evaluation;
- the next experiment requires changing the product/task contract rather than the
  model.

Do not move a gate because the current model misses it. Reopen the contract as a
separate decision with the reason and owner visible.

## 12. Optional self-improvement research mode

A useful progression for agent traces is:

```text
agent runs
-> verified traces
-> versioned training view
-> fine-tuned candidate
-> protected fresh tasks
-> new traces
-> next bounded training iteration
```

This is a self-improving system loop only in the broad operational sense. To
claim improvement of the improver itself, separately evaluate old versus new
research/data-selection/training policies across multiple held-out
model-development problems under fixed or independently governed budgets and
oracles.

## Output contract

Return or persist a compact lab report containing:

1. **Status** — `Ready`, `Running`, `Candidate`, `No-go`, or `Blocked`.
2. **Model contract** — task, metrics, hard constraints, assumptions, budget, and
   stop rules.
3. **Data inventory** — source datasets/traces, provenance/licence/privacy risks,
   transformations, and selected training/evaluation sources.
4. **Evaluation contract** — split/task identities, protected boundary, harness,
   metrics, slices, runtime/provider constraints, and promotion criteria.
5. **Candidate inventory** — base models, baselines, adaptation methods, and why
   apparently obvious choices were rejected.
6. **Training-data recipe** — exact derivation of SFT examples, preference pairs,
   rewards, or other training views when applicable.
7. **Experiment ledger** — reproducible run/job identities, hypotheses, data/model
   revisions, metrics, failures, cost, and disposition.
8. **Pareto frontier** — non-dominated candidates and their trade-offs.
9. **Recommendation** — promote, retain variants, collect better traces/data,
   change training method, change the task contract, or stop.
10. **Reproduction package** — code/config revision, data/model identifiers,
    provider job/deployment identifiers when applicable, seeds, dependencies,
    harness/tool versions, and commands or scripts required to rerun the result.

## Quality gate

Before declaring a candidate ready, verify that:

- success criteria and deployment/provider constraints were declared before
  optimization;
- raw traces were qualified and transformed rather than copied wholesale into
  training because their final outcome was successful;
- training method matches the evidence available for SFT, preference learning, or
  reinforcement;
- data provenance, licence, privacy, secrets, and transfer constraints permit the
  intended training/runtime path;
- a protected evaluation boundary exists and the optimizer could not inspect its
  examples/tasks;
- the untouched base model was measured under a matched harness where applicable;
- candidate improvement survives a fresh protected evaluation at the strength
  required by observed variance;
- safety/policy and critical-slice regressions are visible;
- provider/model/method/region support was verified at execution time rather than
  assumed from stale documentation;
- experiment lineage and negative results are preserved;
- the selected candidate is justified against the declared Pareto objectives;
- stop rules prevented unbounded training/search;
- any self-improvement claim is narrower than the evidence and separately tests
  the improvement process itself.

When evaluating changes to this skill, use the behavioural cases in
[references/skill-evaluation.md](references/skill-evaluation.md) with the matched
baseline/candidate process owned by `skill-creator`.
