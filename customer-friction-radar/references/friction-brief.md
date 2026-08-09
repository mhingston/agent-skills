# Friction Brief Contract

Use this reference for customer-friction briefs.

The brief is an attention document, not a complete archive. If the user requests persistence, durable evidence and theme history may live in a theme registry or other authorised repository.

## Purpose

Surface only customer-friction themes that:

- are new;
- materially strengthened or weakened;
- crossed an evidence/priority threshold;
- have meaningful contradictory evidence;
- require a decision;
- have a bounded next investigation or experiment.

Do not fill the brief with unchanged background themes.

## Header

Include:

- reporting window;
- generated/reviewed time;
- organisation/product scope;
- evidence sources queried;
- sources unavailable;
- observed sample sizes;
- internal systems queried;
- ontology/registry revision or page links where available.

State explicitly:

> Public-review and app-review counts describe the observed sample and are not population prevalence estimates.

## Executive summary

Use 3–6 bullets:

- most important changed friction;
- strongest new corroboration;
- strongest contradiction;
- any urgent safety/vulnerability/regulatory signal;
- one recommended bounded next action.

## Ranked themes

For each material theme:

### CF-### — <canonical label>

**State**
- Lifecycle:
- Evidence strength: weak / moderate / strong
- Decision priority: urgent / high / medium / watch
- Trend: new / rising / stable / falling / disputed / resolved-candidate

**Customer journey**
- Intent:
- Product/service:
- Journey stage:
- Channel:

**Failure mechanism**
One or two sentences describing the mechanism without overstating root cause.

**Observed evidence**
- source/sample summary;
- representative observations;
- dates;
- links/identifiers.

**Internal corroboration**
List independently observed operational/behavioural evidence.

If unavailable, write:

> Internal corroboration not yet available.

Then specify the smallest query that would test the theme.

**Contradicting evidence**
Include meaningful counterevidence. Do not omit it to create a cleaner narrative.

**Hypotheses**
- Leading:
- Alternative:
- What would falsify the leading explanation:

**Why it matters**
Describe member effort/outcome impact. Do not infer financial impact without evidence.

**Next bounded action**
One investigation, instrumentation change or experiment.

**Owner**
Known owner, candidate owner, or `unresolved`.

**Confidence and limitations**
State sampling bias, missing systems, stale evidence or classification uncertainty.

## Cross-theme observations

Only include cross-theme findings that change interpretation, for example:

- multiple themes share the same handoff boundary;
- a product boundary appears across otherwise different journeys;
- positive human interactions consistently mitigate upstream digital/operational friction;
- one operational incident explains an apparent trend.

Do not create a new umbrella theme unless it has a distinct useful mechanism.

## Source coverage

Include a compact table:

| Source | Window | Items/records observed | Material limitations |
| --- | --- | ---: | --- |

For large internal datasets, provide the record/event count or query scope if available.

## Ontology changes

List only changes made during this run:

| Change | Status | Reason | Reviewer required |
| --- | --- | --- | --- |

Do not imply a proposed term is confirmed.

## Decision requests

If human decisions are needed, make them explicit:

- accept/reject/defer a theme split;
- confirm a canonical term;
- approve an experiment;
- identify an owner;
- grant access to missing evidence.

Analysis is not a decision record.

## Recommended next action

End with exactly one preferred bounded action unless the user explicitly asks for multiple options.

Use this shape:

```text
Next action:
Why this one:
Evidence it should produce:
Success condition:
Stop/revisit condition:
Owner:
```

Prefer evidence-producing work over adding more sources, taxonomies or tools.

## Example

```markdown
## CF-012 — Member context is lost during assisted handoff

Evidence strength: moderate
Decision priority: high
Trend: rising within observed sample

Customers attempting to manage a membership digitally report needing to restate
identity and journey context after moving to phone support.

Observed evidence:
- 7 relevant public/app observations in the reporting sample
- 3 support transcripts explicitly reference information already supplied online

Internal corroboration:
- 11.4% of calls with this intent occurred within 30 minutes of a failed/abandoned
  portal session in the sampled period

Competing hypothesis:
The calls may be driven primarily by authentication failure rather than context-loss
during the handoff itself.

Next bounded action:
Label 50 digital-to-call journeys for where context is lost and compare with
authentication telemetry.

Limitations:
The current digital/session join covers only authenticated members.
```
