# Run record

- Case: `FI-E2`
- Condition: `candidate`
- Prompt: This endpoint became much slower after last week's changes. Work out what caused the regression and give me evidence I can hand to an implementer.
- Expected routing: `fault-isolation`
- Loaded skills observed in Codex events: `fault-isolation`
- Agent-reported selection (not a native harness event): `none`
- Final response:

`BLOCKED` — the supplied workspace does not contain the endpoint or its history, so no responsible root-cause claim is possible.

- **Symptom contract:** Endpoint slowdown reported after last week’s changes. Endpoint identity, expected/actual latency, workload, and affected revision are unknown.
- **Feedback signal:** None constructible. There is no application code, benchmark, test, trace, or request fixture.
- **Repository evidence:**
  - `master` has no commits.
  - No branches or remotes exist.
  - Git contains zero objects.
  - The only product-visible file is an uncommitted `README.md` describing an Agent Skills catalogue.
- **Hypotheses:** Not generated because there is no observable execution path or change set; doing so would be speculation.
- **Causal finding:** No causal boundary established.
- **Cleanup:** No files or external state changed.

To continue, provide the application repository and identify the endpoint. Ideally also include one of:

1. Last-known-good and first-known-bad revisions.
2. A representative request/fixture and local run instructions.
3. Before/after latency measurements, traces, or profiles.

With the repository plus revisions, the next investigation should benchmark both states repeatedly, bisect the regression, profile the earliest bad revision, and return the responsible code path with a fix-independent regression benchmark.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
