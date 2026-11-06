# Specialist systems: tiny models, structured actions, and composition

Load this reference when `model-lab` is developing or selecting a bounded
structured-action/extraction model, an on-device specialist, or a pipeline that
uses several small models. It supplements
[compact decision models](compact-decision-models.md) and
[model evaluation](model-evaluation.md). Do not compose models merely because
several are available.

The goal is **minimum sufficient learned capability**, not smallest parameter
count at any cost. A deterministic parser, a classical model, an existing
specialist, a tuned tiny model, a larger general model, or a pipeline may win.
Test the simplest credible option against the actual product contract.

## 1. Establish the capability boundary

For each candidate record:

- Input and state: modality, source, schema, language, context, available tools,
  missing fields and required provenance.
- Output: labels, spans, typed extraction, zero or more tool proposals, embeddings,
  audio segments, or explicit no-op/abstention.
- What must be learned versus what deterministic code can validate: permissions,
  checksums, type constraints, units, date parsing, state transitions.
- Unsafe, unsupported, ambiguous and out-of-distribution inputs; what happens
  without network access or a trusted human reviewer.
- Target hardware/accelerator and actual peak memory, package size, cold start,
  p50/p95 latency, concurrency, battery/thermal impact where measurable.
- Comparison candidates: rules, simple embedding/classifier, specialist,
  general-purpose model, and multi-stage system only when justified.

Grammar-constrained JSON guarantees *syntax*, not tool correctness, factual
grounding, acceptable risk, or permission to execute.

## 2. Structured actions and extraction

Distinguish the following evaluations rather than reporting a single accuracy:

1. **Tool selection:** correct tool(s), correct sequence, no-match responses,
   similar tool collisions, and whether the model should act at all.
2. **Argument grounding:** values supported by input or trusted state; absent
   parameters omitted; no fabricated names, dates, amounts or device IDs.
3. **Output validity:** schema conformance and correct types; report separately
   from grounded task completion.
4. **Policy and outcome:** human/permission gates independent from model scores,
   sandboxed effects, retries, stale state and partial execution.
5. **Selective prediction:** calibrated act/abstain/clarify/escalate policy,
   including the false-action rate at a given coverage.

For typed extraction distinguish *missing*, *ambiguous*, *explicit null*, and
*present* as the product requires. Score exact values, character offsets if
available, unknown-schema generalisation, hallucinated fields, and correction
effort. Null-handling is a capability, not a missing implementation.

Deterministic validators can check identifier formats and checksums, but do
not prove every PII span was found, or that extracted values belong to the
correct entity. Measure detection and end-to-end leakage separately.

For training, include verified examples of off-topic/no tool, unsupported
actions, missing fields, closely related tools, varied argument values, and
multiple requests. Split source/generator/template families across train and
evaluation boundaries. Do not let a synthetic-data generator or teacher own
the only evaluation oracle.

## 3. Adaptive capacity and confidence-gated escalation

A small model can potentially serve routine requests while a larger model or
human handles the remainder. The **whole cascade** is the model-system
candidate.

- Confirm whether a confidence score is available and calibrated for the exact
  checkpoint, depth, tool definitions, data distribution and export method.
  Do not reuse thresholds after adaptation without verification.
- Declare allowed outcomes: execute (only if separately authorised), no-op,
  clarify/review, or escalate to a permitted larger/cloud model.
- Select thresholds on development/calibration data, never by optimising
  against the protected holdout.
- Compare **risk/quality versus coverage**, false executions, review and
  escalation frequency, cost, p95 latency and offline/fallback failure against
  a matched single-model baseline.
- Test each selectable model depth or capacity tier as an actual exported
  inference artefact; do not extrapolate accuracy or speed from parameter
  count alone.
- No cloud fallback if locality, data residency or offline requirements
  prohibit it. Confidence is not authority to take consequential actions.

## 4. Composition as an alternative to a monolithic model

One plausible system shape is:

```text
raw text / audio / document
  -> optional language, perception or topic specialist
  -> typed extraction or proposed tool call
  -> deterministic validation and provenance check
  -> policy + calibrated uncertainty gate
  -> execute / no-op / review / permitted escalation
```

Only add a stage if it solves an evidenced gap. Define typed interfaces,
versioned preprocessing and model identities, explicit missing/uncertain
values, and rules for partial failures, tool state and rollback. Audio stages
must agree on timing conventions; retrieval stages must agree on vector/index
formats. Compare with a simpler complete pipeline or single model.

Measure independent stage quality **and** end-to-end correctness, including
compounding errors (e.g. wrong-language routing, PII surviving redaction,
semantically incorrect but schema-valid fields, missing commands). Measure
cold-start costs, total loaded memory, accelerator transfers, package size,
end-to-end p95, fallback latency, and energy only if actually instrumented.
The sum of standalone vendor latencies is not an end-to-end benchmark.

## 5. Examples of things worth building

These are **illustrative experimental briefs**, not a prescribed project
backlog, copied training recipes, or claims that any one vendor meets the
requirements. For a real request, first establish actual quality gates,
dataset rights, operating conditions, authorisation and experiment budget.

| Potential build | Candidate design and output contract | Baselines and decisive tests |
| --- | --- | --- |
| **Offline home/robot tool router** | Text or local speech -> zero or more typed *proposed* actions, explicit no-op, grounding against device state and independent permission gate. | Rules and general tool caller; wrong tool, fabricated argument, ambiguous/multi-step commands, stale state, critical unsafe actions, device memory and latency. Mobile support does **not** establish ESP32/microcontroller support. |
| **Privacy-first transcript intake** | On-device PII span detection -> deterministic ID/checksum checks -> redacted text and optional structured fields. | Regex and specialist-only baselines; high-impact misses, span offsets, false masking, reversible placeholder handling, multilingual variation, downstream leakage. Never promise perfect redaction. |
| **Invoice, booking or CRM form capture** | Unstructured text -> typed JSON with source offsets, explicit absent fields and business-rule validation; uncertain fields to review. | Rules/NER and general constrained LLM; unfamiliar schemas, invented amounts/dates, unknown/null distinction, OCR artefacts, correction workload. |
| **Local audio-note preparation** | ASR -> optional word timestamps/diarisation/filler flags -> searchable topics and candidate actions; generative summarisation optional. | ASR plus rules and a single audio-language model; word/speaker errors, mistaken deletions, timing drift, pipeline propagation and target-device cold start/latency. |
| **On-device notification triage** | Small language/topic/intent classifier -> deterministic user policy -> route, defer, tag or review. | Rules and single classifier; rare urgent cases, false suppression, drift, abstention coverage, offline behaviour and review burden. |

An app-integration task using already selected SDKs is not automatically
model-development work. The `model-lab` deliverable is a selected/developed
model or composed model-system backed by qualified data, protected evaluation,
runtime evidence and a reproducible experiment ledger.

## 6. Case studies, rights and limits

- [Cactus Compute Needle](https://github.com/cactus-compute/needle)
  illustrates a small structured-action model with constrained outputs,
  no-op examples, selectable depth and possible confidence-gated tool
  execution. Local LoRA adaptation and provider/platform fine-tuning may
  differ in confidence support and exported precision. Verify against the
  current docs, exact checkpoint and target device; vendor benchmarks are
  only prior hypotheses.
- [Desert Ant Labs](https://desertant.com/models/) illustrates single-purpose
  on-device models. [Redact](https://desertant.com/models/redact/) combines
  learned PII detection and deterministic identifier checks;
  [Schemer](https://desertant.com/models/schemer/) demonstrates schema-driven
  extraction with explicit absent-field handling. Check model availability
  (including beta status), supported hardware and independent quality.

**Deployment rights do not imply training rights.** Verify the current
checkpoint/model/SDK licence separately for inference, commercial use,
adapters, teacher labels, distillation, extraction, logging and redistribution.
For example, Desert Ant's
[source-available licence](https://license.desertant.com/1.0)
restricts using its models and outputs to train competing models. Do not
systematically log or reuse restricted outputs as a competing training corpus;
discover a properly licensed teacher or independent labels instead.

Before promotion require the normal protected, matched and deployment
checks in `model-lab`, plus grounded no-action/missing-field behaviour,
calibrated selective inference, independent side-effect authority,
whole-pipeline error accounting, actual packaged runtime measurements and
per-stage data/model licences.
