# Explanation Playbooks

Optional, subject-sensitive scaffolds for **resolving one learning gap** in `teach-me`. The default dialogue protocol and learner receipts remain authoritative. These patterns are not new modes, a textbook template, or instructions to produce a standalone HTML page.

## When to load and select

- In **Learn**, after a learner prediction/attempt and the finite hint ladder, pick at most **one** playbook if it meaningfully improves the explanation of the current concept. Choose by the *kind of reasoning the capability requires*, not a keyword-only domain classifier; skip when a concise explanation already works.
- Calibrate to demonstrated prerequisites and the learner's goal. A playbook is a menu of moves, **not** a sequence of mandatory sections. Explain only the missed mechanism or assumption; do not expand one node into a lecture.
- Never bypass cold retrieval, the confidence gate, rubric grading, or separated transfer evidence. Polished explanations and diagrams are not mastery.
- In explicit **Socratic / Gym** mode, use a playbook only to select a smaller question, analogy, or counterexample; do not reveal the decisive answer or produce the learner's target artifact.
- Prefer provided/authoritative materials for contested, current, high-stakes, or source-constrained claims. Consult `continuity-and-reference.md` for source provenance; don't manufacture references or require web research for every ordinary concept.

## Select the smallest useful pattern

| Learning mechanism | Compact explanation move | Useful boundary or check |
| --- | --- | --- |
| **Engineering / technical system** | Trace one concrete input end-to-end, then explain the invariant/specification separately from an implementation detail. | Change a boundary (retry, failure, queue, race, version); ask what must still hold. |
| **Mathematics / formal reasoning** | Start with one small worked instance, define symbols, then generalise to the rule or proof step the learner missed. | Give a near-miss non-example or a violated assumption; ask why the rule no longer applies. |
| **Empirical / natural science** | Distinguish observation, model, prediction, and test; make assumptions, units, and scale explicit where relevant. | Separate measured effects from inferred causes; ask what observation would distinguish competing models. |
| **Research paper / evaluated model** | Identify question, method, comparison, and the specific result the source actually reports, then explain one example through the mechanism. | Separate author-reported results, independent replication, and the tutor's inference; identify a limitation or missing ablation. |
| **Decision / business / policy** | Ground a decision in a concrete situation, constraints, a quantitative or qualitative trade-off, and consequences. | Show a plausible case where the preferred option fails; identify which assumption or value changes the decision. |
| **Other / everyday** | Start from a familiar observation, explain the causal mechanism, then name one exception. | Say where the analogy stops working; return to the learner's stated capability. |

Use contrasting representations or worked examples **only when they change the learner's predicted answer**. An optional static sketch may help; do not create a visual artifact by default or replace active production with passive reading.

## Apply inside the existing loop

1. After the learner's attempt, identify the **specific gap** (wrong causal step, missing premise, confused terms, unsupported inference).
2. Select one fitting move and give a short concrete case, derivation, or source-grounded account. If the concept has a consequential boundary, show **one** counterexample or limitation instead of enumerating every edge case.
3. Ask the learner to **self-explain** that mechanism or boundary. In the **Connect** step, help identify a meaningful link such as `requires`, `causes`, `enables`, `part-of`, `contrasts-with`, or `applied-in`. Treat these as instructional connections; only hard prerequisite `requires` edges belong in the persisted topic graph.
4. Remove the explanation and return to the existing **cold open-recall probe**, confidence gate, grading, receipt, and changed-context transfer rules. A correct worked example supplied by the tutor is not learner evidence.

### Reading a research paper safely

- Prefer the paper's actual text, version, and exact section/figure when available. A linked abstract or a secondary summary supports **only** what it contains.
- State what was measured, what the authors conclude, what has been independently confirmed (if known), and what remains unknown. Don't turn study results into universal facts.
- Keep a bounded `source_gaps` entry for claims whose methods, data, or version could not be inspected. Never fabricate a DOI, numeric result, paper section, or quote.
- When the learner is studying rather than asking for an immediate paper summary, use the paper to define **one testable claim** with an open probe and rubric, not as an excuse to switch to passive summarisation.

*Conceptual inspiration: [Philosopher-OKF](https://github.com/frypan05/philosopher-OKF) (MIT). This reference adapts teaching patterns; it does not import its output format, classifier, or HTML template.*
