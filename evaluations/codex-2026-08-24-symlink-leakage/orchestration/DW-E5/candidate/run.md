# Run record

- Case: `DW-E5`
- Condition: `candidate`
- Prompt: Build a Mastra dynamic workflow that fetches data from two registered APIs in parallel, combines the results, applies a deterministic threshold, and sends a notification. There is no repository or coding-agent work involved.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `dynamic-workflows`
- Final response:

Below is a deterministic Mastra dynamic workflow definition. It calls registered tools `api-a-fetch` and `api-b-fetch` concurrently, joins their outputs, invokes a pure threshold tool, then sends the resulting verdict through `send-notification`.

```ts
const workflowDefinition = {
  id: "parallel-api-threshold-notification",
  description:
    "Fetch two API measurements concurrently, apply a deterministic threshold, and notify.",

  inputSchema: {
    type: "object",
    properties: {
      subjectId: { type: "string" },
      threshold: { type: "number" },
      recipient: { type: "string" },
    },
    required: ["subjectId", "threshold", "recipient"],
    additionalProperties: false,
  },

  outputSchema: {
    type: "object",
    properties: {
      delivered: { type: "boolean" },
      notificationId: { type: "string" },
    },
    required: ["delivered"],
  },

  graph: [
    {
      type: "parallel",
      steps: [
        {
          type: "tool",
          id: "fetch-api-a",
          toolId: "api-a-fetch",
          options: { retries: 2 },
        },
        {
          type: "tool",
          id: "fetch-api-b",
          toolId: "api-b-fetch",
          options: { retries: 2 },
        },
      ],
    },

    {
      type: "mapping",
      id: "prepare-threshold-input",
      mapConfig: JSON.stringify({
        apiAValue: { step: "fetch-api-a", path: "value" },
        apiBValue: { step: "fetch-api-b", path: "value" },
        threshold: { initData: true, path: "threshold" },
        subjectId: { initData: true, path: "subjectId" },
      }),
    },

    {
      type: "tool",
      id: "evaluate-threshold",
      toolId: "combine-and-threshold",
    },

    {
      type: "mapping",
      id: "prepare-notification",
      mapConfig: JSON.stringify({
        recipient: { initData: true, path: "recipient" },
        subjectId: { initData: true, path: "subjectId" },
        combinedValue: {
          step: "evaluate-threshold",
          path: "combinedValue",
        },
        threshold: {
          step: "evaluate-threshold",
          path: "threshold",
        },
        exceeded: {
          step: "evaluate-threshold",
          path: "exceeded",
        },
      }),
    },

    {
      type: "tool",
      id: "notify",
      toolId: "send-notification",
      options: { retries: 2 },
    },
  ],
};
```

The registered tools should have compatible contracts:

```ts
// api-a-fetch and api-b-fetch
type ApiInput = {
  subjectId: string;
  threshold: number;
  recipient: string;
};

type ApiOutput = {
  value: number;
};

// combine-and-threshold — pure and deterministic
type ThresholdInput = {
  apiAValue: number;
  apiBValue: number;
  threshold: number;
  subjectId: string;
};

type ThresholdOutput = {
  combinedValue: number;
  threshold: number;
  exceeded: boolean;
};

// Example implementation:
// combinedValue = apiAValue + apiBValue
// exceeded = combinedValue >= threshold

// send-notification
type NotificationOutput = {
  delivered: boolean;
  notificationId?: string;
};
```

Register or update it on a running Mastra server:

```ts
const response = await fetch(
  `${process.env.MASTRA_URL}/api/stored/workflows`,
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${process.env.MASTRA_TOKEN}`,
    },
    body: JSON.stringify(workflowDefinition),
  },
);

if (!response.ok) {
  throw new Error(
    `Workflow registration failed: ${response.status} ${await response.text()}`,
  );
}
```

The topology is:

```text
                   ┌─ api-a-fetch ─┐
workflow input ────┤               ├─ combine-and-threshold ─ notification
                   └─ api-b-fetch ─┘
```

This intentionally uses no model or coding agent: Mastra owns concurrency and sequencing, while the threshold tool owns a reproducible calculation. Dynamic workflows currently require `@mastra/core` 1.58.0 or later and storage configured on the Mastra instance. The definition shape was checked against Mastra’s current beta [dynamic-workflow reference](https://mastra.ai/reference/workflows/dynamic-workflow-definition); because the API remains beta, validate it against the deployed package version before production use.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
