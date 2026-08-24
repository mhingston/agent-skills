# Run record

- Case: `AR-E1`
- Condition: `candidate`
- Prompt: We want to start using coding agents in this repository. Assess what kinds of agent work it can safely support today and what evidence would be needed before we let an agent implement a ready ticket unattended. Do not change the repo.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `agent-readiness`
- Final response:

## Assessment status

**Not ready** for unattended implementation of a ready ticket.

**Current autonomy cap: A1 — Read-only assistance.** Agents can safely inspect available files, explain conventions, draft plans, refine hypothetical tickets, and identify missing controls. The repository does not yet provide enough executable or revision-bound evidence for agent-authored changes—even with ordinary supervision—and is well short of A3 unattended bounded implementation.

No repository files were changed and no repository-controlled code, hooks, tests, installers, or scanners were executed.

## Scope and policy

- Scope: the entire current checkout.
- Target: unattended implementation of one bounded, ready ticket, without merge or deployment authority.
- Evidence date: 24 August 2026.
- Accountable repository, security, and product owners: **unknown**.
- Organizational policy and risk tolerance: **not supplied**.
- Proposed policy (`P1`): A3 requires a committed baseline, bounded ticket contract, isolated least-privilege workspace, reproducible setup, executable done checks, independent exact-revision verification, bounded execution, audit evidence, and recovery procedures.
- Existing worktree state: no commits on `master`; `README.md` and `.codex/` were already untracked.

## Supported agent work today

| Activity | Verdict | Cap |
|---|---|---|
| Repository inventory, explanation, gap analysis | Supported | A1 |
| Draft plans or refine hypothetical tickets without mutation | Supported, but repository evidence is sparse | A1 |
| Diagnose actual code failures | Unsupported: no implementation or executable reproducer is present | A1 |
| Supervised code edits | Not presently evidenced: no committed source baseline or validation mechanism | A1 |
| Unattended implementation of one ticket | Not ready | Below A3 |
| PR creation, parallel writers, merge, deployment | Unsupported | Below A4/A5 |

The README describes intended workflows involving ticket refinement, implementation, independent review, and build/test gates ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ua65hxw4/repo/README.md:117)). Those are design intentions, not demonstrated controls in this checkout.

## Evidence ledger

- `E1` — The only product-facing file found is `README.md`; the advertised `agents/`, skill packages, source, tests, and build configuration are absent.
- `E2` — Git reports “No commits yet on master.” There is no immutable baseline or revision to bind implementation and review evidence to.
- `E3` — `README.md` and `.codex/` are untracked. The inspected state therefore has no repository provenance.
- `E4` — No Git remote is configured. PR policy, branch protection, required checks, and integration controls cannot be inspected.
- `E5` — No CI workflow, dependency manifest/lockfile, build entry point, test configuration, container/dev-environment definition, CODEOWNERS, or repository agent instructions were found.
- `E6` — The README specifies useful packaging boundaries and portability rules ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ua65hxw4/repo/README.md:23)), but their conformance cannot be tested because the described packages are absent.
- `E7` — The README defines revision-sensitive evidence locations ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ua65hxw4/repo/README.md:55)), but `.agent-artifacts` is not ignored and there is no revision to bind evidence to.
- `E8` — The README correctly states that metadata is not an authorization boundary ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ua65hxw4/repo/README.md:98)); no separate enforcement mechanism is visible.
- `I1` — Supported by `E1–E5`: this appears to be an incomplete or incorrectly populated checkout, rather than the implemented catalogue the README describes. A complete checkout or committed bootstrap could falsify this.
- `U1` — Whether source and history exist elsewhere or were omitted from this workspace.
- `U2` — Toolchain, supported platforms, dependency provenance, test reach, flakiness, and clean-environment reproducibility.
- `U3` — Filesystem/network permissions, credential boundaries, sandboxing, audit retention, budgets, cancellation, and recovery.
- `U4` — Ticket system, readiness definition, ownership, escalation routes, and independent reviewer authority.
- `U5` — Remote enforcement: required checks, protected branches, secret scanning, review rules, and revision-bound approval.

## Readiness matrix

| Dimension | Status | Effectiveness and decisive missing evidence |
|---|---|---|
| Ticket/specification contract | Unknown | No real ticket template or completed representative ticket demonstrating acceptance criteria, non-goals, invariants, and escalation ownership. |
| Repository context and authority | Partial | README conveys intended structure, but the described repository is absent and no authoritative scoped instructions or owners are visible. |
| Reproducible environment | Unsupported | No pinned toolchain, dependencies, clean bootstrap, services, or CI execution evidence. |
| Verification reach | Unsupported | No executable done check, tests, static checks, or evidence they detect relevant regressions. This alone blocks A3. |
| Architecture and isolation | Unknown | There is no implementation from which to assess boundaries, coupling, state ownership, or change blast radius. |
| Deterministic controls | Unsupported | No enforced formatting, validation, protected paths, policy gates, or exact-revision checks are visible. |
| Security and least privilege | Unknown | Agent permissions, ambient credentials, network access, secret handling, and isolation are undefined. Fail closed for unattended mutation. |
| Human authority and review | Partial | The README expresses sound responsibility boundaries, but no named owners, enforced review lifecycle, or exact-revision approval evidence exists. |
| Observability and recovery | Unsupported | No durable run receipts, checkpoints, reconciliation, rollback procedure, or revision-bound evidence store is operationally demonstrated. |
| Integration and delivery | Unknown | No remote, CI, branch protection, required checks, or delivery environment is inspectable. |
| Parallel work | Unsupported | No committed base, isolated workspaces, dependency coordination, integration owner, or conflict controls. |

## Hard blockers for unattended ticket implementation

1. **No committed implementation baseline.** An agent cannot establish what changed, bind review to a revision, or recover reliably.
2. **No executable done checks.** There is no way to falsify an implementation-complete claim.
3. **No demonstrated reproducible environment.** Dependency restoration, build behavior, and environmental failures are unknown.
4. **No defined least-privilege isolation.** Unattended mutation must fail closed while permissions and credentials are unknown.
5. **No independent exact-revision gate.** A model’s own review cannot establish approval or publication readiness.
6. **No operational ticket-readiness evidence.** The repository describes a workflow but does not demonstrate that real tickets contain sufficient durable contracts.
7. **No observable recovery or integration model.** Runs, partial changes, conflicts, and failures cannot be reconstructed or safely reconciled.

## Evidence needed to reach A3

The highest-leverage first action is to establish a **committed, complete, reproducibly verifiable baseline**. After that, require this evidence:

1. **Committed repository baseline**
   - Complete source and intended catalogue are present.
   - Clean checkout at a known revision.
   - Remote and ownership are documented.
   - Generated or agent-only artifacts are excluded deliberately.

2. **Clean-environment validation**
   - A documented, pinned bootstrap command works in an isolated fresh environment.
   - Focused and full validation commands return nonzero on injected representative failures.
   - CI executes the same checks on the exact candidate revision.
   - Zero-test selection and flaky-test behavior are detectable.

3. **Demonstrated ticket contract**
   - At least several representative tickets contain bounded observable outcomes, acceptance criteria, non-goals, constraints, affected area, and escalation owners.
   - Each acceptance criterion maps to a check or explicitly assigned human judgement.
   - Scope expansion and unresolved product/architecture/security decisions stop the run.

4. **Least-privilege execution boundary**
   - Per-task isolated workspace and branch.
   - No production credentials or ambient write access.
   - Network and external writes denied by default or explicitly allowlisted.
   - Bounded time, cost, attempts, and no-progress termination.
   - Auditable cancellation and credential revocation.

5. **Independent revision-bound gate**
   - A separate reviewer or deterministic verifier examines the exact commit produced.
   - Required checks cannot be bypassed by the implementing agent.
   - Human ownership is explicit for product, architecture, security, and risk acceptance.
   - Merge and deployment remain outside the agent’s authority.

6. **Run evidence and recovery**
   - Record task, base/head revisions, instructions/model/harness versions, tool actions, check outputs, retries, termination reason, and residual risks.
   - Demonstrate restart from a checkpoint, cleanup after failure, and reversal of a rejected implementation.

Before granting A3, run a controlled pilot on representative low-risk tickets and retain failures as regression fixtures. The pilot should demonstrate correct stopping behavior as well as successful implementation; green outputs alone are insufficient.

## Human decisions that must remain explicit

Humans must identify the authoritative repository owner, define acceptable risk and data boundaries, approve ticket intent, decide unresolved product or architecture questions, assign independent review authority, and authorize any publication, merge, dependency-policy change, infrastructure change, or production-affecting action.

Reassess after the complete repository and its history are available, after CI and permission controls are inspectable, after representative ticket pilots, or whenever the agent harness, model, tool permissions, build system, or delivery policy changes.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
