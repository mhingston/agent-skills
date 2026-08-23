# Enforcement options

Use this reference to select the smallest deterministic mechanism that can
express a convention without creating a parallel tooling stack.

## Selection rules

1. Prefer a tool already installed and already run by the repository.
2. Prefer language-standard or ecosystem-standard mechanisms over custom code.
3. Verify support against the repository's actual tool/version before naming an
   option or diagnostic identifier.
4. Prefer a narrow, attributable rule over a broad preset that changes unrelated
   behaviour.
5. Separate the rule/configuration change from bulk remediation when possible.
6. If a rule depends on semantic judgement that deterministic tooling cannot
   distinguish reliably, leave it in guidance/review rather than approximating it
   with a noisy linter.

## Mechanism matrix

| Need | Good first choices | Notes |
| --- | --- | --- |
| whitespace, indentation, newline, charset | `.editorconfig`, formatter | Keep formatting ownership in one place where possible. |
| syntax/style normalisation | formatter or language linter | Prefer autofixable rules for purely mechanical choices. |
| naming and language idioms | language-native analyzer/linter | Verify exact rule support and scoping. |
| unsafe or error-prone constructs | compiler/analyzer/linter | Prefer correctness-oriented diagnostics over style-only warnings. |
| nullability/type strictness | compiler/build configuration | Treat enabling stricter modes as a migration, not a cosmetic toggle. |
| one type/class per file or file/type naming | analyzer/linter if supported; otherwise focused structural validation | `.editorconfig` alone cannot detect arbitrary repository structure unless an analyzer consumes the configured diagnostic. |
| forbidden dependency direction | architecture/dependency tests or dependency graph rules | Keep allowed boundaries explicit and testable. |
| package/module layering | architecture tests, build graph constraints, dependency linting | Scope carefully in monorepos. |
| required tests/files/metadata | repository-native validation script or CI check | Prefer deterministic file/schema checks over model judgement. |
| commit/process policy | hooks plus CI when appropriate | Local hooks improve feedback; CI is usually the reliable shared enforcement point. |
| design or business semantics | review, tests at the behavioural boundary, maintained guidance | Avoid pretending contextual judgement is lintable. |

## Ecosystem examples

These are mechanism examples, not requirements. Use the repository's existing
stack where possible.

### .NET / C#

Useful surfaces may include:

- `.editorconfig` for .NET code-style options and analyzer diagnostic severity;
- compiler/build settings in project files or shared build props;
- built-in .NET/Roslyn analyzers;
- already-installed analyzer packages such as Roslynator, StyleCop Analyzers, or
  project-specific analyzers;
- architecture tests for namespace/project/dependency boundaries;
- `dotnet format`, build, or test commands in CI.

Do not assume a package provides a particular rule ID. Inspect installed package
versions and their documentation/configuration first.

### JavaScript / TypeScript

Useful surfaces may include:

- EditorConfig for basic file settings;
- the repository's formatter, commonly Prettier or Biome;
- ESLint or another existing linter for AST-aware rules;
- TypeScript compiler strictness for type-safety expectations;
- dependency-boundary rules or architecture tests for module constraints;
- package scripts and CI as the execution point.

Avoid enabling overlapping formatting ownership in multiple tools unless the
repository already has a deliberate division of responsibility.

### Python

Useful surfaces may include:

- `pyproject.toml` or tool-specific configuration;
- Ruff, Flake8, Pylint, Black, or other already-adopted tools;
- type-checker configuration such as mypy or pyright when already present;
- import/dependency checks and architecture tests;
- pre-commit and CI execution.

Prefer one clear owner for each rule family rather than stacking equivalent
checks.

### Go

Useful surfaces may include:

- `gofmt`/`go fmt` for formatting;
- `go vet` and existing static-analysis tooling;
- an existing aggregate linter configuration if the project uses one;
- package/dependency tests for architectural rules;
- `go test` and CI validation.

Formatting conventions already owned by `gofmt` generally should not be
re-described as bespoke rules.

### Rust

Useful surfaces may include:

- `rustfmt`;
- compiler warnings/lints;
- Clippy configuration;
- crate/module tests for architectural invariants;
- Cargo commands in CI.

Prefer compiler/Clippy-supported semantics over custom text scanning.

### Java / Kotlin

Useful surfaces may include:

- formatter configuration;
- existing Checkstyle, SpotBugs, Error Prone, PMD, detekt, ktlint, or equivalent
  tooling when present;
- compiler settings;
- architecture tests/dependency rules;
- Gradle/Maven tasks wired into CI.

Do not introduce a second linter merely because it has one convenient rule if the
existing stack can express the same invariant adequately.

## Rollout patterns

### Clean repository, objective rule

If the rule has few/no violations and strong evidence:

1. add the narrow rule;
2. run the authoritative check;
3. fix only trivial safe violations if authorised;
4. make CI blocking once verified.

### Large legacy violation set

Prefer a ratchet:

1. record or scope the existing baseline;
2. block new violations;
3. remediate legacy violations separately;
4. tighten the baseline as debt falls.

Do not hide an unknown baseline behind broad suppressions that future maintainers
cannot explain.

### Mixed convention

Do not pick the majority automatically. Determine whether the difference is:

- module-specific and legitimate;
- evidence of an active migration;
- legacy drift;
- a genuine unresolved choice.

Only codify after the intended target is attributable.

### Explicit rule but weak enforcement

Treat this as an enforcement gap, not a discovery problem. Prefer wiring the
existing rule into the repository's shared verification path before adding new
rules.

## What not to encode

Avoid deterministic rules for preferences such as "make this code elegant",
"prefer the clearest abstraction", or "use a service when appropriate" unless
the repository has a narrower observable invariant that captures the real intent.

A convention is a good automation candidate when both the violation and the
corrective direction can be identified consistently without reconstructing broad
design intent.
