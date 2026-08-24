# Run record

- Case: `PTC-E1`
- Condition: `baseline`
- Prompt: I need to fetch the same three fields for about 250 customer IDs from an existing read-only tool, drop records with status=inactive, group the rest by region, and return counts plus the source IDs. The predicates are fixed and I want to reduce model round trips and context growth.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `dynamic-workflows`
- Final response:

Use a deterministic fan-out/fan-in workflow—no model workers are needed because projection, filtering, and grouping are fixed.

```text
250 customer IDs
  → split into bounded batches
  → fetch only [source_id, status, region]
  → discard status == "inactive"
  → group by region
  → emit { region, count, source_ids[] }
```

Key choices:

- Run the read-only fetches in the workflow/runtime, not through repeated model turns.
- If the tool supports bulk lookup, send batches at its maximum supported size. Otherwise use bounded concurrency, such as 10–20 calls at once.
- Keep raw responses out of model context. Pass structured data directly between deterministic steps.
- Project only the three required fields.
- Deduplicate input IDs and define behavior for missing IDs, duplicate records, null regions, tool errors, and retries.
- Calculate `count` from the final `source_ids` array so the two cannot disagree.
- Sort regions and IDs for reproducible output.
- Return one compact final object:

```json
{
  "regions": [
    {
      "region": "north",
      "count": 42,
      "source_ids": ["C001", "C007", "C019"]
    }
  ],
  "missing_ids": [],
  "failed_ids": []
}
```

This should require one model interaction at most: submitting the job and receiving its final result. The runtime owns batching, concurrency, retries, filtering, and aggregation. An adaptive planner or supervisor agent would only add latency and context growth here.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
