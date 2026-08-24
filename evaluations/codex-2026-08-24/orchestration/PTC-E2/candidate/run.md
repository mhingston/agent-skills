# Run record

- Case: `PTC-E2`
- Condition: `candidate`
- Prompt: My harness can't call MCP tools from generated code, but the same read-only API is available locally through an authenticated project CLI. I have 400 item IDs and need to query them in bounded chunks, deduplicate results, validate the JSON schema, and emit one machine-readable summary for the model.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use a local CLI wrapper, not generated-code MCP calls.

A good shape for this is:

- Input: 400 IDs
- Chunking: fixed bounded chunks, e.g. 25 or 50 IDs per request
- Fetch: call the authenticated project CLI per chunk
- Normalize: parse JSON, reject malformed records
- Dedup: by stable key, usually `id`
- Validate: run schema validation on each record and on the final summary
- Output: one compact JSON object for the model, with counts and only the reduced evidence needed

Recommended control contract:

```text
Use local CLI for bounded read-only fetches over item IDs.
Optimize model context volume and agent-visible tool calls.
Return one JSON summary with counts, invalid records, missing IDs, and deduped items.
Stop after all chunks are processed or on fatal schema/CLI failure.
Retry transient CLI failures at most 2 times per chunk.
```

A practical implementation pattern in Node.js:

```js
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import Ajv from "ajv";

const execFileAsync = promisify(execFile);

const ITEM_SCHEMA = {
  type: "object",
  required: ["id"],
  properties: {
    id: { type: "string" },
    name: { type: "string" },
    status: { type: "string" }
  },
  additionalProperties: true
};

const SUMMARY_SCHEMA = {
  type: "object",
  required: ["status", "inputCount", "chunkCount", "dedupedCount", "invalidCount", "missingCount", "items"],
  properties: {
    status: { enum: ["completed", "partial", "failed"] },
    inputCount: { type: "integer" },
    chunkCount: { type: "integer" },
    dedupedCount: { type: "integer" },
    invalidCount: { type: "integer" },
    missingCount: { type: "integer" },
    items: { type: "array" }
  },
  additionalProperties: false
};

function chunk(array, size) {
  const out = [];
  for (let i = 0; i < array.length; i += size) out.push(array.slice(i, i + size));
  return out;
}

async function fetchChunk(ids) {
  const { stdout } = await execFileAsync("project-cli", [
    "items",
    "fetch",
    "--json",
    "--ids",
    ids.join(",")
  ]);
  return JSON.parse(stdout);
}

async function main(ids) {
  const ajv = new Ajv({ allErrors: true, strict: false });
  const validateItem = ajv.compile(ITEM_SCHEMA);
  const validateSummary = ajv.compile(SUMMARY_SCHEMA);

  const chunks = chunk([...new Set(ids)], 50);
  const seen = new Map();
  const invalid = [];
  const missing = [];

  for (const batch of chunks) {
    let payload;
    try {
      payload = await fetchChunk(batch);
    } catch (err) {
      return {
        status: "partial",
        inputCount: ids.length,
        chunkCount: chunks.length,
        dedupedCount: seen.size,
        invalidCount: invalid.length,
        missingCount: batch.length,
        items: [...seen.values()],
        error: `CLI failure: ${err.message}`
      };
    }

    const items = Array.isArray(payload.items) ? payload.items : [];
    const returnedIds = new Set();

    for (const item of items) {
      returnedIds.add(item?.id);
      if (!validateItem(item)) {
        invalid.push({ id: item?.id ?? null, errors: validateItem.errors });
        continue;
      }
      if (!seen.has(item.id)) seen.set(item.id, item);
    }

    for (const id of batch) {
      if (!returnedIds.has(id)) missing.push(id);
    }
  }

  const summary = {
    status: invalid.length || missing.length ? "partial" : "completed",
    inputCount: ids.length,
    chunkCount: chunks.length,
    dedupedCount: seen.size,
    invalidCount: invalid.length,
    missingCount: missing.length,
    items: [...seen.values()],
    invalid,
    missing
  };

  if (!validateSummary(summary)) {
    throw new Error(JSON.stringify(validateSummary.errors, null, 2));
  }

  process.stdout.write(JSON.stringify(summary));
}

main(process.argv.slice(2));
```

If you want the smallest reliable version, these are the key rules:

- Use a deterministic chunk size.
- Deduplicate input IDs before fetching.
- Validate every chunk response before merging.
- Deduplicate records by the canonical identifier.
- Emit only one final JSON blob.
- Include counts for `inputCount`, `chunkCount`, `dedupedCount`, `invalidCount`, `missingCount`, and `status`.

If you want, I can turn this into:
1. a shell script,
2. a Node script with a real JSON Schema validator and retries, or
3. a wrapper tailored to your actual project CLI command.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
