# reflection-engine Agent Skill

An Agent Skill for evidence-grounded longitudinal reflection across a user's accessible conversation history, memory, files, and other explicitly available personal context.

The skill is inspired by the methodology of **Reflection Engine v1.3** by kropdx/Kevin Rose, but is rewritten as a portable Agent Skill rather than copying the original prompt. The source repository did not expose an obvious license when this derivative skill was created, so the package intentionally avoids bundling or reproducing the original prompt text.

## Files

- `SKILL.md` — activation metadata, evidence protocol, output contract, confidence calibration, stop rules, and quality checks.
- `references/reflection-lenses.md` — a compact set of analytical lenses used for focused or comprehensive reflection.

## Intended behaviour

The skill should:

- retrieve and sample evidence across time and domains when available;
- distinguish observed behaviour from inference;
- avoid treating questions as admissions;
- search for counterevidence;
- account for conversational-corpus bias;
- attach calibrated confidence to major conclusions;
- end insights with concrete, testable actions;
- refuse to manufacture a psychological portrait from thin evidence.

## Source inspiration

- https://github.com/kropdx/reflection-engine
- https://raw.githubusercontent.com/kropdx/reflection-engine/refs/heads/main/Reflection-Engine-v1.3.md

## Validation

The folder follows the Agent Skills directory convention and uses the required `name` and `description` YAML frontmatter in `SKILL.md`.
