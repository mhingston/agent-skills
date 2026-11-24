# Weight-space diagnosis and direct editing (experimental)

Load this reference when `model-lab` is considering either **weight-space
programming** (constructing a task-specific network by specifying its weights)
or **weight-space editing** (changing parameters in an existing checkpoint).
These are distinct, optional methods within the existing model contract,
protected evaluation, experiment ledger and Pareto-selection workflow; neither
is a default replacement for conventional training, and neither grants
permission to modify an accessible checkpoint.

Weight-space editing means reasoning about an existing network's parameters and
proposing specific changes without using a conventional gradient optimizer to
compute them. Weight-space programming instead constructs a network's weights
to implement a task-specific computation, potentially without training on
examples. Both remain exploratory: an editor's diagnosis is a hypothesis, not
proof that a particular tensor causes a behaviour, and a programmed network's
benchmark score is not proof of general correctness.

## 1. Decide whether direct editing is justified

Use this branch only if all of the following hold:

- A concrete model artefact is the desired outcome, not just a one-off claim
  about whether an LLM can infer properties from weights.
- Exact checkpoint and tensor access are available and the operator is
  authorised to inspect, modify and run this model under its licence, privacy
  and deployment rules. A hosted inference API alone is not editable access.
- A reproducible failure and a plausible **localisable** intervention are
  supported by development evidence, not solely a verbal explanation from
  an editing model.
- The task defines independent target, non-target, safety and deployment
  gates, including which regressions veto promotion.
- An isolated execution environment, an immutable base checkpoint, a
  reversible patch format and fixed diagnostic/forward-pass budgets exist.

First test whether the issue is caused or sufficiently solved by generation
settings (especially token limits, sampling and repetition), prompting,
retrieval, data/label quality, calibration, tool use or the harness. Compare
appropriate simpler, LoRA or conventional fine-tuning candidates where
feasible. Do not infer that smaller parameter changes are inherently safer,
cheaper or more generalisable.

Return `No-go` for this method when no defensible local hypothesis exists;
return `Blocked` when rights, checkpoint access, safe execution or reliable
evaluation are unavailable. Continue with the broader `model-lab` candidate
selection when another method remains viable.

## 2. Form a falsifiable intervention

Before making a write, record:

- frozen base checkpoint revision/hash, architecture, tensor names and shapes,
  tokenizer/preprocessor, inference configuration and deployed precision;
- failure definition and development evidence (including how often it occurs);
- causal hypothesis, target components, proposed numerical transformation,
  expected local effect and plausible side effects;
- controls and comparisons: untouched base, cheap decoding/harness fix and
  other appropriate adaptation candidates;
- bounded permitted tensor names/regions, write magnitude or rank, allowed
  forward/activation access, tool calls, compute, spend and stop rules.

The editor can inspect development examples, allowed tensor summaries,
activations and bounded forward-pass feedback where authorised. Treat its
reasoning as a candidate explanation that must survive empirical checks.
Never give it protected evaluation examples, verifier internals or per-case
protected feedback, including through a tool or cached trace.

## 3. Apply a constrained and reversible patch

- Keep the original checkpoint immutable. Work on an isolated copy or a
  versioned delta with no in-place mutation of the canonical artefact.
- Run editor-proposed code in a sandbox with scoped files/tensors, no
  unnecessary network/secrets, resource limits and an explicit allowlist of
  operations. Do not silently execute arbitrary proposed scripts.
- Validate expected tensor names, shape, dtype, finite values, changed-entry
  count, change magnitude and absence of unapproved modifications. Abort
  unexpected writes. Revalidate after serialization and deployed-dtype cast.
- Capture the edit formula/mask or exact tensor delta; source/target tensor
  hashes; parent checkpoint hash; number and share of changed entries;
  editor/model version; code/config revisions; diagnostic and forward-pass
  budgets and actual cost. Avoid making a sparse edit sound safe solely
  because the changed share is small.
- Test deterministic reapplication to the declared base and reversal back to
  the original. A failed replay/revert blocks promotion. Keep patch artefacts
  private unless publication is separately authorised.

Direct editing may not involve a training dataset or loss optimisation, but
all examples and tool feedback used to *choose* the edit are development
material, not protected evidence. Spend limits do not imply permission to
incur external costs. Also apply the relevant execution and final-artefact
checks in [training-execution.md](training-execution.md).

## 4. Evaluate the patched model, not the editor's story

Compare the patched checkpoint against the untouched base under matched
prompts, tool/harness configuration, sampling, budgets and evaluator. Where
a decoding/harness fix addresses the failure, include that cheaper comparator.

Evaluate on development data first. Submit only shortlisted patches to
independent protected confirmation. Require target improvements beyond
measurement noise **and** no unacceptable regression on non-target
capabilities, critical slices, instruction following, calibration (when
relevant), policy/safety, or output validity. Check loop/cut-off rates,
response length and latency when those explain the observed improvement.
If the model is quantized, merged or exported, validate the *actual*
deployed checkpoint with its tokenizer and runtime.

Do not tune the patch through repeated protected evaluations, revise metrics
after seeing failures, or claim a specific cognitive mechanism was improved
when the evidence only supports correcting a decoding/behavioural pathology.
An edited model that fixes one failure can still be worse overall.

## 5. Record the disposition

In the normal `model-lab` experiment ledger, return `promote`,
`retain-on-frontier`, `reject`, `inconclusive` or `blocked`, with the
patch/revert identities, measured comparisons, negative results, residual
uncertainty and a reproducible rollback path. If a later adaptation starts
from the patched model, link the new experiment to that parent checkpoint.
Do not label editor-driven iteration "recursive self-improvement" without
separate evidence that the improvement process itself improved on held-out
model-development tasks.

## 6. Consider weight-space programming for structured algorithms

Weight-space programming is different from editing an existing checkpoint. An
LLM (or another search/programming process) specifies the architecture and
numerical weights of a network so that its forward computation implements a
particular algorithm. A notable variant uses a shared transformer block
repeated for a configured number of steps: the recurrent passes perform
successive stages of an algorithm, so additional computation can increase the
number of steps without increasing the parameter count.

Consider this route only when the task has a crisp, executable specification
and is naturally expressed as a bounded algorithm over structured inputs, for
example graph traversal, path finding, symbolic puzzles or other state
transitions. It is not a general-purpose substitute for language-model
pretraining or fine-tuning.

Before investing in a candidate:

- State the input domain, output contract, supported bounds and exact
  correctness conditions. Distinguish guaranteed coverage from sampled
  benchmark coverage.
- Inspect the proposed architecture, loop/recurrent configuration, numerical
  precision and weight-generation procedure. Record all of them with the
  generated weights so the artefact can be reconstructed.
- Require an independent executable verifier, including edge cases and
  adversarial or boundary inputs. Test beyond the examples used to construct
  or debug the weights; keep a protected set unavailable to the programmer.
- Compare against a straightforward conventional implementation of the
  algorithm, as well as relevant trained-model and prompt/harness baselines.
  A neural implementation is not useful merely because it beats another
  neural model if ordinary code is simpler, faster, smaller or easier to
  verify.
- Measure parameter count, iteration/loop limits, runtime, memory, numerical
  stability and failure behaviour. Treat claims about scaling to larger
  inputs as unverified until those input sizes are independently tested.
- Preserve failed constructions and the exact generation prompt/process,
  model version, architecture/configuration, weights, verifier and test
  identities in the experiment ledger.

Do not let the weight-generating model serve as its own correctness oracle.
Do not expose protected cases or per-case protected feedback during iterative
construction. If the task's correctness can be established more simply with
ordinary code, prefer that solution unless the neural artefact satisfies a
separate, explicit constraint (for example, a required neural execution
substrate).

A weight-space-programmed network is a candidate model artefact, not evidence
that its authoring model has acquired a general algorithmic reasoning ability.
Report benchmark results with their tested domain and limits; do not extrapolate
from finite tests to arbitrary inputs.

## Research provenance

Motivated by Rikiya Takehi et al., [*Sparks of Weight-Space Programming:
LLMs can natively read & write neural network
weights*](https://rikiyat.github.io/blog/weight-space-programming/)
(2 November 2026). The authors publish
[experiment logs and patch reproduction
materials](https://github.com/RikiyaT/lm_understand-logs). Their large
Qwen3.5-0.8B math gain was substantially linked to correcting repetitive
reasoning loops; a Gemma follow-up without that failure saw little gain.
The reported experiments do not establish that direct editing is generally
superior to decoding fixes or conventional adaptation. Recheck the method's
evidence and reproduction details before relying on it for a new model.
