# Run record

- Case: `DW-E5`
- Condition: `baseline`
- Prompt: Build a Mastra dynamic workflow that fetches data from two registered APIs in parallel, combines the results, applies a deterministic threshold, and sends a notification. There is no repository or coding-agent work involved.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `agent-workflow-design`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Using the workflow-design guidance because this is about the workflow itself, not a repository change.

A clean Mastra design is:

- `fetchA` and `fetchB` run in parallel
- a deterministic `combine` step merges the payloads
- a deterministic `threshold` gate decides whether to notify
- a `notify` step sends the message only when the gate passes

A concise shape looks like this:

```ts
import { createWorkflow, createStep } from "@mastra/core/workflows";

const fetchA = createStep({
  id: "fetchA",
  run: async () => {
    const res = await fetch("https://api-a.example.com/data");
    if (!res.ok) throw new Error("API A failed");
    return await res.json();
  },
});

const fetchB = createStep({
  id: "fetchB",
  run: async () => {
    const res = await fetch("https://api-b.example.com/data");
    if (!res.ok) throw new Error("API B failed");
    return await res.json();
  },
});

const combine = createStep({
  id: "combine",
  run: async ({ input }: { input: { a: any; b: any } }) => {
    return {
      score: input.a.value + input.b.value,
      a: input.a,
      b: input.b,
    };
  },
});

const threshold = createStep({
  id: "threshold",
  run: async ({ input }: { input: { score: number } }) => {
    const passed = input.score >= 100;
    return { passed, score: input.score };
  },
});

const notify = createStep({
  id: "notify",
  run: async ({ input }: { input: { score: number } }) => {
    await fetch("https://notify.example.com/webhook", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        message: `Threshold reached: ${input.score}`,
      }),
    });
    return { sent: true };
  },
});

export const dynamicWorkflow = createWorkflow({
  id: "parallel-combine-threshold-notify",
})
  .parallel([fetchA, fetchB])
  .then(combine)
  .then(threshold)
  .branch([
    {
      when: ({ output }) => output.passed === true,
      then: notify,
    },
  ]);
```

Design notes:

- Parallelism is limited to the two API fetches.
- `combine` and `threshold` are deterministic, so their behavior is easy to test.
- The notification only happens after an explicit threshold check.
- If the threshold fails, the workflow ends without side effects.

If you want, I can turn this into:
1. a more realistic Mastra implementation with typed inputs/outputs, or
2. a version that supports retries, timeouts, and failure notifications.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
