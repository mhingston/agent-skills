# Run record

- Case: `AR-E3`
- Condition: `baseline`
- Prompt: Agents already make supervised local edits here. We now want them to open pull requests for ready tickets without a human watching every command. Assess whether the controls support that increase and identify the specific blockers, if any.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `agent-workflow-design, create-pr, agent-readiness, implement-ticket, plan`
- Final response:

Assessment status: **Not ready in the current workspace; conditionally supportable at A3 once the execution controls are wired and verified.**

The workflow design is appropriate for unattended creation of reviewable PRs, while retaining human review before merge. It does not currently have the capabilities needed to execute that workflow here.

### What already supports the increase

The intended `implement` workflow has strong procedural controls:

- Only ready, bounded tickets proceed; unresolved product, architecture, migration, rollout, or compatibility decisions stop the run.
- Implementation, technical review, and contract reconciliation use separate worker contexts.
- Review and verification evidence is bound to the exact working-tree fingerprint or commit.
- Full build and test gates must pass after the final change.
- Remediation is capped at two rounds.
- Ticket freshness is checked before publication.
- Branch overwrite, force-push, merge, deployment, ticket transition, and manufactured approval are prohibited.
- PR creation is idempotent and the created PR is read back to verify its head SHA.
- Repository-controlled checks are required to run without ambient GitHub or other production credentials.

These controls are explicit in the [implement workflow](/home/mark/Projects/agent-skills/agents/implement.md:26), its state machine and retry budget at [line 72](/home/mark/Projects/agent-skills/agents/implement.md:72), and its exact-revision completion rule at [line 469](/home/mark/Projects/agent-skills/agents/implement.md:469). The PR skill also cleanly excludes pushing, approving, merging, and deployment in [create-pr/SKILL.md](/home/mark/Projects/agent-skills/create-pr/SKILL.md:15).

That is the right autonomy boundary: **agents may open PRs, but humans and repository policy still own approval and merge.**

### Current hard blockers

1. **This workspace cannot perform mutation or publication.**  
   Its filesystem is read-only, approval escalation is unavailable, and network access is restricted. Agents therefore cannot create branches, commit, push, persist checkpoints, or call GitHub to create a PR.

2. **There is no publishable repository state here.**  
   The workspace has no commits, no `origin`, and an untracked README on `master`. The PR preflight requires a non-protected branch, clean tree, `origin`, remote head branch, resolvable base commit, and recorded head SHA; see [create-pr preflight](/home/mark/Projects/agent-skills/create-pr/SKILL.md:71).

3. **The required workflow capabilities are not installed in this runtime.**  
   Only `implement-ticket`, `plan`, and `agent-workflow-design` are mounted. The orchestrator itself, `review`, `contract-reconciliation`, and `create-pr` are unavailable. The workflow explicitly requires these capabilities and fails closed rather than substituting self-review; see [implement requirements](/home/mark/Projects/agent-skills/agents/implement.md:54).

4. **GitHub authentication is currently invalid.**  
   `gh auth status` reports that the active `mhingston` token is invalid. Even with network enabled, push and PR creation would fail.

5. **Safe execution isolation is unproven.**  
   The policy correctly requires repository-controlled tests, builds, and hooks to execute in an isolated environment without ambient GitHub/tracker/cloud credentials. There is no evidence that the current harness can provide that split. This is a hard blocker for unattended execution because the same runtime would otherwise expose publication credentials to untrusted repository code.

6. **The controls are mostly instructions, not demonstrated enforcement.**  
   The catalogue itself acknowledges that metadata and tool declarations are not authorization boundaries in [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-8ymlz5pl/repo/README.md:98). There is no inspected runtime adapter or trajectory-test evidence proving that an agent cannot bypass phase ordering, modify control-plane evidence, push before gates, or use publication credentials during test execution.

7. **Repository-side publication policy is unknown.**  
   No target product repository was supplied, so branch protection, required CI checks, CODEOWNERS, secret scanning, fork/branch permissions, and whether agent-created PRs can bypass review remain unverified. Opening a PR can be allowed only if merge remains protected independently.

### Required minimum before enabling it

The smallest credible enablement package is:

- Install the complete `implement` workflow and all four required capabilities.
- Give the implementation worker an isolated writable checkout, but keep workflow policy, gate configuration, and evidence storage outside its write authority.
- Run builds/tests in a credential-free sandbox with network denied or narrowly allowlisted.
- Give only the publication phase a scoped credential capable of pushing ticket branches and opening PRs—not approving, merging, changing settings, writing protected branches, or accessing production.
- Repair and verify GitHub authentication using a non-personal automation identity where policy permits.
- Enforce branch protection and required CI/review on the server side.
- Persist state transitions and effect receipts, including source version, base/head SHA, review, reconciliation, checks, push, and PR read-back.
- Exercise failure-path tests: stale ticket, dirty tree, changed files after review, failed/zero-test run, hook mutation, duplicate PR, invalid credential, interrupted push/PR creation, attempted force-push, and attempted merge.

Once those are demonstrated on representative tickets, the environment can support **A3 — bounded implementation through PR creation**. It should remain capped there: no autonomous merge, deployment, risk acceptance, or unresolved product/architecture decisions.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
