# Repository maintenance guidance

This file defines repository-wide contribution and maintenance guidance for humans
and agents working on `mhingston/agent-skills`. Keep it focused on evolving the
catalogue; do not turn it into a second specification for individual capabilities.

## Sources of truth

| Surface | Owns |
| --- | --- |
| `README.md` | Repository/package rules, catalogues, high-level routing, responsibility boundaries, and canonical validation guidance. |
| `docs/workflows.md` | Outcome-oriented onboarding: where to start, common composition, important alternatives, and anti-workflows. It is intentionally **not** an exhaustive catalogue. |
| `<skill>/SKILL.md` | Authoritative trigger, boundaries, workflow, and output contract for one skill. |
| `agents/<agent>.md` | Authoritative lifecycle, state, delegation, and human-responsibility contract for an orchestrating agent. |
| package/agent `references/` | Conditional detail, evaluation cases, schemas, and deeper guidance loaded only when needed. |
| `AGENTS.md` | Repository-wide maintenance and documentation-sync policy. |

If navigation or summary documentation conflicts with runtime behaviour, fix the
stale documentation rather than duplicating the owning `SKILL.md` or agent
contract.

## Repository maintenance principles

- **Prefer the smallest existing owner.** Strengthen the skill or agent that
  already owns a responsibility before adding another public capability. Add a
  skill only for a genuinely distinct reusable trigger, boundary, and output.
- **Preserve responsibility boundaries.** New mechanisms must not silently move
  approval, authority, persistence, review, or lifecycle responsibilities.
- **Keep skills portable and self-contained.** Do not introduce runtime
  dependencies on repository-level shared folders, another skill package, or an
  agent definition.
- **Use agents only when orchestration earns it.** Agents coordinate lifecycle,
  durable state, delegation, independent stages, and human responsibility; they
  are not wrappers for ordinary procedures.
- **Prefer progressive disclosure.** Keep active instructions compact and move
  optional or specialist detail into directly linked references. Follow the
  active `SKILL.md` line-limit policy in `README.md`.
- **Preserve authority and provenance.** Implementation, generated prose, passing
  tests, memory, historical prevalence, and model inference are evidence, not
  automatic product intent, policy, approval, or human judgement.
- **Prefer the smallest durable, verified change.** More skills, workflow stages,
  policy, or context are not automatically more reliable.

## Decide where a change belongs

Strengthen an existing skill or agent when the same user intent and trigger should
still select it, even if its evidence model, guardrails, state, recovery,
verification, or optional mechanisms improve.

Add a new public skill only when all of these are true:

- a recurring task is not already owned cleanly;
- positive triggers and adjacent near-miss cases can be distinguished;
- the package is independently installable and usable;
- its output and authority boundary are coherent on their own;
- the maintenance and context cost is justified.

Before adding one, inspect the closest sibling capabilities and make the non-overlap
visible in routing and evaluation coverage.

Add or change a workflow-internal module only when its owning agent needs a
distinct narrow stage. Keep ownership explicit and do not advertise the module as
a user-selectable workflow merely because it has its own `SKILL.md`.

## Disambiguation and merge discipline

Treat routing clarity as part of the public skill contract. When public skills are
adjacent, make the distinction visible where a loader or user will encounter it:

- state the owned outcome in the frontmatter description;
- include positive triggers and, when collision is plausible, the nearest useful
  near-miss or alternative;
- preserve materially different authority, permission, lifecycle, runtime, or
  output boundaries explicitly;
- make important alternatives and complements visible in `README.md` and, when
  they affect the starting decision, `docs/workflows.md`.

Treat two public skills as merge candidates when the same user intent and trigger
could reasonably select either and the remaining differences are mainly modes,
data sources, wording, or output formatting. Prefer one coherent skill with
explicit modes when that reduces routing ambiguity without weakening portability
or responsibility boundaries.

Keep skills separate when the split protects a meaningful distinction such as
read versus write authority, design versus execution versus evaluation, human
judgement, lifecycle stage, runtime/framework dependency, or an independently
useful output contract. Similar vocabulary, shared evidence, or a common backend
alone is not sufficient reason to merge.

When highly similar siblings remain separate, document the routing distinction
rather than relying on names alone. If trigger or applicability behaviour changes,
update the relevant routing/outcome evaluation cases as well.

## Keep documentation in sync deliberately

Documentation should change because a user-facing decision changed, not because
the repository gained files.

### Update `README.md` when

- a public skill or agent is added, removed, renamed, or materially repurposed;
- an internal module or its owner changes;
- a repository/package invariant changes;
- a responsibility boundary or high-level related-capability distinction changes;
- canonical validation commands or policies change.

### Update `docs/workflows.md` when

- the best starting capability for a user goal changes;
- a new common composition or handoff matters;
- capabilities become important alternatives or complements;
- an ownership collision needs an anti-workflow warning;
- a genuinely new user-goal branch needs onboarding guidance.

Do **not** update the workflow guide mechanically for a new reference, schema,
evaluation case, helper, deeper mechanism, or internal-module change when the
public route stays the same. The README remains the complete catalogue.

### Update `AGENTS.md` when

Repository-wide maintenance, packaging, documentation-sync, or contribution
policy changes. Skill-specific behavioural fixes belong in the owning capability,
not here.

## Change and evaluation discipline

For material changes, inspect the current owner, nearest siblings, applicable
references, and recent relevant changes before editing. State the evidenced gap,
make the smallest cohesive change that addresses it, and preserve explicit human
and external authority boundaries.

When trigger, applicability, boundaries, or behaviour change materially, update
relevant package-local routing/outcome evaluation cases and follow the evaluation
contract owned by `skill-creator`. Static validation establishes package/tool
integrity; it is not behavioural evidence. Do not claim behavioural lift from
green CI alone.

## Before opening a pull request

- Re-read the final diff against current `main` and exclude unrelated changes.
- Check that no existing public responsibility is duplicated and no internal module
  is accidentally made public.
- Check relative links and package self-containment for changed skills.
- Run the canonical static/deterministic validation from `README.md` when the
  environment permits it.
- Run relevant matched behavioural evaluation when making a behavioural claim and
  a real harness is available; report unavailable behavioural evaluation honestly
  rather than substituting static CI.
- Apply the documentation-sync rules above instead of updating every catalogue
  surface automatically.
- Keep the PR bounded and explain the gap, design decision, trade-off, and
  validation performed.

If evidence does not justify a new capability, broader workflow, or additional
policy, prefer no change over speculative catalogue growth.
