# Training from agent traces

Use this reference when conversation logs, tool-use transcripts, or agent execution
traces are candidates for fine-tuning or alignment. Raw traces are observational
evidence. They are not automatically trustworthy demonstrations.

## Preserve the raw source

Keep an immutable source record for every accepted trace with enough provenance to
reconstruct the environment that produced it:

- run/task ID and timestamp;
- source model and revision;
- harness/runtime revision;
- system/task instructions;
- skill versions and retrieved context versions;
- available tool schemas, permissions, and relevant environment configuration;
- observable messages, tool calls, tool results, and environment outputs;
- human interventions or overrides;
- independent outcome evidence such as tests, verifier results, review findings,
  policy checks, latency, cost, and completion status.

Do not require hidden chain-of-thought. Train from observable state, actions,
messages, tool interactions, public rationale when explicitly available, and
outcomes.

## Remove unsafe or misleading material before derivation

Before a trace can contribute to training, inspect or deterministically screen for:

- secrets, tokens, credentials, customer identifiers, private source, and other
  content that the training environment is not authorised to receive;
- protected evaluation tasks or close variants;
- accidental access to expected answers, hidden tests, reviewer conclusions, or
  other leakage;
- test/evaluator tampering or reward hacking;
- unsupported destructive side effects;
- traces whose final success is accidental or cannot be attributed confidently;
- malformed, truncated, duplicated, or version-ambiguous traces.

Keep rejected traces and rejection reasons in provenance where lawful; do not let
filtering erase evidence about collection quality.

## Qualify behaviour inside successful traces

A successful trajectory can still contain bad actions. Distinguish at least:

- **useful** — causally supported behaviour worth imitating;
- **recovery** — an error followed by useful diagnosis/correction; may be valuable
  when the preceding state is represented honestly;
- **neutral/redundant** — unnecessary loops, repeated reads, verbosity, or retries;
- **harmful** — leakage, policy violations, destructive actions, fabricated state,
  evaluator manipulation, or unjustified edits;
- **unknown** — insufficient evidence to label the action reliably.

Do not train every step of a successful run as positive behaviour merely because
the final verifier passed.

## Build versioned training views

Preserve raw traces separately and derive explicit versioned views for a chosen
training objective.

### SFT / behavioural cloning

Use when there are trusted demonstrations of the behaviour the target model should
produce.

A useful unit is often:

```text
observable state + instructions + available tools -> desired next message/action
```

or a short verified sub-trajectory rather than the entire run.

For tool-using models preserve the exact tool schemas expected by the target
runtime and represent tool calls/results using the target model/provider's
supported chat template or dataset format.

SFT is strongest when the desired action is actually known. Do not convert an
ambiguous branch into an SFT target just because one historical agent chose it.

### Preference optimization / DPO-style data

Use when two outputs/actions are comparable from sufficiently similar states and
there is defensible evidence that one is preferable.

Potential evidence includes:

- explicit human preference;
- independent task/verifier outcome;
- lower-risk policy-compliant behaviour with equivalent correctness;
- materially lower cost or latency when quality is equivalent and efficiency is
  part of the contract.

Record the basis for each `chosen` / `rejected` pair. Do not manufacture weak
preference pairs by comparing unrelated tasks or substantially different states.

### Reinforcement fine-tuning / agent RL

Use when the current policy can generate fresh rollouts in an environment and a
reward or verifier can be applied reliably enough to guide learning.

Before using RL/RFT, test the reward for shortcuts. Prefer objective executable
signals such as hidden tests, simulators, deterministic constraints, or other
independent outcome checks where the task supports them. LLM judges may be useful
components but should not silently become the sole oracle for consequential
behaviour.

Keep reward components explicit. A reward such as:

```text
correctness + policy compliance - excessive cost
```

is only valid when those terms and their trade-offs were accepted before training.
Do not tune the reward after inspecting protected failures merely to make a
candidate score well.

### Distillation

A stronger model's trace can seed a smaller or cheaper target when:

- the teacher trace is independently verified;
- teacher identity and prompting/harness context are recorded;
- the target's intended tool/runtime contract is compatible;
- protected tasks are excluded;
- generated data remains labelled as teacher-generated rather than human truth.

Use rejection sampling, verifier filtering, or human review where appropriate
before teacher outputs enter the training view.

## Split at the right unit

Random row-level splitting is often unsafe for agent data. Group related examples
before assigning train/development/protected roles.

Possible grouping keys include:

- original task or issue;
- repository and commit family;
- conversation/session lineage;
- generated task seed/template;
- user/customer/entity;
- time window when deployment drift matters.

All segments derived from one trace belong to the same split. Near-duplicate tasks
and reruns should not cross the train/protected boundary.

## Keep training/evaluation harnesses distinct

Training examples may contain historical tool calls and results, but promotion
should occur on fresh protected tasks executed by the candidate model in the
actual target harness whenever the product outcome is agent behaviour.

Compare the fine-tuned model against the untouched base model with matched:

- system/task instructions;
- skill/context versions;
- tool schemas and permissions;
- inference budgets and sampling settings;
- environment/task versions;
- verifier and termination policy.

This distinguishes genuine weight-adaptation gains from unrelated harness or
prompt changes.

## Managed/cloud training

The training-data contract is independent of the backend. Local Hugging Face/TRL,
rented GPU compute, Microsoft Foundry, Azure Machine Learning, or another managed
service can execute the training when they satisfy the model contract.

For every managed training backend verify the current provider documentation at
execution time for:

- supported base models and customization methods;
- accepted dataset schemas and file limits;
- region and data-residency behaviour;
- RBAC/identity and storage permissions;
- quota, pricing, job limits, and deployment availability;
- data retention, abuse-monitoring, and provider training-data terms relevant to
  the corpus;
- whether SFT, preference optimization/DPO, reinforcement fine-tuning, LoRA/PEFT,
  or full-weight training is actually available for the chosen model.

Provider support changes frequently. Record the verified provider/model/method and
date in the experiment ledger rather than treating a copied compatibility matrix
as durable guidance.

For Microsoft-managed fine-tuning in particular, treat Microsoft Foundry or Azure
Machine Learning as execution backends. Use the same local data qualification,
protected evaluation, provenance, and promotion contract; a successful provider
job is not itself evidence that the model improved.

## Minimum trajectory training record

For a derived training view record:

```text
view_id
source_trace_set_version
source model/harness/skill/tool versions
filter and redaction rules
split/grouping policy
training objective: SFT | preference | RL/RFT | distillation | other
transformation code/config revision
example/pair/trajectory counts
licence/privacy/approval status
base model and target chat/tool template
provider/runtime export format
```

For each training run also record the provider or runtime job ID, base model
revision, hyperparameters, adapter/full-training choice, training-data fingerprint,
observed cost, and resulting model/deployment identifier.

## Stop conditions for trace-derived training

Stop or return `Blocked` when:

- provenance or authorisation for the traces is insufficient;
- redaction would remove the information needed to learn the task;
- protected-task contamination cannot be bounded;
- no reliable target, preference, reward, or teacher-verification signal exists;
- a managed provider cannot satisfy data residency or handling constraints;
- the candidate does not outperform the untouched base under matched protected
  evaluation after the declared budget;
- improvements depend on leakage, reward exploitation, or task-specific memorisation.
