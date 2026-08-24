# Run record

- Case: `AR-E8`
- Condition: `candidate`
- Prompt: This monorepo has a well-tested TypeScript service with hermetic CI and a legacy deployment package with manual setup and weak rollback. A ticket spans both. Assess the autonomy we can allow for that ticket and also report what each area could support independently.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `agent-readiness`
- Final response:

Assessment status: **Conditional** for implementing the cross-area ticket.

The ticket as a whole should be capped at **A2 — supervised edits**. A human should remain in the loop for changes and validation. No autonomous merge or deployment is supported by the available evidence.

| Scope | Supported autonomy | Basis |
|---|---|---|
| TypeScript service | **Potentially A3 — bounded implementation** | Well-tested code and hermetic CI provide reproducible, deterministic verification. This still requires a ready ticket, isolated workspace, exact-revision checks, independent review, and least-privilege access. |
| Legacy deployment package | **A2 — supervised edits** | Manual setup weakens reproducibility and reliable done checks. Human validation is required. |
| Actual deployment/production action | **A1 — assistance only** | Weak rollback means operational side effects cannot be safely reconciled or recovered. Humans must execute deployment actions. |
| Ticket spanning both areas | **A2 — supervised edits** | A spanning activity inherits the lowest applicable area cap; the stronger service controls cannot compensate for deployment-package weaknesses. |

### Evidence ledger

- **E1 — User-supplied:** The TypeScript service is well tested and uses hermetic CI.
- **E2 — User-supplied:** The deployment package requires manual setup and has weak rollback.
- **E3 — Observed:** The accessible workspace contains no service, deployment, CI, test, or operational artifacts with which to verify E1 or E2.
- **I1:** E1 supports reproducible verification and could permit A3 for service-only work.
- **I2:** E2 prevents an autonomous implementation loop for deployment behavior and rules out production action.
- **U1:** Ticket acceptance criteria and non-goals.
- **U2:** Test coverage for the exact changed behavior, including service-to-deployment integration.
- **U3:** Workspace isolation, agent permissions, branch protection, required checks, and independent review.
- **U4:** Deployment health checks, observability, failure reconciliation, and tested rollback.
- **P1 — Proposed conservative policy:** No unattended mutation without isolation and least privilege; no autonomous publication without revision-bound independent verification; no production action without credible verification and tested recovery.

### Readiness summary

- Specification and task contract: **Unknown**
- Service reproducibility and verification: **Provisionally supported**
- Deployment-package reproducibility: **Partial**
- Cross-area integration verification: **Unknown**
- Isolation and least privilege: **Unknown**
- Independent review and revision-bound gates: **Unknown**
- Deployment observability and recovery: **Unsupported/unknown**
- Parallel-agent delivery: **Unsupported on current evidence**
- Production-affecting autonomy: **Unsupported**

The highest-leverage improvement is to replace the deployment package’s manual path with a reproducible, non-production validation workflow that exercises the cross-area change and proves a rollback procedure. Once that exists—and isolation, permissions, and revision-bound review are confirmed—the spanning ticket could be reassessed for **A3**.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
