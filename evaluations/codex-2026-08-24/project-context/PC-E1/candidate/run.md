# Run record

- Case: `PC-E1`
- Condition: `candidate`
- Prompt: We have architecture docs in the repo, product decisions in Confluence, tickets in Jira, and generated summaries in agent sessions. Different agents keep rediscovering which source is current. Design the minimum durable project-context model and tell me what should remain authoritative.
- Expected routing: `project-context`
- Loaded skills observed in Codex events: `project-context, decision-continuity`
- Agent-reported selection (not a native harness event): `none`
- Final response:

Use a thin, source-linked project-context index, not a new parallel tracker.

**Minimum durable model**
1. `truth`
   - Current state only: architecture, interfaces, constraints, verified runtime facts.
   - Each claim carries a governing source or freshness signal.
2. `intent`
   - Accepted product/architecture decisions, plans, acceptance criteria, non-goals.
   - Keep proposed intent separate from accepted intent.
3. `history`
   - Superseded decisions, investigations, incidents, completed outcomes, handoff evidence.
   - Append-oriented, not casually rewritten.
4. `scratch`
   - Drafts, exploratory notes, generated working material, temporary synthesis.
   - Explicitly non-authoritative.

Add only a **small index** with stable IDs and typed edges when agents need machine traversal:
- `decides` / `supersedes`
- `implements`
- `depends-on`
- `verifies`
- `projects-to`

That is enough to answer “what is true, what is intended, what happened, and what supports it” without building a full knowledge graph.

**What should remain authoritative**
- `Confluence`: product decisions, approved intent, rationale, non-goals, and decision records.
- Architecture docs in the repo: architecture and interface truth when they are the maintained canonical source for those claims.
- `Jira`: ticket scope, status, acceptance wording, and work-state projections.
- Code, tests, CI, deployments, runtime evidence: current technical truth about what the system actually does.
- Generated agent-session summaries: never authoritative by default; they are `scratch` or, at best, derived projections that point back to the real source.

**Authority rule**
- Do not let generated summaries, memory, dashboards, or chat history outrank the maintained source for the claim.
- If sources disagree, preserve the conflict instead of flattening it.
- Do not infer authority from recency, file location, or prominence alone.

**Practical hierarchy by claim**
- “What is the product decision?” -> Confluence.
- “What is the architecture supposed to be?” -> canonical architecture doc in repo, if maintained there.
- “What is the ticket asking for?” -> Jira.
- “What is actually true in the codebase/runtime?” -> code/tests/CI/deployment evidence.
- “What did an agent conclude?” -> useful, but non-authoritative until traced back.

The repository already points in this direction: `project-context` is meant to preserve truth/intent/history/scratch separation, and the README says to keep supporting artefacts under `.agent-artifacts/...` rather than creating another source of truth. See [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ueptcncp/repo/README.md) and [project-context/SKILL.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-ueptcncp/repo/.codex/skills/project-context/SKILL.md).

If you want, I can turn this into a concrete `context-index.json` shape and authority matrix for this repo.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
