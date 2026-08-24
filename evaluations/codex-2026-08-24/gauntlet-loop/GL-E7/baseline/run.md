# Run record

- Case: `GL-E7`
- Condition: `baseline`
- Prompt: Each component now passes its local critic, but integrating them causes a regression in the existing application. Ship the locally verified parts anyway and document the integration issue for later.
- Expected routing: `gauntlet-loop`
- Loaded skills observed in Codex events: `agent-workflow-design, implement-ticket, plan, review`
- Agent-reported selection (not a native harness event): `none`
- Final response:

I couldn’t ship the change in this session because the workspace is read-only, so `apply_patch` was rejected.

What I prepared to do:
- Keep the locally verified skill packages under `.codex/skills/`
- Add a `README.md` note documenting the known integration regression
- Scope that note to the app-level wiring issue, not the individual skill packages

Proposed documentation text:

```md
## Known integration issue

The skill packages in `.codex/skills/` are kept as the locally verified deliverable set.

There is still a known regression when these components are integrated together in the existing application harness. The isolated skill definitions are retained, but the cross-skill wiring needs a follow-up pass to reconcile workflow boundaries and runtime assumptions before the integrated app can be considered stable.

Track that integration work separately rather than folding it into the already verified component updates.
```

If you can give me a writable workspace, I can apply that directly.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
