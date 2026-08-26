# Evaluation Case Generation

Read this file when a skill needs realistic evaluation cases but production
failures, user examples, or maintained fixtures do not already provide enough
coverage.

Generated cases are candidate measurements, not evidence that the skill works or
that its instructions are correct. Prefer source-linked real cases when they are
available and safe to reproduce.

## 1. Start from the evaluated capability

Use the skill body, its applicability boundaries, and any supplied user intent or
source-linked `eval_seed` to identify a small set of representative usage
scenarios. Do not derive cases only from the frontmatter description: routing
metadata may omit material body behaviour by design.

Generate the smallest useful set, normally:

- one routine positive case;
- one boundary, fallback, or near-miss case;
- one failure-prone or discipline case when the skill exists to prevent a known
  class of mistakes.

Do not manufacture a broad benchmark merely because generation is cheap.

## 2. Preflight environment feasibility

Before writing the prompt or fixture, identify what the case requires and classify
each material dependency as:

- `available` — the current harness/environment already supplies it;
- `fixtureable` — a faithful local fixture or isolated substitute can supply it;
- `requires_setup` — credentials, services, repository state, human interaction,
  or other setup is needed before the case can run faithfully;
- `not_executable_here` — the required behaviour cannot be represented faithfully
  in the current environment.

Check only requirements that can affect validity, such as:

- required CLI/runtime or package versions;
- repository and Git state;
- filesystem, network, browser, database, or external-service access;
- MCP or other tool availability;
- credentials and permission boundaries;
- multi-turn or human-approval interactions;
- pre-populated application or project state.

Prefer a faithful fixture over an external dependency when the fixture preserves
the behaviour being tested. Do not replace a material integration or authority
boundary with a toy fixture and then generalise the result to the real system.

If the case cannot run faithfully, retain it as an explicit `requires_setup` or
`not_executable_here` contract when it is valuable; do not silently discard the
hard part of the skill and claim representative coverage.

## 3. Generate the task independently of the answer

Write a natural user task and the minimum inputs needed to execute it. Preserve
realistic ambiguity, pressure, or incomplete context only when that condition is
part of the deployed task.

Do not leak into the solver prompt:

- the expected answer;
- verifier implementation details;
- hidden check IDs or rubric wording;
- a condensed copy of the skill procedure;
- the intended candidate improvement;
- which condition is being evaluated.

A case should remain meaningful when run against the baseline. If the prompt tells
the baseline exactly how the candidate skill says to behave, the comparison no
longer measures skill lift.

## 4. Derive checks from the task contract

Create checks from externally observable success criteria, accepted invariants,
source-backed policy, or an independently established oracle. Do not grade prose
similarity to the skill.

When useful, distinguish two outcome dimensions:

- `goal_completion` — whether the requested task or artefact is actually correct
  and usable;
- `instruction_following` — whether material workflow, authority, evidence,
  convention, or process constraints owned by the skill were followed.

Use these dimensions only when the distinction improves interpretation. Ordinary
checks may remain unclassified. Routing remains a separate harness-specific
experiment and must not be relabelled as an outcome dimension.

Prefer deterministic checks where possible. Use human review for genuinely
subjective qualities. An LLM judge may supplement evidence when justified, but it
must not convert an unverifiable claim into an objective pass.

## 5. Validate the generated case before using it

Reject or repair a generated case when:

- required setup is unavailable and no faithful fixture exists;
- the prompt leaks the answer, procedure, verifier, or candidate hypothesis;
- the checks can be satisfied without completing the intended task;
- the checks merely reward copying the skill wording;
- the baseline cannot reasonably attempt the same task;
- task-specific constants or hidden verifier details would become answer keys;
- the case duplicates another case without exercising a distinct decision rule;
- a simpler real production/example case already provides stronger evidence.

Run a cheap smoke check when possible: confirm fixtures load, required commands or
parsers are available, and the verifier can distinguish an obvious pass from an
obvious failure without revealing those examples to the solver.

## 6. Keep generation subordinate to evidence

Generated cases help bootstrap coverage; they do not justify permanent defensive
instructions on their own. If a generated pressure case exposes a baseline
failure, inspect the trajectory and confirm the failure mechanism before changing
the skill. Then rerun the wider validation set and preserve near misses so the fix
does not overfit the generated example.

When later production evidence contradicts a generated case assumption, update or
retire the case rather than preserving benchmark stability at the expense of
reality.

## Source motivation

This workflow selectively adapts the environment-aware task synthesis and
leakage-control ideas from arXiv:2606.17819v1. The repository's existing matched
pair, deterministic-verifier, routing, and harness-specific evaluation contracts
remain authoritative.
