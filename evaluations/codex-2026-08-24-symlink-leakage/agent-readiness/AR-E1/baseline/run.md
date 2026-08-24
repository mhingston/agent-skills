# Run record

- Case: `AR-E1`
- Condition: `baseline`
- Prompt: We want to start using coding agents in this repository. Assess what kinds of agent work it can safely support today and what evidence would be needed before we let an agent implement a ready ticket unattended. Do not change the repo.
- Expected routing: `agent-readiness`
- Loaded skills observed in Codex events: `none`
- Final response:

## Assessment

**Status: Not ready for unattended ticket implementation.**

The safely supported ceiling today is **A1 — read-only assistance**. Agents can inspect the available material, explain it, check documentation consistency, refine user-supplied requirements, and draft plans. There is not enough repository-local evidence for agent-authored changes, even under an “implementation-ready” ticket.

This assessment covers the current checkout as observed on 24 August 2026. If it is an incomplete export rather than the canonical repository, the missing canonical checkout should be assessed instead.

## What agents can safely do now

| Activity | Current support | Conditions |
|---|---|---|
| Explain or summarize repository documentation | Supported | Read-only; clearly identify missing referenced material |
| Review specifications for ambiguity | Supported | The specification must be supplied by a human; conclusions remain advisory |
| Draft implementation or investigation plans | Supported | No claim that paths, commands, or architecture have been validated |
| Documentation consistency analysis | Supported | Report broken/missing references; do not infer the absent implementation |
| Isolated experiments outside the repository | Conditional | Human-controlled, no claim that results represent this repository |
| Supervised repository edits | Unsupported on current evidence | No recoverable baseline or executable verification exists |
| Unattended implementation of one ready ticket | Unsupported | Fails source, isolation, verification, review, recovery, and delivery gates |
| PR creation, parallel implementation, merge, or deployment | Unsupported | No remote, history, CI, integration model, or operational controls are evidenced |

Even apparently low-risk README edits should remain human-executed or directly supervised until there is a committed baseline and deterministic validation.

## Key evidence

- **E1:** `git status` reports `No commits yet on master`; both `.codex/` and `README.md` are untracked. Git contains zero objects and no remote is configured.
- **E2:** The only ordinary file in the checkout is [README.md](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6ngprrzz/repo/README.md:1). There is no source tree, test tree, package manifest, lockfile, CI workflow, `AGENTS.md`, `.gitignore`, or executable project tooling.
- **E3:** The README describes an intended repository layout containing `agents/`, top-level skill packages, scripts, and assets ([lines 10–35](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6ngprrzz/repo/README.md:10)), but those paths are absent.
- **E4:** It describes an `implement` agent with independent review, contract reconciliation, full gates, and PR creation ([line 121](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6ngprrzz/repo/README.md:121)); the referenced `agents/implement.md` is absent.
- **E5:** It documents local validators and script tests ([line 263](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6ngprrzz/repo/README.md:263)), but none of their referenced files are in this checkout. The claim that they run on pushes and PRs cannot be verified because `.github/workflows` is absent.
- **E6:** `.codex/skills` contains three untracked symlinks into `/home/mark/Projects/agent-skills`. These are machine-local dependencies, not revision-bound repository content.
- **E7:** The README correctly distinguishes static validation from behavioural evaluation and requires unavailable behavioural evidence to be reported as `NOT_RUN` or `BLOCKED` ([lines 296–304](/home/mark/.local/state/codex-desktop/tmp/agent-skills-eval-6ngprrzz/repo/README.md:296)).
- **I1:** The README likely represents a fuller repository that was not copied or checked out here. That would explain the many missing links, but it does not make this checkout safe to mutate.
- **U1:** Ticket system, ownership, security policy, branch protection, agent runtime permissions, CI history, evaluation history, and deployment boundaries were not available.

## Readiness matrix

| Dimension | Status | Why it limits autonomy |
|---|---|---|
| Ticket/specification contract | Unknown | No sample ready ticket, canonical source, versioning, or readiness gate |
| Repository context and authority | Unsupported | Documentation references absent files; no scoped repository instructions |
| Reproducible environment | Unsupported | No pinned toolchain, dependency lock, setup procedure, or clean-build evidence |
| Verification reach | Unsupported | Documented commands cannot run against the absent files; no acceptance-to-test traceability |
| Architecture and change isolation | Unknown | No implementation is present to assess boundaries or blast radius |
| Security and least privilege | Unknown | No executor permission profile, credential isolation, network policy, or protected paths |
| Human control and ownership | Partial | The README states sound responsibility boundaries, but no enforced workflow or named authorities are evidenced |
| Independent review | Unsupported | The described reviewer and exact-revision review mechanism are absent |
| Observability and recovery | Unsupported | No committed base, run receipts, durable checkpoints, rollback exercise, or revision identity |
| Integration and delivery | Unsupported | No remote, CI configuration, protected branch, required checks, or PR evidence |
| Parallel-agent safety | Unsupported | No isolated worktree strategy, dependency ownership, or conflict reconciliation evidence |

## Evidence required before unattended implementation

For **A3 — one bounded ready ticket**, require all of the following as pass/fail gates:

1. **Recoverable canonical baseline**
   - A real committed repository with a configured canonical remote.
   - Clean ticket-specific branch or isolated worktree pinned to an exact base SHA.
   - Demonstrated reset/recreate procedure.
   - Agent artefact storage either safely ignored or kept outside the change.

2. **Durable ready-ticket contract**
   - Versioned ticket identity and immutable snapshot for the run.
   - Observable outcome, acceptance criteria, constraints, invariants, non-goals, dependencies, and affected areas.
   - Explicit product, architecture, security, data, and operational escalation owners.
   - A refinement gate that rejects unresolved consequential decisions.

3. **Authoritative repository context**
   - Committed, scoped agent/contributor instructions.
   - Actual architecture, interface, generated-file, migration, and test conventions.
   - Clear source-of-truth and conflict-resolution rules.
   - Representative evaluations showing that agents use these instructions correctly—not merely that the files exist.

4. **Reproducible isolated executor**
   - Pinned toolchain and locked dependencies.
   - Clean-environment setup repeatedly demonstrated in CI or an equivalent disposable environment.
   - Network disabled by default, no ambient credentials, safe non-production fixtures, and an enforced write scope.
   - Logs that distinguish setup failures from product failures.

5. **Falsifiable verification**
   - Focused and full verification commands that actually exist and pass from a clean checkout.
   - Each acceptance criterion and material invariant mapped to a check capable of detecting a plausible wrong implementation.
   - Zero-test detection, deterministic fixtures, known flake policy, and failure examples.
   - For defects, a stable pre-fix regression oracle; for risky refactors, characterization coverage.
   - Evidence from seeded defects or mutation testing where ordinary green tests do not demonstrate oracle sensitivity.

6. **Independent exact-revision gates**
   - CI runs required checks against the precise proposed commit.
   - Independent technical review produces a revision-bound result.
   - The implementer cannot self-approve, weaken required checks, alter protected oracles unnoticed, merge, or deploy.
   - Contract reconciliation detects missing, contradicted, or extra-scope behaviour.

7. **Budgets, observability, and safe stopping**
   - Limits for time, attempts, tool calls, cost, changed paths, and patch size.
   - Correlated records of ticket/version, base and result SHAs, instructions/model/harness versions, commands, results, retries, side effects, and termination reason.
   - Tested `BLOCKED` and `CONTRACT_INVALIDATED` paths rather than pressure to “finish.”
   - Demonstrated cancellation, resume, cleanup, and uncertain-side-effect reconciliation.

8. **Human-controlled publication**
   - Branch protection and required checks verified with a test PR.
   - Named human authority for risk acceptance and merge.
   - No production credentials, autonomous merge, or deployment in the implementation role.

The decisive proof should be a set of representative, bounded pilot tickets executed in disposable workspaces. Include success cases and adversarial cases: ambiguous requirements, failing setup, pre-existing test failure, attempted scope expansion, protected-oracle modification, secret-like input, and a ticket that must stop for a human decision. Retain exact run evidence and human review outcomes.

## Recommended sequence

1. Restore or identify the complete canonical repository and create a committed baseline.
2. Make one clean-environment validation path real and CI-enforced.
3. Establish the ready-ticket contract and authority/escalation rules.
4. Demonstrate isolated least-privilege execution and recovery.
5. Run supervised pilot tickets, measure escapes and human corrections, then reassess for A3.

Do not pursue parallel agents, autonomous PR publication, merge, or deployment until single-ticket A3 operation has demonstrated reliable exact-revision verification and safe stopping.

No repository files or external state were changed.

Outcome checks remain `not_verifiable` until reviewed against the suite rubric.
