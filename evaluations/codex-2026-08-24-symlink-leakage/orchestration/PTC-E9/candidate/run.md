# Run record

- Case: `PTC-E9`
- Condition: `candidate`
- Prompt: Fetch every account in the supplied ID set and produce a reconciliation report. The compliance verifier requires a row for every input ID, including missing and failed lookups. Don't stop after you see enough examples.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling`
- Final response:

I can do the exhaustive reconciliation, but the supplied ID set and account lookup source aren’t available in the message, workspace, or connected tools.

Please provide:

- The complete ID set (paste or upload it).
- The account system/API to query, or an exported account dataset.

I’ll return exactly one row per input occurrence with statuses such as `found`, `missing`, `lookup_failed`, or `invalid_id`, plus reconciled totals.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
