---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit or optimize an existing skill, run paired evals, benchmark skill performance and variance, or optimize a skill description for accurate triggering.
compatibility: Requires filesystem access to the skill package. Evaluation and description optimization also require an agent harness capable of matched test runs.
---

# Skill Creator

Create focused, reusable procedural packages and improve them through paired
evaluation. Optimize for measurable task lift, not documentation completeness.

## Core workflow

1. Capture the repeated task, trigger conditions, inputs, outputs, success
   criteria, any evidence-backed eval seeds from prior runs or learning reviews,
   and relevant prior evolution history when the skill has already been iterated.
2. Identify the procedural gap the skill must close.
3. Choose the lightest reliable mix of instructions, scripts, references, and
   assets.
4. Write or revise the skill with explicit applicability boundaries and
   validation checks.
5. Compare it against no skill or the previous version on realistic tasks,
   including pressure or shortcut cases when the skill enforces discipline.
6. Remove guidance that adds overhead, encode repeated deterministic work in
   scripts, close only failure modes actually observed in evaluation, and retest.
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

### Treat policy-backed skills as projections of owned policy

Apply this only when a skill operationalises an organisational, team, security,
compliance, architecture, or other explicitly governed policy. Do not force
policy machinery onto ordinary procedural or domain-expertise skills.

For a policy-backed skill identify:

- the canonical written policy source or stable source identity;
- the accountable policy owner or owning role;
- the source revision, version, or freshness signal when the policy can drift;
- whether the skill is advisory or backed by an independently enforced control;
- how a policy-source change invalidates or triggers review of the skill.

Do not infer policy authority from repository prevalence, a skill author's role,
or the fact that instructions exist. A skill can explain or operationalise policy
without becoming the authority for that policy, and prose guidance is not an
authorization or enforcement boundary.

When stable, non-sensitive values improve machine inspection, namespaced metadata
may record the relationship, for example:

```yaml
metadata:
  mhingston.policy-backed: "true"
  mhingston.policy-source: "<stable-source-identity>"
  mhingston.policy-owner: "<accountable-role-or-owner>"
  mhingston.policy-enforcement: "advisory"
```

Use `mhingston.policy-enforcement: "deterministic-backed"` only when an external
hook, policy engine, permission boundary, CI gate, or equivalent control actually
enforces the relevant rule independently of model compliance. Keep volatile or
sensitive source details in an appropriate reference instead of metadata.

### Preserve epistemic state when evidence matters

When a skill retrieves or synthesizes factual evidence, make material epistemic
states distinguishable when they can change the result. The skill may use its own
domain-appropriate vocabulary, but it must not silently collapse:

- directly supported claims;
- inference from evidence;
- insufficient or unavailable evidence;
- evidence compatible with multiple materially different interpretations;
- evidence from authoritative sources that conflicts;
- stale or superseded evidence when freshness affects the answer.

Do not require a universal label set when an existing domain model already
expresses these distinctions clearly. Prefer the smallest representation that
preserves the difference and gives the agent an actionable next step: cite the
support, state the inference and falsifier, preserve competing interpretations,
report the conflict, abstain, or retrieve fresher evidence.

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
8. If the skill operationalises governed policy, who owns that policy, what is
   its canonical source/freshness signal, and what is actually enforced outside
   the model?

Ask only for gaps that materially change the design.

When an upstream learning review supplies an `eval_seed`, treat it as a compact
reproduction packet, not as authority for the proposed skill change. Resolve its
source references when available and separate:

- the observed triggering context;
- the evidenced failure, shortcut, or missed behaviour;
- the desired invariant or outcome;
- any near miss or non-trigger;
- the proposed destination or fix, which remains a hypothesis;
- the verifier or observable signal that could distinguish improvement.

Discard or rewrite incidental instance detail that would leak a one-off answer.
Preserve task-specific detail only when it is genuinely part of the invariant or
needed to reproduce the failure.

When the skill already has meaningful candidate-versus-baseline history, prior
rejected interventions, or repeated improvement cycles, read
[references/evolution-memory.md](references/evolution-memory.md) before proposing
another revision. Treat that history as scoped authoring evidence, not as runtime
context or authority for the next edit.

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

Make the description discriminative. Treat it primarily as routing metadata:
state concrete trigger conditions and boundaries that distinguish near misses,
and include only enough capability summary to make discovery reliable. Avoid
encoding a condensed step-by-step workflow in the description when the deployed
harness might execute from metadata without consulting the body. Do not assume
that shortcut exists across harnesses; when description shape is material,
measure it with the routing/shortcut evaluation described below before imposing a
catalogue-wide convention.

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

For repeated improvement cycles, prefer one coherent behavioural hypothesis per
candidate evaluation. Split independent interventions when practical so an
accepted or rejected result remains attributable. Do not bundle unrelated fixes
merely to improve the chance that the aggregate candidate wins.

When an evidence-backed `eval_seed` exists, normally include its failure shape in
the evaluation suite, but do not simply replay a memorisable answer. Preserve the
trigger, failure mechanism, desired invariant, and verifier while generalising
irrelevant names, constants, or paths. Add at least one sibling case or near miss
that tests the same decision rule in a different context when practical. Keep the
original source-linked reproduction as a regression fixture only when exact
instance fidelity is required to demonstrate the historical failure.

The seed does not prove the proposed instruction is correct. Compare the revised
skill against the previous condition and reject changes that merely solve the
seed while degrading routine cases, near misses, portability, or another stated
invariant.

For a discipline-enforcing skill, include pressure cases that make the forbidden
shortcut attractive when that failure mode is realistic. Vary one pressure at a
time where possible, for example time pressure, sunk cost, an apparently obvious
quick fix, contradictory reviewer advice, incomplete evidence, or a request to
skip a required gate. Capture the baseline agent's actual shortcut or
rationalisation before adding counters to the skill. Prefer the smallest general
instruction that closes an observed failure; do not accumulate generic warnings
for hypothetical excuses.

For evidence-sensitive skills, include adversarial cases when materially relevant:

- the plausible or conventional answer is not established by the evidence;
- two materially different interpretations remain consistent with the evidence;
- authoritative sources conflict;
- evidence is incomplete but strongly suggests an answer;
- stale evidence would change the result;
- the correct behaviour is to preserve alternatives, abstain, or request the
  smallest resolving evidence.

Grade unsupported factual claims, source-to-claim traceability, correct handling
of ambiguity and conflict, appropriate abstention, and false certainty in
addition to ordinary task completion. Do not reward a complete-sounding answer
when the evidence contract requires uncertainty to remain visible.

When a description summarizes procedure, or traces suggest that metadata may be
used as a substitute for loading the skill body, run a harness-specific
**description-shortcut test**. Hold the body and task constant and compare a
trigger/boundary-oriented description with the workflow-summary description.
Measure both activation and whether the resulting behaviour follows the full
body rather than a lossy metadata summary. Treat a direct classification exercise
as a routing surrogate only; it cannot establish that the runtime actually loads
or ignores the body.

### Operationalize behavioural regression checks when CI can run a real harness

For repositories that can execute a credentialled deployment or reference
harness in CI, select behaviour-affecting skill changes deterministically from the
pull-request diff and compare each candidate against the exact base-revision skill
package. Keep the gate advisory until case stability and variance justify a
blocking policy.

Do not substitute package validation, Markdown checks, a classifier, or the
presence of an evaluation specification for a real matched harness run. When CI
cannot run the required harness, report behavioural evaluation as unavailable
rather than manufacturing a green check.

Read [references/ci-evaluation.md](references/ci-evaluation.md) before designing
or reviewing changed-skill CI, incident regression suites, advisory/blocking
thresholds, or scheduled portability runs.

Read [references/evaluation.md](references/evaluation.md) before designing,
running, grading, or reviewing evaluations. Use
[references/evaluation-results.md](references/evaluation-results.md) only when a
portable result format or deterministic aggregation earns its overhead; do not
let the helper replace the active harness, evidence review, or a simpler valid
comparison.

## 5. Improve from evidence

Inspect trajectories and artefacts, not only scores. Ask whether the skill:

- added verifier-relevant detail or only context;
- displaced a simpler native strategy;
- mandated a solver or schema that created a dead end;
- caused repeated helper-code reconstruction that should become a script;
- encoded unchecked assumptions or accepted implausible output;
- collapsed insufficient, ambiguous, conflicting, or stale evidence into an
  unjustified conclusion;
- permitted a shortcut or rationalisation actually observed under realistic
  pressure;
- closed the evidenced failure represented by an eval seed without memorising
  its incidental details or degrading sibling and near-miss cases;
- let description metadata substitute for material body instructions in a
  measured deployment harness;
- contained ignored, ambiguous, unnecessary, or purely hypothetical defensive
  instructions.

Generalize from failures rather than overfitting prompts. Remove guidance that
does not earn its context or execution cost. Do not add a prohibition solely
because one can imagine an agent rationalising around the skill; require an
observed failure, credible production incident, or other concrete evidence that
the countermeasure earns its weight.

When evolution memory is in use, record the proposal outcome whether the candidate
is accepted, rejected, inconclusive, or later superseded. Preserve enough model,
harness, suite-revision, skill-revision, regression, and evidence identity to
explain the result without copying the entire trajectory. Rejected candidates are
learning evidence, not runtime instructions; do not retry them unchanged unless
new evidence or changed conditions justify another attempt.

## 6. Optimize triggering when needed

Treat description optimization as a classification problem with realistic
positive prompts and difficult near misses. Optimize on held-out queries and
apply a revision only when it improves activation without broad over-triggering.
When description-shortcut behaviour is material, include that behavioural result
alongside ordinary activation precision and recall rather than optimizing routing
in isolation.

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
- policy-backed skills preserve canonical policy source, owner, freshness, and
  advisory-versus-enforced status without turning the skill into policy authority;
- evidence-sensitive skills preserve material epistemic distinctions without
  forcing redundant status vocabularies;
- each new or modified script passes representative and edge-case tests;
- a final matched evaluation was run when behaviour materially changed and a real
  harness was available, or the missing execution prerequisite is stated plainly;
- evidence-backed eval seeds were source-checked, generalised where appropriate,
  and supplemented with sibling or near-miss cases rather than used as answer
  keys;
- repeated improvement cycles consulted and updated evolution memory when prior
  proposal history was material to the next authoring decision;
- pressure or description-shortcut cases were included when those mechanisms are
  part of the claimed improvement.

Package only when the user or target environment needs an archive. Preserve the
skill directory as the archive root and inspect the archive contents.

## Resources

- [Agent Skills specification](https://agentskills.io/specification)
- [Skill creation best practices](https://agentskills.io/skill-creation/best-practices)
- [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Evaluating skills](https://agentskills.io/skill-creation/evaluating-skills)
- [Using scripts](https://agentskills.io/skill-creation/using-scripts)
- [references/evaluation.md](references/evaluation.md)
- [references/evaluation-results.md](references/evaluation-results.md)
- [references/evolution-memory.md](references/evolution-memory.md)
- [references/ci-evaluation.md](references/ci-evaluation.md)
- [references/description-optimization.md](references/description-optimization.md)