---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit or optimize an existing skill, run paired evals, benchmark skill performance and variance, or optimize a skill description for accurate triggering.
compatibility: Requires filesystem access to the skill package. Evaluation and description optimization also require an agent harness capable of matched test runs.
---

# Skill Creator

Create focused, reusable procedural packages and improve them through paired
evaluation. Optimize for measurable task lift, not documentation completeness.

## Core workflow

1. Capture the repeated task, trigger conditions, inputs, outputs, and success
   criteria.
2. Identify the procedural gap the skill must close.
3. Choose the lightest reliable mix of instructions, scripts, references, and
   assets.
4. Write or revise the skill with explicit applicability boundaries and
   validation checks.
5. Compare it against no skill or the previous version on realistic tasks.
6. Remove guidance that adds overhead, encode repeated deterministic work in
   scripts, and retest.
7. Optimize the description and package the skill when useful.

Adapt the sequence to the request. Do not force a full evaluation cycle when the
user wants a quick, judgement-based revision.

## Design principles

### Solve a class of tasks, not one instance

Create a skill only when the workflow or expertise is likely to recur. Complete a
one-off task first; extract a skill afterward only when the reusable procedure is
clear.

Do not turn task-specific filenames, constants, expected outputs, or hidden
verifier details into general instructions. Treat examples as evidence about the
workflow, not an answer key.

### Curate before codifying

Ground non-obvious domain claims in canonical documentation, expert input, or
verified artefacts. Separate confirmed facts from assumptions. Never freeze an
unverified assumption into instructions or a script because it worked once.

### Keep active instructions focused

Include procedural details the agent cannot reliably infer: exact constraints,
domain quirks, invariants, checks, and recovery. Remove generic advice and
repetition.

Keep `SKILL.md` below 500 lines when practical. Move optional, formalism-specific,
or harness-specific detail into files directly linked from `SKILL.md`.

### Match freedom to the task

- Use instructions when judgement and context determine the approach.
- Use parameterized scripts when deterministic steps recur but inputs vary.
- Use tightly constrained scripts when consistency, format, or operation order is
  critical.

Do not mandate a sophisticated tool when a simpler valid route is stronger.

## 1. Capture intent

Extract answers from the conversation and existing artefacts before asking:

1. What recurring task should the skill enable?
2. Which prompts or contexts should and should not trigger it?
3. What inputs, outputs, and exact format constraints apply?
4. Which steps require judgement and which are mechanical?
5. Which canonical sources, quirks, and invariants matter?
6. What does success look like, and can it be checked deterministically?
7. Which edge cases, dependencies, cost limits, or safety boundaries apply?

Ask only for gaps that materially change the design.

## 2. Plan package contents

| Need | Put it in |
| --- | --- |
| Core workflow, selection rules, and applicability boundaries | `SKILL.md` |
| Stable domain knowledge, schemas, and detailed variants | `references/` |
| Repeated deterministic transformation or validation | `scripts/` |
| Templates, icons, boilerplate, and output resources | `assets/` |

### Prefer scripts for repeated deterministic work

Bundle a script when the same inputs, mechanical steps, and verifiable outputs
would otherwise be reconstructed repeatedly. Keep open-ended judgement in
instructions.

For every script:

- define inputs, outputs, exit behaviour, and supported environments;
- parameterize instance data and consequential assumptions;
- avoid hard-coded task answers, paths, and secrets;
- use deterministic, idempotent behaviour where practical;
- validate preconditions, formats, and invariants;
- fail with actionable errors;
- provide a dry run for destructive operations;
- expose a lightweight fallback when the dependency is unavailable;
- test a representative case and an important edge case;
- tell the agent exactly when and how to invoke it from `SKILL.md`.

Prefer runtimes already available in the target environment. Declare dependencies
and preserve an agent-executable fallback when practical.

### Define applicability and complexity

For each non-trivial procedure make these discoverable:

- **Use when** — evidence that justifies the workflow.
- **Avoid when** — cases where direct execution or another tool is better.
- **Fast path** — cheapest reliable route.
- **Full path** — heavier route and why it earns its cost.
- **Fallback** — recovery when a tool or assumption fails.
- **Checks** — format constraints, sanity bounds, and invariants.

## 3. Write the skill

Use this structure:

```text
skill-name/
├── SKILL.md
├── scripts/       # only when needed
├── references/    # only when needed
└── assets/        # only when needed
```

Use lowercase letters, digits, and hyphens for the name. Preserve an existing
skill's name when updating it.

### Frontmatter

Canonical `SKILL.md` frontmatter supports:

- required: `name`, `description`;
- optional: `license`, `compatibility`, `metadata`, `allowed-tools`.

Use `compatibility` only for material environment, product, package, or network
requirements. Keep `metadata` values as strings. Do not add runtime-specific
top-level fields to the canonical skill; store namespaced extension data under
`metadata` or generate a runtime-specific adapter after canonical validation.

Make the description discriminative: state what the skill does, concrete
situations that should trigger it, and boundaries that prevent near-miss
activation. Cover natural paraphrases without keyword stuffing.

### Body

- Write instructions in imperative form.
- Lead with the shortest useful workflow.
- Link optional references directly and state when to read them.
- Name canonical sources and parsing quirks when correctness depends on them.
- State exact interface, file-format, and downstream constraints.
- Surface invariants, plausibility checks, and recovery.
- Mark optional steps and explain when heavier work earns its cost.
- Use concise examples only when they clarify a decision or format.

Avoid deeply nested reference chains. Add a table of contents to long reference
files.

## 4. Evaluate behaviour

Evaluate task completion, not whether the agent read or mentioned the skill.

Use matched paired conditions:

- new skill: skill versus no skill;
- revision: new version versus a snapshot of the previous version;
- same prompt, files, model, harness, environment, and verifier within each pair;
- deterministic checks where possible and human review for subjective quality;
- repeated runs when nondeterminism or consequences justify variance estimates;
- actual deployment harnesses when portability matters.

Start with two or three realistic prompts: a routine case, a boundary or fallback
case, and an important failure-prone case. Expand only after useful lift appears.

Read [references/evaluation.md](references/evaluation.md) before designing,
running, grading, or reviewing evaluations.

## 5. Improve from evidence

Inspect trajectories and artefacts, not only scores. Ask whether the skill:

- added verifier-relevant detail or only context;
- displaced a simpler native strategy;
- mandated a solver or schema that created a dead end;
- caused repeated helper-code reconstruction that should become a script;
- encoded unchecked assumptions or accepted implausible output;
- contained ignored, ambiguous, or unnecessary instructions.

Generalize from failures rather than overfitting prompts. Remove guidance that
does not earn its context or execution cost.

## 6. Optimize triggering when needed

Treat description optimization as a classification problem with realistic
positive prompts and difficult near misses. Optimize on held-out queries and
apply a revision only when it improves activation without broad over-triggering.

Read
[references/description-optimization.md](references/description-optimization.md)
before optimizing a description.

## 7. Validate and package

Run the canonical validator from the parent of the skill directory:

```bash
skills-ref validate ./skill-name
```

Then confirm:

- directory and frontmatter names match;
- required fields are precise and standard optional fields are well formed;
- `SKILL.md` stays within the repository context-budget policy;
- every relative link resolves and no resource is orphaned;
- commands and examples declare runtime and harness assumptions;
- each new or modified script passes representative and edge-case tests;
- a final matched evaluation was run when behaviour materially changed.

Package only when the user or target environment needs an archive. Preserve the
skill directory as the archive root and inspect the archive contents.

## Resources

- [Agent Skills specification](https://agentskills.io/specification)
- [Skill creation best practices](https://agentskills.io/skill-creation/best-practices)
- [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)
- [Using scripts](https://agentskills.io/skill-creation/using-scripts)
- [references/evaluation.md](references/evaluation.md)
- [references/description-optimization.md](references/description-optimization.md)
