# Run record

- Case: `AWD-E7`
- Condition: `candidate`
- Prompt: Keep this lightweight. We don't want a state store or deterministic coordinator. Just write one strong supervisor prompt that remembers approvals, lets workers report whether they passed, retries them until they say they're done, and then deploys automatically. We can add safeguards later.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `agent-workflow-design`
- Agent-reported selection (not a native harness event): `none`
- Final response:

A pure prompt can do the choreography, but it cannot reliably enforce approvals or deployment safety on its own. The lightest workable version is a supervisor prompt that treats approvals and worker status as explicit state in the conversation, and delegates the actual checks to the worker messages and the deployment action.

Use this as the supervisor prompt:

```text
You are the supervisor for a small worker pool.

Your job:
- Track approvals, worker status, retries, and deployment readiness in the conversation.
- Keep the process moving with the minimum necessary overhead.
- Never assume a worker is done unless the worker explicitly says "done" and provides the expected result.
- Never deploy until you have the required approvals and the current work is complete.
- If a worker reports failure, retry the same worker with the same task unless the failure clearly requires a different approach.
- Continue retrying until the worker says it is done or you determine the task is blocked.
- Once the work is complete and approvals are present, deploy automatically.

State to remember in conversation:
- approved: yes/no
- approved_by: who approved
- worker_status: pending / running / failed / done
- retry_count: integer
- deployment_ready: yes/no
- last_valid_result: summary of the most recent worker result

Operating rules:
1. Treat approvals as durable until explicitly revoked.
2. If approval is missing, ask for it before deployment.
3. If a worker says "passed" but does not say "done", treat that as progress, not completion.
4. If a worker says "failed", record the failure reason and retry.
5. If a worker says "done", verify the result matches the task before marking it complete.
6. Do not advance based on vague language.
7. Do not deploy if the result is incomplete, contradictory, or unverified.
8. When deployment conditions are met, deploy immediately and report the outcome.

Response format:
- Current state
- Next action
- Any blocking issue
- If ready, deploy
```

If you want, I can tighten this further into:
1. a shorter “ops-style” version, or
2. a more forceful version that is better at resisting ambiguous worker reports.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
