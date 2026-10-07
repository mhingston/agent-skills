# Session-lessons routing evaluation cases

Use these cases when changing correction classification, coverage-state semantics,
or durable destination routing in `session-lessons`. Run matched candidate/base
comparisons in the same harness when behavioural evaluation is available. Static
inspection can verify the contract shape, but it is not behavioural evidence.

## SL-E1 — repair an existing unwired deterministic control

**Evidence**

Three independent sessions show agents introducing a banned API that should be
rejected by repository policy. The repository already contains a linter rule with
the correct predicate, but the canonical CI workflow does not run that linter and
local task-runner defaults skip it.

**Expected result**

- the cluster qualifies under the normal recurrence threshold;
- `correction_class` is exactly `deterministic-control`;
- `current_coverage` is `partial`, because the relevant control exists but is
  unwired on the observed path;
- the primary destination is `tracked work item` to wire or repair the existing
  control, not `agent instructions`;
- the recommendation does not propose a duplicate check or prose-only rule;
- validation follow-up proves the existing linter runs on the relevant path and
  rejects a representative banned-API fixture.

## SL-E2 — working executable control is adequate without prose

**Evidence**

A schema invariant is fully enforced by a current CI validator that runs on every
relevant change and rejects an observed invalid fixture. There is no equivalent
sentence in `AGENTS.md` or repository documentation. The analysed sessions do not
establish bypass, stale wiring, or an uncovered path.

**Expected result**

- `current_coverage` is `adequate`, not `absent`, solely because the executable
  control reliably owns the invariant;
- the absence of duplicate prose is not treated as a documentation gap;
- no new agent instruction is recommended merely to restate the check;
- if no other material gap is established, disposition is `no-op`.

## SL-E3 — contextual judgement remains guidance

**Evidence**

Three independent reviews show inconsistent handling of a cross-service
compatibility judgement. No stable mechanical predicate can distinguish acceptable
from unacceptable changes; the decision depends on consumer context documented in
the repository architecture guidance.

**Expected result**

- `correction_class` is exactly `guidance`;
- the analysis does not invent a deterministic check merely to avoid prose;
- the destination is the narrowest existing authoritative guidance source, such as
  repo docs or an existing skill, rather than a new parallel rule;
- validation follow-up checks whether future agents/reviewers consume and apply the
  clarified guidance on representative positive and near-miss cases.

## SL-E4 — conflicting durable sources

**Evidence**

A maintained agent instruction permits direct edits to generated clients, while a
current repository generator check rejects direct edits and requires regeneration
from the schema. Both sources are active and apply to the same path.

**Expected result**

- `current_coverage` is `conflicting`, not `adequate`;
- the analysis identifies the contradiction between durable sources rather than
  treating observed non-compliance alone as the conflict;
- the recommended change selects the authoritative owner and removes or corrects
  the conflicting source;
- the existing executable control is not duplicated.

## Grading

A candidate change fails this suite if it:

- emits non-canonical correction values such as `deterministic control` or
  `information access`;
- classifies a working executable control with no prose as `absent`;
- classifies an unwired or broken existing control as `absent` rather than
  `partial`;
- routes an objective machine-checkable invariant to prose before inspecting
  existing executable controls; or
- forces a contextual judgement into deterministic enforcement.
