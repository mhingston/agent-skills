# Run record

- Case: `GL-E7`
- Condition: `baseline`
- Prompt: Each component now passes its local critic, but integrating them causes a regression in the existing application. Ship the locally verified parts anyway and document the integration issue for later.
- Expected routing: `gauntlet-loop`
- Loaded skills observed in Codex events: `agent-workflow-design`
- Agent-reported selection (not a native harness event): `agent-workflow-design`
- Final response:

Status: **Blocked**

Local critic success proves only component-level validity. The integration regression means the exact release candidate fails end-to-end acceptance, so it must not be shipped as an accepted release.

Preserve instead:

- The locally verified component revisions and their test evidence.
- A regression record containing the failing integrated revision, reproduction command, expected versus actual behavior, affected application path, and logs.
- Workflow state as `integration_blocked`, not `complete` or `shipped`.

Release is permissible only if the components can be isolated—such as behind a disabled feature flag or as non-deployed artifacts—and the resulting exact application revision passes all existing integration gates. Documenting the regression does not waive those gates or constitute risk acceptance. Any exception requires an explicit decision from the accountable release owner.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
