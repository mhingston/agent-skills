# Author comprehension checkpoint

Use this reference after `create-pr` classifies comprehension risk as `moderate`
or `high`, or when repository policy explicitly requires an author ownership
checkpoint. The checkpoint is revision-bound decision support, not technical
approval.

A polished implementation, plan, review, or PR description produced by an agent
is not evidence that the accountable human author understands the change.
Do not draft, paraphrase, prefill, or improve the human's explain-back. Do not
persist raw answers or per-topic classifications, and do not produce aggregate
scores, percentages, rankings, or merge-readiness signals.

## Prompt construction

When `AUTHOR_EXPLAIN_BACK` is absent, return `AUTHOR_COMPREHENSION_REQUIRED` with
four to six concise prompts covering the material subset of:

- what observable behaviour changed, without relying on filenames;
- one representative runtime or data-flow trace;
- the key invariant and a credible failure mechanism;
- important behaviour not established by current tests;
- first useful production signal and containment or rollback;
- principal trade-off, residual risk, or next plausible requirement.

Choose prompts from the actual change, current technical evidence, blast radius,
and risk map. Do not add trivia or ask the author to memorise implementation
details. Do not provide suggested answers.

## Assessing the explain-back

Compare the human response against the exact current diff, verified intent,
current technical evidence, and risk map. Classify each material topic
transiently as exactly one of:

- `understood` — the material mechanism and consequence are represented;
- `partial` — directionally correct but a material concept is missing;
- `misconception` — conflicts with current evidence or causal behaviour;
- `unknown` — the response does not establish confident understanding.

Cite the evidence supporting the assessment. A verbatim or near-verbatim copy of
an agent-authored plan, implementation summary, review, or PR description is not
comprehension evidence; ask the human to explain the mechanism in their own words
or apply it to a representative scenario.

## Feedback and retry

If any material topic is `partial`, `misconception`, or `unknown`:

1. return `AUTHOR_COMPREHENSION_REQUIRED`;
2. identify the misunderstood concept;
3. provide a targeted evidence-backed correction without drafting the answer;
4. ask only the affected topic again;
5. prefer a varied scenario when it tests transfer rather than memorisation;
6. do not create the PR.

When every material topic is `understood`, record only
`AUTHOR_COMPREHENSION_DEMONSTRATED` plus the exact `HEAD_SHA` in transient
workflow state. Raw responses and topic classifications must not be written to
local artefacts, the PR body, comments, or other durable records.

## Revision invalidation

Any commit after the checkpoint invalidates it. Reclassify comprehension risk
and repeat the checkpoint against the new `HEAD_SHA` before creating the PR.

The checkpoint does not replace independent review, reviewer comprehension,
testing, specialist authority, risk disposition, or the later human verdict.