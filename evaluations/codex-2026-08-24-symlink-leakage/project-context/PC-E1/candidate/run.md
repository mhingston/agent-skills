# Run record

- Case: `PC-E1`
- Condition: `candidate`
- Prompt: We have architecture docs in the repo, product decisions in Confluence, tickets in Jira, and generated summaries in agent sessions. Different agents keep rediscovering which source is current. Design the minimum durable project-context model and tell me what should remain authoritative.
- Expected routing: `project-context`
- Loaded skills observed in Codex events: `project-context`
- Agent-reported selection (not a native harness event): `project-context`
- Final response:

## Assessment

**Need: Thin index.**

The fragmentation warrants a durable orientation layer, but not a new project database or knowledge graph. Keep the existing domain sources and add one small, versioned repository manifest that tells agents:

- which source governs each kind of claim;
- how records relate;
- what version or freshness signal was inspected;
- where conflicts exist;
- how to assemble task-specific context.

Observed: the repository already treats tracked documentation as canonical and generated agent artifacts as workflow-supporting outputs rather than project deliverables. The external Confluence, Jira, and session contents were not accessible in this assessment, so their exact ownership and freshness rules remain to be confirmed.

## What remains authoritative

| Claim | Authority | Important boundary |
|---|---|---|
| Normative architecture, interfaces, schemas, engineering constraints | Version-controlled architecture docs and ADRs | Code divergence is a conflict, not an automatic architecture decision |
| Accepted product outcomes, non-goals, and product decisions | Designated Confluence decision records | Only explicitly accepted records are authoritative; drafts remain proposals |
| Ticket workflow, assignment, dependencies, and delivery status | Jira | Jira does not become authoritative for product or architecture decisions merely by copying them |
| Ticket-specific acceptance contract | Jira, when explicitly approved and linked to governing product decisions | A ticket cannot silently override Confluence or architecture authority |
| Actual implementation at a revision | Code and configuration at that Git revision | This describes what exists, not necessarily what was intended |
| Verified behavior | Tests and recorded results bound to an exact revision | Test prose alone is not evidence that the test passed |
| Deployed/runtime state | Deployment and operational systems | Runtime observations do not automatically redefine intended architecture |
| Historical product rationale | Accepted/superseded Confluence decision history | Supersession must preserve the old decision and its rationale |
| Historical architecture rationale | ADR history | Prefer append/supersede over rewriting history |
| Agent summaries and handoffs | Nothing beyond themselves | Always informational or scratch; rebuild context from current sources |

The thin index is authoritative only for **source identity, authority mapping, relationships, and conflict rules**. It must not duplicate the substantive product or architecture prose.

## Minimum durable model

Use one tracked manifest, for example `project-context.yaml`, with four record roles:

- `truth`: current normative architecture and verified current-state sources;
- `intent`: proposed or accepted outcomes, decisions, tickets, and plans;
- `history`: superseded decisions, ADRs, releases, investigations, and evidence;
- `scratch`: generated summaries, session notes, and exploratory material.

A minimal entry needs only:

```yaml
schema_version: "1"

records:
  - id: ARCH-payments
    role: truth
    authority: canonical
    source: repo
    locator: docs/architecture/payments.md
    state: active
    freshness: git-revision

  - id: PROD-refunds
    role: intent
    authority: canonical
    source: confluence
    locator: "page-id:12345"
    state: accepted
    freshness: confluence-version

  - id: TICKET-PAY-142
    role: intent
    authority: canonical
    source: jira
    locator: PAY-142
    state: active
    freshness: jira-updated-at
    relationships:
      implements: [PROD-refunds]
      constrained_by: [ARCH-payments]

  - id: SESSION-PAY-142-latest
    role: scratch
    authority: informational
    source: agent-session
    locator: "session-id:..."
    state: active
```

Keep the vocabulary deliberately small:

- Authority: `canonical`, `derived`, `informational`
- Lifecycle: `proposed`, `accepted`, `active`, `superseded`, `archived`
- Relationships: `implements`, `constrained_by`, `depends_on`, `supersedes`, `verifies`, `evidenced_by`

Do not store copied document text, ticket descriptions, or generated summaries in this manifest.

## Conflict rules

Every duplicated material claim needs one deterministic rule:

1. A copied claim never outranks its origin.
2. Product intent conflicts resolve to the accepted Confluence decision.
3. Architecture conflicts resolve to the active architecture document or ADR for normative direction.
4. Jira owns delivery fields, but must link upstream when describing product or architecture intent.
5. Code, tests, and runtime evidence describe observed reality; they expose drift but do not approve it.
6. Session summaries lose automatically to current canonical sources.
7. If two sources both appear canonical for the same claim, report `authority-conflict`; do not choose by recency.
8. Missing or stale evidence produces `unknown`, never an inferred “current” state.

## Session orientation contract

A new agent should begin from a Jira key, decision ID, or architecture record ID and receive a freshly rebuilt packet containing:

- ticket and exact freshness timestamp;
- governing accepted product decisions and versions;
- relevant current architecture/ADR records and Git revision;
- dependencies and explicit non-goals;
- accepted, rejected, open, and superseded decisions;
- verification expectations;
- unresolved conflicts, missing links, and stale sources;
- any prior session summary, clearly labelled informational.

The packet should be generated on demand. It should never be carried forward as the new authority.

A minimal interface could provide:

```text
context validate
context resolve PAY-142
context conflicts
context stale
```

`context resolve` should return structured data as well as readable output.

## Derived states worth supporting

Only compute states that help an agent decide whether it may proceed:

- `ready`: accepted governing intent exists, required dependencies resolve, and no authority conflict is open.
- `blocked`: a named dependency or decision gate is unresolved.
- `stale`: a canonical source changed since the orientation packet or evidence was generated.
- `incomplete`: required acceptance evidence for the exact revision is absent.
- `drifted`: Jira or a generated projection disagrees with its governing source.
- `unknown`: required source access, ownership, or freshness information is unavailable.

Each state should include its rule and contributing record IDs.

## Smallest next slice

Create only the manifest and a read-only validator first. Seed it with:

- one active architecture document;
- one accepted Confluence decision;
- one Jira ticket implementing that decision;
- one agent summary marked informational.

Then test these falsifiable checks:

- removing a target causes validation to fail;
- a Jira ticket without governing intent is not `ready`;
- a session summary cannot be marked canonical;
- superseded decisions remain traceable;
- a changed Confluence version makes an existing orientation packet stale;
- a fresh agent can resolve the sample ticket without searching old sessions.

This is enough to stop rediscovery while preserving the authority of architecture docs, Confluence decisions, Jira workflow state, and revision-bound engineering evidence.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
