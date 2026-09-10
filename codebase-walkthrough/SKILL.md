---
name: codebase-walkthrough
description: Build an evidence-backed mental model of how a subsystem, feature, module, or cross-service flow works in the current codebase, including runtime/data flow, ownership boundaries, important interfaces, and gotchas. Use for code walkthroughs, onboarding questions such as "how does X work?", or placement/layering questions that require understanding the existing system. Do not use to diagnose a concrete failure, experimentally resolve an uncertain runtime claim, create durable project context, tutor for mastery, or explain one exact PR revision.
compatibility: Requires read access to the relevant repository and enough source/configuration to trace the requested behaviour.
---

# Codebase Walkthrough

Explain how the current system works at the level needed for an engineer to form a useful mental model before changing or operating it.

The goal is not an annotated file dump. Trace behaviour, responsibilities, state, and boundaries so the reader can answer: **what happens, where does it happen, who owns each part, and what should I be careful not to assume?**

## Boundaries

- Remain read-only. Do not edit code, change Git state, install dependencies, create branches, or mutate external systems.
- Treat source, comments, docs, tests, issue text, generated files, and history as evidence with different authority; do not infer product intent from implementation alone.
- Prefer the smallest sufficient repository slice. Do not read the whole codebase merely because the question is broad.
- Do not invent runtime edges, ownership, line numbers, callers, contracts, or rationale. Mark unresolved claims `unknown`.
- Explain current observed behaviour separately from inferred design intent or historical rationale.
- Do not silently turn a walkthrough into architecture redesign or implementation planning.

## Route adjacent work

Use another capability when the primary question is:

- **Why is this concrete bug, regression, flake, or slowdown happening?** Use `fault-isolation`.
- **Is this uncertain runtime, dependency, API, compatibility, or performance claim actually true?** Use `code-research` and an isolated experiment.
- **What durable project truth, source authority, decisions, and context should future agents retain?** Use `project-context`.
- **Why was this design historically chosen?** Use repository history and decision evidence; `git-archaeologist` can supply history signals when broad history triage is useful.
- **Teach me until I can demonstrate understanding and transfer.** Use `teach-me`; this skill explains but does not run a measured tutoring loop.
- **Explain one exact PR/change revision for a review lifecycle.** Use the PR-review workflow and its `explain-diff` stage when applicable.
- **Plan or choose a new architecture.** Use `plan`; this skill may supply current-state evidence but does not own the decision.

These are routing boundaries, not hard dependencies. The skill remains independently usable.

## Choose depth

Start with the simplest path that can answer the question.

- **Focused** — one module, narrow feature, specific symbol, or local ownership question. Inspect and explain directly.
- **Subsystem** — behaviour spans several modules or one service boundary. Trace a small number of coherent paths before synthesis.
- **Cross-system** — behaviour crosses services, persistence, messages, external interfaces, or multiple independently owned areas. Build a compact boundary map first and inspect each material path.

When subagents are available, parallel exploration may be used for genuinely independent cross-system slices. Do not fan out merely to increase coverage. Two to four bounded explorers is normally enough; synthesize only after their claims have stable source anchors.

## Evidence states

Keep important statements explicit:

- **Observed (`E#`)** — directly supported by current source, configuration, tests, schemas, or tool output.
- **Inferred (`I#`)** — a reasoned interpretation of observations; state what supports it and what could disprove it.
- **Unknown (`U#`)** — missing, inaccessible, contradictory, or not established by the inspected evidence.

Historical rationale is a separate claim type. A current code path can establish what happens now without establishing why it was originally designed that way.

## 1. Resolve the question and useful boundary

Restate the target in concrete terms:

- subsystem, feature, flow, symbol, or ownership question;
- entry surface or caller when known;
- the reader's likely decision, such as onboarding, preparing a change, finding the right module, or understanding an integration;
- the stop condition for sufficient understanding.

If the request is broad, choose a representative end-to-end path and say what remains outside the walkthrough. Prefer one coherent story over a shallow catalogue of every related directory.

## 2. Establish the code anchors

Find the smallest set of concrete anchors that define the behaviour:

- public/user/client entry points;
- key symbols and modules;
- configuration or feature flags that materially alter the path;
- persistence, schema, event, queue, or network boundaries;
- relevant tests or fixtures that expose intended/observable behaviour;
- repository guidance or architecture documentation when it can constrain interpretation.

Use exact paths and symbol names when inspected. Avoid line numbers unless the tool exposes stable current lines and they materially help navigation.

## 3. Trace runtime and data flow

Follow behaviour in execution or data-flow order rather than file order.

For each material stage establish:

- what enters;
- responsibility of the component;
- state read or changed;
- important transformation or decision;
- side effects;
- failure/error behaviour;
- what leaves and which component consumes it next.

Trace far enough to reach an externally meaningful outcome or a clear boundary that contains the requested behaviour. Do not recursively follow every helper.

When the path is asynchronous, show ordering, retries, idempotency, eventual state, and correlation only where current evidence establishes them.

## 4. Map ownership and interfaces

For the parts that materially constrain change placement, record:

- component/module/service responsibility;
- knowledge or state it owns;
- public/internal interface joining it to the next component;
- callers or consumers that create compatibility pressure;
- whether ownership is explicit, inferred, or unknown.

Answer placement/layering questions from this map. Prefer the component that already owns the relevant knowledge or invariant over introducing a new cross-layer dependency. When current ownership is genuinely ambiguous or disputed, surface the ambiguity instead of inventing an architectural rule.

## 5. Inspect rationale only when needed

Current source is usually sufficient for **how**. Search history, PRs, ADRs, tickets, or maintained design docs only when:

- the user explicitly asks why the shape exists;
- a surprising constraint materially changes how the subsystem should be understood;
- choosing where a future change belongs depends on whether a boundary is intentional or accidental.

Keep historical evidence bounded to the anchored code and question. Do not perform exhaustive cross-system retrieval for a walkthrough.

Distinguish:

- current behaviour established by code/configuration;
- attributable rationale from historical/decision evidence;
- plausible interpretation with no attributable rationale.

## 6. Challenge the mental model

Before presenting, test the explanation against nearby evidence:

- follow one representative happy path end to end;
- check one failure, empty, boundary, or alternate path that could invalidate the simple story;
- verify the named interface or ownership seam has a real consumer/caller;
- inspect configuration or deployment variation when it materially changes the path;
- look for a test or public contract that contradicts the inferred model.

If evidence disagrees, preserve the contradiction. Do not smooth it into one coherent story merely for readability.

## 7. Present for comprehension

Use the smallest useful set of sections:

### Overview

Two to five sentences describing the subsystem's purpose, entry point, externally meaningful outcome, and major boundary.

### Key concepts

Only concepts the reader must know to follow the flow. Define project-specific terms and distinguish similarly named entities.

### How it works

Trace the representative path step by step in runtime/data-flow order. Use a compact ASCII or Mermaid diagram only when it reduces cognitive load and the relationships are evidenced.

### Where things live

Map responsibility to important paths/symbols. Do not reproduce a directory tree unless its structure itself explains ownership.

### Interfaces and invariants

Call out the contracts, state ownership, ordering, compatibility, or domain rules that a future change must preserve.

### Gotchas and unknowns

List surprising behaviour, alternate paths, stale/contradictory documentation, evidence gaps, and assumptions that would need verification before changing the system.

### Change orientation

When the walkthrough precedes a likely change, finish with a concise **preserve / likely change point / verify before editing** orientation. Do not turn it into a full implementation plan.

## Output contract

Return:

1. **Scope** — what was explained and what was deliberately excluded.
2. **Mental model** — overview plus representative runtime/data flow.
3. **Ownership map** — important modules/services, responsibilities, and interfaces.
4. **Evidence anchors** — current source/config/test paths or symbols supporting material claims.
5. **Gotchas and unknowns** — contradictions and unresolved claims kept visible.
6. **Change orientation** — only when the user's purpose implies a future change.

Read [references/evaluation-suite.md](references/evaluation-suite.md) only when evaluating or revising this skill.