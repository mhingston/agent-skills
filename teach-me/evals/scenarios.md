# Teach-me explanation and provenance behavioural scenarios

Authoring-time portable evaluations for the **existing** `teach-me` Learn, Review, and Socratic / Gym modes. These are not runtime instructions. Compare the frozen base revision with the candidate in **separate, fresh** sessions using the same model, harness, tool permissions, injected source fixtures, clock, learner turns, and independent grading rubric. Learner productions and canonical receipts — not polished tutor prose — determine demonstrated learning.

## Matched-run and feasibility contract

- **Environment:** For stateful cases TM-E1/E2/E3/E6, supply Node.js 18+ and a separate empty `TEACH_ME_HOME` for each run with the same `TEACH_ME_TODAY` and no prior learner history, except the explicitly seeded due item in E6. If asked to choose storage, the simulated learner replies: "Use the isolated temporary local learning store." In stateless cases TM-E4/E5, append "Keep this session stateless; do not save learner data" to the first user prompt.
- **Sources:** Inject exactly the synthetic text shown below for E3/E4. Do not invent a paper URL or fetch supplemental paper details. An evaluator can provide the fixture as an attachment or visible prompt text, but must use the same form for both runs.
- **Learner driver:** Send one scripted learner utterance **only when the corresponding stage is requested** (initial attempt, teach-back, cold recall, confidence, changed-context transfer, or Socratic follow-up). Do not send a cold answer as a premature hint response. When an optional extra hint follows the initial miss, reply once: "I can't work it out yet; please explain the missing step and then test me." More unplanned prompts, an incorrectly ordered confidence request, or a prompt incompatible with the next scripted answer are **protocol deviations** — record and stop, do not improvise a learner reply. If no transfer is offered after settlement, stop at that settled interaction. If a transfer probe is asked, use the scripted transfer answer and reply `70` to a subsequent confidence request.
- **Assessment:** Where state is enabled, inspect exact learner productions, confidence, rubric verdict, settled receipt, and scheduler projection, rather than assuming they exist because the tutor mentions grading. For stateless cases evaluate observable feedback/uncertainty only; do not require storage or `source_gaps` writes. Do not count a coached reconstruction or a same-session success as delayed mastery.
- **Feasibility:** TM-E1/E2/E3/E6 are `fixtureable` (isolated writable store, Node and controlled learner). TM-E4/E5 are `available` without persistence using the supplied static text/prompts. TM-E7 is `fixtureable` for a catalogue with `eli5` and `teach-me` discoverable; without observable routing, grade routing `not_verifiable`. If the required interaction harness or tool access is unavailable, report the case `NOT_RUN`, not passed.
- **Record separately:** activation, order of learner attempt → explanation → self-explanation → cold retrieval → confidence → verdict/receipt, subject calibration, exact source claim coverage, transfer outcome, intrusive extra stages, cost/latency if observable, and comparisons to the baseline. Use an independent evaluator blind to variant labels when practical.

## TM-E1 — engineering mechanism and failure boundary

**Prompt:** "Teach me how trace context works across an HTTP request and an asynchronous queue. I know HTTP headers but not distributed tracing. Quiz me rather than just giving me a summary."

**Target concept:** Message producers propagate trace context in message metadata so consumers can continue/link tracing across an asynchronous boundary. The concrete probe should ask **what the producer/consumer must preserve**.

**Fixed learner turns through assessment:**
1. Initial prediction: "I don't know how the consumer gets context after the HTTP call ends."
2. Post-resolution teach-back: "The producer writes trace context into message metadata. The consumer extracts it to associate its new work with the originating trace."
3. Cold probe: "Trace context must travel in the message metadata; the consumer extracts it rather than guessing which earlier request it belongs to."
4. Confidence: "70".
5. If transfer is asked (missing metadata): "Without propagated context, the consumer can't reliably reconstruct parentage from timestamps; the trace relationship is missing."
6. If transfer-confidence is asked: "70".

**Pass:** Gets a prediction before resolving; traces one input into queue and consumer; distinguishes the trace-continuity invariant from implementation; tests the metadata-loss boundary; runs the cold probe → confidence → rubric/receipt sequence. Does not confuse timestamp matching with propagation, auto-generate an HTML page, or claim mastery from one result.

## TM-E2 — mathematics, base rates and a non-example

**Prompt:** "Teach me conditional probability for test results. I can multiply probabilities but always confuse sensitivity with the probability of disease given a positive test."

**Target concept:** Sensitivity is `P(positive | disease)`, not `P(disease | positive)`. Posterior probability also depends on prevalence and false positives.

**Fixed learner turns through assessment:**
1. Initial prediction: "A test with 90% sensitivity means a positive result gives a 90% chance of disease."
2. Post-resolution teach-back: "Sensitivity starts with people who have the disease. For chance of disease given a positive, I must also count positive results among people without the disease."
3. Cold probe: "P(positive given disease) and P(disease given positive) reverse the condition. The second needs the base rate and false-positive rate too."
4. Confidence: "70".
5. If transfer is asked (rarer condition, unchanged test): "With rarer disease, false positives make up a larger fraction of positive results; I can't reuse sensitivity as the posterior."
6. If transfer-confidence is asked: "70".

**Pass:** Repairs the directional error using a small numeric cohort before symbolic formalism, contrasts a misleading near-miss, and checks cold open recall. Collects confidence **after** the learner's answer and before any correctness feedback; coached correction does not count as delayed recall.

## TM-E3 — reported result versus source-supported inference

**Prompt:** "Teach me to evaluate this ML paper, not just summarise it. Which results support the core claim?"

**Synthetic fixture supplied verbatim to both runs** (no URL or real DOI):

> Synthetic Study, version 1, for an evaluation fixture only. Section 3: Method B is compared with baseline A on held-out dataset D using the same metric. Table 2: A = 0.74, B = 0.78 on D (author-reported). Section 5: No external dataset evaluation or independent replication is presented. The authors suggest B may generalise to other datasets, but this is not measured.

**Target concept:** Distinguish a supported in-dataset comparison from untested external generalisation.

**Fixed learner turns through assessment:**
1. Initial prediction: "B scored better, so this proves it generalises to any dataset."
2. Post-resolution teach-back: "The comparison measures B versus A on D. A gain on D doesn't test performance on any other distribution."
3. Cold probe: "Table 2 reports 0.78 for B versus 0.74 for A on D. The authors suggest broader generalisation but Section 5 says external datasets were not tested; there is no independent replication."
4. Confidence: "70".
5. If transfer is asked (new dataset E): "I'd need a held-out evaluation on E under a disclosed protocol before claiming generalisation; the D result is insufficient."
6. If transfer-confidence is asked: "70".

**Pass:** Names the exact version, section and Table 2 numbers, uses an example of the comparison, and separates **author-reported measurement**, **author inference**, and **tutor inference**. Learner must produce the distinction before assessment. Never labels the metric independently verified or invents a link to the synthetic paper.

## TM-E4 — abstract-only stateless negative control

**Prompt:** "Teach me the implications of this paper's ablation results." Include the stateless instruction from the run contract.

**Synthetic fixture supplied verbatim to both runs** (all other text inaccessible):

> Abstract only. The proposed approach improved an unnamed evaluation metric over a baseline on benchmark Q. The abstract contains no score, ablation method, component comparison, experiment table, or independent replication information. Full text and supplements are not accessible.

**Target concept:** An overall performance improvement is not evidence that an individual component caused it; no actual ablation is available.

**Fixed learner turns through assessment:**
1. Initial prediction: "The improvement must mean each new component contributed."
2. Post-resolution teach-back: "To infer a component's contribution, I need a controlled comparison removing that component; this abstract doesn't provide one."
3. Cold probe: "The abstract reports an overall improvement but no ablation experiments. I cannot say which component mattered or by how much."
4. Confidence: "70".
5. If transfer is asked (second model with same claim): "I'd look for a component-removal comparison and its measured metric; without one it's still unsupported."
6. If transfer-confidence is asked: "70".

**Pass:** Restricts claims to the abstract and explains what an ablation **would** establish without fabricating methods, sections, numeric results or citations. Calls the missing information an uncertainty **in the response**, with no requirement to create persistent `source_gaps` or a source ledger.

## TM-E5 — Socratic / Gym answer-withholding boundary

**Prompt:** "Use Socratic mode to help me derive Bayes' rule myself. Don't solve it for me." Include the stateless instruction from the run contract.

**Fixed learner turns to the final boundary check:**
1. Initial attempt: "I know conditional probability uses joint probability, but can't see how the two conditions relate."
2. On a narrowing question: "Maybe start with the joint event counted in two different orders?"
3. Next learner turn: "Actually just tell me the equation."
4. If the tutor asks whether to change modes: "No, keep Socratic mode. Give me a smaller case instead."
5. Stop after the tutor's next question/hint (no graded receipt required).

**Pass:** Offers smaller questions, contrast cases or structural hints without revealing the decisive derivation; does not silently treat "just tell me" as exiting Socratic mode. Requires explicit mode exit before supplying the solution; no persistence is required.

## TM-E6 — review must not become a new lesson

**Setup:** In the isolated stateful home, seed an encoding receipt for claim "Trace context must be propagated across asynchronous message boundaries" with cold probe "What must the producer send so the consumer can associate its span with the originating trace?". Advance the frozen clock to the **engine-computed due date** (never fabricate it); ensure one due item and no pending stash. Use the identical seeded state for both runs.

**Prompt:** "Review my due concepts; don't start a new lesson."

**Fixed learner turns through assessment:**
1. Due cold probe: "The producer writes trace context into message metadata; the consumer extracts it so its span is associated with the originating trace."
2. Confidence: "70".
3. If transfer is offered (message without context): "Without that metadata the consumer cannot reconstruct the originating trace just from time proximity."
4. If transfer-confidence is asked: "70".
5. Stop after review verdict and (if offered) transfer grading.

**Pass:** Re-anchors from the engine, probes the due claim **before** explanation, collects confidence before the verdict, records the exact production in a review receipt and uses the engine's due projection. Doesn't preload a new lesson, invoke a playbook without a demonstrated gap, or add mastery credit for prose.

## TM-E7 — one-shot explanation near miss

**Prompt:** "Give me a quick plain-English explanation of webhooks. No quiz, lesson plan, or future review."

**Learner turns:** None. Grade only the assistant's first response and visible routing.

**Pass:** The catalogue does not force `teach-me` onto a one-shot request. `eli5` may own it; no learner-state writes, surprise assessment, or forced HTML artifact.

## Evaluation interpretation

- Run all feasible cases as **matched baseline/candidate** pairs. TM-E1 through TM-E4 test explanation and evidence quality; TM-E4 through TM-E7 are additionally boundary/negative controls.
- Use the same learner script and source fixture in each pair; treat any extra prompts or unmatchable stages as observed regressions rather than inventing continuations.
- Static content inspection or passing state/scheduler tests cannot establish teaching improvement. Report `NOT_RUN` unless a real, matched interactive evaluation was executed and preserved.
