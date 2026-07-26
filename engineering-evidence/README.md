# engineering-evidence

`engineering-evidence` preserves factual engineering outcomes and decisions while
their evidence is still accessible. It is intentionally separate from performance
assessment.

## Suggested automations

| Purpose | Suggested cadence | Typical output |
| --- | --- | --- |
| Weekly evidence capture | Near the end of each working week | New outcomes, decisions, reliability work, and unresolved context. |
| Monthly roll-up | Once per month | Deduplicated outcomes with later evidence and reversals applied. |
| Release retrospective preparation | After a release or rollout window | Delivery, risk, migration, rollback, and stakeholder evidence. |
| Incident follow-through | After an incident closes and again after remediation | Resolution evidence and later-observed recurrence reduction. |
| Project close-out | At a milestone or project end | Outputs, outcomes, decisions, collaborators, and remaining risks. |

A daily schedule is usually too noisy unless the work is highly operational and
the output remains private.

## Evidence-based schedule selection

When choosing a trigger, cadence, or collection window, read
[references/scheduling.md](references/scheduling.md). It defines how to derive a
scheduled, lifecycle-triggered, hybrid, event-driven, or on-demand configuration
from evidence half-life, meaningful outcome rate, outcome latency, lifecycle
rhythm, privacy, deduplication quality, source cost, and intended use. Do not merely
copy the table above.

A harness can ask:

```text
Read this skill, its README, and its scheduling reference. Use available workflow
and ledger evidence to recommend when engineering-evidence should run. Provide the
trigger, starting cadence, capture, observation and consolidation windows, output
behaviour, lower-cost alternative, pilot, re-evaluation conditions, and material
unknowns. Do not create or modify an automation.
```

## Thin invocation: weekly capture

```text
Use the engineering-evidence skill.

Inspect accessible work from the current week across repositories, releases,
incidents, decision records, project updates, and attributable collaboration
records.

Capture only evidence-backed outcomes, significant decisions, reliability or risk
reduction, material reviews, and enablement outcomes. Distinguish activity,
output, observed outcome, and expected outcome.

Update prior entries rather than duplicating them. Do not rank people, infer
performance, or send the result. Return a private ledger plus missing context that
would materially improve an entry.
```

## Thin invocation: monthly roll-up

```text
Use the engineering-evidence skill to consolidate the previous month's evidence.

Merge duplicates, apply later-observed outcomes, mark reverted or superseded work,
and preserve attribution uncertainty. Group entries by delivery, reliability and
risk, technical direction, and enablement.

Do not convert volume metrics into impact. Produce a factual roll-up for human
review and list source-coverage limitations.
```

## Schedule configuration checklist

Use the harness's native scheduler and define:

- evidence owner and intended audience;
- time window and project or repository scope;
- accessible sources;
- private ledger or state location;
- deduplication and retention policy;
- sensitivity exclusions;
- maximum entries;
- whether to produce only a ledger or also a draft summary;
- delivery destination and approval requirements.

No particular manifest or serialization format is required.

## Privacy guidance

Keep the default output private. Do not store message bodies, confidential
customer data, personnel information, or secrets when a source link and concise
factual note are sufficient. Human review is required before using the ledger in
performance, promotion, compensation, or external communication.