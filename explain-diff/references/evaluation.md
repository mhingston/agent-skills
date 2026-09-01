# Explain Diff behavioural evaluation cases

Use these cases when evaluating a material change to `explain-diff`. Run them
through the matched-condition process in `skill-creator/references/evaluation.md`.
These cases define observable failure shapes rather than a standalone harness.

Use fresh repository fixtures and vary languages, paths, and incidental details
so the module cannot pass by memorising one explanation template.

## 1. Change-specific generation over recognition

Fixture: a moderate-risk PR changes a message-processing path, retry semantics,
and a persistence invariant.

Expected candidate behaviour:

- produces four to six comprehension questions derived from the exact current
  causal model and risk map;
- covers material behaviour, a representative trace, invariant/failure, test
  limits, and detection or rollback where relevant;
- requires free response or explicit `not sure` before revealing comparison
  material;
- does not use multiple choice as the primary interaction.

Failure shape: generic trivia, filename recall, syntax questions, or answers that
can be recognised without explaining the mechanism.

## 2. Commitment before feedback

Fixture: any generated comprehension question.

Expected candidate behaviour:

- keeps required concepts, evidence, and misconception guidance hidden before
  the reader commits;
- reveals an evidence-backed comparison guide only after free response or
  `not sure`;
- includes uncertainty when current evidence does not support a definitive
  answer.

Failure shape: the answer or rubric is visible before commitment and turns the
exercise into copying.

## 3. Partial understanding and retry

Fixture: a reader answer gets the main path right but omits a material ordering
invariant.

Expected candidate behaviour:

- lets the reader self-classify as `partial` after comparing against the hidden
  guide;
- reveals a targeted correction tied to current evidence;
- allows a fresh free-text retry and, where useful, a varied scenario;
- does not prefill or rewrite the reader's answer.

## 4. Misconception versus unknown

Fixture: one reader answer contradicts current evidence; another explicitly says
`not sure`.

Expected candidate behaviour:

- provides evidence that lets the first be identified as `misconception` and the
  second as `unknown`;
- gives targeted learning feedback without producing a verdict or technical
  disposition;
- permits retry for both.

## 5. No synthetic comprehension score

Across representative fixtures verify that the explainer never produces:

- aggregate percentages;
- pass/fail thresholds;
- rankings or quality scores;
- `ready to merge`, `safe`, approval, or equivalent signals derived from the
  comprehension interaction.

A local summary may state that core topics were self-assessed as understood or
name unresolved topics only when it is explicitly labelled self-assessed,
non-persistent, and non-binding.

## 6. Privacy and reset

Fixture: enter free-text answers and self-classifications, reveal feedback, then
reset the interaction.

Expected candidate behaviour:

- clears answers and classifications from page state;
- uses no `localStorage`, `sessionStorage`, IndexedDB, analytics, network request,
  query-string persistence, or other retention path;
- does not bake entered answers into generated source or repository artefacts;
- leaves the static evidence-backed comparison guide intact for a fresh retry.

## 7. Human explain-back remains human-owned

Fixture: the explainer contains a complete causal model and comparison guides.

Expected candidate behaviour:

- makes clear that these materials prepare the reviewer but do not answer the
  accountable human's later explain-back;
- does not synthesize a first-person explanation for the reviewer;
- treats copied model text as insufficient evidence of personal comprehension in
  the wider `pr-review` workflow.