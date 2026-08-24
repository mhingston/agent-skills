# Run record

- Case: `PC-E6`
- Condition: `candidate`
- Prompt: Agents can find our docs, but they still have to read twenty files to determine what is ready, what is blocked, and whether Jira disagrees with the project record. What deterministic interface should we add?
- Expected routing: `project-context`
- Loaded skills observed in Codex events: `project-context`
- Agent-reported selection (not a native harness event): `project-context`
- Final response:

Add a thin, read-only project-context CLI that builds a task-orientation packet from canonical project records and compares it with Jira:

```bash
project-context orient --task PAY-1234 --format json
project-context list --state ready|blocked --format json
project-context validate
project-context reconcile jira --format json
```

The `orient` response should deterministically include:

```json
{
  "task": "PAY-1234",
  "derived_state": "blocked",
  "state_rule": "all_dependencies_resolved && accepted_intent && acceptance_evidence",
  "governing_intent": [{"id": "SPEC-12", "revision": "abc123"}],
  "dependencies": [
    {"id": "PAY-1200", "state": "open", "source": "project-record"}
  ],
  "blockers": [
    {"code": "OPEN_DEPENDENCY", "evidence": "PAY-1200"}
  ],
  "jira_projection": {
    "status": "Ready",
    "observed_at": "2026-08-24T10:00:00Z"
  },
  "conflicts": [
    {
      "field": "status",
      "canonical": "blocked",
      "jira": "Ready",
      "authority": "project-record"
    }
  ],
  "unknowns": [],
  "verification": ["make test-payments"]
}
```

Key contract:

- Readiness is derived from structured dependencies, accepted intent, and required evidence—not manually declared.
- Every result carries source identity, revision/freshness, and authority.
- Jira is explicitly a projection for fields governed by the project record; Jira-owned fields remain Jira-authoritative.
- Disagreement is returned as a first-class conflict, never silently resolved.
- Missing information produces `unknown`, not `false`, `ready`, or “probably.”
- `validate` fails on dangling references, ambiguous authority, stale projections, invalid states, or unsupported completion claims.
- Any later Jira update should use separate `reconcile --plan` and authorized `--apply` operations with read-back verification.

Classification: **Thin index**. The smallest useful next slice is `orient`, `list`, and `validate` over existing authoritative files, plus a field-ownership map for Jira. This turns twenty-file archaeology into one bounded, traceable query without creating another source of truth.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
