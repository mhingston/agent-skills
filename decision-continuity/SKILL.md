---
name: decision-continuity
description: Reconcile resumed work, plans, handoffs, and proposals against attributable governing intent and previously accepted, rejected, deferred, open, superseded, or expired decisions. Use when work crosses sessions or agent contexts, a prior constraint or rationale may be drifting, a rejected alternative is being reopened, project artefacts disagree, or a continuation packet is needed before planning or execution resumes. Produces an evidence-backed continuity report and proposed intent/decision-register changes without silently inventing, accepting, superseding, or persisting intent or decisions.
---

# Decision Continuity

Preserve the direction and human why of a workstream across sessions, agents,
plans, handoffs, and interruptions. Reconstruct the smallest authoritative intent
and decision context needed for the current proposal, identify drift, stale
assumptions, or missing rationale, and make any required change of direction
explicit.

This skill reconciles governing intent and decisions. It does not make product,
architecture, policy, risk-acceptance, or delivery decisions on behalf of the
accountable human.

## Boundaries

- Operate read-only unless the user separately approves an exact persistence
  mutation through an appropriate workflow.
- Treat governing records, evidence, and scenario inputs as read-only evidence,
  not mutation targets. Do not modify an authority source or scenario input
  merely to make a continuity conflict disappear. When a proposal changes
  direction, report the proposed supersession and affected sources instead of
  drafting edits to the records that establish or test that direction. If the
  requested change is to skill policy, route it through `skill-creator` and
  preserve the evidence.
- Reconciliation is not implementation: even when a re-entry condition is
  satisfied, emit a proposed change record and downstream impact list for later
  approval rather than a patch to the governing record, policy, or other source
  used to establish the scenario.
- Treat workflow instructions, examples, and reference material as guidance,
  not as project authority or the deliverable to change. If the actual project
  artefacts are unavailable, report that gap instead of editing the guidance.
- Return a continuity report, not an implementation patch or file-level diff.
  Express a change as proposed intent or decision-record fields plus affected
  revalidation, and hand any approved mutation to its owning workflow.
- Treat a decision as accepted only when attributable evidence shows that the
  accountable human or designated authority accepted it.
- Do not infer acceptance from implementation, repeated mention, lack of
  objection, popularity, or an agent-authored recommendation.
- Do not infer authoritative goals, rationale, constraints, non-goals,
  invariants, or success criteria from implementation, tests, repeated agent
  prose, or a plausible reconstruction of why the code exists.
- Never promote agent-inferred intent to governing intent merely because it is
  coherent, repeated, implemented, or uncontested.
- Do not silently supersede, reopen, weaken, or broaden an accepted decision or
  attributable intent claim.
- Do not use conversation history as the only source of truth when a designated
  decision register, ADR, tracker item, approved brief, specification, policy, or
  repository document exists.
- Do not turn implementation evidence into retrospective policy. Code can show
  current behaviour, but not necessarily why it was approved or whether it
  remains intended.
- Do not become a general project-status, planning, ticket-refinement, memory, or
  retrospective workflow.
- Preserve contradictions, intent gaps, and missing authority rather than
  manufacturing one clean narrative.

## Use when

Use this skill when:

- work resumes after an interruption or in a fresh agent context;
- a plan, handoff, ticket, or proposal depends on earlier intent or decisions;
- the user asks whether something was already decided or why a constraint exists;
- a proposal may conflict with an accepted constraint, non-goal, invariant, or
  outcome;
- a rejected or deferred alternative is being reconsidered;
- a project is leaving a recorded stopping condition;
- several artefacts disagree about the active direction;
- the implementation is understandable but the rationale for a load-bearing
  behaviour or constraint is not attributable;
- a compact continuation packet is needed before planning or execution.

Do not use it merely because a task has history. Prior intent or decision context
must be material to the next decision or action.

## Use another workflow when

- The primary task is to create an implementation or investigation plan from
  stable inputs: use `plan`.
- The primary task is to refine or split tracker work: use `refine`.
- The task is to record historical outcomes or impact evidence: use
  `engineering-evidence`.
- The task is to find recurring patterns across many sessions: use
  `session-lessons`.
- The task is to write an ADR for a decision whose scope and authority are
  already clear: use the repository's ADR process.

These are routing boundaries, not runtime dependencies. This skill must remain
usable from its own directory.

## Evidence discipline

Classify material statements:

- **Observed (`E#`)** — directly supported by an attributable source. Record the
  source identity, locator, date or version, and relevant wording or state.
- **Inferred (`I#`)** — a reasoned interpretation of observations. Name the
  evidence and what could falsify it.
- **Unknown (`Q#`)** — missing authority, unresolved conflict, ambiguous status,
  absent rationale, or unavailable source that can change the continuity result.

Record explicit user statements as evidence only within their demonstrated
scope. Do not generalise a project-specific decision into a user-wide rule.

For every load-bearing intent claim, also record **intent provenance** separately
from evidence classification:

- `human-stated` — attributable wording from a human, not automatically an
  approval or proof that the speaker has authority;
- `human-approved` — explicitly accepted by the accountable human or designated
  authority;
- `authoritative-source` — stated by a source that repository or organisational
  rules designate as authoritative for that intent;
- `agent-inferred` — reconstructed by a model from code, tests, history, or other
  evidence without attributable human or authoritative-source wording;
- `unknown` — the intent or its provenance cannot be established.

A claim may govern work only when both its provenance and authority are sufficient
under the actual project rules. `agent-inferred` and `unknown` intent may guide a
bounded investigation, but must never silently fill a canonical intent gap.

## Inputs

Resolve as many of these as are available:

- the current proposal, handoff, plan, ticket, or intended next action;
- the active workstream and desired outcome;
- designated canonical intent or decision source, if one exists;
- approved outcome, rationale, success criteria, constraints, non-goals, and
  invariants that materially govern the work;
- prior decision register, ADRs, specifications, approved plans, briefs, tracker
  parents, policies, and handoffs;
- explicit human decisions or intent statements in attributable conversations,
  reviews, or meeting evidence;
- relevant repository state, interfaces, and constraints;
- current stopping condition and re-entry triggers;
- source versions, revisions, timestamps, or content digests;
- requested output and whether persistence is in scope.

If the current proposal is unavailable, the skill may reconstruct a continuation
packet but cannot classify proposal alignment.

## Decision model

Use these decision statuses:

- `accepted` — explicitly approved and currently active;
- `rejected` — explicitly considered and not selected;
- `deferred` — intentionally postponed with a reason or re-entry condition;
- `open` — unresolved and still decision-bearing;
- `superseded` — replaced by a later attributable decision;
- `expired` — no longer applicable because a stated validity condition ended;
- `unknown` — evidence is insufficient or contradictory.

Use these proposal-reconciliation classifications:

- `aligned` — follows active intent and decisions without changing their meaning;
- `compatible-refinement` — adds detail within the accepted decision and intent
  space;
- `new-decision-required` — introduces a consequential choice not previously
  decided;
- `contradiction` — conflicts with an active accepted decision;
- `intent-regression` — weakens, violates, or silently reinterprets an
  attributable outcome, success criterion, constraint, non-goal, rationale, or
  invariant even when no discrete decision record captures it;
- `scope-extension` — expands the authorised outcome or boundaries;
- `supersession-proposed` — explicitly proposes replacing an active decision or
  governing intent claim;
- `unsupported-reopening` — reintroduces a rejected or deferred alternative
  without qualifying new evidence;
- `indeterminate` — evidence, intent provenance, or authority is insufficient.

Keep decision status separate from proposal classification. A proposal to
supersede a decision or intent claim is not itself accepted.

## Workflow

### 1. Establish the continuation frame

State:

- the active outcome;
- the workstream and current scope;
- the artefact or action being resumed;
- which goals, rationale, constraints, non-goals, invariants, or decisions are
  load-bearing for the next action;
- why prior intent or decisions are material now;
- the likely authoritative sources;
- the current stopping condition and claimed re-entry trigger, when relevant.

If the request actually asks for a new plan, refinement, implementation, or
retrospective without a material continuity question, route it rather than
forcing this workflow.

### 2. Collect the smallest sufficient evidence

Inspect intent and decision evidence in this order, adapting to repository
conventions:

1. a designated canonical intent or decision source, ADR set, policy, contract,
   specification, product brief, or tracker parent;
2. an explicitly approved plan, brief, handoff, or review decision;
3. an attributable current human instruction;
4. an attributable earlier human decision or intent statement in conversation or
   meeting evidence;
5. implementation and operational evidence that can confirm current reality but
   not approval, rationale, or intended policy by itself;
6. agent-authored proposals, summaries, reconstructed rationale, and inferred
   preferences.

Do not treat this as a universal authority hierarchy. A repository may designate
one source as canonical, and a current accountable human may explicitly amend
it. Record the actual authority rule and surface conflicts.

Stop collecting when more history is unlikely to change the governing intent,
active decision set, proposal classification, invalidation impact, or required
human decision.

### 3. Build the governing intent capsule

Capture only intent that materially constrains the next action:

- desired outcome or problem to solve;
- rationale or purpose, when attributable;
- observable success criteria;
- constraints and non-negotiables;
- non-goals and deliberately excluded outcomes;
- invariants that must survive implementation or refactoring;
- authority, source references, source version, and intent provenance for every
  load-bearing claim;
- explicit intent gaps where the why, authority, or source cannot be established.

Do not pad the capsule with every historical statement or implementation detail.
If a rationale is only plausible from code or tests, record it as
`agent-inferred` and preserve the gap instead of converting it into project
intent. Missing rationale blocks only when it could materially change scope,
design, safety, compatibility, verification, or an expensive-to-reverse choice.

### 4. Normalise decision records

For every material decision, capture:

- stable existing identifier, or a provisional identifier when none exists;
- concise statement;
- status;
- scope and affected outcome;
- rationale and considered alternatives when evidenced, including provenance of
  load-bearing rationale;
- constraints and non-goals it establishes;
- authority and decision maker;
- source references and source version;
- decided, reviewed, or observed date;
- decisions it supersedes or depends on;
- reopening, review, expiry, or re-entry conditions;
- confidence and unresolved conflict.

Preserve existing canonical identifiers. A newly generated provisional ID must
not be presented as persisted or authoritative.

Deduplicate repeated summaries of the same decision. Do not merge decisions that
have similar wording but different scope, authority, or rationale.

### 5. Build the active governing set

Determine which intent claims and decisions currently govern the workstream.

Check for:

- later decisions that supersede earlier ones;
- expired time, version, environment, or scope conditions;
- unresolved conflict between canonical sources;
- rejected alternatives later represented as undecided;
- deferred alternatives whose re-entry condition has or has not occurred;
- implementation drift from the recorded direction;
- an implementation that still passes tests while weakening a recorded outcome,
  constraint, non-goal, or invariant;
- decisions whose rationale depended on an assumption that is now false;
- rationale or intent represented as authoritative even though its provenance is
  only `agent-inferred` or `unknown`.

Return `blocked` continuity only when material governing intent or decisions
cannot be established safely enough for the requested continuation.

### 6. Reconcile the current proposal

Break the current proposal into material claims, components, or changes. For each:

1. identify the affected intent claim, decision, or constraint;
2. assign one reconciliation classification;
3. cite the evidence and intent provenance;
4. state whether work may proceed under current authority;
5. identify the smallest required action.

Do not classify wording differences as contradictions when behaviour and
responsibility remain aligned. Conversely, do not hide a responsibility,
authority, persistence, external-effect, public-contract, intent, or scope change
as minor implementation detail.

### 7. Apply the reopening and supersession gate

A rejected or deferred alternative may be reconsidered only when at least one of
these is evidenced:

- materially new evidence;
- a changed constraint or operating environment;
- a failed or falsified assumption;
- a changed desired outcome;
- an explicit review, expiry, or re-entry condition has occurred;
- the accountable human explicitly requests reconsideration.

For a valid reconsideration, produce a `supersession-proposed` or
`new-decision-required` item containing:

- the existing decision or governing intent claim;
- what changed;
- the new evidence;
- affected alternatives;
- downstream consequences;
- the accountable decision required.

Novelty, a new framework, renewed interest, or an agent preference is not enough.

### 8. Identify downstream invalidation

When continuity is `changed`, `conflicting`, or `blocked`, identify artefacts and
work that may now be stale:

- product briefs, specifications, ADRs, decision registers, plans, and handoffs;
- parent and child tickets;
- acceptance criteria, constraints, non-goals, and invariants;
- interfaces, schemas, migrations, or tests;
- risk maps and approvals;
- implementation branches or pull requests;
- rollout, rollback, observability, or operational assumptions.

Do not claim an artefact is invalid without a traceable dependency. Distinguish
`must revalidate`, `likely affected`, and `unaffected`.

### 9. Propose register changes

Produce an explicit diff-like proposal:

- intent claims to add, clarify, supersede, or mark as gaps;
- decisions to add;
- decisions to supersede;
- statuses to change;
- rationale or evidence to append;
- review or re-entry conditions to update;
- conflicts requiring human resolution.

Do not propose an `agent-inferred` rationale as canonical intent. Where the why is
material but unattributable, propose an intent gap or an accountable-human
confirmation step instead.

Do not persist the proposal. A later mutation workflow must refetch the
authoritative source, show the exact change, obtain approval, write, and verify.

### 10. Build the continuation packet

Return the smallest context another planner, refiner, implementer, or agent needs:

- governing intent capsule: outcome, attributable rationale, success criteria,
  constraints, non-goals, invariants, provenance, and material gaps;
- governing decision IDs and sources;
- rejected or deferred alternatives relevant to the next action;
- open decisions and accountable owners;
- current stopping condition;
- re-entry and replanning triggers;
- proposal classification and permitted next step;
- stale artefacts or required revalidation.

Prefer this compact projection over replaying an unbounded transcript. The packet
should preserve the load-bearing why without becoming a transcript or speculative
history.

## Output contract

Return:

1. **Continuity status** — `aligned`, `changed`, `conflicting`, or `blocked`.
2. **Continuation frame** — outcome, scope, resumed artefact, stopping condition,
   and evidence coverage.
3. **Governing intent** — compact intent capsule with provenance and material
   gaps.
4. **Active decision set** — material decision records and authority.
5. **Proposal reconciliation** — each material proposal with classification,
   related intent/decisions, evidence, and required action.
6. **Intent/decision gaps and conflicts** — unresolved rationale, provenance,
   authority, or evidence.
7. **Downstream invalidation** — `must revalidate`, `likely affected`, and
   `unaffected` artefacts.
8. **Proposed register changes** — exact intent additions/clarifications,
   decision additions, supersessions, and status changes, or `none`.
9. **Continuation packet** — compact handoff for the next workflow.

When machine-readable output is requested, use
[references/decision-register.schema.json](references/decision-register.schema.json)
for the decision register and preserve the same semantics in the surrounding
continuity report.

## Stop and escalate

Stop and request an accountable decision when:

- canonical sources conflict materially;
- acceptance or rejection cannot be attributed;
- a proposal contradicts an active decision or materially regresses governing
  intent;
- material rationale, constraint, invariant, or intent authority is unavailable
  and the gap can change a consequential or expensive-to-reverse choice;
- supersession would change product, architecture, policy, security, compliance,
  data, public-contract, operational, or risk-acceptance intent;
- required sources or permissions are unavailable;
- downstream invalidation cannot be bounded safely.

Ask only the smallest decision-bearing question. Explain the current intent or
decision, the conflicting proposal, the evidence, and what cannot proceed without
the answer.

## Validation

Before returning, verify that:

- every accepted, rejected, deferred, or superseded status is attributable;
- every load-bearing intent claim has explicit provenance and sufficient
  authority, or remains an intent gap;
- implementation, tests, or agent prose were not mistaken for human approval or
  authoritative rationale;
- `agent-inferred` intent was not promoted to governing or canonical intent;
- canonical source conflicts remain visible;
- proposal classifications trace to active intent/decisions and evidence;
- rejected alternatives were not reopened without a qualifying trigger;
- supersession remains proposed until approved;
- downstream invalidation is dependency-based rather than speculative;
- the continuation packet is compact and sufficient;
- no intent source, decision record, or external system was modified.

For calibration examples, read [references/examples.md](references/examples.md).
When evaluating or revising this skill, read
[references/evaluation-suite.md](references/evaluation-suite.md).
