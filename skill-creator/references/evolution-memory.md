# Skill Evolution Memory

Read this file when revising a skill that already has meaningful evaluation history,
prior rejected proposals, or repeated evidence-backed improvement cycles.

The purpose is to preserve **compiled authoring knowledge** across iterations without
turning the runtime skill into a history log or exposing all developmental context to
the task-executing agent.

## Principles

- Keep the executable skill as the compact compiled behaviour, not the learning
  history that produced it.
- Preserve accepted, rejected, inconclusive, and superseded proposals when they carry
  reusable information for later authoring.
- Treat prior outcomes as scoped evidence, not universal truths. Model, harness,
  evaluation-suite revision, environment, and skill revision can change the result.
- Prefer one coherent behavioural hypothesis per evaluation iteration so an outcome
  remains interpretable.
- Revisit a rejected intervention only when new evidence, changed execution
  conditions, or a materially different hypothesis justifies it.
- Do not let evolution memory authorize a skill edit. Current evidence and matched
  evaluation still decide whether a proposed revision should survive.

These principles are informed by the separation used in WikiSkill, where persistent
compiled knowledge supports skill evolution while the task-executing agent receives
the distilled skill rather than the entire learning substrate:
https://arxiv.org/html/2608.27454v1

## When to create or consult it

Use evolution memory when at least one of these is true:

- the skill has undergone more than one meaningful candidate-versus-baseline cycle;
- a prior candidate was rejected for a reusable reason;
- several evidence sources point to the same unresolved behavioural pattern;
- another model, harness, or author is continuing an earlier improvement effort;
- a historical failure is likely to be rediscovered or a failed intervention is
  likely to be retried accidentally.

Do not create a ledger for a one-off wording change or a skill with no meaningful
behavioural history. Small evals can keep their evidence inline until the history
becomes worth preserving.

## Storage boundary

Prefer an existing project learning registry, evaluation workspace, or other durable
authoring store. When repository persistence is appropriate, keep the evolution
record outside the runtime skill package using the repository's established
convention.

Do not add an ever-growing history to `SKILL.md`, and do not place proposal logs under
a skill's `references/` merely because that directory exists. A reference belongs in
the runtime package only when the task-executing agent needs that stable knowledge to
perform the skill.

Keep raw trajectories, transcripts, secrets, personal data, and bulky eval artefacts
outside the compiled ledger unless exact reproduction requires them. Preserve stable
references instead.

## Compact record shape

Use the smallest representation that prevents rediscovery. A Markdown ledger is
usually sufficient; use structured data only when deterministic querying or
aggregation earns the overhead.

### Pattern

Record a reusable observation, not a one-off answer:

```yaml
pattern_id: ambiguous-evidence-collapsed
status: active # active | resolved | contradicted | superseded
summary: Agent collapses two evidence-compatible interpretations into one conclusion.
first_seen: <stable source or timestamp>
last_seen: <stable source or timestamp>
evidence_refs:
  - <eval, incident, feedback, or review reference>
notes: <scope, contradiction, or current understanding when useful>
```

Stable pattern IDs should describe the behavioural mechanism rather than a task-
specific filename, prompt, or expected answer.

### Proposal outcome

Record each material intervention whether it is accepted or rejected:

```yaml
proposal_id: preserve-competing-interpretations-v1
target_patterns:
  - ambiguous-evidence-collapsed
hypothesis: Making competing interpretations explicit will reduce false certainty without increasing unnecessary abstention.
baseline_skill: <path, commit, immutable revision, or stable label>
candidate_skill: <commit, diff, workspace reference, or stable label>
evaluation_suite: <suite identity>
evaluation_suite_revision: <revision or null>
authoring_model: <model that proposed or synthesized the change, when relevant>
runs:
  model: <task-execution model or null>
  harness: <harness and version or null>
  environment: <material execution conditions or null>
outcome: rejected # accepted | rejected | inconclusive | superseded
result_summary: <paired lift, regression, trade-off, or reason evidence was insufficient>
regressions:
  - <material loss or cost>
evidence_refs:
  - <matched results, outputs, trajectory, human review, or CI reference>
```

`authoring_model` and the task-execution `model` answer different questions. Record
both only when the distinction is material; do not invent unavailable provenance.

## Authoring loop

Before changing a repeatedly evaluated skill:

1. Resolve the current source skill and exact baseline revision.
2. Read active patterns and prior proposal outcomes relevant to the requested change.
3. Check whether a later revision already resolved, contradicted, or superseded the
   historical evidence.
4. State one coherent behavioural hypothesis for the iteration. If several
   independent interventions are needed, split them when practical so the eval can
   identify which change caused the result.
5. Make the smallest general change that tests that hypothesis.
6. Run the normal matched evaluation against the current baseline using the same
   prompt, model, harness, tools, environment, and verifier within each pair.
7. Record the proposal outcome even when the candidate is rejected or inconclusive.
8. Update pattern status only when the new evidence supports it; do not mark a
   pattern resolved merely because a candidate was accepted.
9. Carry forward only the distilled behaviour into the executable skill.

A rejected proposal remains useful when it establishes that a particular
intervention caused a regression, added unjustified overhead, failed to close the
pattern, or depended on conditions that no longer hold.

## Relationship to `session-lessons`

`session-lessons` discovers and qualifies recurring evidence and may hand
`skill-creator` a source-linked `eval_seed`. Evolution memory is narrower: it records
what happened **after authoring hypotheses were tried** so future iterations do not
lose accepted and rejected experimental knowledge.

Do not inflate recurrence counts with several candidate runs from the same underlying
pattern. Evaluation trials are evidence about an intervention, not independent
session-level occurrences by themselves.

## Relationship to Skillet

Skillet feedback and immutable revision identity can supply evidence for patterns, but
pre-publication candidate history remains an authoring concern.

Do not publish a rejected candidate as a Skillet revision merely to preserve its
proposal history. Once an accepted candidate becomes an admitted immutable revision,
a publisher may attach revision-bound efficacy evidence according to Skillet's
contract, with the authoritative detailed evaluation remaining external.

This keeps the boundary clear:

```text
runtime experience / revision-bound feedback
        -> learning evidence
        -> authoring evolution memory
        -> candidate skill
        -> matched evaluation
        -> accepted runtime skill revision
```

## Stop conditions

Do not extend the ledger when:

- the proposed entry repeats existing evidence without changing current
  understanding;
- the intervention was trivial and has no reusable lesson;
- the source cannot be tied to a stable skill/evaluation identity where that identity
  matters;
- the record would primarily duplicate raw output rather than compile a reusable
  lesson;
- the history is being used to justify injecting developmental context into every
  runtime execution.

The ledger has earned its cost when it helps an author avoid rediscovering a known
failure, distinguish a new hypothesis from an old rejected one, or carry valid
learning across models, harnesses, sessions, and skill revisions.
