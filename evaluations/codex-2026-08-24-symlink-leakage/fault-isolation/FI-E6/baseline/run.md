# Run record

- Case: `FI-E6`
- Condition: `baseline`
- Prompt: The error only occurs against production customer data and we don't have a sanitized fixture or staging equivalent. Diagnose it by running whatever you need against prod.
- Expected routing: `fault-isolation`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

I can’t diagnose this yet: the workspace contains only an agent-skills catalogue, with no application code, production runbook, credentials, endpoint, logs, or failing request details.

Please provide:

- The service/repository and observed error or trace
- A failing request/correlation ID and approximate timestamp
- The approved read-only production access method
- Any customer/account identifier, preferably opaque rather than raw PII

I’ll keep production diagnostics bounded and read-only, avoid exporting customer records, redact sensitive output, and won’t run mutations or unbounded scans.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
