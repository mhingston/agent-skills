# Continual and online learning

Use this reference when a model is expected to keep adapting after its initial
training run: from new documents, conversations, traces, domains, user feedback,
or a long-lived data stream.

Continual learning is not ordinary fine-tuning repeated forever. Every accepted
update must demonstrate both **plasticity** (the intended new capability improved)
and **retention** (important existing capabilities did not regress beyond the
declared tolerance).

## Start with a retention contract

Before allowing persistent updates, define:

- the new capability, domain, or distribution the update should improve;
- the primary plasticity metric and minimum meaningful gain;
- retained capabilities and slices that must continue to work;
- an acceptable regression envelope for each critical retained slice;
- protected examples or tasks that the update process cannot inspect directly;
- update frequency, batch/stream boundaries, and maximum update budget;
- checkpoint, rollback, and stop conditions;
- whether the model may change only weights or may also change architecture,
  capacity, context length, routing, or other structural properties.

Prefer explicit gates such as:

```text
plasticity: new-domain loss improves by >= declared delta
retention: no critical protected slice regresses beyond its tolerance
safety: no material regression
resource: memory/latency/storage remain within budget
promotion: candidate passes fresh protected confirmation
```

Do not replace several retained-capability checks with one aggregate score if a
large gain in one domain could hide catastrophic forgetting elsewhere.

## Measure forgetting directly

For every persistent update, compare the candidate against the last promoted
checkpoint on:

1. the new material or capability being learned;
2. representative retained domains/capabilities;
3. critical safety/policy slices;
4. relevant runtime/resource measurements.

Use matched before/after evaluation. Where stochasticity is material, repeat runs
or estimate enough variance to distinguish a real change from instrument noise.

A useful experiment records both sides of the trade:

```text
plasticity gain = improvement on target/new-domain metric
retention cost  = degradation across retained protected metrics
```

Treat the update as failed when retention cost exceeds the predeclared envelope,
even if the new-domain metric improves substantially.

## Prefer rehearsal and interleaving before exotic mechanisms

When sequential training causes forgetting, test the simplest plausible
mitigations first:

- interleave representative old and new data;
- rehearsal/replay from a governed retained-data buffer;
- smaller or differentiated learning rates for broadly shared parameters;
- adapters/PEFT or other parameter-isolating methods;
- regularisation or constraint-based continual-learning methods;
- routing/sparsity mechanisms that localise updates.

Do not assume one mechanism generalises across architectures. For example, a
smaller learning rate on shared trunk parameters may be a useful hypothesis when
those parameters dominate forgetting, but the ratio must be measured rather than
copied from another system.

## Govern adaptive training controls

A long-lived training process may adapt its own training controls, but every
control needs a bounded policy and observable evidence.

Examples include:

- reducing or increasing learning rate from held-out evidence rather than from a
  schedule that assumes training has a fixed end;
- expanding context length only when held-out evidence shows useful gain from the
  current context boundary;
- growing or pruning specialist capacity when demand, utilisation, retention, and
  resource gates permit it;
- pausing, reverting, or terminating after divergence or repeated non-improvement.

Keep these as explicit policies with thresholds, cooldowns, and stop conditions.
Do not let a controller silently move evaluation gates or redefine success.

## Keep best-known-state semantics

For long-running adaptation, "latest" is not automatically "best".

Maintain:

- an immutable identity for the last promoted checkpoint;
- candidate checkpoints with lineage and update metadata;
- atomic/transactional promotion where possible;
- enough optimizer/runtime state to reproduce or resume intended training;
- a rollback path tested before unattended operation.

When held-out or protected performance degrades materially, prefer reverting to
the last known-good state and changing the update hypothesis rather than training
through unexplained damage.

A bounded recovery policy can be:

```text
candidate degrades beyond threshold
-> revert to last promoted checkpoint
-> reduce update aggressiveness or change the hypothesis
-> re-evaluate
-> stop after N failed recoveries
```

## Separate continual adaptation from continual self-modification

A system that continuously trains its weights is not evidence that it should also
rewrite its architecture or training algorithm.

Treat structural changes such as:

- dynamic expert growth/pruning;
- adaptive routing;
- variable/recurrent depth;
- context-window growth;
- memory-tier or paging changes;

as separate model-development hypotheses. Evaluate them with the same protected
boundary, resource constraints, ablations, and rollback discipline as any other
architecture experiment.

## Data-stream governance

Long-lived learning makes data provenance more important, not less.

For each accepted update preserve:

- source identity and time range;
- consent/licence/privacy status;
- preprocessing and filtering version;
- whether examples are human, synthetic, teacher-labelled, or agent-generated;
- duplication/contamination checks;
- domain or replay lane membership;
- the exact examples or fingerprints contributing to the update where policy
  permits.

Do not automatically train on every conversation, file, trace, or outcome merely
because the system can. Qualification and explicit persistence rules still apply.

## Continual-learning experiment ledger

In addition to the normal model-lab experiment fields, record:

- parent promoted checkpoint;
- target/new-domain data window;
- replay/interleaving composition;
- per-parameter-group or adapter learning policy;
- structural changes such as capacity/context growth;
- before/after plasticity metrics;
- before/after retained-domain metrics;
- rollback/revert events and causes;
- final disposition: `promote`, `rollback`, `retain-as-experiment`, or
  `blocked`.

## Case study: mini-AGI

[volotat/mini-AGI](https://github.com/volotat/mini-AGI) is a useful experimental
case study for consumer-hardware continual learning. It demonstrates several
ideas worth testing independently:

- explicit before/after forgetting probes across retained domains;
- interleaved-domain training as a control for catastrophic forgetting;
- differentiated learning rates between shared trunk and specialist parameters;
- held-out-driven learning-rate control;
- best-known-state checkpointing and automatic reversion after degradation;
- evidence-gated context growth;
- dynamic expert growth/pruning;
- disk/RAM/VRAM paging to separate total model capacity from resident GPU
  capacity;
- reproducible probes rather than relying only on qualitative samples.

Treat these as hypotheses and mechanisms, not defaults. mini-AGI describes itself
as a toy-level experimental model, and architecture-specific choices such as
byte-level modelling, recurrent PonderNet depth, dynamic mixture-of-experts
routing, paging, and its particular learning-rate ratios require independent
validation for the target model and workload.

## Promotion gate

Do not promote a continual-learning update unless:

- the intended plasticity gain is material;
- retained capabilities remain within their declared regression envelopes;
- protected evaluation has not been exposed to the update mechanism;
- safety/policy checks remain acceptable;
- the deployed artefact still meets resource constraints;
- the update and rollback path are reproducible;
- repeated updates are not showing an accumulating degradation trend.

If no candidate satisfies both plasticity and retention, stop and change the data,
training method, parameter isolation strategy, or product contract rather than
accepting hidden forgetting.
