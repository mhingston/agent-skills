# Run record

- Case: `PC-E2`
- Condition: `candidate`
- Prompt: Plan how to add an idempotency key to this existing POST endpoint. The repo has a clear architecture doc, ADRs, tests, and a ready ticket.
- Expected routing: `plan`
- Loaded skills observed in Codex events: `plan`
- Agent-reported selection (not a native harness event): `planning`
- Final response:

Plan status: **Blocked** — the mounted workspace is not the described application repository.

Evidence:

- The only project file is [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ppn_o64_/repo/README.md), which describes an Agent Skills catalogue.
- Git reports an unborn `master` branch with no commits.
- There are no remotes, alternate worktrees, architecture documents, ADRs, tickets, endpoint code, manifests, or tests.
- `.codex/skills` is empty in the workspace.

Without those sources, I cannot identify the endpoint contract, persistence boundary, concurrency semantics, accepted idempotency behavior, or exact verification commands without inventing them.

Please mount or point me to the intended repository—or provide the architecture document, relevant ADRs, ready ticket, endpoint code, and tests. I can then produce an evidence-linked plan covering:

- key validation and request-fingerprint semantics;
- atomic claim/store/replay behavior under concurrent requests;
- response and error replay policy;
- storage lifecycle and expiry;
- compatibility, observability, rollout, and rollback;
- exact implementation slices and test commands.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
