# Data and model discovery

Use this reference when public/local data or existing checkpoints could materially
change the design. Discovery is a decision stage, not a catalogue dump.

## Dataset search order

Start with the narrowest authoritative or representative source available, then
broaden only when coverage is insufficient:

1. approved user/local/domain data;
2. canonical task benchmarks or datasets linked from authoritative papers;
3. Hugging Face datasets;
4. Kaggle, OpenML, and other public registries;
5. weakly labelled, augmented, or synthetic data created for a documented gap.

Do not prefer a public benchmark over representative local data merely because it
is easier to download.

## Dataset qualification record

For each serious candidate capture:

| Field | Why it matters |
| --- | --- |
| Stable ID/version | Reproduction and drift detection |
| Source/provenance | Trust, contamination, and authority |
| Licence/terms | Training, commercial use, redistribution, derivatives |
| Task fit | Whether the labels actually express the target decision |
| Domain/population fit | Expected transfer to intended inputs |
| Languages/regions/time | Coverage and likely distribution gaps |
| Size | Statistical support and training cost |
| Label distribution | Class imbalance and rare-case coverage |
| Label origin | Human, weak, synthetic, heuristic, imported |
| Duplicate risk | Inflated metrics and split leakage |
| PII/sensitive content | Handling and publication constraints |
| Known benchmark overlap | Train/eval contamination risk |
| Access/gating | Reproducibility and operational friction |

A useful scoring rubric is:

```text
fitness = task fit + domain fit + label quality + licence clarity
          + coverage + reproducibility
          - contamination risk - privacy risk - access friction
```

Do not treat this as a universal numeric formula. Use it to make the reasons for
ranking visible.

## Dataset rejection reasons

Reject or quarantine a candidate when any of these are material and unresolved:

- licence or intended-use terms are incompatible or ambiguous;
- labels encode a proxy rather than the desired task;
- provenance is too weak to assess contamination or legal use;
- the dataset contains sensitive data that cannot be handled in the active
  environment;
- the split is known or likely to overlap with the protected evaluation set;
- synthetic examples cannot be distinguished from independently sourced data;
- distribution mismatch is so large that the result would not answer the model
  contract.

## If no dataset is good enough

Prefer an explicit acquisition plan over training on bad data. Possible routes:

- human-labelled seed set with a written annotation guide;
- active learning over approved unlabeled examples;
- weak supervision with independently checked labels;
- targeted retrieval from additional lawful sources;
- augmentation for known invariances;
- synthetic generation for a named gap, followed by independent validation.

Never let the same generator create both the majority of training data and the
only final evaluation evidence without a separate justification.

## Model discovery

Search existing checkpoints before training from scratch. For each serious
candidate record:

| Field | Why it matters |
| --- | --- |
| Model/checkpoint ID and revision | Reproduction |
| Architecture/family | Expected fit and export path |
| Parameter count | Training/deployment cost proxy |
| Input/context limits | Task compatibility |
| Pretraining/task history | Transfer expectations and contamination risk |
| Licence/terms | Intended deployment and redistribution |
| Trainable artefacts available | Whether further training is practical |
| Export formats | Target runtime compatibility |
| Quantization support | Deployment feasibility |
| Reported benchmark evidence | Prior signal, not local proof |

A published inference artefact is not automatically a useful training starting
point. Check whether full or adapter-trainable weights, tokenizer/preprocessor,
configuration, and compatible licence terms are actually available.

## Search breadth

Do not search only transformer checkpoints. Depending on the task, include:

- deterministic rules/recognizers;
- n-gram or bag-of-words models;
- linear/classical classifiers;
- static or learned embeddings plus shallow heads;
- compact CNN/RNN models;
- small encoder models;
- existing specialist checkpoints;
- small generative models only when structured generation is required.

The search is complete enough when there is at least one credible cheap baseline,
one credible pretrained/adaptable candidate where such models exist, and no
unexamined family is likely to dominate under the hard deployment constraints.
