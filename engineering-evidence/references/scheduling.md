# Scheduling `engineering-evidence`

Use this reference when asked whether, when, or how often to run
`engineering-evidence`. Read the skill and README first, then derive a schedule
from the evidence lifecycle and intended audience. Do not merely copy an example
cadence.

## Choose the trigger type

Prefer:

- **scheduled capture** when useful evidence accumulates continuously and is easy
  to lose or costly to reconstruct later;
- **lifecycle-triggered capture** after a release, incident, migration, milestone,
  project close-out, or other bounded delivery event;
- **hybrid capture** when lightweight periodic collection should be supplemented by
  richer lifecycle reviews;
- **on demand** capture for uncommon or sensitive retrospectives;
- **event-driven collection** only when the event is authoritative and the output
  can remain private and deduplicated.

Do not schedule frequent summaries merely to produce activity reports. The goal is
to preserve verifiable outcomes and decisions while their evidence is available.

## Evidence to inspect

Use available evidence about:

- how quickly source evidence, decision rationale, or stakeholder context becomes
  difficult to reconstruct;
- the number of meaningful outcomes and decisions produced in a normal work cycle;
- release, incident, migration, and milestone frequency;
- how long expected outcomes take to become observable;
- how often previous runs added new evidence versus repeating unchanged activity;
- sensitivity, privacy, retention, and intended audience;
- the availability and quality of prior-ledger deduplication;
- source freshness, runtime, and collection cost;
- when the resulting ledger will be reviewed or used.

State which sources and outcome evidence were unavailable. Do not increase
frequency to compensate for weak attribution or missing outcome evidence.

## Choose collection and consolidation windows

Separate:

- **capture window** — recent work whose evidence should be preserved now;
- **observation window** — older entries whose expected outcomes may now be
  verifiable;
- **consolidation window** — the period over which duplicates, reversals, and
  supersession should be reconciled.

A frequent capture run may remain private and incremental, while a less frequent
roll-up can consolidate outcomes for human review. Avoid retaining sensitive source
content when a concise note and source route are sufficient.

## Choose a starting cadence

Balance:

1. **Evidence half-life** — how quickly facts, rationale, and attribution become
   difficult to recover.
2. **Meaningful evidence rate** — how often the workflow produces outcomes worth
   recording.
3. **Outcome latency** — how long later-observed results take to emerge.
4. **Lifecycle rhythm** — releases, incidents, projects, and review cycles.
5. **Privacy and interruption cost** — whether output remains private or is prepared
   for a wider audience.
6. **Deduplication quality** — whether previous entries can be updated rather than
   repeated.

Prefer the lowest cadence that preserves evidence before it decays. A daily run is
usually unjustified unless the environment is highly operational, evidence is
short-lived, and the output remains private and quiet.

## Common starting hypotheses

Treat these as pilot candidates, not defaults:

- private weekly capture near the end of the working week;
- monthly consolidation with later-observed outcomes and reversals applied;
- lifecycle-triggered capture after a release or rollout window;
- one capture after an incident closes and another after remediation evidence is
  expected;
- milestone or project close-out capture;
- hybrid weekly collection plus lifecycle-triggered enrichment.

## Recommend a pilot

Return:

```text
Recommended trigger:
[scheduled, lifecycle-triggered, hybrid, event-driven, or on demand]

Starting cadence:
[human-readable recommendation]

Why:
[evidence about evidence half-life, meaningful evidence rate, and lifecycle rhythm]

Windows:
- Capture:
- Outcome observation:
- Consolidation:

Output behaviour:
[private ledger, changed entries only, roll-up, or draft for human review]

Alternative:
[a lower-cost or less frequent configuration]

Pilot:
[minimum captures, lifecycle events, or representative period]

Increase frequency when:
[evidence-backed conditions]

Decrease or pause when:
[evidence-backed conditions]

Unknowns:
[missing evidence that could materially change the recommendation]
```

During the pilot, record new useful entries, duplicates, missing context, later
outcome updates, sensitive-data concerns, source coverage, runtime, and whether the
ledger was actually useful. Do not publish, send, or reuse the ledger for personnel
decisions without separate human review and approval.