# Run record

- Case: `DW-E5`
- Condition: `baseline`
- Prompt: Build a Mastra dynamic workflow that fetches data from two registered APIs in parallel, combines the results, applies a deterministic threshold, and sends a notification. There is no repository or coding-agent work involved.
- Expected routing: `dynamic-workflows`
- Loaded skills observed in Codex events: `agent-workflow-design, programmatic-tool-calling`
- Final response:

Below is a standalone Mastra workflow. It executes two registered API tools concurrently, joins their outputs, computes a deterministic score, compares it with a caller-supplied threshold, and sends a notification only when the threshold is met.

```ts
import { Mastra } from "@mastra/core/mastra";
import { createTool } from "@mastra/core/tools";
import {
  createStep,
  createWorkflow,
} from "@mastra/core/workflows";
import { z } from "zod";

/*
 * Registered API tools
 * Replace each execute implementation with the real API integration.
 */

const apiA = createTool({
  id: "api-a",
  description: "Fetches a numeric measurement from API A",
  inputSchema: z.object({
    entityId: z.string(),
  }),
  outputSchema: z.object({
    value: z.number(),
    observedAt: z.string(),
  }),
  execute: async ({ context }) => {
    const response = await fetch(
      `https://api-a.example.com/entities/${context.entityId}`,
    );

    if (!response.ok) {
      throw new Error(`API A returned HTTP ${response.status}`);
    }

    const body = await response.json();

    return {
      value: z.number().parse(body.value),
      observedAt: z.string().parse(body.observedAt),
    };
  },
});

const apiB = createTool({
  id: "api-b",
  description: "Fetches a numeric measurement from API B",
  inputSchema: z.object({
    entityId: z.string(),
  }),
  outputSchema: z.object({
    value: z.number(),
    observedAt: z.string(),
  }),
  execute: async ({ context }) => {
    const response = await fetch(
      `https://api-b.example.com/entities/${context.entityId}`,
    );

    if (!response.ok) {
      throw new Error(`API B returned HTTP ${response.status}`);
    }

    const body = await response.json();

    return {
      value: z.number().parse(body.value),
      observedAt: z.string().parse(body.observedAt),
    };
  },
});

const sendNotification = createTool({
  id: "send-notification",
  description: "Sends a threshold notification",
  inputSchema: z.object({
    destination: z.string(),
    deduplicationKey: z.string(),
    message: z.string(),
  }),
  outputSchema: z.object({
    notificationId: z.string(),
  }),
  execute: async ({ context }) => {
    const response = await fetch("https://notifications.example.com/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "idempotency-key": context.deduplicationKey,
      },
      body: JSON.stringify({
        destination: context.destination,
        message: context.message,
      }),
    });

    if (!response.ok) {
      throw new Error(`Notification API returned HTTP ${response.status}`);
    }

    const body = await response.json();

    return {
      notificationId: z.string().parse(body.id),
    };
  },
});

const workflowInputSchema = z.object({
  entityId: z.string().min(1),
  threshold: z.number().finite(),
  destination: z.string().min(1),
  runKey: z.string().min(1),
});

const measurementSchema = z.object({
  value: z.number(),
  observedAt: z.string(),
});

const fetchFromApiA = createStep({
  id: "fetch-from-api-a",
  inputSchema: workflowInputSchema,
  outputSchema: measurementSchema,
  execute: async ({ inputData }) =>
    apiA.execute({
      context: { entityId: inputData.entityId },
    }),
});

const fetchFromApiB = createStep({
  id: "fetch-from-api-b",
  inputSchema: workflowInputSchema,
  outputSchema: measurementSchema,
  execute: async ({ inputData }) =>
    apiB.execute({
      context: { entityId: inputData.entityId },
    }),
});

/*
 * A parallel operation produces:
 *
 * {
 *   "fetch-from-api-a": { value, observedAt },
 *   "fetch-from-api-b": { value, observedAt }
 * }
 */

const parallelResultSchema = z.object({
  "fetch-from-api-a": measurementSchema,
  "fetch-from-api-b": measurementSchema,
});

const decisionSchema = z.object({
  entityId: z.string(),
  destination: z.string(),
  runKey: z.string(),
  apiAValue: z.number(),
  apiBValue: z.number(),
  combinedValue: z.number(),
  threshold: z.number(),
  thresholdMet: z.boolean(),
});

const combineAndApplyThreshold = createStep({
  id: "combine-and-apply-threshold",
  inputSchema: parallelResultSchema,
  outputSchema: decisionSchema,
  execute: async ({ inputData, getInitData }) => {
    const initial = workflowInputSchema.parse(
      await getInitData<z.infer<typeof workflowInputSchema>>(),
    );

    const apiAValue = inputData["fetch-from-api-a"].value;
    const apiBValue = inputData["fetch-from-api-b"].value;

    // This rule is ordinary code—not an LLM decision.
    const combinedValue = apiAValue + apiBValue;
    const thresholdMet = combinedValue >= initial.threshold;

    return {
      entityId: initial.entityId,
      destination: initial.destination,
      runKey: initial.runKey,
      apiAValue,
      apiBValue,
      combinedValue,
      threshold: initial.threshold,
      thresholdMet,
    };
  },
});

const workflowOutputSchema = decisionSchema.extend({
  notified: z.boolean(),
  notificationId: z.string().optional(),
});

const notify = createStep({
  id: "notify",
  inputSchema: decisionSchema,
  outputSchema: workflowOutputSchema,
  execute: async ({ inputData }) => {
    const result = await sendNotification.execute({
      context: {
        destination: inputData.destination,
        deduplicationKey:
          `${inputData.runKey}:${inputData.entityId}:${inputData.threshold}`,
        message:
          `Threshold reached for ${inputData.entityId}: ` +
          `${inputData.apiAValue} + ${inputData.apiBValue} = ` +
          `${inputData.combinedValue}, threshold ${inputData.threshold}.`,
      },
    });

    return {
      ...inputData,
      notified: true,
      notificationId: result.notificationId,
    };
  },
});

const skipNotification = createStep({
  id: "skip-notification",
  inputSchema: decisionSchema,
  outputSchema: workflowOutputSchema,
  execute: async ({ inputData }) => ({
    ...inputData,
    notified: false,
  }),
});

export const thresholdWorkflow = createWorkflow({
  id: "dynamic-threshold-workflow",
  inputSchema: workflowInputSchema,
  outputSchema: workflowOutputSchema,
})
  .parallel([fetchFromApiA, fetchFromApiB])
  .then(combineAndApplyThreshold)
  .branch([
    [
      async ({ inputData }) => inputData.thresholdMet,
      notify,
    ],
    [
      async ({ inputData }) => !inputData.thresholdMet,
      skipNotification,
    ],
  ])
  .commit();

export const mastra = new Mastra({
  tools: {
    apiA,
    apiB,
    sendNotification,
  },
  workflows: {
    thresholdWorkflow,
  },
});
```

Run it dynamically with different entities, thresholds, and destinations:

```ts
const workflow = mastra.getWorkflow("thresholdWorkflow");
const run = await workflow.createRunAsync();

const result = await run.start({
  inputData: {
    entityId: "customer-42",
    threshold: 100,
    destination: "ops-alerts",
    runKey: crypto.randomUUID(),
  },
});

console.log(result);
```

The control flow is:

```text
API A ─┐
       ├─ join → sum → combinedValue >= threshold? → notify or skip
API B ─┘
```

The notification uses an idempotency key so retries do not normally produce duplicate messages. Any failed API read prevents the join and therefore prevents a decision based on incomplete data. Mastra’s current workflow API uses typed steps, `.parallel()`, `.branch()`, and `.commit()` for this pattern. [Mastra workflow documentation](https://mastra.ai/ai-workflows)

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
