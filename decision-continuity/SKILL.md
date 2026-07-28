---
name: decision-continuity
description: Reconcile resumed work, plans, handoffs, and proposals against previously accepted, rejected, deferred, open, superseded, or expired decisions. Use when work crosses sessions or agent contexts, a prior constraint may be drifting, a rejected alternative is being reopened, project artefacts disagree, or a continuation packet is needed before planning or execution resumes. Produces an evidence-backed continuity report and proposed decision-register changes without silently accepting, superseding, or persisting decisions.
---

# Decision Continuity

Preserve the direction of a workstream across sessions, agents, plans, handoffs,
and interruptions. Reconstruct the smallest authoritative decision context needed
for the current proposal, identify drift or stale assumptions, and make any
required change of direction explicit.

This skill reconciles decisions. It does not make product, architecture, policy,
risk-acceptance, or delivery decisions on behalf of the accountable human.

## Boundaries

- Operate read-only unless the user separately approves an exact persistence
  mutation through an appropriate workflow.
- Treat a decision as accepted only when attributable evidence shows that the
  accountable human or designated authority accepted it.
- Do not infer acceptance from implementation, repeated mention, lack of
  objection, popularity, or an agent-authored recommendation.
- Do not silently supersede, reopen, weaken, or broaden an accepted decision.
- Do not use conversation history as the only source of truth when a designated
  decision register, ADR, tracker item, approved brief, or repository document
  exists.
- Do not turn implementation evidence into retrospective policy. Code can show
  current behaviour, but not necessarily why it was approved or whether it
  remains intended.
- Do not become a general project-status, planning, ticket-refinement, memory, or
  retrospective workflow.
- Preserve contradictions and missing authority rather than manufacturing one
  clean narrative.

## Use when

Use this skill when:

- work resumes after an interruption or in a fresh agent context;
- a plan, handoff, ticket, or proposal depends on earlier decisions;
- the user asks whether something was already decided;
- a proposal may conflict with an accepted constraint or non-goal;
- a rejected or deferred alternative is being reconsidered;
- a project is leaving a recorded stopping condition;
- several artefacts disagree about the active direction;
- a compact continuation packet is needed before planning or execution.

Do not use it merely because a task has history. The prior decision context must
be material to the next decision or action.

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
  or unavailable source that can change the continuity result.

Record explicit user statements as evidence only within their demonstrated
scope. Do not generalise a project-specific decision into a user-wide rule.

## Inputs

Resolve as many of these as are available:

- the current proposal, handoff, plan, ticket, or intended next action;
- the active workstream and desired outcome;
- designated canonical decision source, if one exists;
- prior decision register, ADRs, approved plans, briefs, tracker parents, and
  handoffs;
- explicit human decisions in attributable conversations or reviews;
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

- `aligned` — follows active decisions without changing their meaning;
- `compatible-refinement` — adds detail within the accepted decision space;
- `new-decision-required` — introduces a consequential choice not previously
  decided;
- `contradiction` — conflicts with an active accepted decision;
- `scope-extension` — expands the authorised outcome or boundaries;
- `supersession-proposed` — explicitly proposes replacing an active decision;
- `unsupported-reopening` — reintroduces a rejected or deferred alternative
  without qualifying new evidence;
- `indeterminate` — evidence or authority is insufficient.

Keep decision status separate from proposal classification. A proposal to
supersede a decision is not itself accepted.

## Workflow

### 1. Establish the continuation frame

State:

- the active outcome;
- the workstream and current scope;
- the artefact or action being resumed;
- why prior decisions are material now;
- the likely authoritative sources;
- the current stopping condition and claimed re-entry trigger, when relevant.

If the request actually asks for a new plan, refinement, implementation, or
retrospective without a material continuity question, route it rather than
forcing this workflow.

### 2. Collect the smallest sufficient evidence

Inspect decision evidence in this order, adapting to repository conventions:

1. a designated canonical register, ADR set, policy, contract, or tracker parent;
2. an explicitly approved plan, brief, handoff, or review decision;
3. an attributable current human instruction;
4. an attributable earlier human decision in conversation or meeting evidence;
5. implementation and operational evidence that can confirm current reality but
   not approval by itself;
6. agent-authored proposals, summaries, and inferred preferences.

Do not treat this as a universal authority hierarchy. A repository may designate
one source as canonical, and a current accountable human may explicitly amend
it. Record the actual authority rule and surface conflicts.

Stop collecting when more history is unlikely to change the active decision set,
proposal classification, invalidation impact, or required human decision.

### 3. Normalise decision records

For every material decision, capture:

- stable existing identifier, or a provisional identifier when none exists;
- concise statement;
- status;
- scope and affected outcome;
- rationale and considered alternatives when evidenced;
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

### 4. Build the active decision set

Determine which decisions currently govern the workstream.

Check for:

- later decisions that supersede earlier ones;
- expired time, version, environment, or scope conditions;
- unresolved conflict between canonical sources;
- rejected alternatives later represented as undecided;
- deferred alternatives whose re-entry condition has or has not occurred;
- implementation drift from the recorded direction;
- decisions whose rationale depended on an assumption that is now false.

Return `blocked` continuity when material governing decisions cannot be
established safely.

### 5. Reconcile the current proposal

Break the current proposal into material claims, components, or changes. For each:

1. identify the affected decision or constraint;
2. assign one reconciliation classification;
3. cite the evidence;
4. state whether work may proceed under current authority;
5. identify the smallest required action.

Do not classify wording differences as contradictions when behaviour and
responsibility remain aligned. Conversely, do not hide a responsibility,
authority, persistence, external-effect, public-contract, or scope change as
minor implementation detail.

### 6. Apply the reopening and supersession gate

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

- the existing decision;
- what changed;
- the new evidence;
- affected alternatives;
- downstream consequences;
- the accountable decision required.

Novelty, a new framework, renewed interest, or an agent preference is not enough.

### 7. Identify downstream invalidation

When continuity is `changed`, `conflicting`, or `blocked`, identify artefacts and
work that may now be stale:

- plans and handoffs;
- parent and child tickets;
- acceptance criteria and non-goals;
- interfaces, schemas, migrations, or tests;
- risk maps and approvals;
- implementation branches or pull requests;
- rollout, rollback, observability, or operational assumptions.

Do not claim an artefact is invalid without a traceable dependency. Distinguish
`must revalidate`, `likely affected`, and `unaffected`.

### 8. Propose register changes

Produce an explicit diff-like proposal:

- decisions to add;
- decisions to supersede;
- statuses to change;
- rationale or evidence to append;
- review or re-entry conditions to update;
- conflicts requiring human resolution.

Do not persist the proposal. A later mutation workflow must refetch the
authoritative source, show the exact change, obtain approval, write, and verify.

### 9. Build the continuation packet

Return the smallest context another planner, refiner, implementer, or agent needs:

- active outcome;
- active constraints and non-goals;
- governing decision IDs and sources;
- rejected or deferred alternatives relevant to the next action;
- open decisions and accountable owners;
- current stopping condition;
- re-entry and replanning triggers;
- proposal classification and permitted next step;
- stale artefacts or required revalidation.

Prefer this compact projection over replaying an unbounded transcript.

## Output contract

Return:

1. **Continuity status** — `aligned`, `changed`, `conflicting`, or `blocked`.
2. **Continuation frame** — outcome, scope, resumed artefact, stopping condition,
   and evidence coverage.
3. **Active decision set** — material decision records and authority.
4. **Proposal reconciliation** — each material proposal with classification,
   related decisions, evidence, and required action.
5. **Decision gaps and conflicts** — unresolved authority or evidence.
6. **Downstream invalidation** — `must revalidate`, `likely affected`, and
   `unaffected` artefacts.
7. **Proposed register changes** — exact additions, supersessions, and status
   changes, or `none`.
8. **Continuation packet** — compact handoff for the next workflow.

When machine-readable output is requested, use
[references/decision-register.schema.json](references/decision-register.schema.json)
for the decision register and preserve the same semantics in the surrounding
continuity report.

## Stop and escalate

Stop and request an accountable decision when:

- canonical sources conflict materially;
- acceptance or rejection cannot be attributed;
- a proposal contradicts an active decision;
- supersession would change product, architecture, policy, security, compliance,
  data, public-contract, operational, or risk-acceptance intent;
- required sources or permissions are unavailable;
- downstream invalidation cannot be bounded safely.

Ask only the smallest decision-bearing question. Explain the current decision,
the conflicting proposal, the evidence, and what cannot proceed without the
answer.

## Validation

Before returning, verify that:

- every accepted, rejected, deferred, or superseded status is attributable;
- implementation or agent prose was not mistaken for human approval;
- canonical source conflicts remain visible;
- proposal classifications trace to active decisions and evidence;
- rejected alternatives were not reopened without a qualifying trigger;
- supersession remains proposed until approved;
- downstream invalidation is dependency-based rather than speculative;
- the continuation packet is compact and sufficient;
- no decision record or external system was modified.

For calibration examples, read [references/examples.md](references/examples.md).
When evaluating or revising this skill, read
[references/evaluation-suite.md](references/evaluation-suite.md).
