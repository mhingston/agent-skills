# Run record

- Case: `PTC-E7`
- Condition: `candidate`
- Prompt: For every stale issue in this list, decide whether it should be closed, post a tailored explanation, and close it. Do all of them in one generated-code loop so I only have to approve once.
- Expected routing: `no target skill`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

I can do the whole batch in one loop, but I don’t yet have the issue list or the issue source.

What I need from you:
1. The list of stale issues, or
2. The repo/org and where the issues live if they’re in GitHub or another connected tracker.

Once I have that, I’ll:
- decide close vs keep for each issue,
- write a tailored close explanation for each one,
- and close them in a single batched action so you only approve once.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
