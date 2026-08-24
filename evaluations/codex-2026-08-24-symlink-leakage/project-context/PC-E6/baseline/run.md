# Run record

- Case: `PC-E6`
- Condition: `baseline`
- Prompt: Agents can find our docs, but they still have to read twenty files to determine what is ready, what is blocked, and whether Jira disagrees with the project record. What deterministic interface should we add?
- Expected routing: `project-context`
- Loaded skills observed in Codex events: `repository-ontology`
- Agent-reported selection (not a native harness event): `repository-ontology`
- Final response:

Add a versioned, machine-readable **Project State Projection**: a deterministic read-only interface generated from the canonical project record and Jira.

Expose it as both:

```bash
project-state inspect --format json
project-state inspect PAY-1234 --format json
```

and a generated `.agent-context/project-state.json` or equivalent API response.

Each work item should return:

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-08-24T10:00:00Z",
  "source_revisions": {
    "project_record": "sha256:...",
    "jira_sync": "2026-08-24T09:58:00Z"
  },
  "items": [{
    "id": "PAY-1234",
    "state": "blocked",
    "ready": false,
    "readiness_rule": "ticket-ready@2",
    "failed_preconditions": ["acceptance_criteria_confirmed"],
    "blockers": [{
      "id": "BLK-17",
      "kind": "unresolved-decision",
      "summary": "Retry ownership is undecided",
      "evidence": ["project/decisions/retry-policy.md#open-question"]
    }],
    "discrepancies": [{
      "field": "status",
      "canonical": {
        "value": "blocked",
        "source": "project-record"
      },
      "projection": {
        "value": "Ready for Development",
        "source": "jira"
      },
      "resolution": "unresolved",
      "severity": "blocking"
    }]
  }]
}
```

The contract should guarantee:

- `ready` is derived by a versioned, testable rule—not copied from Jira or inferred by an agent.
- Every state, blocker, and precondition has source provenance and freshness.
- Authority is defined per field. Jira may own scheduling fields without owning accepted intent or readiness.
- Disagreements remain explicit `discrepancies`; generation must never silently choose, merge, or update either source.
- Missing, stale, ambiguous, and disputed data fail closed using controlled states such as `ready`, `blocked`, `not_ready`, `unknown`, and `disputed`.
- Output ordering and identifiers are stable, with JSON Schema validation and fixture-based tests.
- Agents consume this interface first and open underlying documents only for evidence or remediation.

The minimum semantic model is a typed concept model—`WorkItem`, `ReadinessAssessment`, `Precondition`, `Blocker`, `SourceAssertion`, and `Discrepancy`—plus deterministic projection rules. RDF or a knowledge graph would add maintenance cost without improving these bounded queries.

This follows the repository’s existing rule that projections may encode authority and derived state but must not become a competing source of truth ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-kj581ug3/repo/README.md:249)).

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
