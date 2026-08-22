---
name: gauntlet-loop
description: Execute large or quality-sensitive work through dependency-aware fan-out, independent adversarial verification, and bounded producer-critic loops against an explicit acceptance contract. Use when asked to implement, build, refine, or substantially improve an artifact to a demanding quality bar and there is a credible specification, answer key, reference, executable oracle, or other acceptance source. Do not use to invent materially unresolved requirements or as a substitute for planning.
---

# Gauntlet Loop

Drive a complex piece of work to a **verified quality bar**, not merely to agent
satisfaction.

Decompose the outcome into independently workable parts where safe, assign focused
producers, verify each candidate against the same explicit acceptance contract
using fresh adversarial critics, iterate on concrete failures, then integrate the
parts and verify the whole system again.

The Gauntlet Loop is an **execution and verification workflow**. It is not a
planning method and it is not an instruction to retry indefinitely.

## Core invariant

The producer never decides that its own work is good enough.

Advancement requires evidence against a quality bar that existed independently of
the candidate being judged.

Never replace this with:

- "looks good";
- "seems production ready";
- a producer's confidence score;
- a critic inventing new requirements;
- an arbitrary numerical quality score;
- repeated retries without new evidence;
- "keep going until perfect."

## Route adjacent work

Use `gauntlet-loop` when the primary task is **execution against a sufficiently
clear quality bar**.

Use another workflow when the primary task is:

- resolving what should be built or clearing substantial planning fog: use a
  planning or wayfinding workflow;
- designing the orchestration system itself: use an agent-workflow-design
  workflow;
- reviewing an existing change without modifying it: use a review workflow;
- making one small, local, easily verified change: execute it directly rather
  than introducing ceremonial fan-out.

A Wayfinder map, product specification, issue, approved plan, acceptance-test
suite, design reference, golden dataset, or other planning artifact may provide
the Gauntlet Loop's acceptance source. The skill does not require any particular
planning workflow.

## 1. Establish the acceptance source

Before decomposing work, identify the source or sources that define success.

Apply explicit authority rather than silently combining conflicting sources.
Typical sources include:

1. explicit user requirements and constraints;
2. an approved specification, answer key, plan, or decision record;
3. executable acceptance tests or deterministic invariants;
4. reference artifacts, products, examples, screenshots, datasets, or behaviours;
5. repository and domain conventions;
6. subjective quality judgement only for properties that cannot be established
   more directly.

Read [references/acceptance-contract.md](references/acceptance-contract.md) when
the acceptance source is distributed, subjective, reference-based, or otherwise
non-trivial.

Produce a compact **Acceptance Contract** containing stable criterion identifiers
(`R#`). For every material criterion record:

- the required outcome;
- whether it is mandatory or advisory;
- the authoritative source;
- what evidence can pass it;
- what evidence can fail it;
- whether verification is deterministic, semantic, comparative, or human-owned;
- applicable constraints or tolerances;
- any exact state, revision, artifact, dataset, or environment to which the
  evidence must be bound.

Do not invent missing product intent merely to make the contract complete.

### Acceptance-source gate

Return `Blocked` before implementation when:

- a material requirement remains ambiguous enough to change what should be built;
- authoritative sources materially conflict;
- the only available quality bar would be the executing agent's own judgement;
- a consequential criterion has no credible way to determine pass or fail.

State the missing decision or evidence and route the work back to planning,
wayfinding, research, prototyping, or the accountable human.

## 2. Resolve execution state and boundaries

Inspect enough current state to know what is actually being changed.

Record where relevant:

- repository, workspace, artifact, or source revision;
- current branch or work item;
- dirty or concurrent state;
- permitted mutation scope;
- protected files or control-plane artifacts;
- commands and environments available for verification;
- external side effects;
- cost, token, attempt, latency, or concurrency limits supplied by the user or
  environment.

Do not let a worker modify the acceptance contract, evaluator configuration, test
oracle, policy, or other machinery used to judge that same worker unless the
change itself is explicitly in scope and independently verified.

## 3. Build the work graph

Decompose by **independently verifiable outcomes**, not by maximizing agent count.

For each work item define:

- `W#` identifier and outcome;
- acceptance criteria it contributes to;
- dependencies;
- inputs and relevant context;
- expected outputs or artifacts;
- mutable state or write set;
- verification available locally;
- integration contracts with other work items;
- whether it may execute concurrently.

Prefer vertical or behaviourally coherent slices. Do not create separate agents
for mechanical actions whose execution is already deterministic.

### Parallelism gate

Run mutating work in parallel only when:

- dependencies permit it;
- workers have isolated mutable state or non-overlapping enforced write sets;
- shared contracts are already sufficiently defined;
- there is an explicit integration owner.

If those conditions do not hold, sequence the work. Read-only investigation or
review may still fan out where useful.

## 4. Run a producer-critic loop per work item

Each eligible work item follows the same loop.

### 4.1 Produce

Give the producer:

- its single `W#` outcome;
- relevant `R#` criteria;
- exact allowed scope;
- required interfaces and dependencies;
- available evidence;
- required verification commands;
- known constraints.

Do not give it responsibility for deciding whether the result passes.

The producer may investigate and implement within its scope. It should return:

- what changed or was produced;
- exact candidate identity or revision;
- verification it ran;
- remaining uncertainty;
- any discovered evidence that could invalidate the work graph or acceptance
  contract.

### 4.2 Run deterministic gates first

Before spending semantic-review capacity, independently run applicable mechanical
checks such as:

- schema or parser validation;
- compilation and type checking;
- linting and static analysis;
- unit, contract, integration, or end-to-end tests;
- security scanners;
- golden-data comparison;
- benchmark or performance thresholds;
- artifact existence, shape, dimensions, or metadata checks;
- actual diff or write-set verification.

A command executing successfully does not imply the underlying criterion passed.
Record the observed result.

When a deterministic gate fails, return its concrete failure evidence to the
responsible producer without asking a critic to rediscover it.

### 4.3 Critique in a fresh context

For criteria that require semantic or comparative judgement, dispatch a **critic**
that did not produce the candidate.

Read [references/critic-contract.md](references/critic-contract.md) before
dispatching semantic critics.

Give the critic:

- the immutable acceptance-contract slice;
- candidate identity and evidence;
- only the context needed to judge the criteria;
- reference artifacts when applicable;
- deterministic gate results.

Do not provide producer self-justification unless it is itself evidence required
by the contract.

The critic is read-only with respect to the candidate. Its task is to **find
reasons the candidate does not satisfy the contract**, not to improve or rewrite
the work.

The critic returns criterion-level results:

- `pass`;
- `fail`;
- `unverified`.

Every result must include evidence.

A harsh tone is unnecessary. Adversarial evidence-seeking is the required
property.

### 4.4 Correct concrete failures

If mandatory criteria fail and correction remains within scope, send the producer:

- failed criterion IDs;
- exact observed evidence;
- the smallest useful explanation of the gap;
- constraints that still apply.

Do not send vague instructions such as "make it better" or "try harder."

Create a new candidate and rerun every gate whose evidence the change could have
invalidated. Evidence from an old revision does not automatically transfer to a
new one.

## 5. Bound the loop

Gauntlet Loop is not an infinite retry primitive.

Continue a producer-critic loop only while attempts are producing materially new
evidence or reducing the gap to acceptance.

Stop the affected work item when any of these occurs:

- every mandatory criterion passes;
- an attempt or resource budget is exhausted;
- materially equivalent approaches have failed twice without new evidence;
- the same failure repeats without meaningful progress;
- fixes oscillate between previously seen states;
- satisfying one mandatory criterion necessarily violates another;
- the critic requires evidence or capability unavailable to the harness;
- the work discovers a material requirement or architecture decision that was not
  actually settled;
- continuing would expand scope or authority beyond the user's request.

Classify the stop as `Blocked` or `Exhausted` rather than claiming completion.
Capture the best-known candidate, failures, attempts, and the exact decision or
evidence needed next.

## 6. Compare against references correctly

A reference product or artifact may be part of the acceptance contract, but it
does not become an unlimited instruction to copy it.

For reference-based evaluation:

1. identify the exact properties being compared;
2. normalize environment and inputs where practical;
3. compare equivalent states or scenarios;
4. retain objective checks separately from subjective judgement;
5. record material ways the comparison is not equivalent.

Examples include visual hierarchy, interaction responsiveness, animation quality,
information density, error behaviour, accessibility, output quality, latency, or
fidelity to a supplied example.

### Blind comparison

Call a comparison **blind** only when the harness actually conceals candidate
identity from the evaluator, for example by randomizing neutral labels and
withholding provenance.

If true blinding is unavailable, perform an ordinary reference comparison and
state that limitation.

Never claim that a critic performed a side-by-side visual comparison unless it
actually received both renderable artifacts.

## 7. Integrate verified work

Passing local work items does not establish that the integrated result passes.

An explicit integration owner combines accepted work items in dependency order.
After integration:

1. bind the integrated candidate to an exact identity or revision;
2. verify cross-work-item interfaces and contracts;
3. rerun deterministic checks affected by integration;
4. run end-to-end acceptance criteria;
5. run a fresh final semantic critic for applicable global criteria;
6. inspect for regressions introduced by composition.

Do not allow parallel workers to integrate their own competing changes into shared
state without a coordinating owner.

If integration changes a locally verified artifact, its old verification becomes
stale for the changed properties.

## 8. Run the final Gauntlet

The final candidate must face the acceptance contract as a whole.

For every mandatory `R#` criterion record one of:

- `pass` — sufficient current evidence supports it;
- `fail` — current evidence contradicts it;
- `unverified` — available evidence cannot establish it.

Trace every pass to actual evidence. Do not turn absence of a reported defect into
a pass.

Where applicable, challenge the final result from multiple independent dimensions
rather than asking one critic to produce a global vibe score. Select only
dimensions justified by the acceptance contract and artifact, such as correctness,
specification alignment, usability, visual quality, security, accessibility,
performance, operational resilience, or maintainability.

## Harness adaptation

The protocol is authoritative; harness-specific features are optional accelerators.

### Subagents available

Fan out independent producers and critics up to the harness's safe concurrency
limit. Prefer one focused responsibility per producer, fresh critic contexts,
isolated workspaces for concurrent writers, and one integration owner.

Do not create nested delegation unless the harness can preserve the same
acceptance, isolation, budget, and provenance rules.

### No subagents

Execute work items sequentially.

Use a fresh context for criticism when the harness supports it. Otherwise maintain
separate producer and critic passes in the current context and report
`single-context verification`.

Do not claim reviewer independence that did not exist.

### Native loop commands

A harness may provide commands such as `/loop`, agent graphs, background workers,
teams, swarms, or other orchestration features.

Use them when they preserve this skill's contracts, but do not make the workflow
depend on their names or existence. Keywords such as `ultracode` are
harness-specific hints, not part of the Gauntlet Loop protocol.

## Artifact storage

Persistence is optional for small runs.

When durable artifacts materially improve long-running or multi-agent execution
and the repository already supports the canonical ignored artifact namespace, use:

```text
<repository-root>/.agent-artifacts/<work-branch>/gauntlet-loop/<run-id>/
```

Typical contents:

```text
acceptance-contract.md
work-map.md
evidence/
attempts/
final-report.md
```

Do not modify repository ignore rules merely to persist Gauntlet Loop state.

If the canonical artifact location is unavailable, keep the state in the harness's
supported workflow state or return it inline rather than inventing a new
repository convention.

## Output contract

Return the smallest result that preserves:

1. **Status** — one of `Verified`, `Partial`, `Blocked`, or `Exhausted`.
2. **Candidate** — exact artifact, revision, or state that was evaluated.
3. **Acceptance summary** — every mandatory `R#` with `pass`, `fail`, or
   `unverified`.
4. **Work graph** — completed work items, dependencies, and execution mode.
5. **Verification evidence** — deterministic checks and semantic or comparative
   evaluations actually performed.
6. **Iteration summary** — attempts that materially changed the candidate or
   evidence; omit noisy internal churn.
7. **Limitations** — unavailable tools, non-independent critics, non-blind
   comparisons, stale evidence, or criteria that could not be established.
8. **Next action** — only when status is not `Verified`; identify the exact
   missing decision, evidence, correction, or escalation.

`Verified` means that available evidence establishes every mandatory criterion for
the exact reported candidate. It is not a guarantee of perfection and does not
replace accountable human approval where one is required.

## Stop conditions

Do not report `Verified` when:

- any mandatory criterion fails or remains unverified;
- evidence refers to a superseded candidate;
- a worker judged its own semantic work without independent verification where
  independence was required;
- deterministic checks expected by the contract were skipped without an explicit
  limitation;
- integration invalidated prior evidence;
- requirements changed during execution without revalidating the acceptance
  contract;
- the final judgment depends on an invented quality bar.

When the destination itself is still in the fog, stop the Gauntlet Loop and go
find the way first.
