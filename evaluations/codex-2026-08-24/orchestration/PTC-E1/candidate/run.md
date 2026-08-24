# Run record

- Case: `PTC-E1`
- Condition: `candidate`
- Prompt: I need to fetch the same three fields for about 250 customer IDs from an existing read-only tool, drop records with status=inactive, group the rest by region, and return counts plus the source IDs. The predicates are fixed and I want to reduce model round trips and context growth.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use a single bounded batch stage, not 250 individual model-driven calls.

**Pattern**
- Input: `customer_ids[]`
- Tool call: one batch fetch against the read-only tool for the 3 fixed fields only
- Deterministic reduction in code:
  - drop records where `status == "inactive"`
  - group remaining records by `region`
  - count per region
  - collect source `customer_id`s per region
- Output: compact summary only, not raw rows unless you need them for audit

**Best execution contract**
```text
Use one batch read-only fetch for up to 250 customer IDs with fixed field projection.
Optimize model round trips and context volume.
Return per-region counts and source customer IDs after filtering inactive records.
Stop after one fetch plus deterministic local aggregation.
```

**Why this is the right shape**
- It removes the model from the inner loop entirely.
- Context stays small because you never re-inject 250 per-ID results as separate turns.
- The predicates are fixed, so the filtering and grouping should be done deterministically, not by the model.

**If the tool supports it**
- Prefer a native batch endpoint: `fetch_customers(ids=[...], fields=[f1,f2,f3])`
- Even better, if the tool can accept server-side filters:
  - `status != inactive`
  - `group_by = region`
  - `count = true`
  - `return_ids = true`
- That is the lowest-cost option because it reduces both downstream payload and model-visible context.

**If the tool does not support batching**
- Chunk the 250 IDs into fixed batches, for example 25 or 50.
- Fetch all chunks in a deterministic loop.
- Aggregate locally after each chunk or at the end.
- Only return the reduced grouped result to the model.

**Recommended result shape**
```json
{
  "status": "completed",
  "total_input_ids": 250,
  "total_returned_records": 241,
  "filtered_inactive": 9,
  "by_region": [
    {
      "region": "EMEA",
      "count": 87,
      "customer_ids": ["C123", "C456"]
    }
  ]
}
```

If you want, I can help you turn this into:
1. a concrete pseudo-code loop,
2. a wrapper/composite tool spec, or
3. a provider-specific implementation pattern.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
