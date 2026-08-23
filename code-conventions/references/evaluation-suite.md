# Code Conventions evaluation suite

Use these paired cases when changing the skill's trigger description, evidence
rules, or routing boundaries. The goal is to verify that the skill activates for
convention discovery/codification while adjacent capabilities retain ownership of
their outcomes.

## Positive trigger cases

### 1. Infer and enforce a .NET structural convention

**Prompt**

> This C# repository appears to keep every class in its own file. Can you check
> whether that is really a project convention and suggest how we should enforce
> it? We already use Roslynator and EditorConfig.

**Expected**

- trigger `code-conventions`;
- inspect explicit config/tool versions before broad code sampling;
- treat class-per-file as a candidate until evidence establishes its status;
- prefer the existing analyzer stack if it can express the invariant;
- verify actual rule support rather than inventing a diagnostic ID;
- explain that EditorConfig may configure analyzer severity but is not by itself
  an arbitrary structural analyzer;
- recommend a staged rollout if existing violations are numerous.

### 2. Turn recurring review comments into tooling

**Prompt**

> Our reviewers keep asking for the same naming, async and dependency-boundary
> fixes. Look through the repo, identify which of those are actual conventions,
> and tell us which can become lint/analyzer/CI rules.

**Expected**

- trigger `code-conventions`;
- distinguish objective enforceable rules from judgement-heavy review guidance;
- rank opportunities by value, objectivity and effort;
- prefer existing tooling and shared CI execution.

### 3. Existing rules appear unenforced

**Prompt**

> We have ESLint and Prettier configs but the codebase is still inconsistent.
> Work out what is actually enforced and where the gaps are.

**Expected**

- trigger `code-conventions`;
- inspect package scripts and CI rather than assuming config files execute;
- distinguish configured, executed, non-blocking and drift states;
- avoid adding another formatter unless justified.

### 4. Monorepo with different local norms

**Prompt**

> Find the coding conventions in this monorepo. The backend and frontend were
> built by different teams, so don't assume they should be identical.

**Expected**

- trigger `code-conventions`;
- sample representative modules;
- preserve scoped conventions;
- avoid manufacturing a global majority rule.

### 5. Explicit guidance conflicts with prevalent code

**Prompt**

> CONTRIBUTING says we do constructor injection, but lots of services use a
> service locator. Which convention should tooling enforce?

**Expected**

- trigger `code-conventions`;
- classify the discrepancy as drift/conflict rather than voting by prevalence;
- preserve the explicit maintained source as higher authority unless evidence
  shows it is stale/superseded;
- avoid codifying a disputed target without resolving intent.

### 6. Codify an accepted convention

**Prompt**

> We've agreed nullable reference types should be enabled for all new C# projects.
> Update the shared build configuration and add the lightest check that prevents
> regressions.

**Expected**

- trigger `code-conventions` in codify mode;
- verify current shared build structure and compiler support;
- make a minimal change;
- avoid opportunistic warning cleanup;
- run the narrow authoritative verifier and report migration debt separately.

## Negative / adjacent-routing cases

### 7. LSP setup

**Prompt**

> Detect the languages in this repository and configure Copilot CLI language
> servers plus VS Code extension recommendations.

**Expected**

- do not use `code-conventions` as the primary skill;
- route to `lsp-config`.

### 8. Repository semantic model

**Prompt**

> Build an ontology of our services, domain concepts, events, schemas and their
> relationships so agents can traverse the repository semantically.

**Expected**

- do not trigger `code-conventions` as primary;
- route to `repository-ontology`.

### 9. Durable project context

**Prompt**

> Establish a maintained project context record that captures architecture,
> decisions, conventions, current truth and historical evidence for future agents.

**Expected**

- route primarily to `project-context`;
- `code-conventions` may later supply evidence for the conventions slice but does
  not own the context substrate.

### 10. Concrete PR review

**Prompt**

> Review PR #52 and tell me whether the change violates our standards or has any
> correctness/security problems.

**Expected**

- route primarily to `review`;
- convention evidence may be consulted as part of review context, but
  `code-conventions` should not replace the revision-bound review workflow.

### 11. General architecture decision

**Prompt**

> Should this system use vertical slices or a layered architecture?

**Expected**

- do not trigger `code-conventions` solely because either choice could later
  become a convention;
- use an architecture/planning workflow appropriate to the decision.

## Adversarial evidence cases

### 12. Generated code dominates the repository

**Setup**

- 80% of files are generated clients using one naming/layout pattern;
- maintained application code uses a different consistent pattern.

**Expected**

- generated code is excluded/down-weighted;
- no repository-wide convention is inferred from raw file counts.

### 13. Template clones look like independent evidence

**Setup**

- ten services were generated from the same template and retain identical
  structure;
- two independently maintained services differ.

**Expected**

- template repetition is not treated as ten independent confirmations;
- confidence reflects the weak independence of the evidence.

### 14. Mixed active migration

**Setup**

- older Python modules use one formatter/linter stack;
- recently changed modules and CI show migration to a newer established tool;
- both patterns remain common.

**Expected**

- identify migration/drift rather than reporting a simple mixed preference;
- use history/CI to resolve current direction when attributable;
- recommend a bounded migration or ratchet, not a majority vote.

### 15. Unlintable preference

**Prompt**

> The code usually uses small abstractions and avoids over-engineering. Add a
> linter rule so agents can't make designs too complicated.

**Expected**

- trigger only to assess enforceability;
- explain that the broad preference is not a reliable deterministic invariant;
- look for narrower observable rules if they exist;
- otherwise leave it to guidance/review rather than creating a noisy custom
  heuristic.

## Success criteria

A strong run should demonstrate all of the following:

- explicit evidence outranks prevalence;
- convention status, scope, confidence and conflicts remain visible;
- existing toolchains are extended before introducing overlapping dependencies;
- rule identifiers and tool capabilities are verified, not guessed;
- local configuration is distinguished from shared/CI enforcement;
- rollout avoids unnecessary mass rewrites;
- adjacent skills retain clean ownership boundaries;
- deterministic enforcement is recommended only for objectively detectable
  invariants.
