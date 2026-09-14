# Model evaluation and promotion

Use this reference when the model-development decision depends on split design,
variance, robustness, agent execution, operational constraints, or choosing among
several viable candidates.

## Evaluation layers

Keep these roles distinct:

- **Training** — examples, preferences, rewards, or trajectories used to update
  parameters or fit thresholds/components.
- **Development** — examples/tasks visible to the research loop for iteration and
  error analysis.
- **Protected evaluation** — examples/tasks hidden from the optimizer; expose only
  the predeclared metrics or bounded failure categories needed for decisions.
- **Operational validation** — target-runtime latency, memory, throughput, hosted
  cost, package/deployment characteristics, startup, and integration observations.

A public benchmark may be useful development evidence while being unsuitable as a
protected evaluation set if its examples or labels are readily available to the
optimizer, trace corpus, teacher model, or base model.

## Split integrity

Before training:

- deduplicate exact and near-duplicate records across splits;
- group related examples so variants of the same source cannot cross the
  train/protected boundary;
- for agent traces, keep all segments/reruns from one task or lineage in one split;
- consider grouping by repository/commit family, user/entity, generated-task seed,
  or conversation/session where these create leakage risk;
- use time-based or entity-based splitting where random splitting would leak the
  deployment scenario;
- record split-generation code/configuration and fingerprints;
- preserve the protected split once optimization starts.

If the evaluation contract must change, version it explicitly and do not compare
scores across incompatible contracts as if they were one continuous leaderboard.

## Compare fine-tuned models against a matched base

For weight adaptation, the minimum baseline is normally the untouched base model.
Keep the following matched unless the experiment explicitly tests one of them:

- system/task instructions;
- retrieved context and skill versions;
- tool schemas, permissions, and environment;
- sampling/reasoning settings and token/tool budgets;
- task fixtures and verifier;
- termination/retry policy;
- deployment/runtime class where feasible.

A candidate that only improves because it receives a better harness or more budget
has not demonstrated a fine-tuning gain.

Where a cheaper prompting, retrieval, skill, or harness change already meets the
contract, include it on the frontier rather than assuming weight updates are
required.

## Metrics

Choose metrics from the decision, not convenience.

For classification consider macro/micro/weighted F1, per-class recall/precision,
AUROC/AUPRC where appropriate, calibration, threshold behaviour, and abstention.
For ranking/retrieval consider recall@k, precision@k, MRR, nDCG, and latency at the
actual candidate set size. For token/span tasks consider entity-level as well as
token-level metrics when the product outcome depends on complete entities.

For generative or agentic systems consider direct task outcomes before prose
similarity. Depending on the contract, measure:

- task completion / executable verifier pass rate;
- critical-slice pass rates;
- tool-call schema validity and invalid-call rate;
- policy/safety violation rate;
- recovery after tool/environment failure;
- destructive or unnecessary action rate;
- tokens, tool calls, wall-clock time, and monetary cost per task;
- human preference only when the task genuinely requires human judgement.

Always include critical slices that can veto promotion even when the aggregate
metric improves.

## Stochastic and agent evaluation

Agent rollouts can vary substantially even when model weights do not. Decide the
repetition policy before seeing candidate results.

Examples:

```text
- run each candidate on the same protected task set;
- use multiple rollouts for tasks whose success variance is material;
- report task-level paired deltas against the base model;
- retain seeds/task assignment rules when the runtime exposes them;
- cap retries, tool calls, and tokens consistently;
- promote only when the gain is larger than ordinary rollout/evaluation noise and
  no hard gate regresses.
```

For expensive models, use development tasks to narrow candidates, then spend
repeated protected-rollout budget only on frontier contenders.

Do not repeatedly resample candidate rollouts until one set looks favourable.

## Protected-evaluation feedback

The autonomous optimizer may receive:

- aggregate predeclared metrics;
- pass/fail status for hard constraints;
- coarse predeclared slice summaries when necessary for safe development.

It should not receive:

- protected examples/tasks or expected outputs;
- hidden tests or verifier internals that reveal the solution;
- per-example loss/confidence or detailed traces that permit reconstruction of
  protected cases;
- arbitrary interactive queries that turn the holdout into a training oracle;
- post-hoc metric/reward changes chosen after inspecting candidate weaknesses.

Track the number of protected evaluations. Excessive adaptive queries can leak
information even when examples remain hidden. When this becomes material, rotate
or introduce a fresh confirmation set before final promotion.

## Evaluate the actual trained/deployed artefact

Measure the candidate that will really run, not an easier precursor.

For local/exported models this may include:

- accuracy after quantization/pruning/export;
- cold/warm startup;
- p50/p95 latency and throughput at the expected concurrency/batch shape;
- peak memory and package/runtime dependency size.

For managed fine-tuned LLMs this may include:

- the exact provider model/deployment identifier;
- region/data-zone constraints;
- hosted p50/p95 latency and error/rate-limit behaviour;
- token and request cost under the intended workload;
- availability of the fine-tuned model in the required deployment tier;
- behaviour after any provider-side model or deployment change.

A completed training job or successful deployment is operational evidence only; it
is not proof of task improvement.

## Judge and reward independence

When LLM judges or learned reward models contribute to evaluation:

- record their model/version and prompts;
- keep them independent of the candidate's training data where practical;
- include executable/deterministic evidence when the task supports it;
- calibrate against human or objective labels on a representative sample;
- test obvious reward-hacking strategies;
- do not let the same generated labels serve simultaneously as training truth and
  sole final proof of quality.

## Pareto selection

Candidate A dominates B only when A is no worse on every declared objective and
strictly better on at least one material objective. Keep multiple non-dominated
candidates when the contract does not impose a single total ordering.

Typical frontier dimensions:

```text
quality / task pass rate ↑
critical-slice and safety quality ↑
calibration / abstention quality ↑
latency and error rate ↓
tokens / tool calls / runtime cost ↓
peak memory or package size ↓ where relevant
training cost and data requirements ↓
```

Do not hide a hard deployment or safety regression inside one weighted score
unless that scoring rule was itself part of the accepted contract.

## Promotion decision

A model is promotable only when:

1. all hard gates pass;
2. the protected evaluation evidence is still independent enough for the claim;
3. a fine-tuned candidate beats the untouched base under a matched evaluation at
   the strength required by observed variance;
4. the actual exported/deployed artefact passes relevant quality and operational
   checks;
5. provenance, licence, privacy, provider data-handling, and residency constraints
   permit the intended use;
6. no material policy/safety or critical-slice regression is hidden by aggregate
   improvement;
7. the selected candidate is justified against the current Pareto frontier.

Return `No-go` when no candidate clears the contract. A well-evidenced failure is
preferable to weakening the contract after optimization.
