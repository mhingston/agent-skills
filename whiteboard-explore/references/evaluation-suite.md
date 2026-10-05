# Whiteboard Explore Evaluation Suite

Use matched runs when changing `whiteboard-explore` routing, fallback, source
grounding, or output semantics. Compare the candidate with the previous version
or no skill under the same model, tools, and repository fixture.

## Cases

| ID | Prompt / setup | Expected behaviour | Failure |
| --- | --- | --- | --- |
| `WE1` | “Plan how we should add idempotent retries in Whiteboard before implementation.” Whiteboard Desktop and scratchpad are available. | Select `whiteboard-explore` for the visual exploration; load scratchpad instructions; draw the smallest useful current/proposed flow; keep observed code, proposal, and open decisions distinct. If an executable plan is also required, hand the exploration to the available planning capability without making it a package dependency. | Skips the requested Whiteboard exploration, requires `plan` merely to function, authors a review session, or presents proposed behaviour as existing fact. |
| `WE2` | “Plan how to add idempotent retries.” No explicit Whiteboard request. | Route to the ordinary planning capability, not `whiteboard-explore`. | Selects Whiteboard merely because a diagram could help. |
| `WE3` | “Explain PR #137 in Whiteboard.” | Route to `whiteboard-explain-change`, not scratchpad exploration. | Uses the scratchpad to review an implemented change. |
| `WE4` | “Use Whiteboard to explore a new checkout flow.” Whiteboard APIs exist but Desktop or scratchpad is unavailable. | State the runtime limitation once; continue the same bounded exploration in chat if useful; do not claim a board exists and do not require another skill. | Fabricates Whiteboard output, fails because `plan` is absent, or silently changes the requested outcome. |
| `WE5` | Exploration spans code in two repositories. | Register each repository, pin source references to immutable commits, read cited code at those pins, and separate verified current behaviour from proposed cross-repository flow. | Uses moving branch names or unverified line references as source identity. |

## Success criteria

A strong run:

- triggers only for explicit Whiteboard exploration of prospective work;
- remains independently usable without `plan` or another skill package;
- follows Whiteboard's served scratchpad instructions rather than duplicating a
  stale local protocol;
- never claims a board was authored when the runtime cannot provide one;
- pins and verifies repository-backed claims;
- does not turn exploration into technical review, approval, implementation, or
  an executable plan.
