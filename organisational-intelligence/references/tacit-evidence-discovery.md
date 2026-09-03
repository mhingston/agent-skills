# Tacit evidence discovery

Use this reference when the organisational question depends on knowledge that is
unlikely to exist as a clean canonical statement. The goal is to find evidence of
how the organisation actually behaves without promoting conversational residue
into authority merely because it is discoverable.

This is a retrieval technique inside `organisational-intelligence`, not a separate
knowledge-management workflow. The decision, evidence map, claim-specific source
authority, ambiguity handling, and human judgement rules in `SKILL.md` still own
the investigation.

## Search for traces, not just answers

Direct topic searches favour formal artefacts and already-known vocabulary. When
tacit knowledge is material, also search for traces left by decisions, exceptions,
workarounds, and repeated confusion.

Use only the patterns relevant to the current question:

| Trace | What it may reveal | Follow-up |
| --- | --- | --- |
| Repeated question | Missing or weak shared understanding | Compare who asked, when, and whether answers agree. |
| Exception | De-facto rules that differ from documented policy | Check whether the supposed exception recurs and what authority permitted it. |
| Reversal | A decision that changed or was undone | Reconstruct the sequence, dates, trigger, and whether the original rationale still applies. |
| Named expert | Knowledge or operational dependency concentrated in a person | Follow the person's attributable contributions; do not treat reputation or mention volume as authority. |
| Workaround | Undocumented process carrying real operational load | Find the originating constraint, affected systems, age, and whether the workaround became routine. |
| Warning | Operational scar tissue from an incident or failed attempt | Find the underlying incident, review, ticket, or decision and verify whether the lesson remains current. |
| Stale artefact | Documented intent that no longer matches observed behaviour | Compare the artefact revision with newer authoritative or operational evidence. |

Generate queries from conversational and operational language rather than only
formal domain terms. Search engines differ, so adapt the phrasing to the source
instead of assuming one query syntax.

## Follow evidence handles across systems

A first pass should teach you vocabulary that was unavailable at the start. Re-run
bounded searches using newly discovered:

- acronyms, project names, product nicknames, and internal terminology;
- people who made, implemented, challenged, or repeatedly explained a decision;
- exact ticket, pull-request, incident, customer, case, or document identifiers;
- dates, launches, incidents, migrations, or recurring events that bound the
  likely decision window.

Prefer exact cross-system handles when available. A ticket ID mentioned in chat or
a pull request referenced by an incident gives a stronger navigation path than
broad semantic similarity alone.

Do not expand into unrelated organisational discovery merely because new terms or
people appear. Every widening pass must remain tied to the framed decision or a
material competing explanation.

## Treat search results as leads

Before promoting a trace to a finding:

1. Open the underlying artefact, thread, review, ticket, transcript, or record when
   available; snippets and summaries are navigation aids.
2. Follow a conversation or review far enough to detect later correction,
   disagreement, reversal, or supersession.
3. Record the date or revision and test whether the evidence applies to the period
   in question.
4. Search for corroborating or contradictory evidence using a materially different
   phrasing, source type, or exact identifier when the claim is consequential.
5. Apply claim-specific authority from the evidence map. Conversational evidence
   may establish observed practice or rationale without establishing formal policy.

When an artefact is materially discredited for a claim class, scope, or period,
withdraw or lower its authority for that scope. Do not use adjacent unverified
claims from the same artefact as convenient gap-fillers merely because nothing has
contradicted them yet.

## Preserve search-state provenance

Missing evidence has different meanings. Keep these states distinct:

- **evidence found** — attributable evidence was retrieved and inspected;
- **searched, no evidence** — the relevant reachable source was searched within a
  stated scope but nothing material was found;
- **not searched** — the source exists or is plausible but was outside the chosen
  scope or unavailable to the current investigation;
- **inaccessible** — the source should be searched for the decision but access is
  missing or blocked.

Never turn `not searched` or `inaccessible` into `searched, no evidence`. Negative
evidence is useful only when the search scope makes its absence meaningful.

## Stop when discovery saturates

Retrieval should converge. Stop widening a tacit-evidence hunt when either the
main decision-oriented stop condition is met or two consecutive bounded passes
produce no material new:

- vocabulary or identifiers;
- relevant people or source types;
- dates or decision events;
- contradictions, reversals, exceptions, or competing explanations.

At that point, report the remaining uncertainty as a gap and state the smallest
source, experiment, or accountable human question that could resolve it. Do not
keep rephrasing searches to manufacture a sense of completeness.

## Design provenance

The trace-oriented retrieval idea was informed by
[`TenexTony/tribal-knowledge`](https://github.com/TenexTony/tribal-knowledge),
particularly its emphasis on discovering undocumented knowledge through repeated
questions, exceptions, reversals, workarounds, warnings, people, and stale
artefacts. This adaptation keeps `organisational-intelligence`'s existing
claim-specific authority model, bounded decision framing, and ambiguity rules
rather than adopting a parallel workflow.
