# Agent Skills

A catalogue of reusable agent skills for software engineering, learning,
workflow improvement, and accountable AI-assisted delivery.

## Packaging rule

Every skill is self-contained. A skill can be copied or installed by copying its
own directory only.

- The entry point is `<skill-name>/SKILL.md`.
- Supporting files, when needed, live under that skill's own
  `<skill-name>/references/` directory.
- A skill must not depend on files in a parent directory, a repository-level
  shared folder, or another skill's directory.
- Small pieces of process guidance may be intentionally duplicated between
  skills so each package remains portable and independently loadable.
- Skills may mention companion skills as optional workflow stages, but they must
  still behave safely and usefully when installed alone.

This repository's root README is a catalogue only; it is not a runtime
dependency of any skill.

## Skill catalogue

| Skill | Use it for |
| --- | --- |
| [`adopt`](adopt/SKILL.md) | Compare the current codebase with another project or idea and identify high-value, low-friction patterns worth adapting. |
| [`audit-me`](audit-me/SKILL.md) | Audit recurring work and connected work surfaces for dropped commitments, fragmented context, and automation opportunities. |
| [`coach-me`](coach-me/SKILL.md) | Analyse how a user collaborates with advanced models and produce focused coaching and a personalised AI working manual. |
| [`create-pr`](create-pr/SKILL.md) | Investigate a branch, gather proportionate evidence, assess comprehension risk, and create one reviewable pull request without approving or merging it. |
| [`deep-learning`](deep-learning/SKILL.md) | Turn passive study into active understanding through explanation, retrieval, diagnosis, application, and reinforcement. |
| [`explain-diff`](explain-diff/SKILL.md) | Build a causal, interactive mental model of a diff, commit, branch, or pull request so a reader can reason about and participate in future work. |
| [`git-archaeologist`](git-archaeologist/SKILL.md) | Use repository history to identify ownership patterns, defect hotspots, maintenance risk, and investigation priorities. |
| [`human-verdict-gate`](human-verdict-gate/SKILL.md) | Prepare a revision-specific decision packet for an accountable human without choosing, recording, or implying the verdict. |
| [`record-verdict`](record-verdict/SKILL.md) | Persist an explicitly human-supplied verdict against the exact pull-request revision as a structured, idempotent GitHub record. |
| [`repository-ontology`](repository-ontology/SKILL.md) | Assess whether a repository needs an ontology, establish the smallest evidence-backed model, and validate its usefulness for people and agents. |
| [`session-lessons`](session-lessons/SKILL.md) | Analyse multiple sessions for recurring friction and effective patterns that deserve durable codification. |

## Human-verdict workflow

The change-review skills compose as separate responsibility boundaries:

```text
agent implementation and local verification
                    ↓
create-pr — assemble evidence and create the review surface
                    ↓
explain-diff — build a causal mental model when proportionate
                    ↓
human-verdict-gate — prepare the current decision packet
                    ↓
human chooses and explains a verdict
                    ↓
record-verdict — persist the decision against the exact PR revision
```

Each stage can also be installed and used independently.

### `create-pr`: make the change reviewable

Use when a branch is ready to become a pull request. It inspects the complete
change, traces behaviour and likely blast radius, records exact verification
results and limitations, and identifies when deeper explanation is warranted.

It creates evidence, not approval.

### `explain-diff`: make the change understandable

Use when a reviewer needs more than a concise PR description. It teaches
previous and new behaviour, invariants, runtime or data flow, failure modes,
trade-offs, and extension points. Understanding checks and explain-back prompts
support reflection; they do not prove correctness.

### `human-verdict-gate`: make the decision judgeable

Use immediately before a consequential decision. It revalidates the current
revision, evidence, checks, review state, unresolved concerns, operational
readiness, and comprehension evidence. It leaves explain-back, risk acceptance,
and verdict fields for the accountable human.

### `record-verdict`: make the human decision durable

Use only after a human explicitly supplies the decision, rationale, evidence
assessment, and accepted risks. It binds the record to the exact PR head SHA and
creates or updates a canonical GitHub comment idempotently. A later commit makes
an older record stale.

`record-verdict` deliberately does not approve, merge, or deploy. Its JSON
Schema and comment template are packaged inside
[`record-verdict/references/`](record-verdict/references/).

## Design principles

1. Evidence is not approval.
2. Explanation is not proof of correctness.
3. Model-generated rationale is not human judgment.
4. A verdict applies only to the exact revision reviewed.
5. Green checks cannot silently replace explicit risk acceptance.
6. Automation may enforce a recorded verdict, but it must not invent one.
7. Use the lightest skill and artefact proportionate to the task and risk.
8. Portability and correct skill-loading boundaries take priority over avoiding
   small amounts of duplicated guidance.

## Installation and use

Copy the directory for each required skill into the skill location used by your
agent harness. Do not copy any parent-level support folder; there should not be
one.

Examples:

```text
create-pr/
└── SKILL.md

record-verdict/
├── SKILL.md
└── references/
    ├── verdict-comment-template.md
    └── verdict-record.schema.json
```

Skill support varies between agent products. The Markdown files are intended to
serve as both executable agent guidance and reviewable process documentation.
