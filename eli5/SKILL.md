---
name: eli5
description: Give a short, adult, plain-language orientation to an unfamiliar topic. Use for `/eli5`, "eli5 this", "break this down for me", "I know nothing about X, catch me up", or similar requests for the quick gist of how something works. Prefer `technical-plain-english` when the reader already needs the technical content and the main job is to make the prose clearer, shorter, or more natural. Prefer `teach-me` when the user wants tutoring, quizzes, durable learning, review, exam or interview preparation, or a multi-session learning workflow. Prefer `technical-diagram` when the requested primary deliverable is a standalone technical diagram, architecture visual, or infographic rather than a prose orientation.
compatibility: Rendered story graphics require filesystem or artifact support for creating and attaching a self-contained HTML file; the verbal explainer has no special environment requirement.
---

# ELI5

Explain an unfamiliar topic to an intelligent adult who is new to **this topic**, not new to ordinary adult life. Deliver the gist quickly, preserve the real terminology, and avoid turning a quick explainer into a lesson plan.

## Use when

Use this skill when the user wants a one-shot, plain-language orientation or a compact walkthrough of how something works.

Typical triggers include:

- `/eli5 <topic>`;
- "eli5 this";
- "break this down for me";
- "I know nothing about X, catch me up";
- "give me the quick version" or an equivalent request for a fast explainer.

## Avoid when

Do not use this skill as a substitute for `technical-plain-english` when the reader already needs the technical content and the requested outcome is better prose: clearer, shorter, more direct, more natural, or less AI-sounding. A request to rewrite a PR description, ADR, ticket, design note, status update, or similar technical artifact is a writing task, not an unfamiliar-topic orientation.

Do not use this skill as a substitute for `teach-me` when the user asks to:

- be taught or tutored over multiple turns;
- be quizzed, tested, or coached;
- build durable recall or review previous learning;
- prepare systematically for an exam or interview;
- create a learning plan or track learning progress.

Do not use this skill as a substitute for `technical-diagram` when the user primarily wants a standalone architecture diagram, system visual, infographic, flow graphic, or presentation-ready technical illustration. `eli5` may create a small supporting story graphic, but the prose orientation remains its primary output.

Do not force this format onto a request for exhaustive research, formal documentation, or a complete technical treatment unless the user explicitly asks to start with a quick explainer.

## Fast path

1. **Calibrate without interviewing.** State one brief assumption about the reader's topic knowledge, based on the request and conversation, then continue immediately. Example: "Assuming you know what a server is but not what a webhook actually does — tell me if I'm off."
2. **Orient in one line.** Say where the concept lives and what job it does.
3. **Give the core in one sentence.** If the reader stops here, they should still have the main point.
4. **Walk the main path.** Use `Here's how it works:` followed by roughly 3–6 numbered steps, normally one or two spoken-sounding sentences each.
5. **Teach real terms where they happen.** Bold a key term on first use and explain it inline at the moment it becomes relevant. Do not front-load a glossary.
6. **Close with one useful truth.** End the verbal explanation with the one sentence that makes the point, constraint, or safety property click. Do not add a recap section.
7. **Add a rendered story graphic only when the topic has motion.** If the topic has a sequence, before/after, request flow, state transition, or one thing acting on another, read [references/story-graphic.md](references/story-graphic.md), build the graphic from [assets/story-graphic-template.html](assets/story-graphic-template.html), and attach the rendered HTML in the same turn. Lead into it with: `Here's a quick graphic in case helpful:`

For a static concept with no useful sequence, skip the graphic. Do not ask permission first.

## Calibration rules

Treat "5" as a stand-in for **zero prior knowledge of the topic only**.

- Assume normal adult knowledge unless the conversation says otherwise.
- Do not define ordinary words such as money, internet, company, manager, admin, customer, phone, file, or other concepts a typical adult already owns.
- If the user demonstrates relevant knowledge, move the assumed boundary forward and do not re-explain covered ground.
- Never open by asking the user questions before providing the quick win.

## Language rules

Prefer specific literal language over clever analogy.

- Keep the real domain term so the reader can recognise or search it later; define it briefly in place.
- Use an analogy only when plain literal wording still leaves the mechanism unclear.
- Keep any analogy to one sentence and use an adult frame, not a childlike one.
- Avoid stacked analogies, whimsical metaphors, and oversimplification that changes the mechanism.
- Keep the whole verbal explainer comfortably under a minute to read unless the topic genuinely needs a little more context.

## Tone and shape

Write like a knowledgeable friend catching up another capable adult.

Do not use:

- praise or preamble such as "great question", "let's get you up to speed", or "so glad you asked";
- "simply put", "it's easy", or references to explaining something to a child;
- walls of text, dense subsection stacks, or nested bullet trees;
- definitions of things the user already said they understand;
- a closing summary or a menu of possible next threads.

Numbered steps are encouraged when they are the actual walkthrough.

## Follow-ups

Stay in the same concise calibration mode for ordinary follow-up questions. Use newly revealed knowledge to go deeper rather than repeating the original explanation.

If the follow-up changes the job from quick orientation to rewriting or generating a technical prose artifact, hand off to `technical-plain-english`. If it changes the job to structured tutoring, retrieval, assessment, or durable learning, hand off to `teach-me`. If it changes the job to producing a standalone technical visual, hand off to `technical-diagram` rather than stretching `eli5` into a diagram-authoring workflow.

## Graphic fallback

If the topic earns a visual but the environment cannot create and attach a rendered HTML artifact, give the verbal explanation only. Do not substitute raw Mermaid, HTML, SVG, ASCII art, or another code-fenced diagram and call it the visual.

## Checks

Before finishing, verify that:

- the answer contains a useful core sentence near the top;
- ordinary adult concepts were not unnecessarily defined;
- jargon was introduced only where it became useful;
- the main mechanism is a short narrated path rather than a catalogue of facts;
- the answer ends on one useful truth rather than a recap;
- a static concept did not get a forced visual;
- a flow-based topic got a rendered HTML story graphic when artifact support was available;
- no raw Mermaid or code-block diagram was presented as the visual;
- a technical-prose writing request was not stolen from `technical-plain-english`;
- a tutoring request was not stolen from `teach-me`;
- a standalone technical-visual request was not stolen from `technical-diagram`.

Read [references/evaluation.md](references/evaluation.md) when changing the description, routing boundary, response shape, or visual behaviour.
