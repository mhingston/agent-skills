# Evidence Discipline

Use this reference whenever an agent reports on consequential work or prepares
information for a human decision.

## Epistemic labels

Use these labels consistently:

- **Observed** — directly supported by inspected code, diff, tests, command
  output, logs, traces, screenshots, approved requirements, or documentation.
- **Inferred** — a reasonable conclusion drawn from observations. Identify the
  supporting observations and label the conclusion when it affects a decision.
- **Unknown** — not established by the available evidence. Convert it into a
  question, validation step, condition, or explicit residual risk.

Do not present inferred intent as fact. Do not treat absence of evidence as
positive evidence.

## Claim-to-evidence map

For each material claim, capture:

| Claim | Status | Evidence | Result | Limitation |
| --- | --- | --- | --- | --- |
| Behaviour, safety, compatibility, or readiness claim | Observed, inferred, or unknown | Inspectable source, command, test, trace, review, or artefact | Pass, fail, partial, conflicting, not run, or unknown | What this evidence does not establish |

A list of passing tests is not enough. Explain which risks each test covers and
which important behaviours remain untested.

## Evidence independence

Identify when implementation and evidence share the same assumptions. Examples:

- the same agent wrote both the code and tests;
- generated tests reproduce implementation details rather than requirements;
- a model critique relies only on the original model's summary;
- a fixture encodes the same mistaken interpretation as the implementation;
- a benchmark excludes the difficult or failing scenarios.

Additional model output may strengthen investigation, but it does not create
independent human accountability.

## Assumptions and unknowns

Separate:

- verified assumptions;
- unverified assumptions;
- inherited assumptions from existing code or documentation;
- conflicts between evidence sources;
- unknowns that block a decision;
- unknowns that can be accepted as residual risk.

Prefer `unknown` over unsupported reassurance.

## Risk and operations

For consequential changes, report:

- credible failure modes;
- affected users, systems, data, or contracts;
- blast radius and irreversibility;
- detection signals and expected alerting;
- containment and rollback mechanisms;
- migration or compatibility concerns;
- security, privacy, consistency, concurrency, ordering, and performance risks;
- residual risk after controls.

Do not claim that work is safe, correct, production-ready, or fully tested unless
an authorised human or policy has made that determination from sufficient
evidence.

## Adversarial questions

Ask, where relevant:

- What is the strongest technical case against proceeding?
- What could pass the current tests and still be wrong?
- Which requirement may have been misunderstood?
- Has complexity or coupling moved somewhere less visible?
- What important boundary received the least attention?
- What evidence would change the current assessment?
- What would a sceptical domain expert ask next?

Prioritise plausible and consequential objections rather than inventing filler.

## Freshness

Evidence and verdicts are revision-specific.

- Record the analysed commit or PR head SHA.
- Recheck after material changes.
- Mark prior evidence or verdicts stale when the target revision changes.
- Do not silently carry approval across a force-push, rebase, conflict
  resolution, or substantial review update.
