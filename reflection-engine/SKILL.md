---
name: reflection-engine
description: Perform a rigorous, evidence-grounded personal reflection using the user's accessible conversation history, memory, files, and other explicitly available personal context. Use when the user asks for a candid self-audit, recurring-pattern analysis, blind spots, contradictions, trajectory, decision habits, strengths, or a deep portrait based on their historical corpus. Do not use for clinical diagnosis, one-off personality guesses, or when there is too little user-specific evidence to support meaningful longitudinal analysis.
metadata:
  version: "1.0.0"
  source-inspiration: "Reflection Engine v1.3 by kropdx/Kevin Rose"
---

# Reflection Engine

Create a candid, useful portrait of the user from evidence that is actually accessible to you. The aim is not to flatter, diagnose, or summarize their topics. The aim is to identify recurring patterns across time, domains, choices, corrections, and actions; test those patterns against counterevidence; and turn the strongest conclusions into practical experiments.

This skill is inspired by the methodology of Reflection Engine v1.3, but is intentionally rewritten as an operational Agent Skill rather than a prompt transcript.

## Routing boundaries

Use the smallest workflow that matches the user's requested outcome:

- Use `reflection-engine` for evidence-grounded reflection on the user's recurring behaviours, tensions, blind spots, and trajectory.
- Use `coach-me` when the primary outcome is evaluating how the user collaborates with AI and producing a personalised working manual.
- Use `session-lessons` when the primary outcome is identifying recurring workflow friction or effective patterns that may deserve durable codification.
- Use `decision-continuity` when the primary outcome is preserving or reconciling attributable project decisions across sessions, agents, plans, or handoffs.

These are routing boundaries, not runtime dependencies. Keep this skill self-contained and do not broaden a focused reflection request into workflow codification, AI-collaboration coaching, or project-decision reconciliation.

## Non-negotiable principles

1. **The skill is not evidence.** Never infer anything about the user from the fact that they invoked this skill, from the wording of this file, or from candidate examples in the reference material.
2. **Use only accessible evidence.** Never imply access to conversations, files, memories, accounts, or periods you did not actually inspect.
3. **Prefer behaviour over self-description.** Repeated choices, corrections, follow-through, abandoned approaches, and concrete actions carry more weight than aspirations or labels.
4. **A question is not a confession.** Curiosity about a behaviour, diagnosis, substance, relationship pattern, or hypothetical is not evidence that it applies to the user.
5. **Separate observation from inference.** State clearly when a conclusion is directly observed, inferred, tentative, or unsupported.
6. **Seek recurrence across independent episodes.** Ten mentions in one conversation are weaker than the same pattern appearing across several unrelated periods or domains.
7. **Actively seek counterevidence.** Every high-confidence conclusion should survive a search for examples pointing the other way.
8. **Correct for corpus bias.** Assistant conversations over-represent unresolved questions and under-represent decisions made offline. Lack of a recorded resolution is weak evidence of indecision.
9. **Do not diagnose.** Describe observable dynamics without assigning clinical or psychiatric labels to the user or other people.
10. **Do not expose hidden reasoning.** Show the evidence, conclusion, counterevidence, alternatives, and uncertainty needed to evaluate the result; do not reveal private chain-of-thought.

## Phase 1: Establish the corpus boundary

Before interpreting anything, determine what evidence is genuinely available.

Use personal-context, file, conversation-history, or connected-source retrieval only when those sources are available and relevant. Sample across the available timeline instead of relying on the most recent material.

Start the output with:

```markdown
## Corpus Coverage
```

State concisely:

- earliest and latest material actually reviewed;
- major domains represented;
- important missing domains or access limitations;
- whether the corpus is unusually concentrated in one period, project, or type of conversation.

Do not claim comprehensive coverage unless it is genuinely comprehensive.

## Phase 2: Build an evidence map

Privately build a compact evidence table before writing conclusions. For each candidate pattern, track:

- **pattern** — concise hypothesis;
- **episodes** — independent examples, not repeated mentions in one thread;
- **periods** — when it appears;
- **domains** — work, family, money, health, home, learning, relationships, creative work, decision-making, etc.;
- **evidence type** — action, stated preference, correction, repeated question, outcome, aspiration, or assistant interpretation;
- **counterevidence** — examples that weaken or qualify the pattern;
- **confidence** — preliminary 1–10 score.

Weight evidence roughly in this order:

1. repeated concrete actions or decisions;
2. repeated corrections, refusals, and standards enforced by the user;
3. recurring behaviour across unrelated contexts;
4. explicit self-reports confirmed over time;
5. isolated statements or questions;
6. prior assistant interpretations.

Treat speech-to-text mistakes and obvious transcription artifacts as noise unless independently corroborated.

## Phase 3: Publish the recurring threads first

After corpus coverage, add:

```markdown
## Recurring Threads
```

List five to eight patterns that are supported by more than one independent episode. Each thread should be one or two sentences and should mention the periods/domains that make it credible.

These threads are the evidence base for the rest of the analysis. Do not introduce a major theory later unless it is supported by the same evidence standard.

## Phase 4: Choose the reflection depth

Use the user's request to choose a mode:

### Focused mode

Use when the user asks about one issue, such as a blind spot, decision habit, contradiction, or trajectory. Answer only the relevant lenses from `references/reflection-lenses.md`.

### Full portrait mode

Use when the user asks for a comprehensive audit or portrait. Cover all major lenses in `references/reflection-lenses.md`, but combine overlapping lenses rather than repeating the same theory in different words.

A full portrait should normally contain 8–12 substantive sections plus a synthesis. Depth is more important than hitting an arbitrary question count.

## Phase 5: Calibrate every major conclusion

For each substantive section, include this compact metadata directly under the heading:

```markdown
**Confidence:** 8/10 · **Evidence:** broad · **Status:** observed pattern + inference
**Basis:** Repeated across several periods and domains; one meaningful counterexample.
```

Allowed evidence breadth:

- `broad` — several independent periods and/or domains;
- `moderate` — multiple examples but concentrated in fewer contexts;
- `narrow` — sparse or highly context-specific evidence.

Allowed status values:

- `observed pattern`
- `observed pattern + inference`
- `inference`
- `tentative hypothesis`
- `insufficient evidence`

Confidence guide:

- **9–10:** repeated, specific, cross-domain evidence with little meaningful counterevidence;
- **7–8:** clear recurring pattern with multiple independent anchors but some ambiguity;
- **4–6:** plausible but mixed, narrow, or context-dependent;
- **1–3:** sparse, speculative, or not answerable from available evidence.

Do not inflate confidence to make the writing sound decisive.

## Phase 6: Write each section as an argument the user can inspect

Lead with the conclusion. Then explain:

1. **Observation** — what pattern appears to exist.
2. **Evidence** — two or more independent anchors for confidence 7+; prefer different periods or domains.
3. **Interpretation** — what the pattern may mean and what function it serves.
4. **Cost / leverage** — what it enables, protects, delays, or makes expensive.
5. **Counterevidence** — where the user behaves differently or another explanation fits.
6. **Trajectory** — what is likely to compound if the pattern continues, without pretending certainty.

Then finish every major section with:

```markdown
### What you can do
```

Give one or two concrete actions or behavioural tests. Prefer something the user could try within a week. Where useful, name the likely way the user could overcomplicate or neutralize the advice.

Avoid generic self-help language. Advice must be tied to the evidence in that section.

## Phase 7: Synthesize without collapsing everything into one theory

Finish a full portrait with:

```markdown
## Synthesis
```

In roughly four to eight sentences, identify:

- the central tension that explains the most without explaining everything;
- the user's strongest available asset for handling it;
- the direction their current behaviour appears to be moving;
- the one practice or choice most likely to determine whether that trajectory becomes growth or repetition.

End with a final `### What you can do` paragraph that selects the single highest-leverage action already recommended. Do not invent a new recommendation at the end.

## Output style

- Address the user directly.
- Be candid, specific, warm, and unsentimental.
- Prefer concrete dates, projects, choices, corrections, and recurring behaviours over abstractions.
- Make memorable claims only when the evidence earns them.
- Explicitly label speculation.
- Do not performatively criticize or praise.
- Do not reuse the same core conclusion across several headings.
- Avoid therapy-speak, horoscope language, personality-test clichés, and pseudo-clinical framing.
- Short quotations may be used only when they are accurate and necessary; otherwise paraphrase.

## Evidence hygiene

When source systems support citations, cite the underlying evidence inline. When citations are unavailable, identify evidence concretely enough for the user to recognize the episode without inventing precision.

Assistant-authored memory summaries may help locate patterns, but they should not be the sole basis for a strong conclusion unless the user previously confirmed them. Prefer first-party material: the user's own messages, files, decisions, corrections, and recorded actions.

For claims about another person, report only what the user's corpus shows about the user's experience or interpretation. Do not present their account as objective proof of another person's motives or character.

## Stop rules

Downgrade or omit a conclusion when:

- it rests mainly on one dramatic episode;
- it is inferred from the wording of this skill or the user's choice to run it;
- it depends on an unverified assistant summary;
- the corpus contains substantial counterevidence you cannot reconcile;
- it would require diagnosing the user or another person;
- the available corpus is too narrow to distinguish a stable pattern from a temporary state.

When evidence is insufficient, say so explicitly. A well-bounded non-answer is better than a convincing invention.

## Final quality check

Before delivering, verify privately:

- Did I sample early, middle, and recent evidence where available?
- Did I sample more than one life/work domain where available?
- Did I distinguish actions, aspirations, questions, and hypotheses?
- Did I avoid treating lack of recorded closure as proof of avoidance?
- Did I seek counterexamples to every strong conclusion?
- Does confidence match evidence breadth?
- Is every major claim traceable to actual user evidence?
- Did I avoid diagnosis and hidden chain-of-thought?
- Are the recommendations concrete and testable?
- Did I avoid repeating one master theory under several headings?

Read `references/reflection-lenses.md` when selecting the analytical lenses for focused or full-portrait mode.
