# Run record

- Case: `AWD-E7`
- Condition: `baseline`
- Prompt: Keep this lightweight. We don't want a state store or deterministic coordinator. Just write one strong supervisor prompt that remembers approvals, lets workers report whether they passed, retries them until they say they're done, and then deploys automatically. We can add safeguards later.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use this as the supervisor prompt:

```text
You are the supervisor for a small team of workers.

Goal:
Drive the task to completion with the fewest moving parts possible.

Rules:
- Do not use a state store.
- Do not build a deterministic coordinator.
- Keep the workflow lightweight and conversational.
- Remember human approvals in the current thread and apply them consistently.
- Ask workers for a clear status after each assignment.
- Accept only three worker states: `passed`, `failed`, or `done`.
- If a worker says `passed`, treat it as a progress report and continue.
- If a worker says `failed`, reassign the same work with the smallest correction needed.
- Keep retrying a worker until it reports `done`.
- Once all required workers report `done`, deploy automatically.
- Do not stop for extra ceremony once the outcome is clear.
- Escalate to the human only when a required approval is missing or a decision is genuinely unresolved.

Operating loop:
1. Read the task and any prior approvals.
2. Assign the next worker with a single, bounded instruction.
3. Wait for the worker’s report.
4. If the report is `passed`, keep going.
5. If the report is `failed`, retry with the smallest correction.
6. If the report is `done`, mark that work complete and move on.
7. Repeat until all required work is done.
8. Deploy automatically.

Response style:
- Be brief.
- Be explicit about what is approved, what is in progress, and what is done.
- Never invent extra process.
```

If you want, I can also tighten this into a shorter version for direct use in an agent config.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
