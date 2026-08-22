# Critic Contract

A Gauntlet Loop critic is an independent evaluator, not a second implementer.

Its purpose is to falsify the claim that a candidate satisfies a defined slice of
the acceptance contract.

## Inputs

Provide:

- exact candidate identity;
- applicable `R#` criteria;
- authoritative source excerpts or references required to interpret them;
- candidate artifact or a reliable way to inspect it;
- relevant deterministic results;
- comparison artifacts where required;
- known evaluator limitations.

Do not provide unnecessary producer reasoning, previous critic verdicts, attempt
count, or statements such as "this should now be fixed." These can anchor the
evaluation.

## Behaviour

For each assigned criterion:

1. inspect the actual candidate;
2. seek concrete counterexamples;
3. compare observations with the criterion;
4. attempt to falsify apparent success;
5. return `pass`, `fail`, or `unverified`;
6. cite the evidence that justifies that result.

Do not:

- edit the candidate;
- invent additional requirements;
- reward effort or improvement;
- lower the bar because previous attempts failed;
- pass a criterion because no obvious problem was noticed;
- report a numerical score unless the acceptance contract defines one;
- infer unavailable runtime, visual, behavioural, or external evidence.

## Result contract

Return:

```yaml
candidate: <exact identity>

criteria:
  - id: R1
    status: pass | fail | unverified
    evidence:
      - <specific observation>
    gap: <required only for fail>
    confirmation_needed: <required only for unverified>

limitations:
  - <material evaluator limitation>
```

For `fail`, describe the observable gap rather than prescribing a detailed
implementation unless the contract explicitly requires a design direction.

Good:

> R4 fail — at 375px viewport width the primary action is clipped below the card
> and cannot be reached without horizontal scrolling.

Weak:

> The mobile UI doesn't feel polished enough.

## Adversarial review

"Adversarial" means attempting to disprove compliance.

Useful techniques include:

- boundary cases;
- counterexamples;
- alternate user paths;
- malformed inputs;
- changed viewport or environment;
- failure and recovery paths;
- comparison against source requirements;
- checking exact values independently;
- looking for contradictions between criteria;
- inspecting places where integration commonly invalidates local assumptions.

It does not mean being theatrical, hostile, or demanding impossible perfection.

## Comparative evaluation

When references are part of the contract, judge only the defined comparison
dimensions.

For A/B comparison:

- use equivalent inputs and states where possible;
- label candidates neutrally;
- randomize ordering where the harness supports it;
- withhold identity and provenance if genuine blinding is required;
- record environmental differences.

Only describe the evaluation as `blind` when candidate identity was actually
hidden.

If the evaluator cannot inspect both candidates directly, return `unverified`
rather than simulating the comparison from descriptions.

## Freshness and independence

Prefer a fresh critic context for each materially new candidate.

Do not show the critic previous verdicts unless evaluating whether a specific
reported defect was corrected and the contract requires that history.

Record the available execution mode:

- `fresh-independent-context`;
- `fresh-context-shared-model`;
- `single-context-separated-pass`;
- `human-review`;
- another accurately described mode.

Parallel execution alone does not prove independence.

## Passing

A critic may pass a criterion only when the available candidate evidence
positively supports it.

An empty list of complaints is not itself evidence of a pass.

When evidence is unavailable or the evaluator lacks a necessary capability, use
`unverified`.

The critic judges the candidate. The Gauntlet Loop coordinator decides whether
the combined evidence permits the workflow to advance.
