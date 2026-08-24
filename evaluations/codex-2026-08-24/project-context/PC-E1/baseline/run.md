# Run record

- Case: `PC-E1`
- Condition: `baseline`
- Prompt: We have architecture docs in the repo, product decisions in Confluence, tickets in Jira, and generated summaries in agent sessions. Different agents keep rediscovering which source is current. Design the minimum durable project-context model and tell me what should remain authoritative.
- Expected routing: `project-context`
- Loaded skills observed in Codex events: `decision-continuity`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use a 4-layer model:

1. `Canonical sources`
- Architecture docs: authoritative for system shape, interfaces, invariants, and technical constraints.
- Confluence product decisions: authoritative for product intent, accepted choices, non-goals, and decision status.
- Jira tickets: authoritative for the current work item, scope boundary, owner, priority, and delivery status.
- Agent session summaries: not authoritative; treat them as scratch/provenance unless explicitly promoted into a canonical source.

2. `Decision register`
- A small record of only load-bearing decisions.
- Fields: decision, status (`accepted` / `rejected` / `deferred` / `open` / `superseded`), authority, date, source link, and supersedes/depends-on.
- This is the minimum thing agents should consult when they need to know “what is decided.”

3. `Working context`
- Current task, current assumptions, current open questions, current blockers.
- This is mutable and short-lived.
- It can summarize canonical sources, but it cannot outrank them.

4. `Scratch / session trace`
- Drafts, summaries, intermediate reasoning, and agent-generated recaps.
- Useful for recovery and continuity, but never a source of truth by itself.

What should remain authoritative:
- Architecture docs for technical architecture and invariants.
- Confluence decisions for product direction and approved choices.
- Jira for task execution state and scope.
- The decision register only as a normalized index into those authorities, not as a competing truth source.
- Agent summaries only as evidence of what an agent saw or inferred, not as durable truth.

What should not become authoritative:
- Any agent-generated summary, even if repeated.
- Implementation state, unless it is explicitly captured by a canonical source.
- “Consensus” across sessions without attributable approval.

This matches the repo’s own framing: `project-context` is the durable substrate, `decision-continuity` protects attributable accepted direction, and shared memory or derived projections must not become a second source of truth ([README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-u67po90q/repo/README.md#L142), [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-u67po90q/repo/README.md#L161), [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-u67po90q/repo/README.md#L200)).

If you want, I can turn this into a concrete schema next:
1. a JSON/YAML model,
2. a Confluence page template,
3. or a repo-local `project-context` spec.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
