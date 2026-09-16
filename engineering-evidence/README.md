# engineering-evidence

`engineering-evidence` proactively recovers and substantiates evidence of
engineering and business impact attributable to the user while that evidence is
still accessible. It is an evidence-recovery skill, not an activity report or
performance-assessment tool.

The skill can search across whatever relevant read-only sources a harness exposes,
correlate contributions with downstream outcomes, preserve collaborative
attribution, and separate demonstrated impact from plausible or still-emerging
impact.

Typical questions include:

- What meaningful impact have I had over the last week, month, quarter, project,
  or review period?
- Which team or project outcomes can my contribution reasonably be linked to?
- What measurable changes followed work I contributed to?
- What initiatives, decisions, reviews, mentoring, technical direction,
  unblocking, or cross-team work might otherwise be missed?
- What stakeholder recognition exists, and what work or outcome was it tied to?
- Which promising impact claims still need better evidence?
- What impact is emerging but has not yet had enough time to measure?

## Evidence model

The skill distinguishes four evidence strengths:

| Strength | Meaning |
| --- | --- |
| Observed impact | The outcome occurred and the user's contribution can reasonably be linked to it. |
| Supported contribution | A wider outcome occurred and the user materially contributed, but exclusive causality is not established. |
| Expected impact | Work shipped or changed behaviour, but the intended downstream result has not had enough time or measurement to observe. |
| Candidate impact | Value is plausible, but material context, attribution, measurement, or validation is still missing. |

Activity counts can be useful discovery signals, but they are not impact by
themselves. The skill explicitly avoids treating PR count, commits, story points,
velocity, review count, or praise volume as individual performance measures.

## Sources

The skill is harness-agnostic. Useful evidence may come from:

- GitHub or GitLab;
- Jira, Linear, or Azure DevOps;
- Slack, Teams, or email;
- incident and observability systems;
- ADRs, proposals, and documentation;
- product and business analytics.

Not every source needs to be connected. Missing sources are reported as coverage
limitations rather than interpreted as evidence that no contribution occurred.

## Thin invocation: impact discovery

```text
Use the engineering-evidence skill.

Review my work and attributable outcomes over the last month using whatever
relevant read-only sources are available. Look beyond PR activity for decisions,
reviews, mentoring, technical direction, cross-team unblocking, risk prevention,
simplification, and initiatives I originated or materially advanced.

Correlate evidence across systems where it strengthens or falsifies a claim.
Separate observed impact, supported contribution, expected impact, and candidate
impact. Preserve collaborators and attribution uncertainty. Do not infer
performance or manufacture value from activity counts.

Return the strongest evidenced impacts, additional contributions, stakeholder
signals, emerging impact, missing evidence, and source-coverage limitations.
```

## Thin invocation: review-period evidence

```text
Use the engineering-evidence skill to reconstruct evidence from this review
period.

Search accessible engineering, delivery, collaboration, incident,
documentation, and analytics sources. Prefer meaningful outcome evidence over
activity volume. For quantitative claims, compare suitable periods or populations
where possible and consider competing explanations before attributing a change to
my work.

Produce a factual evidence ledger suitable for later performance-review or
promotion preparation, but do not rate my performance, recommend promotion, or
claim exclusive credit for collaborative outcomes.
```

## Suggested automations

| Purpose | Suggested cadence | Typical output |
| --- | --- | --- |
| Weekly evidence capture | Near the end of each working week | New outcomes, contributions, decisions, recognition, and unresolved context. |
| Monthly roll-up | Once per month | Deduplicated impacts with later evidence, reversals, and emerging outcomes applied. |
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
