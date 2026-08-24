# Run record

- Case: `AWD-E4`
- Condition: `candidate`
- Prompt: I already have an agent workflow. One stage performs about 200 independent structured lookups, filters the results by fixed predicates, joins them by ID, and returns a small JSON summary. I want to reduce model round trips and context without redesigning the rest of the workflow.
- Expected routing: `programmatic-tool-calling`
- Loaded skills observed in Codex events: `programmatic-tool-calling, agent-workflow-design`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use a deterministic orchestration stage, not more model turns.

For your specific stage, the best fit is:

- one bounded batch/fan-out step that performs the ~200 lookups
- fixed-predicate filtering in code
- join-by-ID in code
- a small JSON summary returned to the model only at the end

That cuts both model resumptions and context volume without changing the rest of the workflow.

A good contract for that stage is:

```text
Use deterministic orchestration for 200 independent structured lookups, fixed-predicate filtering, and ID join.
Optimize model round trips and context volume.
Return a small JSON summary with counts, matched IDs, missing IDs, and any failures.
Stop after one batch pass; retry only transient lookup failures within a fixed bound.
```

Implementation options, in order:

1. Native batch or aggregate API, if the lookup system already supports it.
2. A small local script or composite tool that:
   - deduplicates inputs
   - runs lookups concurrently
   - validates schemas
   - filters by the fixed predicates
   - joins on ID
   - emits the reduced JSON
3. Direct model/tool calls only if the lookup results require semantic judgment after each item.

What to keep in model context:

- the final reduced summary
- provenance needed for validation, like source IDs and counts
- explicit missing/malformed items

What to keep out of model context:

- raw lookup payloads
- intermediate filtered lists
- join mechanics
- per-item retries unless they materially change the outcome

The key design rule is: if the predicates and join are fixed, do not ask the model to do that work. Let code own it, and let the model only interpret the final summary if interpretation is still needed.

If you want, I can turn this into a concrete stage contract or pseudocode for your current workflow shape.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
