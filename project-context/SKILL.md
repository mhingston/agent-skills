---
name: project-context
description: Establish or assess a durable, agent-readable project context record that separates current truth, future intent, history, and scratch material; preserves source authority and provenance; supports deterministic validation and task orientation; and prevents trackers, generated views, memory, or stale documents from becoming competing sources of truth. Use for long-running or multi-agent projects where context fragmentation, cold-start reconstruction, cross-system drift, or derived delivery state is a material problem. Do not use for ordinary implementation planning, repository ontology design, one-off documentation cleanup, or personal/shared memory capture.
---

# Project Context

Create or assess the smallest durable context substrate that lets people and
agents answer what is true, what is intended, what happened, and what evidence
supports those claims without reconstructing project state from conversation.

The goal is not more documentation. The goal is a coherent, versioned,
inspectable record with explicit authority and machine-checkable relationships.

Do not prescribe a universal folder layout or tracker. Preserve established
repository conventions when they can express the required semantics safely.

## Boundaries

- Default to read-only assessment unless the user explicitly asks to establish or
  modify a project context record.
- Do not replace a canonical product, architecture, security, operational, data,
  or tracker source merely to make context easier for agents to consume.
- Do not treat generated summaries, memory stores, dashboards, chat history, or
  external tracker projections as authoritative unless the project explicitly
  designates them as such for the claim in question.
- Do not turn observed code patterns into policy without attributable evidence.
- Do not create a second source of truth when an existing maintained record can be
  extended or indexed instead.
- Do not require structured machinery for a small, short-lived, single-agent task
  where ordinary repository documentation and a bounded plan are sufficient.
- Keep human-authored reasoning separate from machine-owned metadata when tools
  need to update the same artifact.
- Prefer deterministic validation for structural claims; use model judgement for
  interpretation, synthesis, and ambiguity that cannot be reduced safely.

## Route adjacent work

Use this skill when the primary problem is the **project context substrate**.
Use another workflow when the task is primarily:

- planning one software change: use a software-planning workflow;
- reconciling a proposal against prior accepted or rejected decisions: use a
  decision-continuity workflow;
- defining repository entities and relationships for semantic retrieval: use a
  repository-ontology workflow;
- persisting reusable organisational knowledge outside the project record: use an
  appropriate memory workflow;
- assessing overall coding-agent autonomy and controls: use an agent-readiness
  workflow;
- implementing or reviewing code: use the relevant implementation or review
  workflow.

A project context record may feed all of those workflows without owning them.

## Evidence discipline

For material claims distinguish:

- **Observed (`E#`)** — directly supported by an inspected source, repository
  artifact, tracker item, configuration, schema, history, or operational result.
- **Derived (`D#`)** — computed mechanically from observed structured state.
- **Inferred (`I#`)** — interpretation from evidence; state what supports it and
  what could falsify it.
- **Unknown (`U#`)** — evidence is missing, inaccessible, stale, ambiguous, or
  contradictory.
- **Required (`P#`)** — an explicit project or organisational rule; name its
  authority.

Do not silently collapse disagreement between sources into one answer. Preserve
provenance and surface the conflict.

## 1. Decide whether a project record is justified

Establish the scope, participants, likely lifetime, number of agent/human handoffs,
external systems, and cost of reconstructing context.

A dedicated project-context record is usually justified when several of these are
true:

- work spans multiple sessions, agents, teams, repositories, or systems;
- important intent or constraints are repeatedly re-explained;
- architecture, decisions, acceptance criteria, or current state are fragmented;
- trackers, repository docs, code, and generated summaries disagree;
- a resumed or replacement agent cannot orient from authoritative sources alone;
- delivery state must be derived from evidence rather than manually reported;
- stale context or missing provenance could cause expensive implementation drift;
- relationships between plans, decisions, tickets, changes, tests, or releases
  need deterministic validation.

Prefer existing maintained sources plus a thin index when that closes the gap.
Avoid inventing a parallel project repository when the current repository already
has a suitable home.

## 2. Map sources and authority before designing structure

Inventory only sources that can materially change project understanding, such as:

- product intent, requirements, acceptance criteria, and non-goals;
- architecture, interfaces, schemas, domain rules, ADRs, and conventions;
- tickets, plans, checkpoints, milestones, and dependencies;
- code, configuration, tests, CI, deployments, releases, and runtime evidence;
- decision records, investigation outcomes, incidents, and handoffs;
- external systems that remain authoritative for particular fields.

For each source record:

- identity and location;
- claims it is authoritative for;
- owner or accountable maintainer when known;
- freshness or version signal;
- write mechanism and permissions;
- consumers and projections;
- conflict-resolution rule;
- whether it is human-authored, machine-authored, or mixed.

Do not infer authority from file location, recency, prevalence, or tool
availability alone.

## 3. Separate semantic roles

The record must make these roles distinguishable even if the repository uses
other names or combines them into a small number of files.

### Current truth

Facts intended to describe the system or project **now**, such as architecture,
interfaces, supported operating assumptions, conventions, and verified current
state.

Current truth must identify its governing source or freshness signal when the
claim can drift.

### Future intent

Accepted or proposed outcomes, specifications, plans, acceptance contracts,
decisions, dependencies, rollout intent, and explicit non-goals.

Distinguish proposed intent from accepted intent. Implementation progress must not
silently turn a proposal into an approved decision.

### History and evidence

Completed outcomes, superseded decisions, investigation results, significant
transitions, release or incident evidence, and other records needed to explain
how the current state arose.

History should be append-oriented or otherwise protected from casual rewriting.
Corrections should preserve the previous state and provenance when accountability
matters.

### Scratch material

Drafts, exploratory notes, generated working material, temporary synthesis, and
other explicitly non-authoritative context.

A governed record needs a safe place for unfinished thought. Scratch content must
not become canonical merely because an agent can retrieve it.

## 4. Define record identity and relationships

Use stable identities when records need machine traversal or cross-reference.
Avoid relying on headings, filenames, URLs, or tracker display names when those
can change independently.

Model only relationships the project needs to validate or traverse, for example:

- `implements` / `implemented-by`;
- `depends-on`;
- `constrained-by`;
- `decides` / `supersedes`;
- `verifies` / `evidenced-by`;
- `projects-to` / `originates-from`;
- `owns` or `governs` when ownership is explicit.

Every typed relationship should define:

- source and target identity;
- direction and semantics;
- whether missing targets are invalid or merely unresolved;
- which side owns the relationship;
- how stale references are detected.

Do not build a general knowledge graph when a small index and a few typed edges
answer the operational questions.

## 5. Establish the machine interface contract

When agents repeatedly need to discover state from the record, define a
machine-readable interface rather than requiring free-form document archaeology.
It may be a CLI, script, API, generated index, or repository-native command.

Prefer commands or operations that answer bounded questions such as:

- validate the record and relationships;
- identify stale, missing, contradictory, or unresolved context;
- resolve a task to its governing intent, constraints, decisions, and checks;
- list work that is ready or blocked from structured dependencies;
- compare canonical state with external projections;
- derive completion or health only from explicit evidence;
- preview external mutations before applying them.

Machine output should be structured, attributable, and distinguish unknown from
false. A failing validation should identify the exact broken invariant and a
repair direction when one can be stated deterministically.

### Optional context index

When the project lacks an existing machine-readable model, a lightweight JSON
index can provide stable identity and relationship validation without dictating
where human documentation lives.

The bundled `scripts/validate-context-record.py` validates this minimal shape:

```json
{
  "schema_version": "1",
  "records": [
    {
      "id": "ARCH-payments",
      "kind": "truth",
      "path": "docs/architecture/payments.md",
      "authority": "canonical",
      "state": "active",
      "refs": ["DEC-refunds"]
    }
  ]
}
```

Supported `kind` values are `truth`, `intent`, `history`, and `scratch`.
Supported `authority` values are `canonical`, `derived`, and `informational`.
Supported `state` values are `active`, `superseded`, and `archived`.

Use this index only when it earns its maintenance cost. It is a portable fallback,
not a required repository convention and not a replacement for a richer existing
machine interface.

Run:

```bash
python3 project-context/scripts/validate-context-record.py \
  path/to/context-index.json --root .
```

The validator checks schema shape, unique identities and paths, path containment,
referential integrity, file existence for governed records, and authority/state
invariants. It does not decide whether prose is semantically correct or current.

## 6. Define session orientation

For recurring agent work, define how a fresh session obtains the smallest
sufficient current packet before acting.

Resolve from the task identity where possible:

- governing accepted outcome and acceptance criteria;
- relevant current architecture, interfaces, schemas, and conventions;
- material accepted, rejected, or superseded decisions;
- dependencies and authority boundaries;
- current repository or external-source revision/freshness;
- validation status and exact verification commands when known;
- unresolved conflicts or unknowns that must not be guessed.

Prefer deterministic retrieval over injecting the entire project record. Rebuild
the packet from current sources on resume rather than trusting an old session
summary. Lifecycle hooks may automate delivery, but hooks are a harness concern
and must remain opt-in and policy-compliant.

## 7. Keep projections subordinate to the record

Trackers, dashboards, generated status pages, client updates, and other views may
remain valuable interaction surfaces. Define explicitly which fields originate in
the project record, which originate externally, and how drift is reconciled.

For machine writes to external systems:

1. compute the intended change from authoritative state;
2. show or persist a deterministic plan/diff;
3. require a separate authorised apply step for consequential writes;
4. read back the result;
5. refuse ambiguous matches rather than guessing;
6. record reconciliation failures as visible state.

Do not let bidirectional sync create unclear ownership of the same field.

## 8. Derive status from evidence

Do not add a manually maintained health field when health can be computed from
lower-level facts.

Define only the derived states that support real decisions. Examples may include:

- ready because required intent and dependencies are resolved;
- blocked because a named dependency or decision gate remains open;
- incomplete because acceptance evidence is missing;
- stale because a governing source changed after the last validation;
- at risk because a policy-required relationship or verification signal is
  missing.

Every derived state should expose its rule and contributing evidence. Missing data
must remain missing or unknown rather than being guessed healthy.

## 9. Validate and evolve the record

Before relying on the record for higher agent autonomy, test representative
questions and workflows:

- Can a fresh agent identify the governing outcome without user reconstruction?
- Can it distinguish accepted intent from drafts and historical alternatives?
- Can deterministic tooling catch a broken or dangling relationship?
- Can the system identify external drift without an LLM comparing prose?
- Can a completion claim be rejected when required evidence is absent?
- Can a human trace a derived state back to source evidence?
- Can current truth be updated without rewriting historical evidence?

Treat repeated context failures as evidence for a better check, index field,
retrieval rule, or skill—not as a reason to add more prose globally.

Read `references/evaluation-suite.md` when evaluating this skill or changing its
trigger boundaries.

## Output contract

For an assessment, return:

1. **Need** — `Not needed`, `Thin index`, `Project record`, or `Blocked`, with the
   evidence supporting the classification.
2. **Source/authority map** — current sources, authority, owners, freshness, and
   material conflicts.
3. **Role coverage** — current truth, future intent, history/evidence, scratch.
4. **Machine-interface gaps** — questions agents still have to reconstruct and
   which are suitable for deterministic tooling.
5. **Orientation contract** — the minimum task-start packet and how it is rebuilt
   from current evidence.
6. **Projection model** — external systems, field ownership, and reconciliation
   direction where relevant.
7. **Derived-state rules** — only decision-useful states that can be computed from
   evidence.
8. **Recommended next slice** — the smallest reversible change that materially
   reduces context reconstruction or drift.

For an establishment request, additionally provide the selected structure,
identities/relationships, validation mechanism, migration steps, and falsifiable
acceptance checks. Do not perform repository or external writes beyond what the
user authorised.

## Quality gate

Before finishing, verify that:

- the design has one authority rule for every duplicated material claim;
- truth, intent, history, and scratch are distinguishable;
- proposed and accepted intent are not collapsed;
- external projections cannot silently become competing sources of truth;
- machine-checkable invariants are not delegated to model judgement without need;
- session orientation is current, bounded, and task-relevant;
- derived status is traceable to evidence and preserves unknowns;
- history and provenance survive corrections and supersession;
- the solution is no heavier than the demonstrated context problem requires.
