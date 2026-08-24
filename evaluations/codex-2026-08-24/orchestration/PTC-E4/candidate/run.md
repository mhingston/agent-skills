# Run record

- Case: `PTC-E4`
- Condition: `candidate`
- Prompt: Search for the most relevant architectural decision, read it, decide what unresolved question it raises, then choose the next document to inspect based on that meaning. Continue until you have enough evidence to explain the design.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

The most relevant architectural decision in this repo is: **skills are designed to be fully self-contained, portable packages, and agents are separate orchestration layers**.

Evidence from [`README.md`](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-979a2uzo/repo/README.md):
- A skill’s entry point is its own `<skill-name>/SKILL.md`.
- Supporting files must stay inside that skill’s directory.
- Skills must not depend on repo-level shared folders, parent paths, or other skills.
- Relative references should stay direct from `SKILL.md`.
- Agent definitions live separately under `agents/` and handle orchestration, lifecycle, delegation, and responsibility boundaries.
- Internal workflow modules are explicitly gated by owning agent context and are intended to fail closed when invoked directly.

Unresolved question this raises:
- **How do individual skills compose or share common behavior without violating the self-contained rule?**
- The README hints at duplication being acceptable when it preserves portability, but it does not define where reuse ends and copy/paste begins.

What I inspected next:
- I looked for other markdown docs that could answer that question, but this checkout contains only [`README.md`](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-979a2uzo/repo/README.md).
- There is no `SKILL.md` or agent file available here to continue the chain, so the available evidence stops at the repository-level contract.

So the design, as documented, is a **catalogue of isolated skill packages plus separate agent orchestrators**, optimized for portability and controlled ownership rather than shared internal coupling.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
