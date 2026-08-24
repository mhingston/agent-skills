# Run record

- Case: `PC-E1`
- Condition: `baseline`
- Prompt: We have architecture docs in the repo, product decisions in Confluence, tickets in Jira, and generated summaries in agent sessions. Different agents keep rediscovering which source is current. Design the minimum durable project-context model and tell me what should remain authoritative.
- Expected routing: `project-context`
- Loaded skills observed in Codex events: `decision-continuity, repository-ontology`
- Agent-reported selection (not a native harness event): `none`
- Final response:

The minimum durable model is a small typed context index—not a knowledge graph and not another narrative summary. Its job is to tell every agent where each kind of truth lives, how freshness is determined, and what to do when sources disagree.

## Authority model

Authority should be claim-specific:

| Information | Authoritative source | Important boundary |
|---|---|---|
| Product outcomes, constraints, non-goals, accepted/rejected/deferred decisions, rationale | Confluence decision register or approved product brief | Only attributable human-approved decisions govern work |
| Architecture principles, system boundaries, interfaces, invariants, ADRs | Versioned repository architecture docs | Architecture docs cannot silently redefine product intent |
| Current implementation behaviour | Code, schemas, configuration, and tests at a named revision | Behaviour is evidence of reality, not evidence that it was intended or approved |
| Ticket scope, acceptance criteria, dependencies, delivery status, assignee | Jira | Jira may reference decisions but should not become a second decision register |
| Generated summaries, handoffs, retrieval indexes, session notes | Agent-session storage or ignored `.agent-artifacts` | Derived, disposable, and never authoritative |
| Cross-source authority and freshness rules | One versioned project-context manifest in the repo | Contains pointers and policy, not copied source content |

This avoids declaring Confluence, Jira, or Git “the single source of truth” globally. Each is authoritative for a defined claim type.

## Minimum conceptual model

Use five record types:

1. `SourceAuthority`

   Defines a source, the claim types it governs, its owner, and how to determine its current version.

2. `IntentClaim`

   A product outcome, constraint, non-goal, success criterion, or invariant. It carries authority, provenance, scope, source locator, and source version.

3. `Decision`

   A stable ID, statement, status, scope, decision maker, rationale, source, date, and any `supersedes` or review condition. Status is one of `accepted`, `rejected`, `deferred`, `open`, `superseded`, `expired`, or `unknown`.

4. `WorkItem`

   A Jira ticket with delivery state and links to the intent claims, decisions, architecture records, and repository revision that govern it. It must not copy their rationale as if Jira owned it.

5. `ContextProjection`

   A generated continuation packet or agent summary. It records `derivedFrom`, source versions, creation time, scope, and expiration/freshness state. It can accelerate retrieval but cannot govern work.

The essential relationships are:

```text
WorkItem ──governedBy──> IntentClaim / Decision
WorkItem ──constrainedBy──> Architecture record
Architecture record ──implements/refines──> IntentClaim / Decision
ContextProjection ──derivedFrom──> all relevant sources
Decision ──supersedes/dependsOn──> Decision
Every record ──authorisedBy / sourcedFrom──> SourceAuthority
```

That is a `typed-concept-model`. RDF, embeddings, or a knowledge graph add cost without solving the present authority problem.

## Durable repository manifest

Keep one small, versioned file such as `project-context.yaml` containing:

```yaml
schema_version: 1

authorities:
  product_intent:
    system: confluence
    canonical_location: "<decision-register URL or page ID>"
    owner: "<role or group>"

  architecture:
    system: repository
    canonical_location: "docs/architecture/"
    owner: "<role or group>"

  delivery:
    system: jira
    project: "<project key>"
    owner: "<role or group>"

  implementation_reality:
    system: git
    reference: "revision-bound"
    owner: "<team>"

derived_context:
  agent_summaries:
    authority: none
    must_include:
      - source_locator
      - source_version
      - generated_at
      - scope
    stale_when_source_changes: true

conflict_policy:
  - "Do not resolve conflicts by timestamp alone."
  - "Stop when two authoritative sources conflict materially."
  - "Implementation cannot prove product or architecture approval."
  - "A later agent summary cannot supersede a human-approved decision."
```

Keep pointers, authority rules, and ownership here. Do not mirror Confluence decisions or Jira tickets into this file; copied content becomes stale and creates another candidate source of truth.

## Agent retrieval rule

At the start of consequential work, an agent should:

1. Read the project-context manifest.
2. Resolve only the sources governing the current ticket.
3. Fetch active product decisions and relevant architecture records.
4. Bind implementation claims to the current Git revision.
5. treat Jira as delivery scope and status.
6. Treat summaries as hints, then verify every load-bearing claim against its cited source.
7. Stop if authority is missing, sources materially conflict, or a proposed change would supersede an accepted decision.

The resulting continuation packet should contain only governing intent, active decision IDs, relevant rejected/deferred alternatives, architecture constraints, open questions, source versions, and the permitted next action.

## Governance rules that prevent rediscovery

- Every durable decision gets one stable ID and one canonical record.
- ADRs link to product-decision IDs when architecture implements a product choice.
- Jira tickets link to decision and ADR IDs; they do not duplicate rationale.
- Every generated summary includes source locators and versions. Missing provenance makes it non-governing.
- Changes to a decision happen in its authoritative system. Other systems receive links or stale markers.
- “Latest” means current according to the source’s lifecycle and supersession rules—not simply the most recently edited page.
- Contradictions remain visible until an accountable human resolves them.

Based on the accessible repository evidence, these authority declarations do not yet exist here; the repo currently exposes only its skill catalogue. Therefore this is a proposed governance model, not a claim about an already-approved project policy.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
