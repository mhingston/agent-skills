# Run record

- Case: `PTC-E1`
- Condition: `baseline`
- Prompt: I need to fetch the same three fields for about 250 customer IDs from an existing read-only tool, drop records with status=inactive, group the rest by region, and return counts plus the source IDs. The predicates are fixed and I want to reduce model round trips and context growth.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `agent-workflow-design`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use a two-stage deterministic pipeline, not a per-ID model loop.

1. Batch the 250 IDs into chunks the read-only tool accepts efficiently.
2. Request only the same 3 fields for each ID, with the fixed predicates applied server-side if the tool supports it.
3. Filter out `status=inactive` in code.
4. Group the remaining records by `region` in code.
5. Return `count` plus the source `customer_id` list for each region.

A good contract is:

```json
{
  "customer_ids": ["...250 ids..."],
  "fields": ["field1", "field2", "field3"],
  "predicate": {
    "status": "active"
  }
}
```

Then post-process deterministically into:

```json
{
  "by_region": [
    {
      "region": "NA",
      "count": 42,
      "source_ids": ["id1", "id2", "id3"]
    }
  ]
}
```

To reduce round trips and context growth:

- Use chunked tool calls, not one call per ID.
- Keep the predicate fixed outside the model prompt, ideally as tool arguments or a query object.
- Do the grouping/filtering in code, not in the model.
- Pass only compact summaries forward between steps.
- If the tool supports bulk export, prefer one export call plus local processing.

If you need the model involved at all, limit it to one bounded decision:
- map the tool’s raw output into the output schema.

If you want, I can turn this into a concrete orchestration pattern or pseudocode for your specific tool interface.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
