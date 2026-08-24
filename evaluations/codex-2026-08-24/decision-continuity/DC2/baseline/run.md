# Run record

- Case: `DC2`
- Condition: `baseline`
- Prompt: Did we decide whether to edit repository-ontology/SKILL.md for optional hooks? The accepted PR discussion says no; implementation and README preserve discoverability.
- Expected routing: `decision-continuity`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Yes. The decision was to **not** edit `repository-ontology/SKILL.md` for optional hooks.

The repo guidance points the other way:
- `SKILL.md` should stay the canonical entry point and remain portable.
- Optional detail belongs in supporting files or the README, not as extra top-level skill fields.
- The catalog entry in [`README.md`](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-i793q2ni/repo/README.md) already preserves discoverability for `repository-ontology`.

I also don’t see a `repository-ontology/` directory in this checkout, so there is nothing here to edit in that path.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
