# Run record

- Case: `AWD-E4`
- Condition: `baseline`
- Prompt: I already have an agent workflow. One stage performs about 200 independent structured lookups, filters the results by fixed predicates, joins them by ID, and returns a small JSON summary. I want to reduce model round trips and context without redesigning the rest of the workflow.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling, dynamic-workflows`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use **programmatic-tool-calling** for that stage, not a redesign of the whole workflow.

The smallest effective change is:

- keep the rest of the workflow as-is
- replace the 200-call stage with one bounded deterministic executor
- have that executor:
  - fan out the independent lookups in parallel
  - apply the fixed predicates in code
  - join by ID in code
  - return only the small JSON summary the next stage needs

What this buys you:

- fewer model resumptions
- much smaller context, because intermediates never enter the model
- less duplicated prompt overhead
- no change to the downstream workflow contract

The key design choice is to move only the **predictable plumbing** out of the model, not the semantic decisions. If the predicates and join keys are fixed, this stage is a good fit for code. If any step needs fresh judgment after each lookup, keep that part model-driven.

Recommended shape:

```text
Stage contract:
- Input: list of ~200 IDs
- Tool set: lookup API(s) only
- Deterministic work: fetch -> filter -> join -> aggregate
- Output: compact JSON summary
- Stop: when all IDs processed or explicit failure threshold reached
- Retry: transient lookup failures only, bounded
```

If you already have a tool layer, the best implementation is usually one of these:

1. A single composite tool that performs the fan-out/filter/join and returns the summary.
2. A local script or service wrapper around the existing lookup APIs.
3. Native batch/aggregate endpoints, if the source system already supports them.

If you want, I can help you turn your current stage into a concrete execution contract or a minimal composite tool interface.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
