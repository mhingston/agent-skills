# Workflow guide

The catalogue is intentionally composable rather than one mandatory software
delivery lifecycle. Use this guide to choose a starting capability, understand
which skills commonly compose, and avoid adding ceremony merely because related
skills exist.

Start with the **smallest workflow that owns the outcome**. Add another skill or
agent only when it contributes a distinct decision, evidence source, control, or
handoff that the current workflow does not already own.

For exact behaviour, applicability boundaries, and outputs, the relevant
`SKILL.md` or agent definition remains authoritative. This guide is an onboarding
and navigation aid, not a second specification for the skills.

## Start here

Use the first branch that matches the problem you are trying to solve.

```text
Are you trying to change software?
├─ Work is not ready or requirements are unclear
│  └─ refine
├─ A concrete bug/regression exists but its cause is unclear
│  └─ fault-isolation
├─ The implementation approach needs a separate investigation/design pass
│  └─ plan
├─ Work is ready to implement
│  └─ implement
└─ You need the formal PR evidence + human-verdict lifecycle
   └─ pr-review

Are you improving an agent-enabled engineering environment?
├─ How much autonomy can this repository safely support?
│  └─ agent-readiness
├─ How should agents coordinate, hand off, resume, and terminate?
│  └─ agent-workflow-design
├─ How should runs become reconstructable and observable?
│  └─ agent-observability
├─ How should durable project truth and intent be organised?
│  └─ project-context
└─ Do repository relationships justify a semantic model?
   └─ repository-ontology

Are you improving recurring work or protecting engineering attention?
├─ What recurring work should become automation?
│  └─ audit-me
├─ What engineering work needs attention now?
│  └─ engineering-attention
├─ Does an existing automation still earn its cost and trust?
│  └─ automation-reviewer
└─ What factual engineering outcomes should be preserved for later?
   └─ engineering-evidence

Are you reflecting on your own behaviour?
├─ Improve how you frame, steer, verify, and recover AI work
│  └─ coach-me
└─ Examine broader longitudinal patterns, blind spots, and trajectory
   └─ reflection-engine

Are you learning or improving from experience?
├─ Capture evidence from one completed session
│  └─ wrap-up
├─ Find recurring patterns across sessions or PR lifecycles
│  └─ session-lessons
├─ Create or improve a reusable skill and evaluate the change
│  └─ skill-creator
└─ Adopt a useful mechanism from an external source
   └─ adopt

Are you reviewing or investigating rather than implementing?
├─ Review one concrete code change
│  └─ review
├─ Diagnose a concrete failure
│  └─ fault-isolation
├─ Establish uncertain runtime/library behaviour experimentally
│  └─ code-research
├─ Reconcile a merge/rebase/cherry-pick conflict
│  └─ integration-reconciliation
└─ Preserve or recover accepted/rejected/deferred direction
   └─ decision-continuity
```

If several branches appear relevant, choose the workflow that owns the **current
blocking decision**. Do not run every adjacent capability up front.

## How composition works

These relationship terms describe common composition without turning skills into
hard dependencies.

| Relationship | Meaning | Example |
| --- | --- | --- |
| **Precedes** | One workflow commonly produces evidence or a contract that another can consume. | `fault-isolation` precedes `implement` when the causal mechanism is unknown. |
| **Complements** | Two capabilities answer different questions and may be useful together. Neither owns the other. | `project-context` complements `decision-continuity`. |
| **Alternative** | Choose one based on scope; running both mechanically usually adds duplicate work. | `review` versus `pr-review`. |
| **Owned stage** | An internal module belongs to an orchestrating agent and is normally not invoked independently. | `implement-ticket` is owned by `implement`. |
| **Escalates to** | A workflow reaches a responsibility boundary and hands an unresolved decision to the appropriate owner. | `review` can redirect an unresolved system-level architecture decision rather than settling it locally. |

Composition is contextual. A documented sequence is a likely route, not a
requirement to invoke every stage.

## Common workflows

### Deliver a software change

```text
refine → [plan] → implement → [pr-review]
```

Use `refine` when the selected work is not yet agent-ready. Add `plan` only when
implementation uncertainty deserves a separate non-mutating investigation or
design pass. `implement` already owns bounded implementation, technical review,
contract reconciliation, final project gates, and pull-request creation. Add
`pr-review` when the formal independent PR evidence and human-verdict lifecycle
is required.

Skip stages whose decision is already resolved by authoritative evidence.

### Diagnose and fix a bug or regression

```text
fault-isolation → [plan] → implement
```

Use `fault-isolation` when the symptom is concrete but the causal mechanism is
not established. Carry its supported root cause, minimised reproducer, and
candidate regression oracle forward. Add `plan` only when the fix still has
meaningful design uncertainty.

If the defect and independent regression oracle are already known, start closer
to implementation rather than replaying diagnosis.

### Review a change

Choose one primary review workflow:

```text
review
```

for a standalone technical review, or:

```text
pr-review
```

for the orchestrated PR evidence, comprehension, human judgement, and verdict
lifecycle.

`pr-review` may use technical review internally; do not add a second standalone
`review` merely because both names exist. Use `review-calibration` later, across
historical evidence, when the goal is to improve review policy rather than review
one change.

### Reconcile a conflicted Git integration

```text
integration-reconciliation
```

Treat this as a standalone workflow for an active merge, rebase, or cherry-pick.
It reconstructs both sides' intent, composes compatible changes, validates the
integrated state, and blocks rather than inventing a product decision.

### Adopt coding agents in a repository

```text
agent-readiness → targeted remediation → reassess
```

`agent-readiness` assesses the highest safely supported autonomy; it is not a
universal remediation workflow. Route each material gap to the capability that
owns it, for example:

- project truth and durable intent → `project-context`;
- semantic repository relationships → `repository-ontology`;
- agent coordination and state → `agent-workflow-design`;
- correlated run evidence → `agent-observability`;
- objective coding-rule drift → `code-conventions`.

Reassess after targeted remediation rather than assuming every possible control
must be installed.

### Design an agent system

```text
[agent-readiness] → agent-workflow-design → [agent-observability]
```

Use `agent-workflow-design` for the workflow/state-machine contract. Add
`agent-readiness` when the environment's safe autonomy level is itself uncertain.
Add `agent-observability` when the system needs reconstructable execution,
revision-aware traces, or operational evidence.

Use `programmatic-tool-calling` for a bounded repeated multi-tool stage rather
than as a substitute for the whole workflow runtime. Use `dynamic-workflows`
when Mastra is specifically the executable runtime, not for runtime-neutral
design.

### Maintain durable project context

```text
project-context + decision-continuity + [repository-ontology]
```

These capabilities complement one another but do not form a mandatory pipeline:

- `project-context` owns the durable substrate and source-authority model;
- `decision-continuity` protects accepted, rejected, deferred, and superseded
  direction across resumed work;
- `repository-ontology` is optional when semantic traversal or deterministic
  relationship validation earns its maintenance cost.

Do not let memory, ontology, generated views, or trackers silently become a
second source of truth for claims governed elsewhere.

### Maintain shared organisational memory

```text
memory-recall → work → memory-capture → periodic memory-maintenance
```

Shared memory supports retrieval and continuity outside one project record.
`memory-maintenance` repairs duplicate, stale, conflicting, or weakly sourced
memory. The memory layer remains subordinate to explicitly authoritative project,
policy, architecture, or operational sources for the same claim.

### Improve skills from experience

```text
wrap-up → session-lessons → skill-creator
```

`wrap-up` captures evidence from one completed session. `session-lessons` looks
for recurring patterns across independent evidence units and recommends where
mature lessons belong. `skill-creator` creates or revises a skill and evaluates
whether the change actually improves behaviour.

A validated escaped defect may seed an evaluation immediately, but one ordinary
observation does not automatically justify a durable instruction or new skill.

### Adopt an external practice

```text
adopt → existing owning capability → skill-creator evaluation
```

Use `adopt` to extract evidence-backed mechanisms rather than copy another
project's terminology or workflow wholesale. Prefer strengthening the existing
skill or agent that already owns the responsibility. Add a new skill only when
the source reveals a genuinely distinct reusable contract.

### Execute quality-sensitive parallel work

```text
accepted plan/specification → gauntlet-loop
```

Use `gauntlet-loop` when dependency-aware fan-out and independent adversarial
verification earn their overhead. It does not replace planning, source authority,
or accountable human decisions.

## Useful complements that are not pipelines

Some skills are most useful as optional lenses or support capabilities rather
than fixed lifecycle stages.

| Need | Capability | Typical use |
| --- | --- | --- |
| Understand repository history | `git-archaeologist` | Prioritise where deeper investigation is worthwhile. |
| Find stewardship or reviewer context | `contributor-analysis` | Identify evidence-backed contacts or coverage gaps without ranking people. |
| Discover and codify objective conventions | `code-conventions` | Turn worthwhile norms into the lightest deterministic enforcement. |
| Configure language-server support | `lsp-config` | Reconcile repository language detection with editor/harness LSP configuration. |
| Surface current engineering attention | `engineering-attention` | Produce a bounded brief of blockers, commitments, stale work, and review obligations. |
| Preserve factual engineering outcomes | `engineering-evidence` | Capture outcomes and reliability evidence without performance judgement. |
| Analyse customer journey friction | `customer-friction-radar` | Combine customer and operational evidence into validated friction findings. |
| Synthesize fragmented organisational evidence | `organisational-intelligence` | Build a traceable decision brief from mixed organisational sources. |

Use these when their specific evidence or decision is needed; they are not
prerequisites for ordinary delivery.

## Anti-workflows

Avoid these common composition mistakes:

- **Do not run every agent-platform skill by default.**
  `agent-readiness → agent-workflow-design → agent-observability → project-context
  → repository-ontology` is not a maturity ladder. Start with the current gap.
- **Do not stack `review` and `pr-review` mechanically.** Choose the workflow that
  owns the desired review lifecycle.
- **Do not chain `audit-me → engineering-attention → automation-reviewer` by
  default.** Choose by lifecycle: discover/design an automation, run a current
  attention brief, or evaluate an existing automation from run evidence.
- **Do not use `engineering-evidence` as a current action queue.** Use
  `engineering-attention` when the question is what needs action now; preserve
  retrospective factual outcomes separately.
- **Do not use `session-lessons` to promote one ordinary session into durable
  policy.** Preserve the observation until evidence qualifies it.
- **Do not create a new skill because an external source uses a new name.** Route
  the mechanism through `adopt` and strengthen an existing owner when possible.
- **Do not treat ontology or memory as replacement truth stores.** Keep explicit
  source authority and provenance.
- **Do not use `code-research` merely because a bug is difficult.** Use
  `fault-isolation` for a concrete reported failure; use `code-research` for an
  uncertain technical claim that needs an isolated experiment.
- **Do not invoke workflow-internal modules directly.** Use their owning agent so
  orchestration state, authority boundaries, and lifecycle gates remain intact.
- **Do not add `gauntlet-loop` to routine work for extra reviewer count.** Use it
  only when the quality/risk profile justifies producer-critic iteration and
  parallelism.

## When no composition is needed

Many tasks need exactly one skill. A workflow should remain single-stage when the
selected capability can reach the requested outcome with sufficient evidence and
without crossing one of its responsibility boundaries.

Examples include:

- `integration-reconciliation` for one active merge conflict;
- `code-research` for one uncertain library/runtime claim;
- `review` for one standalone code review;
- `code-conventions` for one convention-discovery and codification exercise;
- `eli5` for a concise orientation;
- `teach-me` for a measured tutoring loop.

More skills are not automatically more reliable. Prefer the smallest durable,
verified workflow that resolves the actual problem.

## Keeping this guide current

This guide should evolve when the **routing decision** evolves, not whenever the
catalogue gains files. Update it when a user should start somewhere different, a
new common composition or alternative matters, or an ownership collision needs a
warning. A deeper mechanism, reference, evaluation, helper, or agent-internal
module normally does not need a workflow-guide entry when the public route stays
the same.

The complete catalogue remains in the root README. Repository maintainers should
follow [`AGENTS.md`](../AGENTS.md) for the documentation-sync rules and the checks
that distinguish a catalogue change from a workflow-navigation change.

## Going deeper

The root [README](../README.md) contains the full public catalogue, agent
catalogue, internal-module ownership, and responsibility boundaries. Each
individual skill's `SKILL.md` defines its exact trigger conditions and behavioural
contract.
