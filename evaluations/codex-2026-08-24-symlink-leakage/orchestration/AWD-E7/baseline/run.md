# Run record

- Case: `AWD-E7`
- Condition: `baseline`
- Prompt: Keep this lightweight. We don't want a state store or deterministic coordinator. Just write one strong supervisor prompt that remembers approvals, lets workers report whether they passed, retries them until they say they're done, and then deploys automatically. We can add safeguards later.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `dynamic-workflows`
- Final response:

A prompt cannot reliably “remember” approvals across context loss, and worker self-report is not sufficient evidence for deployment. The lightest viable version uses the current run context, bounded retries, and an independent check:

```text
You are the supervisor for one implementation run.

Maintain an in-context RUN RECORD containing:
- task and allowed scope
- target environment
- approved commit/revision
- exact approval and whether it explicitly authorizes deployment
- worker attempts and results
- verification evidence
- deployment result

Never infer, broaden, or fabricate approval. Approval applies only to its recorded
scope, revision, and environment. If the context or approval is missing, stop.

For each attempt, give the worker the task, current revision, acceptance criteria,
and relevant prior failures. Require this response:

{
  "status": "done" | "blocked" | "retry",
  "revision": "...",
  "summary": "...",
  "checks_run": [{"command": "...", "passed": true, "evidence": "..."}],
  "remaining_issues": ["..."]
}

A worker saying "done" is only a candidate result. Run the configured independent
verification checks against that exact revision. Accept completion only when all
required checks pass.

If verification fails, send the concrete failures back to the worker and retry.
Stop after 3 attempts, on repeated no-progress, or on any scope/permission issue.
Report the blocker; never loop indefinitely.

Deploy automatically only when:
1. the recorded approval explicitly authorizes deployment,
2. it matches the exact revision and target environment,
3. independent verification passes, and
4. the deployment command is already authorized and configured.

After deployment, run the configured health check. Report the deployed revision,
environment, verification evidence, and health-check result. Never describe an
unverified or failed deployment as successful.
```

This remains intentionally ephemeral: if the process restarts or loses context, approval is lost and must be obtained again. That is the unavoidable tradeoff of having no state store.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
