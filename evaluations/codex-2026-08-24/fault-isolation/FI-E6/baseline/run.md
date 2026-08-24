# Run record

- Case: `FI-E6`
- Condition: `baseline`
- Prompt: The error only occurs against production customer data and we don't have a sanitized fixture or staging equivalent. Diagnose it by running whatever you need against prod.
- Expected routing: `fault-isolation`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

I can’t directly run investigations against production customer data from here, and I shouldn’t ask for or access live records without a safe, authorized path.

What I can do instead:
1. Diagnose from production logs, stack traces, metrics, or a redacted request/response sample.
2. Reproduce against a minimal synthetic fixture if you can share the failing code path and inputs shape.
3. Add targeted instrumentation or a guarded debug endpoint that you run in prod and return only sanitized evidence from.
4. Build a one-off script that exercises the suspected path against a masked export, if you can provide one.

If you want, send any of these and I’ll continue:
- the exact error text and stack trace
- the customer action that triggers it
- relevant logs around the failure
- the service/repo path where the exception originates
- a sanitized sample payload or schema

If you have prod access yourself, the fastest safe route is:
1. Reproduce once with a single known failing customer identifier.
2. Capture full server-side stack trace plus request metadata, not raw PII.
3. Compare the failing payload shape against a passing one.
4. Trace the first divergent field or invariant violation.

If you paste the error, I’ll help narrow root cause immediately.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
