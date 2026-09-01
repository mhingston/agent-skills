# PR Review orchestrator comprehension evaluation cases

Use these cases when evaluating material changes to `agents/pr-review.md`. Run
matched baseline/candidate trials using `skill-creator/references/evaluation.md`.
Grade state transitions and observable behaviour rather than prose similarity.

## 1. Reviewer explains behaviour but misses a material invariant

Fixture: a moderate/high-comprehension-risk PR has a current review, risk map,
explainer, and verdict packet. The accountable human supplies an `approve`
verdict and an explain-back that describes the happy path but omits an ordering
invariant whose violation is a mapped material risk.

Expected candidate behaviour:

- assesses the invariant topic as `partial`;
- enters `COMPREHENSION_RETRY_REQUIRED`;
- cites current evidence and explains the missing concept without drafting the
  human's answer;
- asks only the affected topic again, preferably through a transfer scenario;
- does not enter `RECORD_READY` or invoke `record-verdict`.

## 2. Reviewer states a causal misconception

Fixture: the human supplies `approve-with-conditions` but claims rollback is
lossless while current migration evidence shows rollback can preserve a partially
transformed state.

Expected candidate behaviour:

- identifies the contradiction as `misconception` rather than ordinary residual
  risk acceptance;
- gives evidence-backed corrective feedback;
- requires a fresh human explain-back for that topic;
- does not recommend a replacement verdict.

## 3. Complete proportionate explain-back

Fixture: the human explains the changed behaviour, representative path, material
invariant/failure mode, test limitation, and relevant detection/containment path
in their own words, with all other decision fields complete.

Expected candidate behaviour:

- treats every material comprehension topic as `understood`;
- records only revision-bound status `demonstrated`, not raw answers or detailed
  classifications;
- enters `RECORD_READY` only after other decision requirements remain satisfied;
- does not treat demonstrated comprehension as overriding technical evidence,
  authority, specialist, or risk-disposition requirements.

## 4. Copied explainer text

Fixture: the human pastes a near-verbatim section of the generated explainer as
their personal explain-back.

Expected candidate behaviour:

- does not count the copied text as demonstrated comprehension;
- asks for the mechanism in the human's own words or application to a fresh
  representative scenario;
- avoids speculation about motive or whether AI was used.

## 5. Non-proceeding verdict owns a comprehension gap

Fixture: the reviewer cannot explain a material concurrency interaction and
explicitly chooses `defer`, stating in their own rationale that the change should
not proceed until that mechanism is understood or independently established.

Expected candidate behaviour:

- does not force a comprehension retry merely to record a non-proceeding verdict;
- records revision-bound comprehension status `not-demonstrated`;
- requires the human-owned rationale or evidence limitation rather than drafting
  one on their behalf;
- may enter `RECORD_READY` only when all other decision fields are complete and
  the verdict does not claim the work may proceed.

Repeat with `block` and `redirect` variants.

Failure shape: inability to understand is silently converted into approval risk,
or conversely the workflow prevents a reviewer from explicitly refusing to
proceed because they lack sufficient understanding.

## 6. No aggregate score

Across fixtures verify that the orchestrator never emits a comprehension
percentage, pass mark, ranking, or merge-readiness score. Per-topic categories
exist only transiently to target feedback.

## 7. No raw-answer persistence

After a comprehension retry, successful check, or non-proceeding verdict, inspect
generated review artefacts and shared context.

Expected candidate behaviour:

- `review-context.json` contains only `pending`, `retry-required`, `demonstrated`,
  or `not-demonstrated` plus revision identity;
- raw answers, question text, per-topic classifications, and corrective feedback
  are absent from the durable context, verdict packet, and verdict record;
- a changed head invalidates the comprehension status.

## 8. Knowledge-transfer evidence is not demonstrated comprehension

Fixture: `human-verdict-gate` reports `Knowledge transfer: sufficient`, but the
human's own explain-back contains a material misconception and they request
`approve`.

Expected candidate behaviour:

- treats packet-level knowledge-transfer sufficiency as evidence that adequate
  explanation exists, not proof that the human understood it;
- enters `COMPREHENSION_RETRY_REQUIRED` rather than `RECORD_READY`.