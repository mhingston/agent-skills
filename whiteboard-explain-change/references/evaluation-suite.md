# Whiteboard Explain Change Evaluation Suite

Use matched runs when changing `whiteboard-explain-change` routing, revision
binding, fallback, or output semantics.

## Cases

| ID | Prompt / setup | Expected behaviour | Failure |
| --- | --- | --- | --- |
| `WX1` | “Explain PR #137 in Whiteboard so I can understand what changed.” Authoring runtime and repository are available. | Select `whiteboard-explain-change`; follow served authoring instructions including file lenses; resolve exact base/head commits; verify the diff; create a compact source-linked explanation. | Routes to technical review, uses moving PR identity as the evidence pin, or invents correctness claims. |
| `WX2` | “Review PR #137 for bugs, test gaps and merge readiness.” | Route to `review` or the appropriate PR-review lifecycle, not this skill. | Treats explanation as adversarial technical review. |
| `WX3` | “Explain this PR and approve it if it looks good.” | Whiteboard explanation may be produced when explicitly requested, but approval remains outside this skill and must route to the accountable review/verdict workflow. | Approves, recommends merge as a verdict, or treats explanation as evidence of correctness. |
| `WX4` | “Explain this branch in Whiteboard.” The branch moves after selection. | Resolve the target to exact immutable base/head commits returned by Whiteboard and bind source claims to those commits; retarget before writing if the intended target moved. | Pins claims only to the branch name or silently describes a different revision. |
| `WX5` | “Explain my uncommitted changes in Whiteboard.” | Use a worktree target with HEAD as base; record exact HEAD; inspect `git diff HEAD` and status; bind the explanation to the Whiteboard worktree generation plus observed diff. | Claims HEAD alone identifies the working tree or omits unstaged/staged state from target validation. |
| `WX6` | Explicit Whiteboard explanation request but authoring APIs are unavailable. | State that a Whiteboard cannot be authored; do not fabricate a session; provide a concise chat explanation only if useful and clearly labelled as fallback. | Pretends a board exists or silently substitutes generic review. |

## Success criteria

A strong run:

- triggers only when an exact implemented change is explicitly requested in
  Whiteboard;
- follows Whiteboard's current served authoring protocol;
- binds PRs and branches to immutable base/head commits and uncommitted work to
  the precise worktree state;
- verifies source references before linking them;
- keeps explanation separate from technical findings, merge readiness, and human
  approval;
- fails transparently when the Whiteboard authoring runtime is unavailable.
