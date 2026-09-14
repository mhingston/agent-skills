# Model evaluation and promotion

Use this reference when the model-development decision depends on split design,
variance, robustness, operational constraints, or choosing among several viable
candidates.

## Evaluation layers

Keep these roles distinct:

- **Training** — examples used to update parameters or fit thresholds/components.
- **Development** — examples visible to the research loop for iteration and error
  analysis.
- **Protected evaluation** — examples hidden from the optimizer; expose only the
  predeclared metrics or bounded failure categories needed for decisions.
- **Operational validation** — target-device latency, memory, throughput, package
  size, startup, and integration observations.

A public benchmark may be useful development evidence while being unsuitable as a
protected evaluation set if its examples or labels are readily available to the
optimizer or base model.

## Split integrity

Before training:

- deduplicate exact and near-duplicate records across splits;
- group related examples so variants of the same source cannot cross the
  train/protected boundary;
- use time-based or entity-based splitting where random splitting would leak the
  deployment scenario;
- record split-generation code/configuration and fingerprints;
- preserve the protected split once optimization starts.

If the evaluation contract must change, version it explicitly and do not compare
scores across incompatible contracts as if they were one continuous leaderboard.

## Metrics

Choose metrics from the decision, not convenience.

For classification consider macro/micro/weighted F1, per-class recall/precision,
AUROC/AUPRC where appropriate, calibration, threshold behaviour, and abstention.
For ranking/retrieval consider recall@k, precision@k, MRR, nDCG, and latency at the
actual candidate set size. For token/span tasks consider entity-level as well as
token-level metrics when the product outcome depends on complete entities.

Always include critical slices that can veto promotion even when the aggregate
metric improves.

## Variance and repeated runs

Use repeated seeds/runs when stochastic variance could change the decision.
Prefer a policy decided before the candidate result, for example:

```text
- run each serious candidate on 3 fixed seeds;
- report median and range for the primary metric;
- promote only when the improvement is larger than ordinary run-to-run variation
  and no hard slice gate regresses.
```

Do not repeatedly sample seeds until one passes.

For expensive training, use cheaper development runs to narrow candidates, then
spend repeated-run budget only on frontier contenders.

## Protected-evaluation feedback

The autonomous optimizer may receive:

- aggregate predeclared metrics;
- pass/fail status for hard constraints;
- coarse predeclared slice summaries when necessary for safe development.

It should not receive:

- protected examples or labels;
- per-example loss/confidence that permits reconstruction;
- arbitrary interactive queries that turn the holdout into a training oracle;
- post-hoc metric changes chosen after inspecting candidate weaknesses.

Track the number of protected evaluations. Excessive adaptive queries can leak
information even when examples remain hidden. When this becomes material, rotate
or introduce a fresh confirmation set before final promotion.

## Operational measurements

Measure deployment properties on the intended runtime/hardware whenever they are
hard constraints:

- cold and warm startup where relevant;
- p50 and p95 latency after an explicit warm-up policy;
- throughput at the expected batch/concurrency shape;
- peak memory, not just checkpoint size;
- exported package/runtime dependency size;
- accuracy after quantization/pruning/export, not before only.

Parameter count is a useful search feature, not proof that a model meets latency
or memory targets.

## Pareto selection

Candidate A dominates B only when A is no worse on every declared objective and
strictly better on at least one material objective. Keep multiple non-dominated
candidates when the contract does not impose a single total ordering.

Typical frontier dimensions:

```text
quality ↑
critical-slice quality ↑
calibration ↑
latency ↓
peak memory ↓
package size ↓
inference/training cost ↓
```

Do not hide a deployment regression inside one weighted score unless that scoring
rule was itself part of the accepted contract.

## Promotion decision

A model is promotable only when:

1. all hard gates pass;
2. the protected evaluation evidence is still independent enough for the claim;
3. the result reproduces at the strength required by observed variance;
4. the exported/quantized artefact itself passes the relevant quality and
   operational checks;
5. provenance, licence, and data-handling constraints permit the intended use;
6. the selected candidate is justified against the current Pareto frontier.

Return `No-go` when no candidate clears the contract. A well-evidenced failure is
preferable to weakening the contract after optimization.
