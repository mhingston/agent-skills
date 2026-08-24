# Run record

- Case: `PTC-E2`
- Condition: `baseline`
- Prompt: My harness can't call MCP tools from generated code, but the same read-only API is available locally through an authenticated project CLI. I have 400 item IDs and need to query them in bounded chunks, deduplicate results, validate the JSON schema, and emit one machine-readable summary for the model.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `plan, implement-ticket, dynamic-workflows, agent-workflow-design, agent-readiness`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use a 3-stage local pipeline and keep the model-facing output to one validated JSON blob:

1. Chunk the 400 IDs into bounded batches, e.g. 25-50 IDs per CLI call.
2. Call the authenticated project CLI from the host environment, not from generated code.
3. Merge, deduplicate, validate against the schema, then emit one summary JSON object.

A practical shape:

```text
IDs -> chunker -> CLI fetch per chunk -> merge -> dedupe -> schema validate -> summary.json
```

Suggested rules:
- Batch size: fixed upper bound, e.g. `50`
- Retry policy: retry each chunk independently on transient failure
- Dedup key: stable object key such as `id`, or a composite key if the API returns multiple rows per ID
- Validation: validate every returned item before merge, then validate the final aggregate
- Output: one machine-readable JSON document, no prose

Minimal summary contract:

```json
{
  "requested_ids": 400,
  "chunk_size": 50,
  "chunks_total": 8,
  "chunks_succeeded": 8,
  "chunks_failed": 0,
  "items_returned": 0,
  "items_unique": 0,
  "items_duplicate": 0,
  "invalid_items": 0,
  "schema_valid": true,
  "errors": [],
  "result": []
}
```

Implementation pattern:
- `split(ids, 50)` to produce chunk files or stdin payloads
- `cli fetch --ids ...` for each chunk
- `jq` or a small local parser to normalize results
- `sort | uniq` only if the records are line-oriented and already canonical; otherwise dedupe in JSON-aware code
- validate with a JSON Schema validator before emitting the final blob

If you want this to be robust in a harness, make the orchestrator own all effects:
- generated code only requests “fetch chunk N”
- the local wrapper actually runs the CLI
- the wrapper returns structured JSON to the model
- the model never needs direct MCP access

If you share the exact CLI command and the item schema, I can turn this into a concrete wrapper and validation flow.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
