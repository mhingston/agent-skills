# Run record

- Case: `PC-E6`
- Condition: `baseline`
- Prompt: Agents can find our docs, but they still have to read twenty files to determine what is ready, what is blocked, and whether Jira disagrees with the project record. What deterministic interface should we add?
- Expected routing: `project-context`
- Loaded skills observed in Codex events: `decision-continuity, plan, repository-ontology`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Add a single machine-readable **workstream state interface**, not another narrative doc.

**Recommendation**
Create a canonical `project-context` record, backed by a strict schema, that answers three questions deterministically:

1. `ready` or `blocked`
2. why, in machine-readable terms
3. whether Jira disagrees with the project record

**Shape**
Use one JSON file per work item or workstream, for example:

```json
{
  "id": "PAY-1234",
  "state": "blocked",
  "reason_code": "missing_decision",
  "ready": false,
  "blocked_by": [
    {
      "type": "decision",
      "id": "D-17",
      "status": "open"
    }
  ],
  "acceptance_criteria": [
    "..."
  ],
  "invariants": [
    "..."
  ],
  "authoritative_sources": [
    "ADR-004",
    "spec-v3"
  ],
  "jira": {
    "issue_key": "PAY-1234",
    "status": "In Progress",
    "last_synced_at": "2026-08-24T00:00:00Z",
    "disagreement": "status_mismatch"
  },
  "freshness": {
    "recorded_at": "2026-08-24T00:00:00Z",
    "source_revision": "abc123"
  }
}
```

**Why this interface**
- It collapses “read twenty files” into one deterministic query surface.
- It separates `state` from `reason_code`, so agents can tell *blocked because of what*.
- It preserves source authority instead of inferring truth from prose.
- It makes Jira parity explicit instead of leaving agents to compare stories manually.

**Minimum contract**
The schema should enforce:
- a closed enum for `state` such as `ready | blocked | deferred | done`
- a closed enum for `reason_code`
- explicit blocker references
- explicit authoritative source references
- explicit Jira reconciliation status such as `aligned | stale | mismatch | unknown`

**Best companion**
Add a deterministic generator or validator, so the interface is produced from the canonical sources rather than hand-maintained. That fits the repo’s existing emphasis on durable project context and decision continuity in [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-xlwo84dd/repo/README.md).

If you want, I can turn this into:
1. a JSON Schema,
2. a compact file layout for the repo, or
3. a concrete `project-context` / `decision-continuity` interface design.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
