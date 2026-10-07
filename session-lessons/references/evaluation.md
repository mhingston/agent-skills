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

## SL-E5 — reusable discovery belongs in shared memory

**Evidence**

Three independent sessions establish the same non-obvious behaviour in an
external CLI: process exit zero means the request was accepted, while final
success or failure is reported only in the returned operation status. The
behaviour is source-linked and materially changed troubleshooting. It is useful
across sessions, but it is not a repository policy and does not define how every
agent must behave.

**Expected result**

- the cluster qualifies under the normal recurrence threshold;
- the candidate is recognised as reusable factual/procedural knowledge rather
  than automatically becoming agent guidance;
- the primary destination is `shared memory` when a configured memory target
  exists **and the repository is not the canonical owner that should document
  the knowledge**;
- `destination_detail` names a stable topic/key and preserves the canonical
  source reference;
- the recommendation hands persistence to `memory-capture` and does not claim
  the write was authorised or completed;
- future retrieval through `memory-recall` is an appropriate validation/use path.

## SL-E6 — behavioural invariant does not become memory

**Evidence**

Three independent sessions show agents treating a successful CLI process exit as
proof that a remote operation succeeded. The returned structured status exposes a
stable machine-checkable success predicate that can be validated in the workflow.

**Expected result**

- the correction is treated as agent/workflow behaviour, not merely reusable
  knowledge;
- `correction_class` is `deterministic-control` when the predicate can be
  reliably enforced;
- the primary destination is a tracked work item to add or repair the smallest
  reliable check, not `shared memory`;
- shared memory may preserve supporting tool knowledge separately, but it is not
  allowed to substitute for the behavioural control.

## SL-E7 — transient detail is not promoted

**Evidence**

A single session records the exact temporary deployment job ID and branch-specific
scratch path used to complete one task. Neither value is expected to remain valid
or save meaningful future investigation.

**Expected result**

- the detail does not qualify as durable shared knowledge;
- no shared-memory write is recommended;
- the candidate remains a watchlist item only if some unresolved reusable pattern
  exists; otherwise the disposition is `no-op`.

## SL-E8 — repository-owned knowledge beats shared memory

**Evidence**

Three independent sessions establish a non-obvious service-specific deployment
procedure. The repository already owns deployment guidance in
`docs/deployment.md`, and maintainers expect that document to be the canonical
human-and-agent source for operating the service. The procedure would also be
useful to retrieve from shared memory.

**Expected result**

- the candidate is recognised as durable reusable knowledge;
- the primary destination is `repo docs`, because the repository should
  canonically explain and maintain the procedure;
- shared memory is not selected merely because retrieval would also be useful;
- a later memory entry may reference the canonical documentation only through a
  separately authorised memory workflow, but it is not the owning destination.

## Grading

A candidate change fails this suite if it:

- emits non-canonical correction values such as `deterministic control` or
  `information access`;
- classifies a working executable control with no prose as `absent`;
- classifies an unwired or broken existing control as `absent` rather than
  `partial`;
- routes an objective machine-checkable invariant to prose before inspecting
  existing executable controls;
- uses shared memory as a substitute for a behavioural rule, deterministic
  control, or canonical source;
- routes repository-owned knowledge to shared memory ahead of the canonical repo
  documentation that should own it;
- promotes transient run state into shared memory; or
- forces a contextual judgement into deterministic enforcement.
