# Run record

- Case: `AR-E8`
- Condition: `baseline`
- Prompt: This monorepo has a well-tested TypeScript service with hermetic CI and a legacy deployment package with manual setup and weak rollback. A ticket spans both. Assess the autonomy we can allow for that ticket and also report what each area could support independently.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `plan`
- Final response:

Plan status: **Conditional**. The ticket’s end-to-end autonomy is capped by the legacy deployment package—the weakest consequential boundary. The agent can work with different autonomy levels within the ticket, but should not autonomously deliver or deploy the ticket as a whole.

| Scope | Safe autonomy | Rationale |
|---|---|---|
| TypeScript service independently | **High implementation autonomy** through code change, tests, hermetic CI, and PR preparation | Deterministic, reproducible verification supports autonomous iteration and falsifiable completion evidence |
| Legacy deployment package independently | **Low autonomy / supervised execution** | Manual setup, environment dependence, and weak rollback make verification and recovery unreliable |
| Ticket spanning both | **Mixed execution, human-gated release** | Success requires coordinated compatibility and deployment; strong service checks cannot prove the legacy package or recovery path |

Recommended operating boundary:

- Let the agent autonomously implement and verify the TypeScript slice, provided the ticket has clear acceptance criteria.
- Let it inspect, document, and prepare deployment-package changes, scripts, validation steps, and rollback improvements.
- Require a human to approve the deployment design, supervise environment-dependent validation, and authorize rollout.
- Do not allow autonomous production deployment until setup is reproducible, preflight and post-deploy checks are deterministic, and rollback is tested.
- Integrate the slices through an explicit contract check: artifact/configuration format, version compatibility, deployment order, failure behavior, and health signals.
- Keep the TypeScript change independently mergeable only if doing so leaves a coherent, backward-compatible state. Otherwise gate the combined merge.

The legacy area could earn greater autonomy by adding:

- scripted, idempotent setup;
- disposable-environment or dry-run validation;
- artifact/configuration contract tests;
- deterministic health checks;
- versioned releases and automated promotion;
- a tested rollback or forward-recovery procedure;
- retained deployment receipts and clear abort conditions.

Evidence limitation: the accessible workspace currently contains only an uncommitted [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-erpq5088/repo/README.md) and no committed service, CI, or deployment files. Therefore the technical characteristics above are supplied by your prompt, not independently verified from repository artifacts. Reassess against the actual CI configuration, deployment scripts, runbooks, and recovery evidence before granting execution authority.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
