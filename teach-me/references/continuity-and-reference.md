# Learning Continuity

Preserve only context that changes a future teaching decision. Receipts remain the canonical record of learner performance; the structures here guide scope and interpretation.

## Mission capsule

Use a mission capsule when learning will span sessions, the stated topic admits several useful directions, or constraints affect sequencing. Keep it compact:

- `why`: the real-world reason for learning;
- `success`: observable capabilities that would satisfy the mission;
- `constraints`: time, access, budget, source, or delivery constraints;
- `out_of_scope`: tempting adjacent goals intentionally deferred.

Do not delay a clear first lesson to complete the capsule. Ask only for fields that change the next move. Keep one capsule per topic arc and confirm with the learner before revising it. When the mission changes, revise the topic and add a `mission-shift` milestone; do not silently leave stale context steering later sessions.

## Decision-grade milestones

Add a milestone only for:

1. demonstrated non-trivial understanding that raises the future starting point;
2. prior knowledge the learner reports, including the depth claimed;
3. a corrected misconception likely to affect related concepts;
4. a mission shift that changes scope or sequencing.

Do not record material merely covered, routine activity, or every successful receipt. Link demonstrated understanding and corrected misconceptions to settled receipts, and keep the summary to the decision-relevant insight plus its implication. Learner-reported prior knowledge is navigation context, not mastery evidence, until tested.

When a later insight replaces an earlier one, create a new milestone whose `supersedes` field names the old milestone. Keep the old record so future coaching can distinguish growth from inconsistency.

## Optional source ledger

Use a source ledger only for multi-session, contested, fast-moving, safety-sensitive, or source-constrained topics. Each source needs:

- a short title;
- a URL, citation, or local path in `location`;
- one sentence in `use_for` explaining when it is authoritative or useful.

When maintaining the ledger, record unresolved `source_gaps` explicitly; in stateless or one-off lessons, describe consequential gaps in the lesson without persisting anything. Prefer primary and high-trust sources, prune sources shown to be shallow or wrong, and keep the ledger small enough to guide decisions. A source ledger supports teaching; reading or collecting it is not learner evidence.

### Claim-level provenance when it matters

For a research paper, changing specification, contested finding, or other source-sensitive claim, make `use_for` precise enough to identify **which claim** the source supports and, when available, the relevant section, page, figure, date, or version. Keep the existing `title`, `location`, and `use_for` schema; do not add required fields or source entries merely for completeness.

In the lesson itself, distinguish **what the retrieved material establishes**, **what its authors report or infer**, and **what the tutor infers or proposes**. A paper's reported metric is not independently verified just because its paper was retrieved. If only an abstract, summary, or outdated version is available, limit teaching claims to that coverage, name the gap, and avoid inventing missing methods, numeric results, quotations, or citations. Source provenance improves epistemic calibration; it neither certifies a claim nor supplies learner mastery evidence.
