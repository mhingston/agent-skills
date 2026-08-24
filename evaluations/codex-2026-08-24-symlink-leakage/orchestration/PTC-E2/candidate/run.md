# Run record

- Case: `PTC-E2`
- Condition: `candidate`
- Prompt: My harness can't call MCP tools from generated code, but the same read-only API is available locally through an authenticated project CLI. I have 400 item IDs and need to query them in bounded chunks, deduplicate results, validate the JSON schema, and emit one machine-readable summary for the model.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling`
- Final response:

Use a bounded local-script fallback. The model-generated code should invoke only the authenticated read-only project CLI; it should not attempt to bridge into MCP.

Recommended contract:

```text
Input: ≤400 unique item IDs
Chunk size: 25–50
Concurrency: 4
Retries: 2 for timeouts, rate limits, and transient CLI failures
Validation: validate every CLI response before aggregation
Deduplication: by the API’s canonical result ID
Output: exactly one JSON document on stdout
Diagnostics: stderr only
```

A Python implementation can follow this shape:

```python
#!/usr/bin/env python3
import argparse
import asyncio
import json
import random
import sys
from collections import Counter
from typing import Any

from jsonschema import Draft202012Validator

MAX_ITEMS = 400
DEFAULT_CHUNK_SIZE = 40
DEFAULT_CONCURRENCY = 4
MAX_RETRIES = 2

# Replace this with the documented CLI response schema.
CHUNK_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id"],
                "properties": {
                    "id": {"type": "string", "minLength": 1}
                },
                "additionalProperties": True,
            },
        },
        "missing_ids": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "additionalProperties": False,
}

validator = Draft202012Validator(CHUNK_RESPONSE_SCHEMA)


def chunks(values: list[str], size: int):
    for start in range(0, len(values), size):
        yield values[start:start + size]


async def query_chunk(
    item_ids: list[str],
    semaphore: asyncio.Semaphore,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    # Pass arguments directly—never construct a shell command from item IDs.
    argv = [
        "project-cli",
        "items",
        "get-batch",
        "--output",
        "json",
        "--ids",
        ",".join(item_ids),
    ]

    async with semaphore:
        for attempt in range(MAX_RETRIES + 1):
            try:
                process = await asyncio.create_subprocess_exec(
                    *argv,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=30,
                )

                if process.returncode != 0:
                    raise RuntimeError(
                        stderr.decode("utf-8", errors="replace")[:1000]
                    )

                payload = json.loads(stdout)
                errors = sorted(
                    validator.iter_errors(payload),
                    key=lambda error: list(error.path),
                )
                if errors:
                    return None, {
                        "ids": item_ids,
                        "kind": "schema_validation",
                        "message": errors[0].message,
                    }

                return payload, None

            except (TimeoutError, RuntimeError, json.JSONDecodeError) as exc:
                if attempt == MAX_RETRIES:
                    return None, {
                        "ids": item_ids,
                        "kind": type(exc).__name__,
                        "message": str(exc)[:1000],
                    }

                await asyncio.sleep((2 ** attempt) + random.random())

    raise AssertionError("unreachable")


async def run(args: argparse.Namespace) -> dict[str, Any]:
    raw_ids = [line.strip() for line in sys.stdin if line.strip()]

    if len(raw_ids) > MAX_ITEMS:
        raise ValueError(f"At most {MAX_ITEMS} input IDs are allowed")

    # Stable input deduplication.
    unique_ids = list(dict.fromkeys(raw_ids))
    batches = list(chunks(unique_ids, args.chunk_size))
    semaphore = asyncio.Semaphore(args.concurrency)

    responses = await asyncio.gather(
        *(query_chunk(batch, semaphore) for batch in batches)
    )

    records_by_id: dict[str, dict[str, Any]] = {}
    duplicate_result_ids: Counter[str] = Counter()
    missing_ids: set[str] = set()
    failures: list[dict[str, Any]] = []

    for payload, failure in responses:
        if failure:
            failures.append(failure)
            continue

        assert payload is not None
        missing_ids.update(payload.get("missing_ids", []))

        for record in payload["items"]:
            canonical_id = record["id"]
            if canonical_id in records_by_id:
                duplicate_result_ids[canonical_id] += 1
                continue
            records_by_id[canonical_id] = record

    status = (
        "failed" if failures and not records_by_id
        else "partial" if failures or missing_ids
        else "completed"
    )

    return {
        "schema_version": "1.0",
        "status": status,
        "counts": {
            "input": len(raw_ids),
            "unique_input": len(unique_ids),
            "input_duplicates_removed": len(raw_ids) - len(unique_ids),
            "chunks": len(batches),
            "chunks_failed": len(failures),
            "records": len(records_by_id),
            "result_duplicates_removed": sum(duplicate_result_ids.values()),
            "missing": len(missing_ids),
        },
        "records": list(records_by_id.values()),
        "missing_ids": sorted(missing_ids),
        "duplicate_result_ids": dict(sorted(duplicate_result_ids.items())),
        "failures": failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        choices=range(1, 101),
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=DEFAULT_CONCURRENCY,
        choices=range(1, 9),
    )
    args = parser.parse_args()

    try:
        summary = asyncio.run(run(args))
        json.dump(summary, sys.stdout, separators=(",", ":"), sort_keys=True)
        sys.stdout.write("\n")
    except Exception as exc:
        json.dump({
            "schema_version": "1.0",
            "status": "failed",
            "counts": {},
            "records": [],
            "missing_ids": [],
            "duplicate_result_ids": {},
            "failures": [{
                "kind": type(exc).__name__,
                "message": str(exc)[:1000],
            }],
        }, sys.stdout, separators=(",", ":"), sort_keys=True)
        sys.stdout.write("\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

Invoke it with IDs on stdin:

```bash
project-id-source | python3 query_items.py > summary.json
```

Important details:

- Prefer a native CLI batch command if one exists.
- Keep credentials inside the authenticated CLI.
- Never use `shell=True` or interpolate IDs into a shell string.
- Validate each chunk before incorporating it.
- Treat schema failures and exhausted retries as visible partial failures.
- Send only `summary.json` to the model; keep progress logs on stderr.
- If records are large, project only the fields the model actually needs. This reduces model context without pretending the underlying API work disappeared.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
