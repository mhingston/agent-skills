# Run record

- Case: `AWD-E4`
- Condition: `candidate`
- Prompt: I already have an agent workflow. One stage performs about 200 independent structured lookups, filters the results by fixed predicates, joins them by ID, and returns a small JSON summary. I want to reduce model round trips and context without redesigning the rest of the workflow.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling`
- Final response:

This stage is an excellent fit for programmatic tool calling because every intermediate decision is deterministic.

Keep the surrounding workflow unchanged, but replace the stage’s repeated model/tool loop with one composite operation:

```text
workflow → batch_lookup(ids, predicates) → compact JSON → workflow
```

Inside that operation:

1. Normalize and deduplicate the IDs.
2. Prefer the data source’s native bulk endpoint, if available.
3. Otherwise run bounded concurrent lookups in chunks.
4. Validate each structured response.
5. Apply the fixed predicates in code.
6. Join by ID and compute the summary deterministically.
7. Return only the summary, provenance, counts, and failures.

A suitable response shape is:

```json
{
  "status": "completed",
  "summary": {},
  "counts": {
    "requested": 200,
    "unique": 197,
    "completed": 197,
    "matched": 23,
    "failed": 0
  },
  "source_ids": ["..."],
  "missing_ids": [],
  "failures": []
}
```

Use, in preference order:

- An existing batch/filter/aggregate API.
- Native programmatic tool calling, if your model runtime lets code invoke allowlisted tools.
- A small local orchestration function when the APIs are directly accessible.
- A narrow composite MCP/tool endpoint when the individual lookups exist only as agent tools and this stage recurs.

Set explicit concurrency, timeout, chunk-size, and retry limits; label partial results; preserve source IDs; and retry only read-only/idempotent operations.

This should reduce the stage to roughly one model resumption and one compact result entering context. It may still perform about 200 downstream lookups unless batching, deduplication, caching, or projection eliminates some of them. No subagents or workflow redesign are needed.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
