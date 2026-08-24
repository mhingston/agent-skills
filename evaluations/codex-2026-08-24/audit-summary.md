# Behavioural audit summary

## Coverage

The 24 August diagnostic pass covered 58 cases: orchestration (21), agent
readiness (9), fault isolation (6), project context (6), decision continuity
(8), and gauntlet loop (8). It used Codex CLI 0.149.0 with `gpt-5.4-mini`, low
reasoning effort, isolated copied skill packages, read-only permissions, and no
external services.

The broad pass was a target-present versus target-omitted diagnostic, not a
previous-revision comparison. The harness exposed successful body reads but no
native primary-selection event, so routing is `not_verifiable`; body loading is
reported only as a diagnostic signal. Sparse fixtures also left most outcome
checks `not_verifiable`.

## Findings

- `agent-workflow-design`, `dynamic-workflows`, `programmatic-tool-calling`,
  `agent-readiness`, `fault-isolation`, and `project-context` produced no
  evidence that justified a skill rewrite. They remain unchanged.
- `gauntlet-loop` had a matched GL-E6 body-level escape: the base skill allowed
  producer-owned verifier changes in 2/3 body-loaded trials; the candidate
  refused or blocked all 3/3. The added invariant protects the independent
  acceptance gate.
- `decision-continuity` had a matched DC3 body-level escape: the base skill
  drafted source edits in 2/2 body-loaded trials; the final candidate returned
  a report/proposed change without a patch in 2/2 body-loaded trials. One trial
  on each side did not load the target body and is not evidence about the fix.
  The added invariant keeps evidence, governing sources, scenario inputs, and
  workflow guidance read-only and routes approved mutations to their owner.

The exact prompts, revisions, harness settings, and compact observations for
the two before/after checks are in [`matched-fixes.md`](matched-fixes.md).

## Limitations

No claim is made about catalogue-wide routing precision or recall. The harness
could not reveal native discovery, and the sparse read-only workspace had no
real verifier, application, tracker, production environment, or Confluence /
Atlassian service. Owning-agent lifecycle cases for `implement`, `pr-review`,
and `refine` were not run.

Raw `run.jsonl`, `stderr.log`, target-omitted records, generated aggregates, and
the invalid symlink-based run were intentionally removed from the repository.
