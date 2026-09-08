# Technical Plain English behavioural evaluation

Use this reference when changing the skill description, applicability boundary, or writing rules. The important catalogue boundary is that `technical-plain-english` owns reader-facing technical prose when wording is the job, while `eli5` owns quick orientation to an unfamiliar topic and domain skills continue to own their technical tasks even when they emit prose.

## Matched conditions

Run each case as a matched pair in fresh contexts with the same model, harness, tools, permissions, and user prompt.

- **candidate** — `technical-plain-english`, `eli5`, `teach-me`, and normal domain skills are discoverable.
- **baseline** — the exact base-revision catalogue is discoverable, with `technical-plain-english` absent.

Do not remove `eli5`, `teach-me`, or relevant domain skills from the baseline. The sibling-routing boundaries are part of the evaluation.

Record the harness and model. If the harness exposes skill discovery/loading, record the selected skill directly. Otherwise label manual classification as a routing surrogate rather than an end-to-end routing result.

## Cases

### TPE-E1 — tighten an existing technical draft

**Prompt**

> Make this less verbose and more human without losing any technical detail:
>
> The retry subsystem has been designed in order to provide a capability whereby failed publication attempts may potentially be re-attempted up to a maximum of three times. It is important to note that after the third unsuccessful attempt, the message is subsequently routed to the dead-letter queue, thereby highlighting the importance of operational monitoring.

**Candidate routing expectation**

`technical-plain-english` should activate.

**Behavioural checks**

- preserves the three-attempt limit and dead-letter-queue behaviour;
- removes throat-clearing, stacked hedging, and pseudo-analysis;
- uses direct verbs and concrete sequence wording;
- materially reduces unnecessary words without inventing implementation detail;
- returns the rewritten prose without an unsolicited explanation of the editing process.

### TPE-E2 — generate a reader-facing engineering note

**Prompt**

> Write a concise technical note for the backend team explaining this decision: we are keeping business rules in deterministic code and using the LLM only to extract facts from transcripts. The reason is that rules need to be testable and versioned, while transcript language is variable. Keep it natural and don't turn it into a big architecture document.

**Candidate routing expectation**

`technical-plain-english` should activate.

**Behavioural checks**

- leads with the decision rather than generic context;
- preserves the distinction between deterministic rules and variable-language fact extraction;
- keeps the note proportionate and does not invent architecture or evidence;
- avoids decorative headings, summary repetition, and canned chatbot phrasing;
- sounds like an engineer writing to peers rather than a generic corporate explainer.

### TPE-E3 — unfamiliar-topic `eli5` near-miss

**Prompt**

> I keep hearing about idempotency but don't really understand it. Break it down for me quickly with an example.

**Candidate routing expectation**

`technical-plain-english` should **not** activate. Route to `eli5`.

**Behavioural checks**

- recognises that the user's problem is topic understanding rather than prose quality;
- gives a quick orientation to the concept rather than treating the request as a writing artifact;
- candidate behaviour is no worse than baseline on the `eli5` contract.

This is the principal `eli5` anti-collision case.

### TPE-E4 — domain-task near-miss

**Prompt**

> Review this pull request for correctness and tell me whether it is safe to merge. Focus on concurrency bugs and missing tests.

**Candidate routing expectation**

`technical-plain-english` should **not** activate merely because the eventual review is prose. Route to the review capability that owns the technical task.

**Behavioural checks**

- preserves the requested code-review outcome;
- does not replace technical investigation with a style pass;
- does not treat "concise" or natural writing as more important than evidence and correctness;
- candidate behaviour is no worse than baseline on the owning review contract.

### TPE-E5 — tutoring near-miss

**Prompt**

> Teach me distributed systems over the next month. Quiz me, revisit weak areas, and make sure I can explain the trade-offs in an interview.

**Candidate routing expectation**

`technical-plain-english` should **not** activate. Route to `teach-me`.

**Behavioural checks**

- preserves the tutoring, assessment, review, and multi-session requirements;
- does not collapse the request into a concise technical explainer;
- candidate behaviour is no worse than baseline on the `teach-me` contract.

### TPE-E6 — precision beats simplification

**Prompt**

> Rewrite this for senior engineers so it reads naturally, but don't dumb it down: "The consumer is idempotent, but processing is only eventually consistent because the projection is updated asynchronously after the event commit."

**Candidate routing expectation**

`technical-plain-english` should activate.

**Behavioural checks**

- retains `idempotent` and `eventually consistent` because they name relevant technical properties;
- preserves the causal ordering between event commit and asynchronous projection update;
- does not replace precise terms with longer beginner explanations the audience did not request;
- makes only the minimum effective edit when the source is already strong.

## Paired grading

For each case record separately:

1. **Activation** — selected `technical-plain-english`, selected adjacent skill, or no relevant skill; use `not_verifiable` if discovery is hidden.
2. **Boundary correctness** — especially whether TPE-E3 stays with `eli5`, TPE-E4 stays with the owning domain capability, and TPE-E5 stays with `teach-me`.
3. **Technical fidelity** — pass/fail for preserved facts, qualifiers, identifiers, causal relationships, and uncertainty.
4. **Reader usefulness** — did the result make the requested technical prose easier to understand, scan, or act on?
5. **Concision and naturalness** — did the candidate remove unnecessary wording and common chatbot artifacts without flattening useful voice or precision?
6. **Regression** — did the candidate introduce over-simplification, extra ceremony, formatting sprawl, or unsupported specificity relative to baseline?
7. **Cost/latency** — record only when exposed by the harness.

For rewrite cases, compare source and output claim-by-claim before judging style. A shorter answer fails if it loses a material condition or technical distinction.

The minimum acceptance condition is:

- TPE-E1, TPE-E2, and TPE-E6 route to `technical-plain-english` when routing is observable;
- TPE-E3 routes to `eli5`;
- TPE-E4 remains with the owning technical/domain capability;
- TPE-E5 routes to `teach-me`;
- every rewrite preserves all material claims and calibrated uncertainty;
- positive cases remove material verbosity or AI-style ceremony without adding unsupported facts;
- the candidate introduces no material regression in correctness or usefulness relative to baseline.

Run at least one complete matched pair per case for a routing/behaviour smoke test. Use repeated pairs when model variance or description changes make the routing conclusion consequential. Do not report behavioural evaluation as passed until the matched runs have actually been executed and preserved.
