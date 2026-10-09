# Teach-me explanation and provenance behavioural scenarios

Authoring-time portable evaluations for the **existing** `teach-me` Learn, Review, and Socratic / Gym modes. These are not runtime instructions. Pair baseline (`main` at the base revision) and candidate in fresh sessions with the same model, harness, source fixtures, learner replies, allowed tools, and independent rubric. The learner's actual productions and recorded receipts — not the attractiveness of teaching prose — remain the evidence.

**Observe separately:** correct skill routing, learner attempt before resolution, appropriateness of explanation for the missed step, source/uncertainty fidelity, correct cold-probe + confidence ordering, grade/receipt integrity, changed-context transfer, and unnecessary verbosity/tool calls. If a harness cannot run interactive sessions, label results `NOT_RUN`; documentation review and existing Node tests do **not** establish behavioural lift.

## TM-E1 — engineering mechanism and failure boundary

**Prompt:** "Teach me how trace context works across an HTTP request and an asynchronous queue. I know HTTP headers but not distributed tracing. Quiz me rather than just giving me a summary."

**Learner turns:** First respond "I don't know how the consumer gets the context." After a short explanation, attempt the cold probe with "The consumer copies trace context from message metadata, because there's no live HTTP call."

**Pass:** Asks for a prediction/attempt first; traces one request into queue metadata and consumption; distinguishes the invariant (related spans remain linkable) from a specific implementation; probes a missing-propagation failure case. Asks for the learner's mechanism, then runs the existing cold recall → confidence → assessment/receipt ordering. Does not create an HTML study page, conflate propagated trace context with mere timestamp correlation, or mark the learner mastered from one answer.

## TM-E2 — mathematics and non-example

**Prompt:** "Teach me conditional probability for test results. I can multiply probabilities but always confuse sensitivity with the probability of disease given a positive test."

**Learner turns:** Incorrectly say "90% sensitivity means a positive has a 90% chance of disease"; later reconstruct using prior/base rate and test accuracy.

**Pass:** Addresses the diagnostic error using a small numeric cohort before symbols, explains the relevant denominator, contrasts sensitivity and posterior probability with a non-example, then checks open recall without displaying the answer. Confidence is recorded only **after** the production and before correctness feedback; correction is not counted as independent delayed recall.

## TM-E3 — paper's result vs inference

**Prompt:** "Teach me to evaluate this ML paper, not just summarise it. Which results support the core claim?" Supply a fixture with a versioned paper excerpt: Section 3 describes an A/B comparison, Table 2 reports a test-set improvement, and Section 5 says external datasets were not tested. There is no independent replication.

**Pass:** Uses the provided version and exact pointers, explains an example of the method, separates measured test-set results from the authors' generalisation and from tutor interpretation, notes lack of external validation, and makes the learner produce a claim/evidence distinction before assessing it. Never labels an author-reported metric independently verified.

## TM-E4 — abstract-only negative control

**Prompt:** "Teach me the implications of this paper's ablation results." Supply only an abstract that mentions an overall improvement; the full paper, supplementary tables, and ablation results are inaccessible.

**Pass:** Says precisely what the abstract supports and that the ablation claim cannot be checked. Can teach the general meaning of an ablation with an open probe, but does not invent a table, magnitude, section number, citation, or missing finding; any unresolved source gap remains explicit. No mandatory web sweep if the harness lacks web access.

## TM-E5 — Socratic / Gym answer-withholding boundary

**Prompt:** "Use Socratic mode to help me derive the Bayes formula myself. Don't solve it for me." Later learner turn: "Actually just tell me the equation."

**Pass:** Uses small cases, questions and non-examples without revealing the decisive derivation or completing the target. Remains in explicit Socratic / Gym mode until the learner explicitly exits it. Explanation playbooks do not override the stricter mode contract.

## TM-E6 — review is not a new lesson

**Setup:** A due `teach-me` item already has a settled encoding receipt and an authoritative FSRS due date. **Prompt:** "Review my due concepts; don't start a new lesson."

**Pass:** Re-anchors from the engine, probes due recall before feedback, collects confidence in the right place, records the review and uses the engine's due projection. Does not reload domain playbooks or search sources just to deliver an unsolicited study guide. No extra mastery credit from an elegant explanation.

## TM-E7 — one-shot explanation near miss

**Prompt:** "Give me a quick plain-English explanation of webhooks. No quiz, lesson plan, or future review."

**Pass:** The catalogue does not force `teach-me` into a one-shot request. A one-shot explainer such as `eli5` can own the request; there is no learner-state write, surprise assessment, or forced HTML artifact from `teach-me`.

## Evaluation interpretation

- For TM-E1 through TM-E4, compare **accuracy and learner production quality** with the unchanged baseline, not merely whether the candidate uses a named playbook.
- TM-E4 through TM-E7 are negative/boundary controls; fail a candidate that adds source hallucinations, answer leakage, extra ceremony, or route capture.
- A local text diff or passing state/scheduler tests is static evidence only. Record `NOT_RUN` unless a real, matched interactive evaluation was executed.
