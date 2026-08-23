---
name: code-conventions
description: Discover evidence-backed coding and repository conventions from an existing codebase, distinguish explicit policy from emergent patterns and drift, and recommend or codify the lightest deterministic enforcement such as EditorConfig diagnostics, formatters, linters, language analyzers, architecture tests, pre-commit checks, or CI gates. Use when asked what conventions a project follows, which recurring review comments can become tooling, how to enforce an observed convention, or how to turn implicit codebase norms into machine-checkable rules. Do not use primarily for LSP wiring, repository ontology design, general project-context management, or reviewing one concrete code change.
compatibility: Requires read access to representative repository code and configuration. Applying recommendations additionally requires write access and the repository's relevant formatter, linter, analyzer, test, or build tooling.
---

# Code Conventions

Turn repeated, evidenced codebase expectations into the smallest useful set of
explicit, machine-checkable controls.

The core distinction is:

> **Observed prevalence is evidence of a candidate convention, not proof of
> policy.**

Prefer existing explicit configuration and maintained guidance over inference.
Use code patterns to discover gaps, drift, local norms, or candidate rules that
still need confirmation.

## Modes

- **Discover** — identify explicit and implicit conventions without changing the
  repository.
- **Assess enforcement** — map conventions to existing controls, gaps, and the
  lightest viable enforcement mechanism.
- **Codify** — when explicitly authorised, make a minimal configuration or test
  change and verify it.

Default to the first two modes. Do not mutate repository state merely because a
convention appears obvious.

## Boundaries

Use this skill when the primary question is **what coding conventions exist and
how should they be made reliably enforceable**.

Route adjacent work elsewhere when the task is primarily:

- configuring Copilot/VS Code language-server wiring: use `lsp-config`;
- modelling repository/domain entities and semantic relationships: use
  `repository-ontology`;
- establishing durable truth/intent/history/scratch project context: use
  `project-context`;
- reviewing one concrete diff or pull request for defects: use `review`;
- designing a broad implementation plan: use the relevant planning workflow;
- defining organisational policy: use the authoritative policy process first,
  then use this skill only to operationalise accepted rules.

This skill may provide convention evidence to those workflows without taking
ownership of their outcomes.

## Evidence hierarchy

Inspect stronger evidence before inferring from source code. For each material
convention, preserve the strongest applicable source:

1. **Explicit enforced configuration** — formatter, linter, analyzer, compiler,
   architecture test, build property, hook, or CI gate currently executed.
2. **Explicit maintained guidance** — contributor docs, coding standards,
   repository instructions, ADRs, or equivalent maintained rules.
3. **Executable tests and project structure** — tests or deterministic checks that
   clearly encode an expectation even when not described as policy.
4. **Representative current code** — recurring patterns across relevant modules.
5. **Version-control history** — useful when current evidence is ambiguous or a
   convention appears to be migrating.

Do not infer authority from prevalence, age, file location, or author identity
alone.

### Exclude or down-weight misleading samples

Do not let these dominate convention discovery unless they are explicitly in
scope:

- generated code and vendored dependencies;
- snapshots, fixtures, golden files, migrations, or machine-produced clients;
- deprecated or legacy modules that the project intentionally contains;
- examples, experiments, benchmarks, and one-off scripts;
- tests when deriving production-code structure, unless the same rule is intended
  for both;
- one highly repetitive subsystem that would distort repository-wide prevalence.

When modules legitimately differ, model scoped conventions instead of forcing a
false global rule.

## 1. Inventory existing controls first

Before reading broad code samples, find the repository's current enforcement
surface. Inspect relevant files such as:

- `.editorconfig` and formatter configuration;
- language/package manifests and build configuration;
- linter/analyzer configuration;
- compiler warning/error settings;
- repository instructions and contributor documentation;
- pre-commit or pre-push hooks;
- architecture/dependency tests;
- CI workflows and scripts that execute checks;
- ignore/suppression/baseline files.

Identify:

- which tools are already dependencies;
- which files are authoritative for their settings;
- which checks actually run in CI versus existing only locally;
- scopes, exclusions, suppressions, and legacy baselines;
- rules configured but apparently not enforced;
- duplicated settings whose ownership is unclear.

Prefer extending an established tool over adding a second overlapping one.

## 2. Mine candidate conventions from representative code

Sample enough current code to detect recurring choices without performing a
repository-wide census by default.

Cover materially different areas, for example:

- public entry points and core domain code;
- application/service layers;
- persistence/infrastructure boundaries;
- tests where test-specific conventions matter;
- multiple packages/projects/modules in a monorepo;
- both older and recently changed code when migration is plausible.

Look for candidates in categories such as:

- formatting and whitespace;
- naming and visibility;
- file/type/module organisation;
- namespace/package/import structure;
- nullability, type-safety, and compiler strictness;
- async/concurrency idioms;
- error/exception/result handling;
- dependency direction and architectural boundaries;
- API and serialization shape;
- testing structure and assertion style;
- dependency injection and object construction;
- logging/telemetry patterns;
- resource/disposal/lifecycle handling;
- comments/documentation only when the repository treats them as a coding rule.

Do not convert taste into a rule merely because another codebase might prefer it.
The question is what this repository intentionally or consistently expects.

## 3. Classify each candidate

Assign one status:

- **Explicit** — directly stated or deterministically configured.
- **Strong consensus** — repeated across representative current code with no
  material contrary evidence, but not yet established as policy.
- **Scoped** — consistent inside a clearly bounded module/layer but not global.
- **Mixed** — materially inconsistent current practice.
- **Drift** — explicit rule and current implementation materially disagree.
- **Unknown** — evidence is too weak, inaccessible, stale, or contradictory.

Also record confidence as `high`, `medium`, or `low` and explain what would change
that confidence.

For inferred candidates, prefer multiple independent examples over raw occurrence
counts. Ten copies produced by one template are weaker evidence than the same
choice appearing independently across several maintained modules.

## 4. Decide whether enforcement is worthwhile

Do not mechanise every convention. Prefer deterministic enforcement when a rule:

- recurs often enough to consume review attention;
- is objective enough to avoid subjective false positives;
- has a stable scope and clear exception model;
- can be detected earlier and more cheaply by tooling than by review;
- meaningfully reduces defects, inconsistency, migration cost, or agent drift;
- can be introduced without forcing a high-risk repository-wide rewrite.

Leave a convention as guidance when it depends materially on design judgement,
business semantics, or contextual trade-offs that a deterministic rule cannot
reliably distinguish.

## 5. Choose the lightest enforcement mechanism

Read [references/enforcement-options.md](references/enforcement-options.md) when
mapping a convention to tooling.

Prefer this order when several mechanisms can express the same invariant:

1. an already-installed formatter/linter/analyzer;
2. standard language/compiler/build configuration;
3. a small repository-native test or dependency rule;
4. an existing hook/CI mechanism;
5. a new established dependency only when the benefit justifies it;
6. a custom analyzer/script only when no simpler maintained mechanism can express
   an important rule.

Typical mapping:

| Convention type | Prefer |
| --- | --- |
| whitespace, indentation, line endings, simple syntax style | EditorConfig or formatter |
| naming, language idioms, API/syntax patterns | language-native analyzer or linter |
| compiler/type-safety expectation | compiler/build settings |
| file/type organisation | analyzer/linter when supported; otherwise a focused structural test/script |
| dependency direction or layer boundary | architecture/dependency test or graph rule |
| repository/process invariant | pre-commit check or CI validation |
| semantic/design judgement | documentation and review, not fake linting |

`.editorconfig` is often a **configuration surface**, not the enforcement engine.
For analyzer-backed diagnostics, verify that the repository's actual analyzer and
version understand the chosen diagnostic or option before recommending a setting.
Never invent rule identifiers from memory.

## 6. Detect enforcement gaps and drift

For each explicit or strong candidate, ask:

- Is it represented in configuration?
- Does the configured tool actually run?
- Does CI fail, warn, or ignore violations?
- Is the rule scoped correctly?
- Are suppressions intentional and attributable?
- Does current code already violate it?
- Is autofix safe and available?
- Would enabling it create a noisy legacy backlog?

Distinguish these states:

- **documented and enforced**;
- **documented but unenforced**;
- **configured but not executed**;
- **executed but non-blocking**;
- **implicit candidate only**;
- **actively migrating**;
- **conflicted or obsolete**.

A configuration file existing in the repository is not evidence that CI or local
development actually applies it.

## 7. Recommend rollout, not just rules

For worthwhile gaps, propose the smallest reversible adoption path.

Prefer:

1. validate the rule against representative code;
2. estimate current violation volume;
3. use safe autofix separately when available;
4. scope or baseline legacy violations rather than mixing mass cleanup into the
   policy change;
5. start as informational/warning when uncertainty or migration cost is material;
6. ratchet toward no-new-violations or CI failure once the signal is trusted;
7. remove temporary baselines only as debt is deliberately paid down.

Do not bundle a repository-wide formatting or cleanup diff into a small policy
change unless the user explicitly requests that migration.

## 8. Codify only when authorised

When the user explicitly asks to implement accepted recommendations:

1. re-read the target configuration and its owning tool/version;
2. verify the selected mechanism supports the exact convention;
3. make the smallest configuration/test/script change that expresses it;
4. preserve unrelated settings, comments, scopes, and suppressions;
5. avoid opportunistic cleanup;
6. run the narrowest authoritative formatter/linter/analyzer/test/build command;
7. inspect the resulting diff;
8. report violations exposed by the new rule separately from the rule change;
9. do not weaken unrelated checks merely to obtain a green result.

If the repository cannot run the relevant verifier, report the unverified change
rather than claiming enforcement works.

## Output contract

For discovery or assessment, return:

1. **Existing enforcement surface** — tools/configuration actually present and
   what is known about execution.
2. **Convention map** — candidate, status, scope, evidence, current enforcement,
   confidence, and material conflicts.
3. **Best enforcement opportunities** — ranked by value, objectivity, and effort;
   include the recommended mechanism and target configuration surface.
4. **Drift and ambiguity** — explicit rules violated in practice, mixed patterns,
   unknowns, and evidence needed before codification.
5. **Next slice** — the smallest useful convention or small coherent set to
   codify first.

Do not produce a giant style guide by default. Focus on conventions that affect
correctness, recurring review effort, agent reliability, or meaningful structural
consistency.

For codification, additionally report:

- exact files changed;
- exact rule/mechanism added or changed;
- verification command and observed result;
- newly exposed violations or migration debt;
- any remaining rollout step before the rule can be considered reliably enforced.

## Quality gate

Before finishing, verify that:

- explicit policy is not being replaced by majority style;
- generated, vendored, legacy, or local-only patterns did not distort inference;
- global recommendations are supported across representative scopes;
- mixed evidence remains mixed instead of being normalised away;
- every proposed rule has a concrete enforcement mechanism or is explicitly left
  as guidance;
- the proposal extends the existing toolchain where practical;
- analyzer/linter rule support is verified rather than guessed;
- rollout avoids unnecessary repository-wide churn;
- CI execution is distinguished from local configuration;
- adjacent skills retain their own responsibilities.

Read [references/evaluation-suite.md](references/evaluation-suite.md) when changing
this skill's trigger boundaries or core decision rules.
