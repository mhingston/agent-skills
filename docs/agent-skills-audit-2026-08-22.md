# Agent Skills audit — 2026-08-22

This is a repository-wide review of every canonical top-level `SKILL.md` against the guidance in [`skill-creator/SKILL.md`](../skill-creator/SKILL.md).

## Scope

Reviewed 39 canonical skill packages on `main` at `68290920b273c9d7a86b44db5805c5d8f164d3f2`:

- 32 public skills;
- 7 workflow-internal modules.

The review covered:

1. discriminative frontmatter and routing boundaries;
2. the shortest useful path, proportional escalation, fallback/recovery, and checks;
3. evidence discipline, authority boundaries, stop conditions, and failure semantics;
4. progressive disclosure and direct use of packaged references;
5. deterministic helper contracts and representative/edge-case tests;
6. package portability and repository validation.

The `skill-creator` headings `Use when`, `Avoid when`, `Fast path`, `Full path`, `Fallback`, and `Checks` are treated as semantic requirements, not a mandatory visual template. A skill passes when those decisions are discoverable through equivalent modes, boundaries, stop conditions, recovery rules, or proportional-depth guidance. This avoids cosmetic rewrites that could change routing without measured benefit.

## Findings

### Repository-level controls

| Check | Result | Evidence / action |
| --- | --- | --- |
| Canonical package validation | Pass | CI runs the pinned official `skills-ref` validator for every top-level skill. |
| Active instruction size | Pass by policy | CI fails any `SKILL.md` over 500 lines. |
| Deterministic helper tests | Gap fixed | `lsp-config/scripts/detect-languages.mjs` was the only bundled deterministic script family without shipped tests. Added `detect-languages.test.mjs` and CI execution under Node 18. |
| Progressive disclosure | Pass | Optional detail is packaged within skill directories and linked from the owning `SKILL.md` when needed. |
| Behavioural evaluation discipline | Pass for this change | No routing description or workflow behaviour is changed in this audit, so a matched behavioural evaluation is not claimed or required. Future routing/behaviour changes should use the owning skill's matched evaluation where available. |
| Audit trail | Gap fixed | The README pointed to a missing 2026-07-21 audit file. This audit replaces that stale reference. |

### Skill-by-skill conformance

| Skill | Status | Notes |
| --- | --- | --- |
| `adopt` | Pass | Clear adoption boundary, bounded evidence transfer, decision rules, validation and escalation. |
| `agent-observability` | Pass | Strong adjacent-work routing, progressive evidence collection, deterministic trace-fitness checks and explicit limitations. |
| `agent-readiness` | Pass | Read-only boundary, evidence states, activity-specific autonomy caps, hard rules, remediation and quality gates. |
| `agent-workflow-design` | Pass | Clear routing, typed claims, deterministic authority, bounded retries, durable recovery, trajectory verification and quality gate. |
| `audit-me` | Pass | Read-only default, bounded audit contract, proportional delivery mechanism, uncertainty handling and reversible pilots. |
| `automation-reviewer` | Pass | Evidence-first baseline, bounded review scope, reversible experiments, validation and explicit mutation boundary. |
| `coach-me` | Pass | Evidence thresholds provide full/preliminary/watchlist paths; insufficient evidence is surfaced rather than filled with inference. |
| `code-research` | Pass | Smallest discriminating experiment, independent oracle, isolation, reproduction, falsification and stop conditions. |
| `contributor-analysis` | Pass | Explicit use/do-not-use/fast path, privacy boundaries, deterministic script contract and shipped tests. |
| `customer-friction-radar` | Pass | Explicit lightest-mode selection, no default full investigation, triangulation, quality checks and stop conditions. |
| `create-pr` | Pass | Tight mutation boundary, exact-revision evidence, optional semantic-tool fallback, proportionate checks and idempotent creation. |
| `decision-continuity` | Pass | Explicit use/adjacent routing, minimum sufficient evidence, provenance discipline, escalation and validation. |
| `dynamic-workflows` | Pass | Fast path, deterministic/adaptive modes, ACP/runtime fallbacks, version checks, routing evaluation reference and quality gate. |
| `engineering-attention` | Pass | Fast/slow/hybrid modes, current-state verification, falsification, bounded output and validation checks. |
| `engineering-evidence` | Pass | Clear non-performance boundary, evidence hierarchy, source-gap handling, proportional summaries and validation checks. |
| `gauntlet-loop` | Pass | Adjacent-work routing, explicit acceptance gate, bounded producer/critic loops, no-subagent fallback and revision-bound verification. |
| `git-archaeologist` | Pass | Fast path, calibrated history limits, deterministic script contract, shipped tests and stop conditions. |
| `lsp-config` | Fixed | Already had use/avoid/fast/full/verification paths and recovery rules. Added representative and important edge-case tests for the bundled detector and wired them into CI. |
| `memory-capture` | Pass | Fast/full paths, durability and authority gates, idempotent mutation, stale-write handling and read-back verification. |
| `memory-maintenance` | Pass | Explicit modes, scoped fast/full paths, propose/apply boundary, stale-write recovery and completion checks. |
| `memory-recall` | Pass | Fast/full retrieval paths, authority/freshness handling, bounded expansion and completion checks. |
| `organisational-intelligence` | Pass | Decision-first framing, minimum sufficient evidence, competing hypotheses, stop conditions and explicit quality bar. |
| `plan` | Pass | Focused/standard/critical depth, on-demand references, evidence/decision gates, replan triggers, stop conditions and quality gate. |
| `programmatic-tool-calling` | Pass | Harness detection, direct/native/script/composite/subagent routing, explicit fallbacks, bounded loops, reusable-workflow tests and matched evaluation guidance. |
| `reflection-engine` | Pass | Clear sibling routing, corpus boundary, focused/full modes, counterevidence and calibrated-confidence rules. |
| `review` | Pass | Explicit fast/full paths, single-context fallback, proportional dimensions, progressive references and evidence limitations. |
| `review-calibration` | Pass | Bounded calibration question, evidence compatibility, reversible proposal discipline and stop conditions. |
| `repository-ontology` | Pass | Assess/establish/evolve modes, minimum-sufficient representation, competency questions, evidence grounding and deterministic guard tests. |
| `session-lessons` | Pass | Explicit use/not-use boundaries, analysis-only default, evidence-source precedence, recurrence threshold and promotion separation. |
| `skill-creator` | Pass | Canonical rubric reviewed as the source of truth for this audit. |
| `teach-me` | Pass | Short start path, engine failure fallback, progressive references, deterministic scheduler/state helpers and dedicated Node 18/22 CI tests. |
| `wrap-up` | Pass | Single-session routing, bounded observation schema, safe persistence fallback, lifecycle-hook contract and shipped helper tests. |
| `implement-ticket` | Pass | Internal invocation contract, fail-closed orchestrator context, bounded mutation, falsifiable verification and explicit blocked/invalidation states. |
| `contract-reconciliation` | Pass | Internal invocation contract, exact state/source identity, bidirectional drift comparison and fail-closed indeterminate/invalidation semantics. |
| `explain-diff` | Pass | Internal invocation gate, exact-revision checks, evidence discipline, proportionate interaction, HTML contract and validation. |
| `human-verdict-gate` | Pass | Internal invocation gate, fail-closed design boundary, exact decision surface, evidence/provenance checks and unanswered-human-field contract. |
| `record-verdict` | Pass | Internal invocation gate, strict allowed values, structural fallback when schema tooling is unavailable, idempotent write and read-back verification. |
| `refine-ticket` | Pass | Internal invocation gate, authoritative readiness rubric, decomposition fallback, one-gap-at-a-time refinement and durable output contract. |
| `split-work` | Pass | Internal invocation gate, discovery/target/block fallbacks, vertical-slice rules, honest dependency edges and return-state checks. |

## Change made by this audit

The only skill implementation gap found was test coverage for the `lsp-config` detector. The added tests cover:

1. a representative multi-language repository while proving ignored dependency directories do not create false positives;
2. relative workspace resolution and case-insensitive manifest detection;
3. a missing workspace root as the documented recoverable scan-error path.

CI now installs Node 18 explicitly and runs this test alongside the other deterministic skill tooling tests.

## What this audit deliberately did not change

No skill descriptions, trigger boundaries, workflow bodies, or output contracts were rewritten merely to standardise headings. `skill-creator` explicitly treats routing as an empirical behaviour problem: changing descriptions or applicability without matched evaluation can regress skill selection even when the prose looks more uniform.

Likewise, this audit does not claim that static package validation proves behavioural task lift. For future material skill changes, use the smallest matched evaluation that can distinguish the proposed behaviour from the current baseline, including sibling-skill near misses when routing is changed.

## Re-run

Run the repository validation workflow or locally execute:

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
python3 wrap-up/scripts/test-wrap-up-hooks.py
node teach-me/scripts/learning-state.test.mjs
node teach-me/scripts/learning-engine.test.mjs
```
