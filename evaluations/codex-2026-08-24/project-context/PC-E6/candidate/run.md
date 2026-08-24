# Run record

- Case: `PC-E6`
- Condition: `candidate`
- Prompt: Agents can find our docs, but they still have to read twenty files to determine what is ready, what is blocked, and whether Jira disagrees with the project record. What deterministic interface should we add?
- Expected routing: `project-context`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Add a single machine-readable **project status manifest** and treat it as the deterministic interface, not the docs themselves.

I would make it something like:

- `project-context.yaml` or `project-status.json` as the canonical entry point
- `project-context.schema.json` to lock the shape
- a small generator/checker that projects from source docs plus Jira into that file

The manifest should answer, at minimum:

- `ready`: what is unblocked and safe to pick up
- `blocked`: what is blocked, by whom/what, and since when
- `jira_disagreements`: where Jira and the project record differ
- `source_of_truth`: which document or tracker owns each claim
- `freshness`: last verified timestamp for each item
- `confidence`: whether the state is derived, asserted, or reconciled

A practical shape would be:

```json
{
  "version": 1,
  "generated_at": "2026-08-24T00:00:00Z",
  "ready": [
    {
      "id": "PAY-1234",
      "title": "Implement checkout retry",
      "owner": "implement",
      "source": ["docs/plan.md", "jira/PAY-1234"],
      "state": "ready"
    }
  ],
  "blocked": [
    {
      "id": "PAY-1235",
      "blocking_reason": "Waiting on API contract signoff",
      "blocked_by": ["PAY-1201"],
      "source": ["docs/context.md"],
      "state": "blocked"
    }
  ],
  "jira_disagreements": [
    {
      "id": "PAY-1236",
      "project_state": "ready",
      "jira_state": "in_progress",
      "diff": "status mismatch",
      "source": ["docs/context.md", "jira/PAY-1236"]
    }
  ]
}
```

Why this is the right interface:

- It collapses 20 files into one queryable answer.
- It makes “ready vs blocked vs disagreement” explicit instead of inferred.
- It separates raw evidence from the derived projection.
- It gives agents a stable contract to validate, rather than a prose summary to reinterpret.

Given your repo, I’d align this with the existing `project-context` and `decision-continuity` split in [`README.md`](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ufkve3ru/repo/README.md): `project-context` should own the manifest, and `decision-continuity` should feed the disagreement/reconciliation state.

If you want, I can draft the exact schema and the update rules next.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
