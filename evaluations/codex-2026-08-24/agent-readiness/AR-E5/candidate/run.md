# Run record

- Case: `AR-E5`
- Condition: `candidate`
- Prompt: We already completed a readiness assessment and decided the missing gate is a deterministic integration test in CI. Plan and implement that test and wire it into the required check.
- Expected routing: `no target skill`
- Loaded skills observed in Codex events: `agent-readiness, agent-workflow-design, implement-ticket, plan`
- Agent-reported selection (not a native harness event): `current`
- Final response:

I planned the gate and identified the exact implementation, but I could not apply it because the workspace is read-only.

Planned change:
- Add [`scripts/check_skill_packages.py`](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-trao4bsy/repo/scripts/check_skill_packages.py)
- Add [`.github/workflows/ci.yml`](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-trao4bsy/repo/.github/workflows/ci.yml)

What the test would enforce:
- every immediate directory under `.codex/skills/` has a `SKILL.md`
- each `SKILL.md` has YAML frontmatter with `name` and `description`
- the declared `name` matches the directory name
- `README.md` still documents the repository package layout

What CI would do:
- run that script on every push and pull request
- expose it as the required `integration` job

If you want, I can re-run this in a writable workspace or you can paste in the two files and I’ll validate the result.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
