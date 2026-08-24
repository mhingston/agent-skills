# Run record

- Case: `PTC-E9`
- Condition: `baseline`
- Prompt: Fetch every account in the supplied ID set and produce a reconciliation report. The compliance verifier requires a row for every input ID, including missing and failed lookups. Don't stop after you see enough examples.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `none`
- Final response:

I’m missing two required inputs:

1. The account ID set—paste it or provide the file.
2. The account system/source to query.

I’ll return one reconciliation row per input occurrence with statuses such as `found`, `missing`, or `lookup_failed`, without stopping early.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
