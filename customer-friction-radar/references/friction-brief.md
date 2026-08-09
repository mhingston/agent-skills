# Friction Brief Contract

Use this reference for recurring or one-off customer-friction briefs.

The purpose of the brief is to surface decision-relevant change, not to reproduce
every review or build a sentiment dashboard.

## Required header

Include:

- reporting window;
- products or journeys in scope;
- sources reviewed;
- observed sample size by source when available;
- internal evidence sources queried;
- important source-access or comparability gaps;
- link to the Confluence Customer Friction Radar root or theme registry when
  available.

## Executive summary

State at most five findings that materially changed or require attention.

For each finding distinguish:

- observed evidence;
- interpretation;
- internal corroboration or contradiction;
- decision relevance.

Do not use generic claims such as "customers are frustrated" when a specific
failure mechanism is known.

## Ranked theme table

Use columns equivalent to:

| Theme | Change | Evidence | Journey | Internal corroboration | Strength | Priority | Next test |
| --- | --- | --- | --- | --- | --- | --- | --- |

`Change` should be one of:

- new;
- rising;
- stable but newly corroborated;
- weakening;
- contradicted;
- resolved candidate;
- no comparable baseline.

Only rank themes that changed, became materially better evidenced, or need a
decision. Stable background themes may be listed separately as `watch` when useful.

## Theme detail

For every material theme include:

### `<theme_id> <canonical label>`

**Customer intent**  
What the customer was trying to accomplish.

**Observed failure mechanism**  
Describe the smallest reusable customer-effort mechanism without asserting an
unverified technical root cause.

**Affected journey**  
Product or service, stage, and channel.

**External evidence**  
State the observed count within the reviewed sample and provide representative,
attributable evidence. Preserve source dates and links or identifiers.

**Trend**  
State only relative to a comparable defined window. If source coverage changed,
use `insufficient-comparable-data`.

**Internal evidence**  
List corroborating, contradicting, or missing operational evidence. Include metric
definitions and denominators when quantitative claims are used.

**Leading hypothesis**  
State the explanation and assumptions.

**Competing hypothesis**  
Include a credible alternative when the issue is causal or diagnostic.

**Evidence strength**  
`weak`, `moderate`, or `strong`, with one-sentence rationale.

**Decision priority**  
`urgent`, `high`, `medium`, or `watch`, with one-sentence rationale.

**Smallest next test**  
Recommend one bounded investigation, instrumentation change, or experiment that
could change the decision state.

**Owner**  
Name the journey, capability, or team owner only when evidence supports it. Do not
assign fault.

**Limitations**  
Call out sample bias, inaccessible sources, stale data, uncertain classification,
or changed source coverage.

## Positive patterns

Include positive evidence only when it helps explain what works and can therefore
inform an intervention.

Prefer contrasts such as:

- the normal path works well while exceptional states fail;
- human handling is strong while cross-channel context is weak;
- status communication is praised when ETA and next action are explicit;
- one journey version has lower effort than another.

Do not create a generic praise leaderboard unless requested.

## Ontology changes

When Confluence was updated, include a compact change log:

- themes created, split, superseded, downgraded, or resolved;
- controlled-vocabulary terms proposed or confirmed;
- aliases added;
- material relationship changes;
- pages updated;
- changes requiring human review.

Do not bury ontology changes inside narrative analysis.

## Recommended action

End with exactly one primary recommended next action unless the user explicitly
asks for a backlog.

The action should identify:

- theme or question;
- evidence it resolves;
- owner or collaborator if known;
- success or falsification measure;
- explicit stop condition.

Examples:

- Compare digitally reported breakdowns with assisted contacts within 30 minutes
  for four weeks; stop if the leakage rate is too small or no common failure state
  emerges.
- Label 100 relevant transcripts for repeated-information friction and compare
  with available digital context; stop if inter-rater agreement is too low to
  support automation.
- Instrument the transition from customer submission to downstream acknowledgement
  and observe failure/latency distribution before changing the user experience.

Prefer evidence from one bounded vertical slice over expanding source coverage or
adding more classification dimensions.

## Source appendix

List the sources actually inspected during the reporting window. For each source,
record:

- source;
- time range;
- observed item count when known;
- access method;
- coverage limitations;
- retrieval date.

If a material source could not be accessed, state that explicitly instead of
implying full coverage.
