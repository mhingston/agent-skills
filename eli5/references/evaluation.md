# ELI5 behavioural evaluation

Use this reference when changing the skill description, applicability boundary, verbal response shape, or rendered-graphic behaviour. The important catalogue boundary is that `eli5` owns fast one-shot orientation while `teach-me` owns tutoring, assessment, review, and durable learning.

## Matched conditions

Run each case as a matched pair in fresh contexts with the same model, harness, tools, permissions, and user prompt.

- **candidate** — `eli5` and `teach-me` are both discoverable.
- **baseline** — `teach-me` remains discoverable but `eli5` is absent.

For a new skill, this baseline represents the pre-skill catalogue. Do not remove `teach-me` from the baseline because the sibling-routing boundary is part of the evaluation.

Record the harness and model. If the harness exposes skill discovery/loading, record the selected skill directly. Otherwise label any manual classification as a routing surrogate rather than an end-to-end routing result.

## Cases

### E5-E1 — quick mechanism explainer

**Prompt**

> ELI5 webhooks. I know what an API is, but I've never really understood what makes a webhook different.

**Candidate routing expectation**

`eli5` should activate.

**Behavioural checks**

- calibrates from the user's stated API knowledge and does not redefine APIs;
- states the core distinction near the top;
- uses a short narrated sequence rather than a broad catalogue of webhook concepts;
- introduces real terminology inline where it becomes useful;
- avoids praise/preamble and closes with one useful truth rather than a recap;
- produces a rendered story graphic when artifact support is available because the topic has a request/event flow.

### E5-E2 — static concept, no forced visual

**Prompt**

> Break down what "open source" actually means for me. Assume I know nothing about software licensing.

**Candidate routing expectation**

`eli5` should activate.

**Behavioural checks**

- explains the core meaning without defining ordinary adult concepts such as companies, files, or money;
- keeps the answer compact and adult in tone;
- introduces relevant licensing terminology only as needed;
- does not force a comic strip merely to satisfy a visual rule when no useful process or transition needs to be shown;
- does not emit raw Mermaid, HTML, SVG, or ASCII art as a substitute visual.

### E5-E3 — tutoring near-miss

**Prompt**

> Teach me probability from scratch over the next few sessions. Quiz me as we go and make sure I actually retain it for an interview next month.

**Candidate routing expectation**

`eli5` should **not** activate. Route to `teach-me`.

**Behavioural checks**

- preserves the tutoring, assessment, retention, and multi-session requirements;
- does not collapse the request into a one-minute explainer;
- candidate behaviour is no worse than baseline on the `teach-me` contract.

This is the principal anti-collision case.

### E5-E4 — knowledgeable follow-up calibration

**Prompt**

> I already understand OAuth authorization codes and redirects. ELI5 what PKCE adds and why it exists.

**Candidate routing expectation**

`eli5` should activate.

**Behavioural checks**

- starts from the user's stated OAuth knowledge rather than re-teaching the authorization-code flow from first principles;
- defines PKCE-specific terms at the point they matter;
- explains the before/after security mechanism in roughly 3–6 steps;
- avoids childlike analogies or definitions of normal adult concepts;
- produces a rendered flow story when artifact support is available.

### E5-E5 — rendered visual fidelity

**Prompt**

> I know what an API key is, but not what actually happens to it when I make a request. Catch me up quickly.

**Candidate routing expectation**

`eli5` should activate.

**Behavioural checks**

- gives the verbal quick win before the visual;
- attaches a self-contained rendered HTML artifact when artifact support is available;
- never presents raw Mermaid or a code-fenced diagram as the visual;
- each panel contains one clear action and roughly 3–4 visual elements;
- panel titles alone tell the complete story in order;
- captions add consequences or caveats instead of restating titles;
- the visual uses consistent cast symbols and does not contradict the verbal mechanism.

## Paired grading

For each case record separately:

1. **Activation** — selected `eli5`, selected `teach-me`, or no relevant skill; use `not_verifiable` if discovery is hidden.
2. **Boundary correctness** — especially whether E5-E3 remains with `teach-me` and E5-E2 avoids a forced visual.
3. **Goal completion** — did the user get a correct, useful orientation quickly?
4. **Instruction following** — pass/fail/not-verifiable for the case-specific calibration, shape, tone, and visual checks.
5. **Regression** — did the candidate add unnecessary ceremony, repetition, or visual overhead relative to baseline?
6. **Cost/latency** — record only when exposed by the harness.

For visual cases, human review may be needed for clarity and aesthetic quality. Blind the condition labels when practical and apply the same rubric to candidate and baseline artifacts.

The minimum acceptance condition is:

- E5-E1, E5-E2, E5-E4, and E5-E5 route to `eli5` when routing is observable;
- E5-E3 routes to `teach-me`;
- all verifiable verbal checks pass;
- E5-E2 does not create a forced process graphic;
- flow-based cases create a rendered HTML story graphic when artifact support is available;
- no case presents raw diagram code as the user-facing visual;
- the candidate introduces no material regression in correctness or usefulness relative to baseline.

Run at least one complete matched pair per case for a routing/behaviour smoke test. Use repeated pairs when model variance or description changes make the routing conclusion consequential. Do not report behavioural evaluation as passed until the matched runs have actually been executed and preserved.
