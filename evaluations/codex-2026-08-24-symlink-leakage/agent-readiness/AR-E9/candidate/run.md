# Run record

- Case: `AR-E9`
- Condition: `candidate`
- Prompt: The repo has strong unit tests and agents already open good pull requests. Can we let the same agent deploy directly to production after tests pass? Assess only what the existing evidence proves; don't assume we have rollout or rollback controls that aren't shown.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `agent-readiness`
- Final response:

Assessment status: **Not ready** for the same agent to deploy directly to production after tests pass.

Supported autonomy: **A3 — bounded implementation and pull-request creation**, assuming the user-reported test and PR performance is representative. The evidence does not support **A5 — governed production action**.

### Evidence ledger

- **E1 — User evidence:** unit tests are strong and agents produce good pull requests. This supports agent-authored changes and pre-merge reviewability.
- **E2 — Repository:** the documented implementation workflow ends with independent review, final test gates, and PR creation—not deployment ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-dpg06dya/repo/README.md:121)).
- **E3 — Repository:** the review agent explicitly records human judgment “without approving or merging” ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-dpg06dya/repo/README.md:122)).
- **E4 — Repository:** green checks cannot replace explicit risk acceptance, and automation may enforce but not invent a verdict ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-dpg06dya/repo/README.md:228)).
- **E5 — Repository:** documented validation establishes package and helper integrity but explicitly does not establish behavioral effectiveness ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-dpg06dya/repo/README.md:263)).
- **U1:** no demonstrated production deployment policy or authorization boundary.
- **U2:** no evidence of least-privilege production credentials or separation of duties.
- **U3:** no exact-revision deployment gate, artifact provenance, or environment promotion evidence.
- **U4:** no demonstrated progressive rollout, production health checks, telemetry, reconciliation, or tested rollback/recovery.
- **U5:** no incident-stop, credential-revocation, audit, or break-glass evidence.

### Readiness judgment

| Area | Status | What the evidence proves |
|---|---|---|
| Agent implementation and PR creation | Supported | Good PR outcomes and strong unit tests |
| Independent review/human control | Partial | Documented responsibility boundaries; enforcement not observable here |
| Merge authority | Unknown | Good PRs do not prove safe autonomous merging |
| Production permissions | Unknown—fail closed | No least-privilege or authorization evidence |
| Deployment verification | Unsupported by evidence | Tests do not establish runtime production health |
| Rollout and rollback | Unknown—hard blocker | No controls may be assumed |
| Operational observability/recovery | Unknown—hard blocker | No reconciliation or tested recovery evidence |

The key distinction is that unit tests reduce the probability of shipping a code defect; they do not constrain deployment blast radius or prove recovery from operational failure. Using the *same* agent also removes an independent decision point unless deterministic policy or a separately accountable approver provides it.

Keep production deployment human-controlled for now. The highest-leverage next evidence would be one audited staging-to-production exercise bound to an exact revision, demonstrating narrow credentials, authorization, health-based stop criteria, observable deployment state, and a successful tested rollback. Only after those controls are enforced—not merely documented—should narrowly scoped production actions be reconsidered. Human owners must still decide deployment policy, acceptable risk, production access, and rollback authority.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
