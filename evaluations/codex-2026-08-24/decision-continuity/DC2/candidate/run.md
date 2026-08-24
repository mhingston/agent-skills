# Run record

- Case: `DC2`
- Condition: `candidate`
- Prompt: Did we decide whether to edit repository-ontology/SKILL.md for optional hooks? The accepted PR discussion says no; implementation and README preserve discoverability.
- Expected routing: `decision-continuity`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Yes. The decision was to **leave `repository-ontology/SKILL.md` unchanged** for the optional hooks.

The rationale, as you summarized it, was:
- the accepted PR discussion said **no** to editing the skill file;
- the implementation already handles the optional hook behavior;
- the README preserves discoverability without putting that burden into `SKILL.md`.

So if you need the short form: **no SKILL.md edit; keep the docs/implementation split as-is.**

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
