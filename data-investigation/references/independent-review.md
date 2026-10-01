# Independent analytical review

Use this review when a claim is consequential, causality is asserted, the
investigation adaptively searched many alternatives, a final holdout is available,
or the user explicitly requests independent verification.

## Independence contract

Name the investigator, reviewer, candidate identity, data snapshot, code revision,
and review question. Independence is about access and evidence, not merely a new
chat session.

For a claim-focused review, give the reviewer:

- the original and revised analytical brief;
- authoritative data notes and approved data access;
- the frozen final code/artefact and environment;
- declared methods, assumptions, metrics, diagnostics, and slices;
- the final claim and stated limitations;
- only the prior-path information needed to reproduce or audit the result.

Withhold the investigator's exploratory narrative and discarded attempts when
they would anchor a supposedly fresh challenge. Preserve the full trail separately
for process audit. Do not hide failed attempts when the review question is whether
adaptive search or selective reporting compromised the conclusion.

A reviewer who can read the investigator's entire workspace, Git history, hidden
holdout results, or prior critique is not independent for claims affected by that
information. Report the limitation rather than using the label loosely.

## Review procedure

1. Restate the exact claim, population, intended use, and evidence strength.
2. Reconstruct the data population and decisive transformations from stable
   sources.
3. Rerun the minimum analysis and diagnostics capable of supporting or falsifying
   the claim.
4. Test the strongest credible alternative explanation or failure mode.
5. Inspect leakage, time ordering, grouping, preprocessing, exclusions, missing
   data, and slice behaviour where relevant.
6. Challenge causal identification, counterfactual construction, and robustness
   when causal language is used.
7. Compare the reported conclusion with what the evidence actually establishes.
8. Record objections with executable or inspectable support; do not substitute
   generic scepticism for review evidence.

## Final confirmation

If a protected or untouched final set exists:

- freeze the selected candidate, thresholds, exclusions, metrics, and evaluator;
- run the final evaluation once in the independently controlled environment;
- report required slices and failure categories, not only the headline metric;
- do not tune after seeing the result and still describe it as final confirmation;
- if the result triggers another change, move it into development evidence and
  require fresh confirmation before making an unbiased promotion claim.

Version control or a separate directory alone is not an access boundary.

## Review dispositions

Return one disposition:

- `Supported` — decisive checks reproduce and no material objection survives;
- `Qualified` — the core result survives but use must be narrowed;
- `Inconclusive` — evidence cannot distinguish the claim from a material
  alternative;
- `Contradicted` — reproduced evidence conflicts with the claim;
- `Blocked` — required data, environment, meaning, or access is unavailable.

For each objection record the affected claim, evidence, consequence, and smallest
resolving action. The accountable decision owner determines whether the reviewed
evidence is sufficient for operational use.
