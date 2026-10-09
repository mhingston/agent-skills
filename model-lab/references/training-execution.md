# Staged training execution and artefact verification

Load this reference when `model-lab` is about to run non-trivial training,
teacher-labelled data generation, distillation, or model export. This is an
**execution gate**, not a new public skill or a substitute for the existing
model contract, data qualification, protected evaluation, and Pareto selection.

## 1. Prepare a reproducible execution brief

Carry forward verified facts without silently re-deriving or upgrading them to
approval. Record what is *verified* (with source/revision/date), *assumed*, and
*unknown*. At minimum identify:

- the exact base checkpoint, trainable adapter/parameter policy, data view,
  preprocessing/tokenizer/chat template, trainer/driver, and runtime revisions;
- the baseline result and the development evaluation fixtures;
- the full sequence of paid steps (data generation, teacher labelling, training,
  checkpoint evaluation, conversion/export, and inference validation);
- the intended output artefacts, inference contract, and permitted publication
  destinations;
- the estimated cost range, total cap, reservations/quota, and stop conditions.

Do not treat instructions from a source article as verified facts for a new
model, dataset, or runtime. Reconfirm material compatibility at execution time.

## 2. Authorise costs and side effects separately

Distinguish **estimated cost**, **maximum allowed cost**, and **permission to
spend**. Before launching paid work, confirm that the operator has already
authorised this kind of operation within a defined cap; otherwise present the
estimate and obtain approval. A cost cap in a brief does not automatically
confer permission to launch a paid job.

- Account for *all* costs in the project, including retried/failed jobs, teacher
  inference, data generation, checkpoint evaluation, storage and export.
- If a provider cannot enforce the cap, expose that limitation and use bounded
  job sizes, conservative estimates and explicit operator approval of the risk.
- Abort, request a new approval, or choose a cheaper route before exceeding the
  authorised ceiling; do not assume the service enforces the ceiling for you.
- External dataset/model publication, moving data to an unapproved environment,
  and deployment/promotion are separate side effects that require their own
  authorisation even when training spend is approved.
- For local/non-billed work, proportionate compute/time/energy limits still
  apply; do not manufacture paid approval steps where no paid operation exists.

## 3. Run a cheap preflight before scaling up

Use a tiny, representative **training/development** subset and the actual
training path wherever possible. Keep protected examples/tasks inaccessible
to the preflight and the optimiser. The preflight should exercise:

1. **Data:** loading, licensing/handling gates, label/target alignment, shapes,
   masks, tokenisation or modality transforms, train/dev boundaries, and
   representative long/edge cases as affordable.
2. **Optimisation:** trainable parameter count is nonzero and as intended;
   at least one update step executes; loss/gradients are finite; expected
   trainable weights or adapter tensors materially change against their initial
   values. Frozen base weights are not expected to change in adapter training.
3. **Persistence:** save and reload the resulting checkpoint/adapter and
   preprocessor; compare inference using the reloaded artefact rather than
   assuming a successful trainer exit proves a usable model.
4. **Execution:** confirm runtime access, dependency versions, precision,
   resource limits, retries, logging, and a bounded failure/cleanup path.
5. **Contract smoke:** run a few *development* inputs through inference and
   verify parsing, schema/output type and basic functionality.

A green smoke test means **the pipeline can run**, not that the adapted model
is better. It is not a substitute for the untouched-base baseline, rigorous
development metrics or protected confirmation. Do not train to artificially
improve a smoke-test score.

Prefer a small number of steps/samples tailored to the trainer and workload,
not a universal step count. If the service cannot support a representative
preflight, document what was checked, the residual uncertainty, and the specific
operator approval needed to accept expensive unverified execution; otherwise
return `Blocked`. Never run an unapproved costly experiment simply because
preflight is technically unavailable.

## 4. Train with bounded checkpoint decisions

- Decide checkpoint cadence, maximum saves/storage and early-stop policy before
  inspecting development outcomes. Retain enough checkpoints to detect
  overfitting or capability bleed, not an unlimited sequence.
- Use the **same fixed development fixtures**, including target slices and
  regression/non-target prompts, to compare checkpoints. For multimodal
  generation, use paired prompts/seeds and predefined scoring or inspection
  criteria when deterministic metrics alone are inadequate.
- Choose a candidate checkpoint based on the declared quality, safety and
  deployment trade-offs; the final/latest checkpoint is not automatically best.
- Do **not** use protected examples, per-case protected feedback, or repeated
  protected queries to select epochs, checkpoints, prompts or thresholds.
- Send only shortlisted candidates through protected confirmation, following
  the existing evaluation-query and promotion policy.

## 5. Verify the actual inference artefact

After selection, validate what will actually be deployed, including:

- checkpoint and adapter/base-model compatibility, reload, tokenizer or
  preprocessor version and prompt/chat template;
- required output format/schema and representative happy-path, long-tail and
  non-target/robustness cases;
- quantisation, ONNX/GGUF or other export steps when relevant, with before/after
  quality and calibration checks proportional to the task;
- target-hardware/runtime latency, memory, startup and errors where relevant;
- a reproducible artefact identity, lineage, training/eval provenance, licence
  and applicable limitations for the model card or private release record.

A successful train job or file export is not proof the deployed artefact works.
Public Hub uploads, demo applications and model cards are optional deliverables;
publish only to approved destinations and never release restricted data by
default.

## 6. Record a stage-gate decision

At each transition capture a compact status: `ready`, `blocked`, or
`approved-exception`; what checks passed/failed; authorised cap versus estimated
and actual cumulative spend; operator decision if required; selected checkpoint
and development rationale; and final export/runtime verification. Preserve
failed jobs and negative results in the normal experiment ledger.

## Provenance

Informed by Hugging Face's [Building with ML Intern](https://github.com/huggingface/blog/blob/main/building-with-ml-intern.md):
explicit untouched-model baselines, cheap initial training checks,
operator-controlled budgets and checkpoint-based selection. These are
transferable practices, not evidence that a particular model, provider or
training recipe is the right choice for a new task.
