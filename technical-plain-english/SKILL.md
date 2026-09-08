---
name: technical-plain-english
description: Generate or rewrite reader-facing technical prose so it is concise, direct, natural, and easy to scan without losing technical precision. Use when the user explicitly asks to make technical writing clearer, shorter, less verbose, less AI-sounding, more human, or plain English, or when the requested deliverable is itself a technical explanation, note, ticket, ADR, status update, review comment, or similar prose artifact and wording is the main job. Do not use merely because another technical task happens to produce prose. For a one-shot explanation of an unfamiliar topic, prefer `eli5`; for tutoring, assessment, or durable learning, prefer `teach-me`.
---

# Technical Plain English

Write technical prose like an experienced engineer communicating with another capable human. Preserve the real technical content while removing ceremony, filler, needless abstraction, and common LLM writing habits.

## Own this outcome

Use this skill when the main deliverable is technical prose and the user wants the wording itself improved or generated in a clear, concise style.

Typical triggers include:

- "make this less verbose";
- "make this sound more human";
- "rewrite this in plain English";
- "tighten this technical explanation";
- "make this PR/ticket/ADR easier to read";
- "write a concise technical note explaining why we changed this".

Do **not** activate only because a coding, planning, review, research, or delivery skill will emit prose. Let the skill that owns the actual task keep ownership unless the user explicitly asks for a writing pass or the prose artifact itself is the requested outcome.

## Distinguish from `eli5`

The boundary is the reader's job, not the vocabulary used.

- Use **`technical-plain-english`** when the reader already needs the technical content and the problem is how clearly, naturally, or concisely it is written.
- Use **`eli5`** when the reader is unfamiliar with the topic and wants a quick orientation to what it is or how it works.
- Use **`teach-me`** when the user wants tutoring, quizzes, review, retention, or a multi-session learning workflow.

Examples:

- "Explain Kubernetes readiness probes to me; I've never used Kubernetes" → `eli5`.
- "Rewrite this readiness-probe ADR so the team can scan it quickly" → `technical-plain-english`.
- "Teach me Kubernetes over the next few sessions and quiz me" → `teach-me`.

Do not turn a rewrite request into a tutorial. Do not turn an unfamiliar-topic explainer into a line-editing exercise.

## Working method

1. Identify the reader, purpose, and required technical claims from the request and supplied material. Infer them when they are obvious; ask only when a missing detail would materially change the writing.
2. Preserve facts, names, numbers, code identifiers, constraints, uncertainty, causal claims, and decision boundaries. Never invent specificity to make prose sound better.
3. Lead with the answer, decision, finding, or action the reader needs first.
4. Cut setup, repetition, throat-clearing, generic transitions, and recap that do not add information.
5. Replace inflated or indirect wording with the shortest precise construction.
6. Keep real technical terms when they carry meaning. Explain a term inline only when the intended reader may not know it.
7. Use structure only when it helps the reader scan a real set, sequence, comparison, or decision. Do not manufacture headings or bullets from ordinary prose.
8. Read the result for cadence. Vary sentence length naturally, remove robotic symmetry, and prefer wording a competent engineer might actually say.
9. Stop editing when further compression would remove a useful distinction, qualifier, example, or piece of evidence.

## Language rules

Prefer concrete actors and actions.

- Prefer "CallCoach publishes an event" to "an event is subsequently facilitated by the CallCoach component".
- Prefer "We retry three times" to "the system has been designed to provide a retry capability of three attempts".
- Prefer "Because" to "due to the fact that" and "To" to "in order to".

Use ordinary words when they are equally precise, but do not dumb down domain language. Terms such as `idempotent`, `eventual consistency`, `backpressure`, `fallback`, `abstraction`, or `robust` may be exactly right when they name a real technical property.

Preserve calibrated uncertainty. Replace defensive or stacked hedging, but do not turn "likely", "may", or "we have not verified" into certainty.

Use active voice when it makes responsibility or causality clearer. Passive voice is fine when the actor is irrelevant or unknown.

## LLM patterns to remove

Remove these when they do not carry real meaning:

- praise and preamble such as "Great question" or "Let's dive in";
- throat-clearing such as "It is important to note" or "It's worth mentioning";
- significance inflation such as "pivotal", "transformative", or "underscores the importance";
- fake-strong verbs such as "serves as" or "stands as" when "is" is clearer;
- canned contrast such as "not just X, but Y" when the direct statement is enough;
- trailing pseudo-analysis such as "highlighting", "showcasing", or "underscoring" without a mechanism;
- repeated rule-of-three lists, identical paragraph shapes, and dramatic fragments;
- decorative bold, excessive headings, emoji, or list sprawl;
- generic summaries and upbeat endings that merely restate the answer;
- automatic "let me know if you want..." menus when the requested job is complete.

Treat these as symptoms, not banned tokens. Keep any wording that is technically necessary or genuinely natural in context.

## Shape the output

For a rewrite, return the finished prose first. Do not add a change log unless the user asks for one or a material ambiguity needs to be surfaced.

For generated prose, match the artifact the user asked for rather than wrapping it in commentary. A short technical answer normally needs no heading. A longer note may use a few descriptive headings. A procedure or comparison may use a list or table when scanning matters.

Default to the shortest version that preserves the information the intended reader needs. Concision is not a word-count target; it is the absence of text that does no useful work.

## Checks

Before finishing, verify that:

- the main point appears early;
- no technical claim, qualifier, constraint, identifier, or decision boundary was lost or invented;
- jargon is retained when precise and explained only when the reader needs it;
- every heading and list earns its structure;
- repeated setup, recap, filler, and chatbot framing are gone;
- uncertainty remains calibrated;
- the prose sounds natural rather than mechanically "polished";
- an unfamiliar-topic orientation was not stolen from `eli5`;
- a tutoring request was not stolen from `teach-me`;
- another domain skill's task was not stolen merely because its output contains prose.

Read [references/evaluation.md](references/evaluation.md) when changing the description, routing boundary, or writing rules.
