# Compact decision models

Use this reference when the model outcome is a bounded semantic decision rather
than free-form generation: classification, calibrated yes/no judgement, ordinal
scoring, ranking, or selection among fixed or runtime-defined categories.

This guidance is architecture-agnostic. A compact encoder, embedding model,
classical classifier, distilled model, or another specialist may satisfy it. The
principles were informed in part by the documented design and evaluation choices
in [Bornholm/indecis](https://github.com/Bornholm/indecis), but this skill does not
depend on Indecis or prescribe its implementation.

## 1. Define the decision shape before the model family

Make the semantic output explicit before selecting an architecture or loss.

| Decision shape | Typical output | Important evidence |
| --- | --- | --- |
| Binary judgement | calibrated probability plus threshold/abstention policy | precision/recall, AUROC/AUPRC, calibration |
| Fixed categorical choice | distribution over a stable taxonomy | per-class metrics, confusion, calibration |
| Ordinal score | ordered level or expected score | MAE/ordinal error, threshold behaviour |
| Ranking/retrieval | ordered candidates | recall@k, MRR/nDCG, latency |
| Open/dynamic categories | best runtime-supplied candidate plus confidence/margin | generalisation to unseen category sets, rejection/abstention |

Do not flatten an ordinal problem into unrelated categories when distance between
levels matters. Do not assume a probability is trustworthy merely because the
model emits a number between zero and one.

Also decide whether one text is the real semantic input or whether the task is
relational, for example `(policy, message)`, `(query, candidate)`, or
`(context, text)`. Preserve that distinction in training and protected
evaluation instead of concatenating fields without testing the effect.

## 2. Choose fixed or open categories deliberately

A stable taxonomy and a runtime-defined taxonomy are different product contracts.

Prefer **fixed learned outputs** when:

- the classes/questions are stable enough that retraining for schema changes is
  acceptable;
- calibrated probabilities or stable class-specific thresholds matter;
- option wording should not change the answer at inference time;
- enough representative labels exist for each important class.

Prefer **open/dynamic selection** such as embedding similarity when:

- categories are supplied or changed at runtime;
- retraining for every new option is unacceptable;
- option descriptions/examples are available;
- empirical confidence/margin thresholds are acceptable.

Open-category flexibility is not free. Validate it on category lists and examples
that were not seen during training. Treat similarity scores or softmax-over-option
scores as uncalibrated until measured. Add explicit rejection/abstention tests for
inputs that fit no candidate.

Where practical, keep both paths on the Pareto frontier rather than assuming
dynamic categories dominate fixed heads or vice versa.

## 3. Preserve label authority and disagreement

Not all labels have equal evidential authority. Record how each label was obtained
and preserve that provenance through training views.

A useful default authority order is:

1. deterministic labels known by construction or authoritative system state;
2. adjudicated human labels under a written policy;
3. independent human labels with measured agreement;
4. multi-teacher consensus under the same written policy;
5. single-teacher, weak, heuristic, or inherited labels.

This is not universal: domain policy or measurement error may change the order.
The important property is that authority is explicit rather than inferred from
volume or model confidence.

When LLMs or other models act as teachers:

- write the labelling policy before large-scale labelling;
- give independent teachers the same decision policy without showing one
  another's answers;
- preserve teacher/model/prompt versions;
- route disagreements and contradictions with higher-authority labels into a
  review or active-learning queue;
- sample-check consensus against independent human or deterministic evidence;
- do not silently let a teacher overwrite labels known by construction.

Agreement between teachers measures consistency under the supplied policy; it does
not make their consensus independent ground truth.

## 4. Treat synthetic data as a family, not independent evidence

Synthetic or template-generated data is useful for targeted coverage, rare cases,
invariances, and labels known by construction. It is especially dangerous when
near-sibling variants cross the evaluation boundary.

For generated data:

- attach a family/lineage identifier for the template, seed, source example, or
  generation recipe;
- split by family/lineage, not by rendered row;
- keep generator/model/prompt/template versions;
- test on independently sourced real inputs wherever deployment involves real
  inputs;
- report generated and real-source slices separately when either could mask the
  other.

A model scoring near-perfectly on held-out variants from the same generator may
only have learned generator phrasing. Treat this as development evidence, not
proof of real-world generalisation.

Paraphrasing synthetic examples is not automatically new semantic coverage. Prefer
new representative source inputs or targeted generation for an evidenced gap.

## 5. Evaluate probability quality separately from discrimination

For decisions consumed as probabilities, separate:

- **discrimination** — can the model rank positives above negatives?;
- **classification quality** — what happens at the chosen operating threshold?;
- **calibration** — do predicted probabilities match observed frequencies?;
- **abstention/rejection** — can uncertain or out-of-scope cases be deferred?;
- **slice behaviour** — do calibration and thresholds hold on critical groups?

Depending on the task, include ECE, NLL, Brier score, reliability curves, and
threshold-specific precision/recall alongside ordinary accuracy/F1/AUC metrics.

Fit calibration and thresholds on development/calibration data, never on the
protected confirmation set. Evaluate the final thresholded behaviour the product
will actually use.

## 6. Check training prior versus deployment prior

A balanced training set can be useful for learning while being unlike production.
For example, positives may be deliberately oversampled during training but rare
in deployment.

Record:

- class prevalence in the training view;
- expected or measured deployment prevalence;
- whether sampling changed that prevalence;
- any prior-shift correction, recalibration, or threshold adjustment.

Do not interpret a training-distribution probability as a production probability
without evidence that the priors and conditional distributions are sufficiently
matched.

When production prevalence changes materially over time, monitor calibration and
threshold behaviour rather than only aggregate accuracy.

## 7. Evaluate the artefact that will actually run

Compression and runtime optimisation can alter both quality and robustness.
Measure the exported/deployed candidate after quantisation, pruning, compilation,
or other transformation.

For compact decision models, include where relevant:

- protected task metrics before and after transformation;
- calibration/threshold behaviour before and after transformation;
- fresh or out-of-domain slices, especially after vocabulary/feature pruning;
- p50/p95 latency and throughput at representative input lengths/concurrency;
- peak and steady-state memory;
- model/package size and startup characteristics.

A compression method that preserves in-domain aggregate accuracy can still damage
unforeseen inputs. Prefer reversible size/precision reductions first; require
fresh-input evidence before aggressive pruning that removes representational
coverage.

## Compact decision-model checklist

Before promotion, verify that:

- the decision shape and semantic input are explicit;
- fixed versus open categories was an intentional product/model choice;
- label provenance and authority are retained;
- teacher disagreements have a review path;
- generated families cannot leak across the protected boundary;
- independently sourced real/fresh inputs test generalisation where applicable;
- calibration, thresholds, abstention, and deployment priors are measured when
  probabilities drive product behaviour;
- the actual compressed/deployed artefact passes both quality and operational
  gates.
