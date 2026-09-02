# Repository maintenance guidance

This file defines repository-wide contribution and maintenance guidance for humans
and agents working on `mhingston/agent-skills`. Keep it focused on how the
catalogue is evolved; do not turn it into a second specification for individual
skills or agents.

## Sources of truth

Use each surface for one job:

| Surface | Owns |
| --- | --- |
| `README.md` | Repository/package rules, public and agent catalogues, high-level routing, responsibility boundaries, and canonical validation guidance. |
| `docs/workflows.md` | Outcome-oriented onboarding: where to start, common composition, important alternatives, and anti-workflows. It is intentionally **not** an exhaustive catalogue. |
| `<skill>/SKILL.md` | The authoritative trigger, boundaries, workflow, and output contract for one public or internal skill. |
| `agents/<agent>.md` | The authoritative lifecycle, state, delegation, and human-responsibility contract for an orchestrating agent. |
| `<skill>/references/` and `agents/references/` | Conditional detail, evaluation cases, schemas, and deeper guidance loaded only when needed. |
| `AGENTS.md` | Repository-wide maintenance policy and documentation-sync rules. |

When two surfaces appear to disagree about runtime behaviour, the owning
`SKILL.md` or agent definition wins. Fix the stale navigation/documentation rather
than duplicating behavioural rules across files.

## Maintenance principles

1. **Prefer the smallest existing owner.** Strengthen the skill or agent that
   already owns a responsibility before adding another public capability. Add a
   new skill only when the task has a genuinely distinct reusable trigger,
   decision boundary, and output contract.
2. **Preserve responsibility boundaries.** A useful new mechanism does not justify
   moving approval, authority, persistence, review, or lifecycle responsibilities
   into the wrong capability.
3. **Keep skills portable and self-contained.** A skill must remain installable by
   copying its own directory. Do not create runtime dependencies on repository-level
   shared folders, another skill package, or an agent definition.
4. **Use agents only when orchestration earns it.** Agents coordinate lifecycle,
   durable state, delegation, independent stages, and human responsibility. Do not
   create an agent merely to wrap one ordinary procedure.
5. **Prefer progressive disclosure.** Keep active instructions compact and move
   optional, formalism-specific, harness-specific, or detailed evaluation material
   into directly linked references. Follow the repository's active `SKILL.md`
   line-limit policy in `README.md`.
6. **Keep developmental history out of runtime instructions by default.** Prior
   proposals, rejected interventions, trajectories, and evolution evidence belong
   in the appropriate authoring/evaluation evidence store unless task execution
   genuinely needs the distilled result.
7. **Preserve source authority and provenance.** Implementation, generated prose,
   passing tests, memory, indexes, historical prevalence, and model inference are
   evidence; they do not silently become product intent, policy, approval, or a
   human decision.
8. **Do not equate more machinery with more reliability.** Prefer the smallest
   durable, independently verifiable change that closes the evidenced gap, and
   stop when further expansion is unlikely to change the decision.

## Decide where a change belongs

Before editing, identify the current problem and the existing owner.

### Strengthen an existing skill or agent when

- the new idea improves an existing workflow stage, evidence model, guardrail,
  recovery rule, evaluation method, or conditional mechanism;
- the same user intent and trigger should still select the existing capability;
- a focused reference can carry optional depth without enlarging active context;
- a new public name would mostly restate an existing responsibility.

### Add a new public skill only when

- users have a recurring task that is not already owned cleanly;
- its positive trigger and adjacent negative/near-miss cases are discriminative;
- it can be installed and used independently;
- its output and authority boundary are coherent without another skill package;
- the maintenance and context cost is justified by evidence or a clear repeated
  need.

When introducing a public skill, explicitly check the closest sibling capabilities
and make the non-overlap visible in routing/evaluation coverage.

### Add or change an internal module only when

- an owning agent needs a distinct stage with a narrow handoff contract;
- the module is not a public entry point;
- ownership remains explicit in metadata, the agent definition, and the README
  internal-module catalogue.

Do not document an internal module as a user-selectable workflow merely because it
has its own `SKILL.md`.

## Keep documentation in sync deliberately

Documentation should change because a user-facing decision changed, not because
file counts changed.

### Update `README.md` when

- a public skill or agent is added, removed, renamed, or materially repurposed;
- an internal module or its owner changes;
- a repository/package invariant changes;
- a responsibility boundary or high-level related-skill distinction changes;
- canonical validation commands or policies change.

### Update `docs/workflows.md` when

- the best starting capability for a user goal changes;
- a new common composition or handoff becomes useful;
- two capabilities become important alternatives or complements;
- an ownership collision needs an anti-workflow warning;
- a public capability adds a genuinely new user-goal branch that newcomers would
  otherwise struggle to discover.

Do **not** update the workflow guide mechanically for:

- a new reference, schema, evaluation case, or deterministic helper;
- a deeper mechanism inside an existing skill or agent;
- an internal-module implementation change that preserves the public lifecycle;
- more detailed evidence, provenance, state, comprehension, contribution-policy,
  or verification handling that does not change where users start or compose work.

The README remains the complete catalogue. The workflow guide should stay small
enough to help a newcomer choose, not force them to scan every capability.

### Update `AGENTS.md` when

- repository-wide maintenance, packaging, documentation-sync, or contribution
  policy changes;
- a recurring repository-level failure shows this guidance is missing or wrong.

Do not place skill-specific behavioural fixes here merely because every agent can
read this file; fix the owning skill and its evaluation instead.

## Skill and agent change discipline

For a material change:

1. inspect the current owner, nearest sibling capabilities, applicable references,
   and recent relevant changes before designing the edit;
2. state the behavioural or maintenance gap being addressed;
3. make the smallest cohesive change that tests that hypothesis;
4. keep newly optional detail out of active context when a reference is sufficient;
5. preserve explicit human-owned decisions and external authority boundaries;
6. update or add package-local routing/outcome evaluation cases when trigger,
   applicability, boundaries, or behaviour materially change;
7. use the exact previous revision as the baseline for behavioural claims rather
   than comparing only with an idealised rubric;
8. keep model, harness, suite revision, environment, and other material provenance
   when interpreting evaluation evidence;
9. retain rejected or inconclusive intervention evidence when it carries reusable
   authoring information, but do not compile it into runtime instructions by
   default.

Static validation proves package/tool integrity, not behavioural lift. Never claim
that a skill improved because CI is green or because its desired evaluation cases
exist.

## Before opening a pull request

- Re-read the final diff against current `main` and verify the branch is not
  carrying unrelated changes.
- Confirm the change does not duplicate an existing public responsibility or
  accidentally make an internal module public.
- Check relative links and package self-containment for every changed skill.
- Run the repository's canonical static/deterministic validation from `README.md`
  when the environment permits it.
- Run the relevant matched behavioural cases in a real harness when the change
  makes a behavioural claim and such a harness is available.
- Report unavailable behavioural evaluation as `NOT_RUN`, `BLOCKED`, or
  `not_verifiable`; do not substitute static CI or a classifier surrogate.
- Verify documentation synchronization using the rules above rather than updating
  every catalogue surface automatically.
- Prefer a bounded PR that explains the gap, design decision, trade-off, validation
  performed, and credible case against the change when material.

If the evidence does not justify a new capability, broader workflow, or additional
policy, prefer no change over speculative catalogue growth.
