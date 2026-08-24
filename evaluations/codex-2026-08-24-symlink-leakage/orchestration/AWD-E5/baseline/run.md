# Run record

- Case: `AWD-E5`
- Condition: `baseline`
- Prompt: Before we let coding agents implement tickets unattended, assess this repository and tell us what level of autonomy its tests, permissions, CI, review, observability, and recovery controls can actually support.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `agent-readiness`
- Final response:

## Assessment

**Status: Not ready for unattended ticket implementation.**

**Supported autonomy cap: A1 — read-only assistance.**

Agents can safely inspect this checkout and produce explanations, investigations, or plans. The evidence does not support unattended edits, pull-request creation, parallel implementation, merge, deployment, or production-affecting actions.

This is a baseline assessment of the current checkout as observed on 24 August 2026. No repository files were changed, dependencies installed, or repository-controlled code executed.

## Scope and policy

Target activity: implementing bounded tickets unattended.

Conservative proposed policy (`P1`):

- Isolated, least-privilege workspace.
- Explicit ticket contract and bounded execution budget.
- Reproducible setup and executable done checks.
- Independent review and required CI on the exact revision.
- Human-controlled merge and deployment.
- Reconstructable runs and tested recovery.

No organisational policy, accountable owners, hosting configuration, or production environment evidence was supplied.

## Why the cap is A1

The checkout is not an operational copy of the repository described by its README:

- Git reports **no commits on `master`**, no remote, and an entirely untracked working tree.
- The only ordinary repository file is [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-fwrw4efa/repo/README.md).
- `.codex/skills/*` are runtime-provided symlinks outside this checkout, not tracked repository content.
- The source directories, agents, skills, tests, and CI files referenced by the README are absent.
- There is no `.gitignore`, so the documented `.agent-artifacts` storage prerequisite is not satisfied.
- There is no exact base revision to which tests, review, or recovery could be bound.

This fails three hard rules for A3:

1. No executable done check means no autonomous implementation loop.
2. No demonstrated safe isolation and least privilege means no unattended mutation.
3. No independent revision-bound verification means no autonomous publication.

## Readiness matrix

| Control area | Status | Effective evidence and consequence |
|---|---|---|
| Tests | **Unsupported** | README names validation commands, but their scripts, fixtures, dependencies, and source packages are absent. Test reach, determinism, flakiness, runtime, and failure detection cannot be established. |
| Permissions | **Unknown / gate** | This assessment session is read-only, which safely supports A1 but cannot implement tickets. No repository policy establishes agent filesystem, network, secret, API, or production permissions for a future mutable runner. |
| CI | **Unsupported** | README claims push/PR validation, but no `.github`, GitLab, Jenkins, or other CI configuration exists in the checkout. No check can be shown to run or be required on an exact revision. |
| Review | **Partial in intent; unsupported in enforcement** | [README.md:121](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-fwrw4efa/repo/README.md:121) describes independent review and human judgement, and its responsibility boundaries are sound. The referenced agent definitions, `CODEOWNERS`, reviewer ownership, branch protection, and revision-bound approval enforcement are absent. |
| Observability | **Partial in design; unsupported operationally** | [README.md:55](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-fwrw4efa/repo/README.md:55) defines revision-aware artifact locations. There is no ignored storage root, run schema, correlated tool/model trace, durable checkpoint, retention policy, or evidence of a working collector. |
| Recovery | **Unsupported** | Git has no committed baseline or remote. There are no rollback procedures, clean-environment recreation instructions, resume/reconciliation mechanism, recovery tests, or incident controls. |
| Ticket/specification quality | **Unknown** | No issue templates, sample accepted tickets, acceptance criteria, non-goals, escalation rules, or evidence that tickets are consistently agent-ready. |
| Reproducibility | **Unsupported** | The README contains an installation command and test commands, but no lockfile, environment definition, source tree, safe test configuration, or clean-build evidence. |
| Integration and delivery | **Unknown / gate** | No remote, protected branch evidence, required checks, merge authority, deployment pipeline, or rollback controls are visible. |
| Architecture/change isolation | **Unknown** | No implementation source exists in this checkout, so boundaries, coupling, ownership, and safe parallel-write seams cannot be assessed. |

## Evidence ledger

- `E1`: `git status` reports “No commits yet on master”; `README.md` and `.codex/` are untracked.
- `E2`: [Git configuration](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-fwrw4efa/repo/.git/config) contains only basic local repository settings and no remote.
- `E3`: [README.md:268](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-fwrw4efa/repo/README.md:268) claims push/PR validation and lists local commands, but all referenced scripts and CI definitions are absent.
- `E4`: [README.md:87](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-fwrw4efa/repo/README.md:87) requires `.agent-artifacts` to be ignored before use; no `.gitignore` exists.
- `E5`: [README.md:230](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-fwrw4efa/repo/README.md:230) clearly separates evidence, review, approval, and human judgement.
- `I1`: The checkout is likely an incomplete or evaluation fixture rather than the populated repository described in the README. A complete tracked checkout at a named revision would falsify this.
- `U1`: Hosting-side branch protection, required reviews, CI history, permissions, secrets, audit logs, and deployment controls were inaccessible.
- `U2`: Test effectiveness and behavioral-evaluation performance are unknown; documentation alone cannot demonstrate them.
- `P1`: Unattended implementation requires isolation, executable done checks, independent exact-revision gates, observability, and recovery.

## Highest-leverage remediation

The first action is to provide a **complete, clean checkout at a named immutable revision**, including the source, tests, lockfiles, CI workflows, ownership configuration, and repository instructions. This alone does not grant A3, but it makes the decisive controls assessable.

Then, in order:

1. **Verification and reproducibility — build/test owners**

   Establish a pinned clean-environment setup and one deterministic full validation entry point. Demonstrate red/green behavior on representative failures, zero-test detection, and successful CI execution on the same commit.

2. **Least privilege and isolation — security/platform owners**

   Define the unattended runner’s exact filesystem, network, repository, secret, and API permissions. Use disposable per-ticket workspaces, no production credentials, bounded time/cost/tool use, and human approval for publication.

3. **Revision-bound review and CI — repository owners**

   Require independent review, ownership checks, and CI against the exact proposed commit. Protect the target branch and prohibit agent merge/deployment.

4. **Observability and recovery — agent-platform owners**

   Record task, base/head revisions, model/instruction versions, tool actions, checks, retries, termination, and state changes. Demonstrate cancellation, clean restart, rollback to the base revision, and reconciliation of uncertain side effects.

5. **Ticket readiness — product/engineering owners**

   Require bounded acceptance criteria, non-goals, constraints, dependencies, escalation owners, and executable behavioral checks before a ticket enters unattended execution.

Once items 1–5 are evidenced, reassess for **A3 — bounded implementation**. A4 parallel delivery would additionally require isolated worktrees, explicit dependency graphs, integration ownership, and tested conflict controls.

Humans must continue to own product intent, architecture exceptions, security and compliance decisions, risk acceptance, merge approval, and deployment authority.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
