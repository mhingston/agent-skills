# Run record

- Case: `PTC-E1`
- Condition: `candidate`
- Prompt: I need to fetch the same three fields for about 250 customer IDs from an existing read-only tool, drop records with status=inactive, group the rest by region, and return counts plus the source IDs. The predicates are fixed and I want to reduce model round trips and context growth.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling`
- Final response:

Use one bounded programmatic tool call that performs the fan-out and deterministic reduction in code.

Recommended contract:

- Normalize and deduplicate the ~250 customer IDs.
- Prefer a native bulk lookup if the read-only tool supports one.
- Otherwise fetch only the three required fields in chunks, with bounded concurrency.
- Validate every response.
- Drop records where `status === "inactive"`.
- Group remaining records by `region`.
- Return only counts, source customer IDs, and failure metadata.

Example result:

```json
{
  "status": "completed",
  "regions": {
    "emea": {
      "count": 81,
      "source_ids": ["cust_001", "cust_007"]
    },
    "amer": {
      "count": 103,
      "source_ids": ["cust_002", "cust_009"]
    }
  },
  "summary": {
    "input_ids": 250,
    "unique_ids": 247,
    "active_records": 184,
    "inactive_dropped": 59,
    "missing": 2,
    "failed": 2
  },
  "failures": [
    {"source_id": "cust_123", "reason": "timeout"}
  ]
}
```

Operational bounds I’d use:

- Chunk size: 25–50 IDs
- Concurrency: 8–12 read-only requests
- Retries: at most 2 for timeouts, rate limits, and transient server failures
- No retries for malformed IDs or authorization failures
- Per-call and total timeouts
- Explicit `partial` status if any IDs remain unresolved
- Final reconciliation invariant:

```text
unique_ids = active_records + inactive_dropped + missing + failed
```

This should reduce roughly 250 model resumptions to one. It does not necessarily reduce the 250 underlying lookups unless the source tool offers batching. The main savings are model round trips and context volume because raw records are filtered and aggregated before reaching the model.

No autonomous agent loop is needed: this is a fixed, deterministic sequence with a mechanically checkable completion condition. If this operation will recur, the durable version is a narrow composite tool such as `summarize_customers_by_region(ids)` rather than regenerating fan-out logic each time.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
