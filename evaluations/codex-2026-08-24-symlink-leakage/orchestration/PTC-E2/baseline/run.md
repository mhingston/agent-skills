# Run record

- Case: `PTC-E2`
- Condition: `baseline`
- Prompt: My harness can't call MCP tools from generated code, but the same read-only API is available locally through an authenticated project CLI. I have 400 item IDs and need to query them in bounded chunks, deduplicate results, validate the JSON schema, and emit one machine-readable summary for the model.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `dynamic-workflows`
- Final response:

Use a deterministic fan-out → aggregate pipeline. The generated code should invoke only the authenticated project CLI; no MCP or model worker is needed.

```text
400 IDs
  → normalize + deduplicate IDs
  → split into fixed-size chunks
  → query CLI with bounded concurrency and retries
  → validate every response
  → flatten + deduplicate results
  → emit exactly one JSON summary to stdout
```

Key controls:

- Fixed chunk size, e.g. 25 IDs.
- Fixed concurrency, e.g. 4 subprocesses.
- Per-call timeout and bounded retries.
- Pass IDs through stdin or argument arrays—never construct a shell command string.
- Capture CLI stdout as JSON; send diagnostics to stderr.
- Validate chunk responses before aggregation using JSON Schema/Ajv.
- Deduplicate by the API’s stable result key, not serialized object equality.
- Treat conflicting duplicates as errors or report them explicitly.
- Sort final results for reproducibility.
- Emit one final JSON document; intermediate output must not reach stdout.
- Exit nonzero if any chunk fails or violates the schema.

A suitable final envelope is:

```json
{
  "schemaVersion": "1",
  "requested": 400,
  "uniqueRequested": 397,
  "chunks": {
    "total": 16,
    "succeeded": 16,
    "failed": 0
  },
  "results": {
    "received": 401,
    "unique": 397,
    "items": []
  },
  "missingIds": [],
  "errors": []
}
```

Keep orchestration in ordinary runtime code, not in model prompts. If using a workflow runtime such as Mastra, each chunk query is a bounded read-only step and the final aggregation is deterministic. Persist only explicit JSON state so retries and resumes do not depend on conversation history.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
