---
name: coach-me
description: >
  Analyses the current user's session history against Anthropic's Claude Code
  Expertise research framework to identify their strongest and weakest prompting
  behaviours, the 20% changes that would produce 80% of improvement, and writes
  a personalised "User Manual for Working With AI". Use when a user wants to
  understand and improve how they collaborate with advanced models.
---

# Coach Me

> **Personal only.** This skill analyses the *current user's* session history.
> It never analyses another person's data. Output is diagnostic — no code is
> written, no files are committed.

Evaluate the user's real prompting behaviour against the Anthropic Claude Code
Expertise research framework and produce a coaching report covering strengths,
weaknesses, high-leverage improvements, and a personalised "User Manual".

**Announce at start:** "I'm using the coach-me skill to analyse your
session history."

---

## When to use

- A user wants to understand their AI collaboration patterns
- A user wants concrete, evidence-backed suggestions for more effective prompting
- A team lead wants a baseline read on their own usage before coaching others

---

## Prerequisites

- Internet access to fetch the Anthropic research article
- At least ~30 user prompts worth of session history, sourced by any method
  available in the current environment (see Step 1)

---

## Research Benchmark

Fetch the Anthropic research before analysing any sessions:

```
URL: https://www.anthropic.com/research/claude-code-expertise
```

Key framework dimensions to extract and hold in context:

| Dimension | What to look for |
|-----------|-----------------|
| **Expertise scale** | Novice → Intermediate → Expert (5-point). Expert markers: precise framing, domain-specific vocabulary, user corrects AI (not reverse), each prompt sets off 12+ agent actions vs ~5 for novice |
| **Division of labour** | Typical: user makes ~70% planning decisions, Claude makes ~80% execution decisions |
| **Verified success** | Requires a hard signal (passing tests, committed work, explicit user confirmation). Experts reach verified success 2× more often than novices |
| **Recovery from trouble** | Experts recover at 3× the rate of novices when a session hits trouble |
| **Actions per prompt** | Expert prompts set off ~12 actions + ~3,200 words of output vs ~5 actions + ~600 words for novice |

---

## Step 1 — Collect session history

The goal is **30+ real user prompts** from actual AI sessions. Use whichever
source is available in the current environment — the analysis method in later
steps is identical regardless of how the prompts were collected.

### Source options (try in order)

**A. Current conversation context**
The simplest source. Scroll back through the current conversation and note every
user message. Works in any tool with no extra setup.

**B. Tool-native session store**
If the host environment exposes a queryable session history (e.g. a local
database, an API, or a CLI command), use it to retrieve recent user messages
across sessions. Retrieve at least 80 rows sorted newest-first, filtering to
messages longer than 30 characters. Also retrieve any available session
summaries or checkpoint overviews for wider context.

**C. Git artifacts**
If no session store is accessible, mine git history for user-authored text:
commit messages, PR descriptions, and issue/ticket bodies written by the user
are reasonable proxies for how they frame work for an AI.

**D. User-provided examples**
If none of the above are available, ask the user to paste 10–20 representative
prompts they have sent to an AI coding assistant. Explain you need them to run
the analysis.

### Minimum viable sample

- **30+ distinct user messages** for a full report
- **10–29** for a preliminary report — flag the sample size and mark findings
  as indicative
- **Fewer than 10** — ask the user to provide additional examples before
  proceeding

---

## Step 2 — Classify prompts

For each retrieved user message, classify it against these dimensions. Work
through at least 30 distinct prompts before drawing conclusions.

### Expert markers (positive signals)

- **Constraint injection**: mentions what *not* to use/do before stating the goal
- **Pinned artefacts**: includes specific versions, file paths, branch names, URLs
- **Inline triage**: narrows the problem space in the prompt itself (rules out causes, routes to tools)
- **Scope policing**: user corrects the agent mid-session rather than being corrected
- **Process encoding**: specifies *how* work should be done (slice-by-slice, TDD, review gates)
- **Tool/skill routing**: names skills or tools explicitly to shrink agent inference overhead
- **Hard verification criterion**: ends with a testable assertion, not "please verify"

### Novice/weak markers (negative signals)

- **Multi-concern bundling**: 3+ tasks, questions, and instructions in one turn
- **Open-ended bootstrapping**: defers problem framing to the agent ("ask if anything is unclear")
- **Reactive constraint injection**: domain knowledge appears only *after* misalignment
- **Missing acceptance criteria**: goal stated but no clear definition of done
- **Technical identifier typos**: package names, command flags, version strings misspelled
- **Scope drift without explicit pivot**: requirements evolve mid-session without a reframe turn
- **Redundant context in follow-ups**: repeats information the agent already has

---

## Step 3 — Score and rank

Produce a frequency count across the classified turns:

| Behaviour | Count | Representative example |
|-----------|-------|----------------------|
| Constraint injection | N | "..." |
| Pinned artefacts | N | "..." |
| ... | | |

Rank behaviours by frequency. The top 3 positive behaviours are the user's
**strengths**. The top 3 negative behaviours are their **weaknesses**.

---

## Step 4 — Identify the 20/80 changes

Apply the 80/20 rule: which 2–3 changes, if applied consistently, would
eliminate the most friction or unlock the most agent capacity?

Prioritise changes that:
1. Affect the *first turn* of a session (highest leverage — sets the action chain)
2. Eliminate a pattern the user repeats across multiple sessions
3. Would push the user's weakest prompts up to match their strongest prompts
   (internal gap is often larger than the novice–expert gap in the research)

For each change:
- Quote the weak prompt as written
- Explain why it limits success
- Write a better version of the same prompt

---

## Step 5 — Write the output report

Produce the full report in this exact structure:

---

### The Anthropic Research Benchmark

Brief summary of the expertise framework (2–3 sentences). State which tier the
user most closely resembles based on the evidence.

---

### ✅ Strongest Prompting Behaviours

For each of the top 3 strengths:
- **Behaviour name** (bold)
- Quoted representative prompt (blockquote)
- Pattern explanation (1 paragraph)
- Why it helps (1 sentence)

---

### ❌ Weakest Prompting Behaviours

For each of the top 3 weaknesses:
- **Behaviour name** (bold)
- Quoted representative prompt (blockquote)
- Pattern explanation (1 paragraph)
- Why it hurts (1 sentence)
- **Better version** of the prompt (code block or blockquote)

---

### The 20% Changes → 80% of the Improvement

Numbered list of 2–3 high-leverage changes. Each item:
- Change name (bold)
- One-sentence rationale referencing the research
- Before/after prompt pair

---

### User Manual: Working with [username]

One page (~500 words). Sections:
1. **Who you are as a collaborator** — expertise tier, domain strengths, mental model of the agent system
2. **Where you get the most value** — the work modes and prompt patterns where your sessions consistently succeed
3. **Where you waste effort** — the patterns that cost turns or cause abandoned sessions
4. **How to become a more effective collaborator** — 4–5 concrete, durable habits ranked by leverage

---

## Output contract

The report is written directly in the conversation. Do not commit it to git, do
not create a file in the repo. If the user wants to save it, offer to write it
to their session folder (`~/.copilot/session-state/<session-id>/files/prompting-report.md`).

---

## Guardrails

- **Never analyse another user's data.** If the session store returns turns from
  multiple users, filter to the current user's sessions only.
- **No speculation.** Every finding must be backed by a quoted prompt from the
  session data. If fewer than 10 distinct user prompts are available, state the
  sample size limitation at the top of the report and flag findings as
  preliminary.
- **Typos are signal, not noise.** Technical identifier typos (package names,
  command flags) are a genuine prompting risk and should be noted. Natural
  language typos are not a finding.
- **Respect the research scope.** The Anthropic study covers Claude Code sessions
  specifically. If the session data is from a different tool (e.g., pure chat),
  note the caveat.

---

## Quick Reference

| Step | Action |
|------|--------|
| 1 | Fetch Anthropic research from URL above |
| 2 | Collect 30+ user prompts via whichever source is available (conversation context, tool-native store, git artifacts, or user-pasted examples) |
| 3 | Classify 30+ prompts against expert/novice markers |
| 4 | Score, rank, and find the 20/80 changes |
| 5 | Write report in the defined structure |
