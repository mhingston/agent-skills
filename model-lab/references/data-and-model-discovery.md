# Data and model discovery

Use this reference when public/local data, agent traces, existing checkpoints, or
managed-provider offerings could materially change the design. Discovery is a
decision stage, not a catalogue dump.

## Dataset search order

Start with the narrowest authoritative or representative source available, then
broaden only when coverage is insufficient:

1. approved user/local/domain data and authorised production traces;
2. canonical task benchmarks or datasets linked from authoritative papers;
3. Hugging Face datasets;
4. Kaggle, OpenML, and other public registries;
5. weakly labelled, augmented, synthetic, teacher-generated, or programmatically
   generated data created for a documented gap.

Do not prefer a public benchmark over representative local data merely because it
is easier to download. For agent traces, use the additional qualification and
transformation contract in `trajectory-training.md`.

## Dataset qualification record

For each serious candidate capture:

| Field | Why it matters |
| --- | --- |
| Stable ID/version | Reproduction and drift detection |
| Source/provenance | Trust, contamination, and authority |
| Licence/terms | Training, commercial use, redistribution, derivatives |
| Task fit | Whether labels/outcomes express the target decision |
| Domain/population fit | Expected transfer to intended inputs |
| Languages/regions/time | Coverage and likely distribution gaps |
| Size | Statistical support and training cost |
| Label/outcome distribution | Class imbalance and rare-case coverage |
| Label/reward origin | Human, verifier, weak, synthetic, heuristic, imported |
| Duplicate/lineage risk | Inflated metrics and split leakage |
| PII/secrets/sensitive content | Handling, transfer, and publication constraints |
| Known benchmark overlap | Train/eval contamination risk |
| Access/gating | Reproducibility and operational friction |

A useful scoring rubric is:

```text
fitness = task fit + domain fit + signal quality + licence clarity
          + coverage + reproducibility
          - contamination risk - privacy risk - access friction
```

Do not treat this as a universal numeric formula. Use it to make the reasons for
ranking visible.

## Dataset rejection reasons

Reject or quarantine a candidate when any of these are material and unresolved:

- licence or intended-use terms are incompatible or ambiguous;
- labels, preferences, or rewards encode a proxy rather than the desired task;
- provenance is too weak to assess contamination or legal use;
- sensitive data cannot be handled by the active or planned training backend;
- the source is known or likely to overlap with protected evaluation tasks;
- synthetic/teacher-generated examples cannot be distinguished from independent
  evidence;
- distribution mismatch is so large that the result would not answer the model
  contract.

## If no dataset is good enough

Prefer an explicit acquisition plan over training on bad data. Possible routes:

- human-labelled seed set with a written annotation guide;
- additional authorised trace collection with richer outcome evidence;
- active learning over approved unlabeled examples;
- weak supervision with independently checked labels;
- targeted retrieval from additional lawful sources;
- augmentation for known invariances;
- teacher/synthetic generation for a named gap, followed by independent
  verification.

Never let the same generator or judge create both the majority of training data
and the only final evaluation evidence without a separate justification.

## Model discovery

Search existing checkpoints and managed-provider offerings before training from
scratch. For each serious candidate record:

| Field | Why it matters |
| --- | --- |
| Model/checkpoint/provider ID and revision | Reproduction |
| Architecture/family | Expected fit and adaptation path |
| Parameter count / scale | Training and inference cost proxy |
| Input/context/modality limits | Task compatibility |
| Pretraining/task history | Transfer expectations and contamination risk |
| Licence/terms | Intended training, deployment, and redistribution |
| Trainable artefacts/interface | Whether further training is practical |
| Supported adaptation methods | SFT, PEFT/LoRA, DPO/preference, RFT/RL, full FT, etc. |
| Deployment/runtime availability | Target environment feasibility |
| Region/data-residency support | Governance and transfer feasibility |
| Quantization/export support | Deployment feasibility for open/local models |
| Reported benchmark evidence | Prior signal, not local proof |

A published inference artefact is not automatically a useful training starting
point. For open-weight models, check whether full or adapter-trainable weights,
tokenizer/preprocessor, configuration, and compatible licence terms are actually
available. For managed models, check whether the provider currently exposes the
required customization method and deployment path.

Provider capabilities change quickly. Verify current provider documentation at
execution time instead of treating a copied model/method/region matrix as durable
repository knowledge.

## Search breadth

Do not search only one model scale or architecture. Depending on the task and
constraints, include:

- deterministic rules/recognizers;
- n-gram or bag-of-words models;
- linear/classical classifiers;
- static or learned embeddings plus shallow heads;
- compact CNN/RNN models;
- encoder models such as ModernBERT-like families;
- existing specialist checkpoints;
- small and medium open generative models;
- larger open-weight LLMs where their capabilities justify the training/runtime
  cost;
- managed proprietary or open LLMs that support the required fine-tuning method;
- distillation or no-weight-change alternatives when they satisfy the contract
  more cheaply or safely.

The search is complete enough when there is at least one credible baseline, the
main plausible adaptation paths have been considered, and no unexamined family is
likely to dominate under the hard quality, governance, training, or deployment
constraints.
