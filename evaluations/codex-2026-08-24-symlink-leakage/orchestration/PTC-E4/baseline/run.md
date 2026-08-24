# Run record

- Case: `PTC-E4`
- Condition: `baseline`
- Prompt: Search for the most relevant architectural decision, read it, decide what unresolved question it raises, then choose the next document to inspect based on that meaning. Continue until you have enough evidence to explain the design.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `agent-readiness, agent-workflow-design, dynamic-workflows, implement-ticket, plan`
- Final response:

No formal ADR exists in this sparse checkout, so the closest and most relevant architectural decision is the workflow-design contract.

The semantic trail was:

1. [agent-workflow-design/SKILL.md](</home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-3glwsw2w/repo/.codex/skills/agent-workflow-design/SKILL.md:121>)  
   Decision: deterministic orchestration—not model conversation state—owns sequencing, policy, state, effects, retries, and acceptance.

   Unresolved question: How is that separation implemented when the workflow topology varies by task?

2. [dynamic-workflows/SKILL.md](</home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-3glwsw2w/repo/.codex/skills/dynamic-workflows/SKILL.md:19>)  
   Answer: Mastra owns the executable graph and lifecycle; ACP workers execute bounded coding tasks. Known topology uses deterministic mode. Task-dependent topology uses adaptive mode.

   Unresolved question: Doesn’t an adaptive planner regain control of orchestration?

3. [adaptive-planning.md](</home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-3glwsw2w/repo/.codex/skills/dynamic-workflows/references/adaptive-planning.md:1>)  
   Answer: No. The planner only proposes a structured graph drawn from registered primitives. Deterministic code validates schemas, dependencies, scopes, concurrency, loops, and budgets. Material mutation or cost requires approval. The exact accepted graph is persisted with an identity or digest.

   Unresolved question: Which runtime mechanisms actually execute and preserve those controls?

4. [mastra-runtime.md](</home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-3glwsw2w/repo/.codex/skills/dynamic-workflows/references/mastra-runtime.md:8>)  
   Answer: Mastra resolves stable primitive IDs, executes graph ordering and mappings, stores definitions, and manages runs. The surrounding application policy—not Mastra itself—owns permissions, allowed resources, approval, and cost/concurrency limits.

   Important qualification: persisted graph definitions do not themselves prove durable run resumption. Suspension, persistence, and resume behavior must be verified against the installed Mastra version.

   Unresolved question: How can coding workers remain interchangeable without leaking harness-specific concerns into the graph?

5. [acp-harnesses.md](</home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-3glwsw2w/repo/.codex/skills/dynamic-workflows/references/acp-harnesses.md:1>)  
   Answer: ACP-over-stdio is the compatibility boundary. Authentication, sessions, and permission requests belong to the selected harness. The graph references only preregistered worker IDs; a planner cannot invent executables, credentials, providers, or registrations.

The resulting design is:

```text
Human/application policy
        ↓ approval, scope, budgets
Deterministic coordinator
        ↓ validates and persists exact graph
Mastra runtime
        ↓ invokes registered primitive IDs
ACP boundary
        ↓
Interchangeable coding worker
        ↓
Repository and explicit artifacts as shared truth
```

Its central principle is constrained delegation: models supply semantic judgment, but never become the authoritative control plane. Their outputs are proposals or claims. Deterministic validation, explicit approval, independent verification, and revision-bound receipts decide whether execution may advance.

The main genuinely unresolved implementation issue is runtime-version evidence: the repository deliberately refuses to promise exact Mastra APIs or cross-process resumability until the installed version’s types, storage behavior, and lifecycle semantics have been tested.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
