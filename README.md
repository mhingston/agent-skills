# Agent Skills

A catalogue of reusable **Agent Skills** and orchestrating agent definitions for
software engineering, learning, workflow improvement, and accountable
AI-assisted delivery.

Skills are portable procedure packages. Agents coordinate skills, lifecycle,
state, delegation, and human responsibility boundaries.

New to the catalogue? Start with the [workflow guide](docs/workflows.md) to choose
a starting capability, see which skills commonly complement one another, and
avoid unnecessary composition.

## Repository structure

```text
agents/
  <agent-name>.md          # orchestration and workflow state

<skill-name>/
  SKILL.md                 # canonical Agent Skills entry point
  references/              # optional, loaded on demand
  scripts/                 # optional deterministic helpers
  assets/                  # optional output resources
```

## Packaging rules

Every skill is self-contained and can be installed by copying its own directory.

- The entry point is `<skill-name>/SKILL.md`.
- Supporting files live inside that skill's directory.
- A skill must not depend on a repository-level shared folder, parent path,
  another skill's directory, or an agent definition.
- Small process guidance may be duplicated when that preserves portability.
- Relative references should be direct from `SKILL.md`; avoid nested reference
  chains.
- Keep active `SKILL.md` instructions under 500 lines. Move optional detail into
  focused references.

Canonical frontmatter uses only specification fields:

```yaml
---
name: skill-name
description: What the skill does and when to use it.
license: Apache-2.0                # optional
compatibility: Requires git ...   # optional
metadata:                         # optional string mapping
  example.key: "value"
allowed-tools: Bash(git:*) Read   # optional, experimental
---
```

Runtime-specific properties must not be added as new top-level fields to the
canonical skill. Store portable extension information under namespaced
`metadata`, then translate it into a generated harness adapter when needed.

## Agent workflow artefacts

Repository-local supporting artefacts created by agents or skills use one
canonical root:

```text
.agent-artifacts/<work-branch>/<workflow>/<artifact>
```

Use the exact short work-branch name and preserve `/` as path separators. For
example, artefacts for `feature/PAY-1234` live under
`.agent-artifacts/feature/PAY-1234/`. A PR-scoped workflow uses the PR head
branch; a working-tree workflow uses the active branch. When no named branch can
be resolved for a revision-bound operation, use
`.agent-artifacts/detached/<full-head-sha>/...`.

Revision-sensitive workflows should add a revision directory beneath the
workflow when one is available, for example:

```text
.agent-artifacts/feature/PAY-1234/review/<head-sha>/report.md
.agent-artifacts/feature/PAY-1234/review/<head-sha>/risk-map.json
.agent-artifacts/feature/PAY-1234/implement/<commit-sha>/implementation-evidence.json
.agent-artifacts/feature/PAY-1234/create-pr/<head-sha>/body.md
```

For an uncommitted working-tree review, use a clearly non-revision label such as
`review/working-tree/` and bind the artefact content to the reviewed base plus
working-tree evidence or digest.

This root is intentionally suitable for a single `.gitignore` entry. Before
writing repository-local supporting artefacts, verify the root is ignored and
contains no tracked files. Never add or modify ignore rules implicitly. If the
canonical root is not safely ignored, return the artefact inline or keep it in
orchestration state when possible; if an on-disk artefact is required to
continue, stop with the missing storage prerequisite rather than writing to an
arbitrary repository path or external temporary directory.

The convention applies to workflow-supporting outputs such as review reports,
risk maps, implementation-evidence packets, resumable checkpoints, generated
handoffs, and temporary PR bodies. It does not relocate user-requested product
or repository deliverables that are meant to be tracked as part of the change.

## Public and internal skills

Public skills may be invoked directly. Workflow-internal modules sit behind an
agent interface and fail closed without the owning agent's orchestration state.

Internal modules use canonical metadata such as:

```yaml
metadata:
  mhingston.internal: "true"
  mhingston.owner-agent: "pr-review"
  mhingston.user-invocable: "false"
```

This metadata communicates intent but is not an authorization boundary. The
module's body must still require its owning agent's exact context and return
`REQUIRED_ORCHESTRATOR_CONTEXT` when invoked directly. A runtime adapter may map
the metadata to its native visibility mechanism.

## Agent catalogue

| Agent | Use it for |
| --- | --- |
| [`implement`](agents/implement.md) | Orchestrate a ready ticket through a ticket-keyed feature branch, delegated behaviour-first implementation with falsifiable verification, independent technical review, explicit contract reconciliation, full build/test gates, and pull-request creation. |
| [`pr-review`](agents/pr-review.md) | Require a current independent technical review and revision-bound risk map, provide proportionate comprehension support, redirect unresolved architecture decisions upstream, prepare explicit human judgement, and record the human verdict without approving or merging. |
| [`refine`](agents/refine.md) | Classify selected work, clarify unresolved decisions, refine one bounded ticket or split larger clear work into agent-ready vertical slices, resolve publication targets, and update the selected tracker after human approval. |

## Suggested workflows

The catalogue is composable rather than one mandatory SDLC. Start with the
smallest workflow that owns the outcome; add adjacent skills only when their
extra evidence or control is useful. Square brackets below indicate optional
stages rather than required ceremony.

| Goal | Suggested flow | Notes |
| --- | --- | --- |
| Deliver a ticket | `refine` → [`plan`] → `implement` → [`pr-review`] | `plan` is useful when design or uncertainty deserves a separate non-mutating pass. `implement` already owns implementation, independent technical review, contract reconciliation, final project gates, and `create-pr`. Add `pr-review` when the formal human-verdict lifecycle is required. |
| Isolate an unclear bug or regression | `fault-isolation` → [`plan`] → `implement` | Use `fault-isolation` when the causal mechanism is not established. Hand off the supported root cause, minimised reproducer, and candidate regression oracle; skip the diagnostic stage when the defect and oracle are already known. |
| Reconcile a conflicted Git integration | `integration-reconciliation` | Standalone flow for an active merge, rebase, or cherry-pick. It reconstructs both sides' intent, preserves compatible behaviour, validates the integrated state, and blocks rather than inventing a product decision when authority is unresolved. |
| Adopt coding agents in a repository | `agent-readiness` → targeted remediation → reassess | Route gaps to the owning capability such as `project-context`, `repository-ontology`, `agent-observability`, or `agent-workflow-design`; readiness itself remains an assessment, not a remediation workflow. |
| Reduce coding-convention drift | `code-conventions` → targeted codification → CI verification | Mine explicit and implicit conventions, choose only objective high-value rules, extend the existing formatter/linter/analyzer stack, and roll out with baselines or no-new-violations where legacy debt is material. |
| Design an agent system | `agent-readiness` → `agent-workflow-design` → `agent-observability` | Add `programmatic-tool-calling` for bounded multi-tool loops. Use `dynamic-workflows` when Mastra is specifically the executable runtime. |
| Improve skills from experience | `wrap-up` → `session-lessons` → `skill-creator` | One run produces observations; longitudinal evidence qualifies durable changes; `skill-creator` evaluates proposed revisions. A validated escaped defect may seed regression evaluation early but does not bypass the codification gate. |
| Adopt an external practice | `adopt` → existing owning skill or agent → `skill-creator` evaluation | Prefer strengthening the existing responsibility over adding a parallel workflow. Use a new skill only when the source reveals a genuinely distinct reusable contract. |
| Maintain durable project context | `project-context` + `decision-continuity` + [`repository-ontology`] | `project-context` owns the durable substrate, `decision-continuity` protects attributable accepted direction, and ontology is optional when semantic traversal or validation earns its cost. |
| Maintain shared organisational memory | `memory-recall` → work → `memory-capture` → periodic `memory-maintenance` | Shared memory complements project context and canonical sources; it does not automatically become authoritative over them. |
| Review and improve review | `review` or `pr-review` → accumulated revision-bound evidence → `review-calibration` | Use `review` for standalone technical review, `pr-review` for the orchestrated PR/human-verdict lifecycle, and `review-calibration` for evidence-backed changes to review policy. |
| Execute quality-sensitive parallel work | accepted plan/specification → `gauntlet-loop` | Use when dependency-aware fan-out plus independent adversarial verification earns its overhead. It does not replace planning, source authority, or human decisions. |

## Choosing related skills

Several skills are deliberately adjacent without being substitutes for each
other:

| If you need to... | Use | Rather than |
| --- | --- | --- |
| Decide how much coding-agent autonomy an environment can safely support | `agent-readiness` | using `agent-workflow-design` as a maturity assessment |
| Design the workflow/state machine around agents | `agent-workflow-design` | treating `agent-readiness` as an implementation design |
| Make an agent workflow reconstructable from traces and receipts | `agent-observability` | treating observability as correctness or approval |
| Implement a Mastra-owned executable workflow | `dynamic-workflows` | using it for runtime-neutral workflow design |
| Optimize a bounded repeated multi-tool stage | `programmatic-tool-calling` | building a full workflow runtime around one loop |
| Discover project coding norms and turn objective ones into deterministic checks | `code-conventions` | using `review` as a style-mining workflow or treating code prevalence as policy |
| Configure repository language-server wiring | `lsp-config` | using convention discovery to manage editor/LSP integration |
| Establish durable project truth/intent/history/scratch relationships | `project-context` | turning shared memory or an ontology into a second source of truth |
| Model repository entities and semantic relationships | `repository-ontology` | using ontology machinery for ordinary project documentation |
| Preserve accepted/rejected/deferred direction across resumed work | `decision-continuity` | reconstructing intent from implementation or chat history |
| Isolate why a concrete bug, regression, flake, or slowdown is happening | `fault-isolation` | using `code-research` for a reported failure or jumping straight to implementation from a plausible theory |
| Establish uncertain runtime/library/compatibility semantics with a controlled experiment | `code-research` | inventing a concrete failure just to fit `fault-isolation` |
| Reconcile an active merge/rebase/cherry-pick conflict from both sides' intent | `integration-reconciliation` | using generic `decision-continuity` or code review to edit conflict markers |
| Retrieve or persist reusable shared organisational knowledge | `memory-recall` / `memory-capture` | treating shared memory as canonical project state |
| Review one concrete change | `review` | using historical `review-calibration` as a reviewer |
| Run the full PR evidence and human-verdict lifecycle | `pr-review` | expecting standalone `review` to approve or merge |
| Improve review dimensions, thresholds, or routing from historical evidence | `review-calibration` | silently changing review policy inside a single review |
| Capture useful evidence from one ending session | `wrap-up` | promoting a one-off observation directly into durable guidance |
| Find recurring patterns across sessions and PR lifecycles | `session-lessons` | using one session as proof of a general rule |
| Create or revise a reusable skill and measure its effect | `skill-creator` | treating a lesson or incident as an automatic skill change |
| Get a quick plain-language orientation to an unfamiliar topic | `eli5` | using `teach-me`'s tutoring, assessment, and durable-learning workflow |

## Public skill catalogue

| Skill | Use it for |
| --- | --- |
| [`adopt`](adopt/SKILL.md) | Transfer evidence-backed mechanisms from an external source into a concrete target context. |
| [`agent-observability`](agent-observability/SKILL.md) | Design or assess correlated, revision-aware telemetry for agent runs, model/tool calls, handoffs, evaluators, retries, recovery, cost, and termination without reconstructing missing evidence or over-retaining sensitive payloads. |
| [`agent-readiness`](agent-readiness/SKILL.md) | Assess the highest safely supported coding-agent autonomy from evidence about specifications, repository context, reproducibility, verification, architecture, tooling, security, human control, observability, recovery, and delivery. |
| [`agent-workflow-design`](agent-workflow-design/SKILL.md) | Design durable agentic workflows and state machines with deterministic orchestration, bounded model judgement, structured claim handoffs, independent gates, enforced authority boundaries, resumability, and trajectory verification. |
| [`audit-me`](audit-me/SKILL.md) | Audit recurring work and connected work surfaces for dropped commitments, fragmented context, and automation opportunities. |
| [`automation-reviewer`](automation-reviewer/SKILL.md) | Evaluate scheduled prompts and reusable skills from run evidence, then propose reversible changes without silently modifying automation policy. |
| [`coach-me`](coach-me/SKILL.md) | Analyse the current user's real AI-session evidence and produce focused coaching and a personalised working manual. |
| [`code-conventions`](code-conventions/SKILL.md) | Discover evidence-backed coding and repository conventions, distinguish explicit policy from emergent patterns and drift, and map worthwhile objective rules to the lightest deterministic formatter, linter, analyzer, architecture-test, hook, or CI enforcement. |
| [`code-research`](code-research/SKILL.md) | Resolve uncertain technical claims with bounded, isolated, reproducible experiments, independent oracles, raw evidence, and exact rerun instructions. |
| [`contributor-analysis`](contributor-analysis/SKILL.md) | Find evidence-backed reviewer candidates, stewardship coverage, onboarding contacts, and continuity questions without profiling people or ranking performance. |
| [`customer-friction-radar`](customer-friction-radar/SKILL.md) | Analyse and validate evidence-backed customer-journey friction across reviews, complaints, assisted-service interactions, digital telemetry, and operational signals. |
| [`create-pr`](create-pr/SKILL.md) | Inspect a committed branch, carry current technical-risk evidence into a behaviour-first PR description, and create one reviewable pull request. |
| [`decision-continuity`](decision-continuity/SKILL.md) | Reconcile resumed work and current proposals against attributable accepted, rejected, deferred, superseded, and open decisions without silently changing direction. |
| [`dynamic-workflows`](dynamic-workflows/SKILL.md) | Build executable Mastra dynamic workflows whose runtime owns orchestration while ACP-compatible coding workers remain swappable across harnesses. |
| [`eli5`](eli5/SKILL.md) | Give a concise, adult, plain-language orientation to an unfamiliar topic, with a rendered story graphic for flow-based concepts when artifact support is available. |
| [`engineering-attention`](engineering-attention/SKILL.md) | Produce a small evidence-backed brief of blockers, commitments, stale work, review obligations, and engineering risk that needs attention now. |
| [`engineering-evidence`](engineering-evidence/SKILL.md) | Preserve factual engineering outcomes, decisions, reliability work, and enablement evidence without turning activity into performance judgement. |
| [`fault-isolation`](fault-isolation/SKILL.md) | Diagnose hard bugs, regressions, flaky failures, and performance problems by building a reproducible symptom signal, minimising the failure, testing competing hypotheses, and handing off root-cause and regression-oracle evidence without implementing the fix. |
| [`gauntlet-loop`](gauntlet-loop/SKILL.md) | Execute large or quality-sensitive work through dependency-aware fan-out, independent adversarial verification, and bounded producer-critic loops against an explicit acceptance contract. |
| [`git-archaeologist`](git-archaeologist/SKILL.md) | Use calibrated repository-history signals to prioritise deeper code, ownership, and operational investigation. |
| [`integration-reconciliation`](integration-reconciliation/SKILL.md) | Resolve active merge, rebase, or cherry-pick conflicts by reconstructing both sides' intent and authority, composing compatible changes, blocking on unsupported semantic choices, and validating the integrated result before continuing Git. |
| [`lsp-config`](lsp-config/SKILL.md) | Detect repository languages and safely reconcile GitHub Copilot CLI LSP configuration and VS Code recommendations. |
| [`memory-capture`](memory-capture/SKILL.md) | Persist durable shared project knowledge, decisions, and procedures to a configured Confluence memory area with stable identity, provenance, uncertainty, idempotent updates, and verified writes. |
| [`memory-maintenance`](memory-maintenance/SKILL.md) | Audit and repair duplicate, stale, conflicting, weakly sourced, or noisy Confluence shared memory and produce bounded source-linked digests without erasing history. |
| [`memory-recall`](memory-recall/SKILL.md) | Retrieve the smallest sufficient task-relevant context from a configured Confluence shared-memory area while preserving source authority, lifecycle, freshness, and conflicts. |
| [`organisational-intelligence`](organisational-intelligence/SKILL.md) | Turn fragmented organisational evidence into a bounded, traceable decision brief using claim-specific source authority, semantic context where useful, explicit reasoning frameworks, competing hypotheses, and human-verifiable recommendations. |
| [`plan`](plan/SKILL.md) | Create evidence-grounded, non-mutating implementation and investigation plans for software-engineering work. |
| [`programmatic-tool-calling`](programmatic-tool-calling/SKILL.md) | Design bounded multi-tool orchestration with native programmatic runtimes or safe fallbacks. |
| [`project-context`](project-context/SKILL.md) | Establish or assess a durable agent-readable project context record with explicit source authority, truth/intent/history/scratch separation, deterministic validation, task orientation, projection reconciliation, and evidence-derived state. |
| [`reflection-engine`](reflection-engine/SKILL.md) | Perform evidence-grounded longitudinal self-reflection across accessible personal history, with counterevidence, calibrated confidence, and concrete behavioural tests. |
| [`review`](review/SKILL.md) | Perform a standalone read-only review, falsify candidate findings, assess test-oracle quality and regression sensitivity, record reviewer provenance, and produce a revision-bound technical risk map. |
| [`review-calibration`](review-calibration/SKILL.md) | Evaluate historical review evidence and propose reversible, human-governed changes to dimensions, thresholds, falsification, and reviewer routing. |
| [`repository-ontology`](repository-ontology/SKILL.md) | Assess whether a repository needs an ontology and establish the smallest evidence-backed semantic model. |
| [`session-lessons`](session-lessons/SKILL.md) | Analyse multiple sessions for recurring friction and effective patterns that deserve durable codification. |
| [`skill-creator`](skill-creator/SKILL.md) | Create, improve, validate, and evaluate Agent Skills. |
| [`teach-me`](teach-me/SKILL.md) | Run measured tutoring, review, and learning-coach loops with durable receipts and transfer evidence. |
| [`wrap-up`](wrap-up/SKILL.md) | Capture material lessons from one completed agent session as structured observations for later longitudinal analysis, with optional opt-in lifecycle hooks for Claude Code and Codex. |

## Workflow-internal modules

| Module | Owning agent | Owned stage |
| --- | --- | --- |
| [`implement-ticket`](implement-ticket/SKILL.md) | `implement` | Implement or remediate one bounded ticket with a behaviour-first verification map and observed evidence. |
| [`contract-reconciliation`](contract-reconciliation/SKILL.md) | `implement` | Compare the reviewed implementation with the immutable accepted ticket contract and surface implementation drift or contract invalidation before final gates. |
| [`explain-diff`](explain-diff/SKILL.md) | `pr-review` | Build a causal explainer for moderate or high comprehension risk. |
| [`human-verdict-gate`](human-verdict-gate/SKILL.md) | `pr-review` | Prepare a revision-specific decision packet with unanswered human fields. |
| [`record-verdict`](record-verdict/SKILL.md) | `pr-review` | Persist explicit human judgement and material-risk dispositions for one exact revision. |
| [`refine-ticket`](refine-ticket/SKILL.md) | `refine` | Assess and draft one bounded work item against the readiness contract. |
| [`split-work`](split-work/SKILL.md) | `refine` | Decompose a clear multi-ticket outcome into vertical slices and an acyclic dependency graph. |

## Responsibility boundaries

1. Evidence is not approval.
2. Explanation is not proof of correctness.
3. Technical severity is not policy disposition.
4. A policy threshold is not a human verdict.
5. Model-generated rationale or risk acceptance is not human judgement.
6. A review artefact or verdict applies only to the exact revision it names.
7. Green checks cannot silently replace explicit risk acceptance.
8. Automation may enforce a recorded verdict but must not invent one.
9. Agents coordinate capabilities; they do not erase responsibility boundaries.
10. Portability and correct skill-loading boundaries take priority over avoiding
    small amounts of duplicated guidance.
11. Review calibration may propose policy experiments but must not silently change
    thresholds, reviewer topology, required dimensions, or approval rules.
12. Decision continuity may identify drift and propose supersession, but must not
    silently rewrite accepted direction or manufacture decision authority.
13. Contract reconciliation may classify implementation drift or invalidate the
    current contract from evidence, but it must not revise canonical intent or
    accept a deviation as a second source of truth.
14. Shared memory is durable context, not automatic authority over a designated
    canonical source for the same claim.
15. Memory capture and maintenance must preserve provenance, uncertainty,
    supersession, and conflict; derived digests must not become source truth.
16. Project-context indexes and projections may encode explicit source authority
    and derived state, but they must not invent authority or become a competing
    source of truth for claims owned elsewhere.
17. Code prevalence is evidence of a candidate convention, not automatic policy;
    codification must preserve stronger explicit authority, scope, and conflicts.
18. Fault isolation may support or narrow a causal explanation, but diagnosis is
    not implementation and containment is not automatically root-cause proof.
19. Integration reconciliation may compose evidence-supported active intent, but
    eliminating conflict markers or completing Git does not grant authority to
    invent, supersede, or accept product behaviour.

## Validation

Validation has two distinct layers. A green result in one layer must not be
reported as evidence from the other.

### Static and deterministic validation

The repository validates every top-level skill on pushes and pull requests using
the official `skills-ref` validator pinned to a reviewed upstream commit. It also
enforces the repository's 500-line active-instruction policy and runs bundled
deterministic script tests. These checks establish package, format, and helper-tool
integrity; they do **not** establish that a changed skill improves agent behaviour.

Local validation:

```bash
python -m pip install \
  "git+https://github.com/agentskills/agentskills.git@38a2ff82958afee88dadf4831509e6f7e9d8ef4e#subdirectory=skills-ref"
for skill_md in */SKILL.md; do
  skills-ref validate "$(dirname "$skill_md")"
done

python3 skill-creator/scripts/test-aggregate-evals.py
python3 contributor-analysis/scripts/test-analyse-contributors.py
python3 git-archaeologist/scripts/test-analyse-history.py
node --test lsp-config/scripts/detect-languages.test.mjs
python3 repository-ontology/scripts/test-ontology-guard.py
python3 project-context/scripts/test-validate-context-record.py
python3 wrap-up/scripts/test-wrap-up-hooks.py
node teach-me/scripts/learning-state.test.mjs
node teach-me/scripts/learning-engine.test.mjs
```

### Behavioural evaluation

When a material skill change can be executed in a real deployment or reference
harness, compare the candidate with the exact base-revision skill package under
matched prompts, fixtures, model, harness, permissions, tools, and verifier.
Behavioural evaluation is additional evidence, not a reinterpretation of static
CI. If the required harness, credentials, baseline, or verifier is unavailable,
report the behavioural result as `NOT_RUN` or `BLOCKED` rather than treating green
static validation as a behavioural pass.

See [`skill-creator`](skill-creator/SKILL.md) and
[`skill-creator/references/ci-evaluation.md`](skill-creator/references/ci-evaluation.md)
for the evaluation and CI contracts.

## Installation

Copy each required public skill directory into the location used by the target
agent harness. Install canonical agent definitions from `agents/` separately and
adapt them to the harness's agent format.

When a harness supports generated adapters, translate namespaced metadata there;
do not fork the canonical `SKILL.md` merely to add non-standard top-level fields.