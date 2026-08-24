# Run record

- Case: `DC4`
- Condition: `candidate`
- Prompt: Which source governs? An ADR and tracker parent conflict, and repository policy does not declare precedence.
- Expected routing: `decision-continuity`
- Loaded skills observed in Codex events: `decision-continuity, memory-recall, repository-ontology, implement-ticket, memory-maintenance, memory-capture, plan, project-context`
- Agent-reported selection (not a native harness event): `none`
- Final response:

The governing source is **not determined by the repository policy as written**.

- The repo only says that shared memory, code prevalence, and derived context do **not** become authority over a designated canonical source, and that decision continuity must not silently manufacture authority ([`README.md` lines 243-254](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-nhmnrdrg/repo/README.md#L243)).
- The decision-continuity fixture for this exact case says that when an **ADR and tracker parent conflict and policy does not declare precedence**, the correct status is **blocked** and the accountable authority must decide ([`decision-continuity/references/evaluation-suite.md` line 33](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-nhmnrdrg/repo/.codex/skills/decision-continuity/references/evaluation-suite.md#L33)).

So the answer is:

- **No automatic winner**
- **Conflict remains open**
- **Ask the accountable human or designated authority to declare precedence**

If you want, I can help draft the smallest decision question to resolve it.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
