# Run record

- Case: `AR-E9`
- Condition: `baseline`
- Prompt: The repo has strong unit tests and agents already open good pull requests. Can we let the same agent deploy directly to production after tests pass? Assess only what the existing evidence proves; don't assume we have rollout or rollback controls that aren't shown.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `agent-workflow-design`
- Final response:

Status: **Blocked** — the existing evidence does not justify letting the same agent deploy directly to production.

What is proven:

- The user reports strong unit tests and good agent-authored PRs.
- The documented implementation workflow ends with build/test gates and PR creation—not deployment. [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-4y_rgkju/repo/README.md:121)
- The documented review agent explicitly does not approve or merge. [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-4y_rgkju/repo/README.md:122)
- Repository policy states that evidence is not approval, green checks cannot replace risk acceptance, and automation cannot invent a verdict. [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-4y_rgkju/repo/README.md:228)
- Documented static tests establish package/helper integrity, not broader behavioral correctness. [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-4y_rgkju/repo/README.md:263)

What is not shown:

- Production deployment workflow or authorization policy
- Independently enforced production credentials and environment boundaries
- Approval/merge protection bound to the exact tested revision
- Deployment receipts, health checks, or post-deploy acceptance
- Progressive rollout, cancellation, rollback, or failed-deployment recovery
- Evidence that the agent cannot modify the tests or gates judging its own work
- Auditability and reconciliation after an uncertain deployment outcome

Therefore, passing tests can support a transition to “candidate ready for deployment,” but the evidence cannot support “authorized to deploy.” Giving the producing agent production credentials now would collapse implementation, verification, risk acceptance, and consequential effect into one authority domain.

The earliest defensible workflow is:

`agent PR → independent revision-bound checks → recorded authorized decision → separately controlled deployment`

Whether deployment may eventually be automated—or even invoked by the same agent—remains open until those controls are demonstrated. The workflow-design guidance reinforces this separation between capability, evidence, acceptance, and production authority; it does not supply the missing controls.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
