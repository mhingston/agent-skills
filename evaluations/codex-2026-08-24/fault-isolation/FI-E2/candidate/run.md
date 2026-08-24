# Run record

- Case: `FI-E2`
- Condition: `candidate`
- Prompt: This endpoint became much slower after last week's changes. Work out what caused the regression and give me evidence I can hand to an implementer.
- Expected routing: `fault-isolation`
- Loaded skills observed in Codex events: `fault-isolation, code-research, implement-ticket, plan`
- Agent-reported selection (not a native harness event): `none`
- Final response:

**Blocked on repository evidence**
- I can’t identify the regression cause from this workspace because the repo has **no commits, no branches, and no endpoint implementation** to compare against last week. `git status` reports “No commits yet on master”, and `git log` is empty.
- The only concrete performance-regression guidance available here is the fault-isolation evaluation prompt itself, which explicitly expects a repeatable baseline, known-good/bad state, and profiling/comparison before theory. See [`.codex/skills/fault-isolation/references/evaluation-suite.md`](.codex/skills/fault-isolation/references/evaluation-suite.md#L36) and [the repo guidance](README.md#L164).

**Evidence I have**
- `Observed`: no Git history in this workspace, so there is no “last week’s changes” diff to inspect.
- `Observed`: the workspace contains only [`README.md`](README.md) and the local skill scaffolding under [`.codex/skills/...`](.codex/skills/fault-isolation/references/evaluation-suite.md#L36).
- `Observed`: the repository guidance routes concrete regressions to `fault-isolation`, but there is no application code or endpoint source here to measure or profile.

**What I need to continue**
- The affected repository, or at minimum:
  - the endpoint path/name,
  - the last known good commit SHA,
  - the first known bad commit SHA or PR,
  - a reproducible request or fixture,
  - and any timing/profiling data you already have.

**What I can hand an implementer once I have that**
- a minimized reproducer,
- the measured good/bad baseline,
- the most likely causal change with falsifiable evidence,
- and a regression oracle that matches the observed slowdown.

If you can point me at the actual service repo or provide the bad/good SHAs, I can do the isolation work next.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
