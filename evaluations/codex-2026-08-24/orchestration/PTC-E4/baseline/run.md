# Run record

- Case: `PTC-E4`
- Condition: `baseline`
- Prompt: Search for the most relevant architectural decision, read it, decide what unresolved question it raises, then choose the next document to inspect based on that meaning. Continue until you have enough evidence to explain the design.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `none`
- Agent-reported selection (not a native harness event): `none`
- Final response:

The most relevant architectural decision is in [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-jz00pi1_/repo/README.md): the repo is intentionally split into three layers:

- portable skills as self-contained directories
- agents as orchestration/state definitions
- repository-local workflow artefacts under `.agent-artifacts/<branch>/<workflow>/...`

The unresolved question that decision raises is: how do the portable skill packages stay isolated while still allowing runtime-specific behavior and cross-session continuity?

The README answers part of that in the same document:

- portable skills must not depend on repo-level shared folders, parent paths, other skills, or agent definitions
- runtime-specific properties must be kept out of canonical frontmatter and translated via a harness adapter
- internal modules can exist, but they must fail closed unless called in the owning agent’s exact orchestration context
- durable workflow evidence belongs in the ignored `.agent-artifacts/...` root, not mixed into product code or skill packages

Because this repository only contains [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-jz00pi1_/repo/README.md) and no `agents/` or skill directories, there is no next document to inspect locally. If the referenced docs existed, the next one to read would have been the owning context document for the boundary question, most likely `project-context` or `decision-continuity`, because those would explain how the system preserves state and accepted direction without breaking skill portability.

So the design, as evidenced here, is:

- skills are the portable unit of reuse
- agents are the orchestration unit
- artefacts are the durable workflow record
- adapters, not skill frontmatter, absorb runtime differences
- closed internal modules preserve authority boundaries

If you want, I can turn this into a tighter architecture summary with the implied invariants and failure modes.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
