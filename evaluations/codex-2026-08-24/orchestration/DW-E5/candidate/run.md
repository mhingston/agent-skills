# Run record

- Case: `DW-E5`
- Condition: `candidate`
- Prompt: Build a Mastra dynamic workflow that fetches data from two registered APIs in parallel, combines the results, applies a deterministic threshold, and sends a notification. There is no repository or coding-agent work involved.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `dynamic-workflows`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use this as a deterministic Mastra dynamic workflow shape:

```ts
// Pseudocode / workflow blueprint
export const parallelFetchCombineThresholdNotify = {
  id: "parallelFetchCombineThresholdNotify",
  inputSchema: {
    type: "object",
    properties: {
      threshold: { type: "number" },
      recipient: { type: "string" },
    },
    required: ["threshold", "recipient"],
  },

  steps: [
    {
      id: "fetch_api_a",
      type: "tool",
      tool: "registeredApiA.fetch",
      input: {},
      run: "parallel",
    },
    {
      id: "fetch_api_b",
      type: "tool",
      tool: "registeredApiB.fetch",
      input: {},
      run: "parallel",
    },
    {
      id: "combine_results",
      type: "transform",
      input: {
        a: "{{steps.fetch_api_a.output}}",
        b: "{{steps.fetch_api_b.output}}",
      },
      outputSchema: {
        type: "object",
        properties: {
          score: { type: "number" },
          details: { type: "object" },
        },
        required: ["score", "details"],
      },
      run: ({ a, b }) => {
        const score = (a.value ?? 0) + (b.value ?? 0);
        return {
          score,
          details: { a, b },
        };
      },
    },
    {
      id: "apply_threshold",
      type: "condition",
      input: {
        score: "{{steps.combine_results.output.score}}",
        threshold: "{{input.threshold}}",
      },
      branches: {
        above: "notify",
        below: "stop_no_notify",
      },
      run: ({ score, threshold }) => score >= threshold,
    },
    {
      id: "notify",
      type: "tool",
      tool: "registeredNotifier.send",
      input: {
        recipient: "{{input.recipient}}",
        message: "Combined score {{steps.combine_results.output.score}} met threshold {{input.threshold}}.",
      },
    },
    {
      id: "stop_no_notify",
      type: "end",
      output: {
        status: "below_threshold",
        score: "{{steps.combine_results.output.score}}",
      },
    },
  ],
};
```

What it does:
1. Fetches from two registered APIs in parallel.
2. Combines the two responses deterministically.
3. Applies a fixed threshold comparison.
4. Sends a notification only if the threshold is met.

A cleaner operational version would have these explicit constraints:
- Parallelism only for the two independent fetch steps.
- No model-based decision-making in the threshold path.
- Fixed JSON schemas for both API outputs and the combined payload.
- One notification side effect, guarded by the condition step.

If you want, I can turn this into:
1. a Mastra-native TypeScript implementation,
2. a JSON workflow definition, or
3. a version with retries, timeout handling, and failure notifications.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
