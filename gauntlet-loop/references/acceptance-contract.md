# Acceptance Contract

Use this reference when success cannot be represented by a few obvious executable
checks.

The acceptance contract is the Gauntlet Loop's answer key. It must exist
independently of the candidate being evaluated.

## Sources

Record each material source with:

- identifier;
- type;
- locator;
- authority;
- relevant version, revision, or freshness signal;
- scope;
- conflicts or limitations.

Do not silently reconcile conflicting authoritative sources.

## Criteria

Assign stable `R#` identifiers.

Use the smallest useful representation:

| ID | Requirement | Priority | Source | Verification | Pass evidence | Fail evidence |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | ... | mandatory | ... | deterministic | ... | ... |
| R2 | ... | mandatory | ... | semantic | ... | ... |
| R3 | ... | advisory | ... | comparative | ... | ... |

### Verification types

**Deterministic**

Use when an executable observation can establish the property.

Examples include tests, schema checks, exact values, compilation, static analysis,
invariant checking, and benchmark thresholds.

**Semantic**

Use when interpretation is genuinely required.

Examples include clarity, coherence, maintainability, usefulness, and visual
polish.

Define the observable characteristics being judged rather than saying only
"high quality."

**Comparative**

Use when the contract intentionally uses one or more reference artifacts.

Specify:

- comparison target;
- scenarios or states to compare;
- relevant dimensions;
- what does not need to match;
- how the comparison will be made;
- whether blinding is actually possible.

**Human-owned**

Use when acceptance requires accountable human judgement.

The agent may prepare evidence but must not manufacture the human decision.

## Reference-derived quality bars

A reference artifact should answer:

> Better according to what observable property?

Avoid a single criterion such as:

> As good as Product X.

Prefer criteria such as:

- loading feedback is at least as immediate and legible as the supplied reference;
- animation remains smooth under the agreed scenario;
- information hierarchy is no less clear than references A and B;
- the target workflow requires no more interaction steps than the approved
  reference flow;
- output quality on the supplied evaluation set meets or exceeds the recorded
  baseline.

The reference informs the criterion. It does not replace the criterion.

## Subjective criteria

For a subjective requirement, define:

- evaluation context;
- dimensions;
- observable failure examples;
- references where useful;
- minimum acceptable condition;
- evaluator limitations.

Prefer multiple concrete dimensions over one overall 1-10 score.

For visual work, dimensions might include:

- composition;
- hierarchy;
- spacing;
- typography;
- material and lighting consistency;
- animation;
- interaction feedback;
- clipping or rendering defects;
- responsive behaviour;
- reference fidelity.

For prose, they might include:

- factual support;
- completeness;
- logical coherence;
- audience fit;
- concision;
- terminology consistency.

## Traceability

Every mandatory criterion must map to at least one verification route.

Every work item must state which criteria it contributes to.

The final integrated candidate is checked against the complete mandatory set,
regardless of what passed locally.

## Changing the contract

A producer discovering new evidence may propose a contract change, but it may not
silently alter the bar against which its own candidate is judged.

When new evidence materially changes a requirement:

1. stop affected execution;
2. record the new evidence;
3. obtain the required planning or accountable decision;
4. version the acceptance contract;
5. invalidate affected prior evidence;
6. replan dependent work before continuing.

Never weaken a criterion merely because repeated attempts failed it.
