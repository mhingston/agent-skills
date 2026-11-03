# Weight-space diagnosis and direct editing (experimental)

Load this reference only when `model-lab` is considering an LLM-guided
interpretation or **direct change of model parameters** to deliver an adapted
checkpoint. This is an optional method within the existing model contract,
protected evaluation, experiment ledger and Pareto-selection workflow; it is not
a new skill, a default replacement for gradient-based training, or permission
to modify any accessible checkpoint.

Weight-space programming means reasoning about network parameters and proposing
specific edits without using a conventional gradient optimizer to compute those
edits. Early demonstrations are promising but exploratory. Diagnosis is a
hypothesis, not proof that a particular tensor causes a behaviour.

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
