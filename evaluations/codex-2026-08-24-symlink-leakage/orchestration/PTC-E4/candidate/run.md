# Run record

- Case: `PTC-E4`
- Condition: `candidate`
- Prompt: Search for the most relevant architectural decision, read it, decide what unresolved question it raises, then choose the next document to inspect based on that meaning. Continue until you have enough evidence to explain the design.
- Expected routing: `agent-workflow-design`
- Loaded skills observed in Codex events: `agent-readiness, agent-workflow-design, dynamic-workflows, implement-ticket, plan, programmatic-tool-calling`
- Final response:

The repository’s central architectural decision is:

> Deterministic orchestration owns control; model workers perform bounded semantic work.

I followed this evidence chain:

1. [agent-workflow-design/SKILL.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-03cj0n3i/repo/.codex/skills/agent-workflow-design/SKILL.md)  
   Establishes the decision: explicit state machines own sequencing, policy, state, retries, acceptance, and recovery. Model outputs are claims—not proof—and require independent gates.

2. [dynamic-workflows/SKILL.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-03cj0n3i/repo/.codex/skills/dynamic-workflows/SKILL.md)  
   Answers which runtime realizes it: Mastra owns the executable workflow graph, while ACP provides a replaceable coding-worker boundary.

3. [adaptive-planning.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-03cj0n3i/repo/.codex/skills/dynamic-workflows/references/adaptive-planning.md)  
   Resolves how runtime-generated workflows remain controlled. A planner may propose a typed graph, but cannot create capabilities, expand permissions, approve itself, or mutate during planning. Deterministic validation and, where necessary, human approval precede execution.

4. [mastra-runtime.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-03cj0n3i/repo/.codex/skills/dynamic-workflows/references/mastra-runtime.md)  
   Maps the design to concrete machinery: persisted JSON-compatible graphs reference pre-registered agents, tools, workflows, and control-flow primitives. Mastra handles execution and lifecycle; the surrounding application layer retains authority and policy.

5. [acp-harnesses.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-03cj0n3i/repo/.codex/skills/dynamic-workflows/references/acp-harnesses.md)  
   Defines worker interchangeability safely. Any ACP-over-stdio executable can serve as a worker, but authentication, sandboxing, and permissions remain properties of that harness. Hidden conversational state must never become workflow truth.

The resulting design is a layered control system:

```text
Human / application policy
        ↓ authority and approval
Deterministic validation layer
        ↓ accepted graph
Mastra workflow runtime
        ↓ bounded tasks
ACP coding workers
        ↓ observable effects
Repository + explicit persisted state
        ↓
Independent verification and run receipts
```

Its important consequences are:

- Known control flow is encoded directly; no supervisor model improvises it.
- Adaptive planning changes topology, not authority.
- Workers can only reference capabilities registered in advance.
- Repository and persisted workflow state outrank chat memory.
- Parallel reads are encouraged; parallel writes require disjoint scopes or isolated workspaces.
- Phase completion, valid output, and end-to-end acceptance are deliberately separate.
- Approval binds to the exact graph, permissions, scope, concurrency, and budget—not merely the original prompt.
- Resume continues the same approved graph; replanning creates a new identity and requires renewed validation.
- Verification observes actual state rather than trusting worker success messages.

The remaining unresolved questions are intentionally deployment-specific: exact installed Mastra schemas and APIs, storage guarantees, ACP executable selection, permission policy, cost limits, and cross-process resume behavior. The architecture requires these to be verified from the installed runtime before implementation; it explicitly refuses to invent them.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
