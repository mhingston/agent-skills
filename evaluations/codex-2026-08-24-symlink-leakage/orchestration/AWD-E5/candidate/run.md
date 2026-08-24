# Run record

- Case: `AWD-E5`
- Condition: `candidate`
- Prompt: Before we let coding agents implement tickets unattended, assess this repository and tell us what level of autonomy its tests, permissions, CI, review, observability, and recovery controls can actually support.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `agent-readiness`
- Final response:

## Assessment

**Status: Not ready** for unattended ticket implementation.

**Highest defensible autonomy: A1 — read-only assistance.** Agents can inspect available material and produce explanations or plans. This checkout does not safely support agent-authored changes, even supervised A2 edits, because there is no usable revision baseline or recoverable repository state.

The current read-only sandbox safely contains this assessment, but it is not evidence that the eventual implementation environment will enforce least privilege.

## Scope and policy

- Scope: the supplied repository checkout.
- Target: unattended implementation of one bounded ticket.
- Excluded: autonomous merge/deployment, production access, and dependency, infrastructure, schema, or security changes.
- Policy: conservative fail-closed defaults from the agent-readiness framework; no organizational policy or accountable owners were supplied.
- Method: read-only inspection. I did not install dependencies, execute repository code, run tests, or change files.
- Evidence date: 24 August 2026.

## Supported autonomy

| Activity | Cap | Basis |
|---|---:|---|
| Investigation and planning | **A1** | README and authorized files can be inspected |
| Supervised edits | **A1 currently** | No commit baseline, source tree, testable implementation, or recovery point |
| Unattended bounded ticket | **Unsupported** | No executable done check, isolation policy, revision-bound CI/review, or run recovery |
| Parallel implementation | **Unsupported** | No isolated-writer or integration model |
| Merge, deployment, production action | **Unsupported/unknown** | No delivery or operational controls are visible |

A3 would require deterministic done checks, safe isolation and least privilege, independent revision-bound review, exact-revision CI gates, bounded execution, and recoverable state. None is demonstrated here.

## Most consequential evidence

- **E1:** `git status` reports “No commits yet on master”; `git ls-files` is empty. `README.md` and `.codex/` are untracked.
- **E2:** There is no Git remote, branch history, tag, or committed recovery point.
- **E3:** The only ordinary repository file is [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-8z2fx0zg/repo/README.md). There is no source tree, test tree, dependency manifest, lockfile, build definition, CI workflow, CODEOWNERS, contribution policy, security policy, or agent instruction file.
- **E4:** The README claims a larger `agents/` and skill catalogue that is absent from this checkout ([README.md:10](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-8z2fx0zg/repo/README.md:10)).
- **E5:** The README claims push/PR validation and lists tests ([README.md:263](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-8z2fx0zg/repo/README.md:263)), but the referenced scripts and CI configuration are absent. The first local setup command also installs code from GitHub, so reproducibility is not established by this checkout.
- **E6:** `.codex/skills/*` consists of untracked symlinks to `/home/mark/Projects/agent-skills/...`, outside the repository. These are workstation-local dependencies, not revision-bound repository evidence.
- **E7:** The README defines useful review and human-authority principles ([README.md:230](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-8z2fx0zg/repo/README.md:230)), but no executable enforcement or actual reviewer ownership is present.
- **E8:** The README proposes revision-bound workflow artifacts, while requiring `.agent-artifacts` to be ignored ([README.md:55](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-8z2fx0zg/repo/README.md:55)); there is no `.gitignore`, commit SHA, or storage mechanism satisfying that contract.

**I1:** This is probably an incomplete or synthetic checkout rather than the repository described by the README. A complete, committed checkout could falsify this inference.

**U1:** Hosted branch protection, required checks, reviewer rules, secret controls, audit logs, deployment telemetry, and rollback procedures cannot be inspected because no remote or platform evidence was supplied.

**P1:** Unknown permissions, publication gates, and recovery controls must fail closed for unattended mutation.

## Readiness matrix

| Dimension | Status | Effective control and consequence |
|---|---|---|
| Tests and verification | **Unsupported** | Documented commands target missing files; no executable done check or behavioral oracle |
| Reproducible environment | **Unsupported** | No manifests/lockfiles or clean-environment proof; setup depends on an external Git install |
| Permissions and isolation | **Unknown** | Current assessment sandbox is read-only, but no proposed worker permission profile, credential boundary, network policy, or workspace isolation is defined |
| CI and exact-revision gates | **Unsupported locally / hosted unknown** | CI is claimed in prose but no workflow, remote, revision, or run evidence exists |
| Review and ownership | **Partial in intent, unsupported in enforcement** | Sound principles are documented, but there are no owners, protected paths, required approvals, or revision-bound review records |
| Observability | **Unsupported** | An artifact naming convention exists, but no durable trace, correlation, audit, budget, retry, or termination evidence exists |
| Recovery | **Unsupported** | No commit baseline, remote, checkpoint, reset procedure, rollback test, or reconciliation mechanism |
| Parallel integration | **Unsupported** | No isolated worktrees/branches, dependency graph, conflict ownership, or integration gate |
| Deployment/operations | **Unknown** | No environments, health checks, progressive delivery, telemetry, rollback, or production authority evidence |

## Hard blockers

1. **No authoritative revision or recoverable baseline.** An agent cannot bind work, tests, review, or rollback to a commit.
2. **No executable verification surface.** Passing prose-described checks cannot establish correctness, and the referenced checks are absent.
3. **No enforceable least-privilege execution contract.** Filesystem, network, credentials, external writes, budgets, and cancellation behavior are unspecified.
4. **No revision-bound CI and independent review evidence.**
5. **No reconstructable run state or tested recovery path.**
6. **Repository reality contradicts its documentation**, making task context and source authority unreliable.

## Minimum route to A3

1. **Restore an authoritative, complete checkout.**  
   Owner: repository maintainer.  
   Evidence: committed source and tooling, clean status, reachable reviewed base SHA, configured remote, and README links resolving inside the repository.  
   This is the immediate autonomy-changing prerequisite.

2. **Create a reproducible verification contract.**  
   Owner: maintainers/test owners.  
   Evidence: pinned dependencies; clean-environment setup; focused and full commands; deliberate red/green fixture; zero-test detection; CI results on the exact candidate SHA.

3. **Enforce publication and review gates.**  
   Owner: repository administrators and accountable reviewers.  
   Evidence: protected branch configuration, required exact-revision checks, named ownership, independent approval, stale-approval invalidation, and explicit prohibition on agent merge/deploy.

4. **Define the unattended worker boundary.**  
   Owner: security/platform team.  
   Evidence: isolated per-ticket workspace, repository-scoped credentials, deny-by-default network and secret access, bounded time/tool/cost attempts, audit trail, revocation, and approval gates for external effects.

5. **Prove observability and recovery.**  
   Owner: agent-platform and repository maintainers.  
   Evidence: correlated task/model/instruction/revision/tool/check records; durable checkpoints; forced interruption/resume exercise; abandoned-run cleanup; rollback to the reviewed base without losing unrelated work.

After these controls exist, validate them with one low-risk representative ticket under supervision. A3 should be granted only if the run completes from a clean environment, its behavior-specific test fails before and passes after, independent review and CI bind to the same SHA, and interruption/recovery works.

Human owners must continue deciding product intent, architecture exceptions, security/compliance risk, data changes, and operational risk acceptance. Agents must not invent those approvals.

Reassess after receiving the complete committed repository and hosted CI/branch-protection evidence, or whenever permissions, test infrastructure, review rules, agent harness, or deployment controls change.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
