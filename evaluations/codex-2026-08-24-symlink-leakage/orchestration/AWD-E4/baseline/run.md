# Run record

- Case: `AWD-E4`
- Condition: `baseline`
- Prompt: I already have an agent workflow. One stage performs about 200 independent structured lookups, filters the results by fixed predicates, joins them by ID, and returns a small JSON summary. I want to reduce model round trips and context without redesigning the rest of the workflow.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling`
- Final response:

Replace only that stage with a bounded programmatic orchestration step.

Recommended order:

1. Use a native bulk/batch lookup endpoint if the data source provides one.
2. Otherwise, use native programmatic tool calling so one model turn launches the lookups concurrently and code performs the fixed filtering/join.
3. If your harness cannot call tools from code, expose the stage as one narrow composite tool such as `build_lookup_summary(ids, predicates)`.

Its contract should be roughly:

```text
Input: up to 200 IDs
Process:
  - normalize and deduplicate IDs
  - perform read-only lookups with bounded concurrency
  - validate each structured response
  - apply fixed predicates
  - join by ID
  - produce deterministic aggregates
Output: one compact JSON object
```

Include operational metadata in that JSON:

```json
{
  "status": "completed",
  "summary": {},
  "counts": {
    "input": 200,
    "deduplicated": 198,
    "completed": 197,
    "failed": 1
  },
  "missing_ids": [],
  "failed_ids": [],
  "provenance": []
}
```

Set explicit concurrency, timeout, and retry limits—perhaps 10–25 concurrent reads and at most two retries for transient failures. Mark incomplete execution as `partial`; never silently omit failures.

This should collapse roughly 200 model resumptions and their intermediate context into one stage result. It does **not** inherently reduce the approximately 200 downstream operations unless batching, deduplication, caching, or projection is available.

No autonomous agent loop or subagents are warranted: the filtering and join are mechanically defined and require no fresh model judgment. Keep the stage’s existing input/output interface, and the rest of your workflow should need little or no redesign.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
