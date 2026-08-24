# Run record

- Case: `AR-E3`
- Condition: `candidate`
- Prompt: Agents already make supervised local edits here. We now want them to open pull requests for ready tickets without a human watching every command. Assess whether the controls support that increase and identify the specific blockers, if any.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `agent-readiness`
- Final response:

## Assessment status

**Not ready** for unattended pull-request creation from this workspace.

The supported cap remains **A2 — supervised local edits** based on the current operating model you reported. Moving to unattended implementation and PR publication requires A3 controls that are either demonstrably absent here or unavailable for verification.

This conclusion covers opening a PR only. It grants no merge, deployment, production, or risk-acceptance authority.

## Scope and policy

- Scope: the current repository/workspace.
- Target: one agent implements one ready ticket, pushes a branch, and opens a reviewable PR without command-by-command supervision.
- Evidence: read-only inspection on 2026-08-24; no builds, tests, hooks, installers, or external actions were executed.
- Accountable product, security, repository, and review owners: **unknown**.
- Proposed policy (`P1`): unattended PR creation requires bounded task authority, isolated least-privilege execution, deterministic done checks, independent exact-revision verification, controlled Git publication, observable side effects, and safe retry/reconciliation.

## Specific blockers

1. **There is no publishable Git repository state (`E1`).**  
   The repository has no commits, its branch is unborn `master`, and [.git/config](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-40news5z/repo/.git/config) has no remote. An agent cannot create a revision-bound PR from this workspace.

2. **There is no executable verification gate (`E2`, `U1`).**  
   The only visible project content is [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-40news5z/repo/README.md). No source, tests, build configuration, CI workflow, or required-check configuration is present. The README describes desired workflow conventions, but does not prove that a ticket is complete or correct. Under the proposed policy, no deterministic done check means no unattended implementation loop.

3. **Independent, exact-revision review is unproven (`U2`).**  
   No CI or review mechanism was available that independently evaluates the exact commit being published. README language about review and revision-bound evidence is procedural intent, not enforcement. This blocks autonomous publication.

4. **Git-host controls are unknown (`U3`).**  
   There is no evidence for branch protection, required checks, CODEOWNERS, fork/branch permissions, PR API permissions, or protection against force-pushing and writing to default branches. Unknown publication permissions must fail closed.

5. **Runner isolation and credential blast radius are unknown (`U4`).**  
   Filesystem, network, Git-host token, cloud, secret, and production access have not been inventoried. Unattended mutation is unsafe until the agent’s credentials are narrowly scoped and revocable.

6. **The unattended execution envelope is undefined (`U5`).**  
   No enforceable limits were found for attempts, runtime, cost, tool use, no-progress detection, cancellation, stale tickets, newly discovered scope, or escalation.

7. **PR side-effect recovery is unproven (`U6`).**  
   There is no evidence of idempotent PR creation, detection of an already-created PR after a timeout, durable run identity, audit records, or reconciliation after an uncertain push/API response.

## Readiness matrix

| Dimension | Status | Effect on PR autonomy |
|---|---|---|
| Ready-ticket contract and authority | Unknown | Cannot establish bounded intent or escalation boundaries |
| Reproducible environment | Unknown | Cannot distinguish product failure from environment failure |
| Deterministic verification | Unsupported in visible repo | Hard blocker |
| Independent exact-revision checks | Unknown | Hard blocker |
| Git repository and remote | Unsupported | PR creation is mechanically impossible |
| Least privilege and isolation | Unknown | Hard blocker |
| Branch protection and review ownership | Unknown | Publication safety is unproven |
| Bounded orchestration | Unknown | Unattended loops could run or expand indefinitely |
| Audit, reconciliation, and recovery | Unknown | External side effects cannot be safely reconstructed |
| Documentation/context | Partial | README states useful conventions, but the referenced catalogue is not present in this checkout |

## Smallest path to reassessment

1. **Establish a real revision and delivery target.**  
   Repository owner provides a committed default branch and a configured remote. Completion evidence: clean clone can create a feature branch and identify its base commit.

2. **Create an enforced PR gate.**  
   Engineering owners define the command set for a ready ticket and run it independently in CI against the exact head SHA, with zero-test detection and required status checks. Completion evidence: a deliberately failing fixture cannot be published as “ready,” and changing the head invalidates prior approval.

3. **Constrain publication credentials.**  
   Security/repository owners document and test an agent identity that can create only non-protected branches and PRs, cannot merge, bypass protection, alter required checks, access production, or expose unrelated secrets, and can be revoked. Completion evidence: positive and negative permission tests in isolation.

4. **Make PR creation bounded and recoverable.**  
   Workflow owner supplies immutable ticket scope, attempt/time limits, cancellation and escalation rules, durable run/task/commit IDs, idempotent PR lookup/creation, and reconciliation after simulated timeout. Completion evidence: interrupted runs resume without duplicate PRs or ambiguous branch state.

5. **Require independent human review before merge.**  
   A human remains responsible for product, architecture, security, data, and risk decisions. The agent may propose a PR; it must not approve its own work, merge it, or invent risk acceptance.

Once those controls are demonstrated on representative ready tickets, **A3 — bounded implementation with PR creation but no autonomous merge** would be supportable. Reassess after runner-permission, CI, branch-protection, workflow, model/harness, or Git-host changes, and after any duplicate PR, escaped defect, credential exposure, or uncertain publication incident.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
