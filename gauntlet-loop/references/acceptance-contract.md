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

### Objective integrity and proxy resistance

Before freezing a consequential criterion, ask whether a candidate could satisfy
its literal wording while materially failing the underlying outcome. Treat this as
a contract-quality check, not as permission for the evaluator to invent new
requirements later.

For metrics, scores, thresholds, counts, latency targets, benchmark results, or
other indirect success signals, record when material:

- **Objective** — the user or system outcome the signal is intended to protect;
- **Signal** — the observable proxy used to help judge that outcome;
- **Guardrails** — invariants, non-goals, quality bounds, or unacceptable trade-offs
  that must remain true even when the signal improves;
- **Gaming case** — at least one credible way to improve the signal while leaving
  the objective unchanged or making it worse;
- **Independent evidence** — an observation capable of detecting that apparent
  success is only proxy optimization.

Do not add ceremony when a criterion directly expresses the observable outcome and
there is no credible proxy gap. Do challenge aggregate scores and optimization
targets whose components can trade off in ways that hide a material regression.

A metric is evidence, not automatically the objective. Do not declare success
solely because a proxy improves when the contract also contains outcome evidence,
guardrails, or invariants that contradict that conclusion.

Examples:

- reducing average handling time is not sufficient if required customer outcomes
  or quality constraints regress;
- increasing test count is not sufficient if the added tests cannot detect the
  behaviour the contract cares about;
- improving a benchmark score is not sufficient if the candidate exploits a
  fixture artifact or violates an explicit resource or correctness bound;
- maximizing task-completion count is not sufficient if tasks are split, skipped,
  or reclassified to inflate the count without improving the protected outcome.

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

When a material criterion uses a proxy signal, its objective and applicable
guardrails must remain traceable through verification rather than disappearing
behind the proxy value.

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
