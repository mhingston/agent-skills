# Agent Skills specification audit — 2026-07-21

## Scope

This audit reviewed every top-level `SKILL.md` in `mhingston/agent-skills` at
baseline revision:

```text
cc0546370db34c10f31bebd4aa3af86720f60cf4
```

The review used the current canonical guidance:

- <https://agentskills.io/specification>
- <https://agentskills.io/skill-creation/best-practices>
- <https://agentskills.io/skill-creation/optimizing-descriptions>
- <https://agentskills.io/skill-creation/evaluating-skills>
- <https://agentskills.io/skill-creation/using-scripts>

Canonical structural validation is pinned to `skills-ref` revision:

```text
38a2ff82958afee88dadf4831509e6f7e9d8ef4e
```

## Method

Each skill was checked for:

1. valid directory and `SKILL.md` structure;
2. canonical frontmatter fields and constraints;
3. a description covering both capability and trigger conditions;
4. explicit applicability boundaries and failure behaviour;
5. proportionate active instructions and progressive disclosure;
6. direct, valid resource references;
7. deterministic script suitability, dependencies, errors, and tests;
8. output and validation contracts;
9. stale, task-specific, or unsupported assumptions;
10. evaluation readiness.

This was a specification and qualitative best-practices audit. It did **not** run
matched behavioural evaluations for all skills across deployment harnesses.
Consequently, the audit does not claim measured task lift, triggering precision,
or cross-harness parity. Those require curated positive and near-miss query sets,
matched baselines, repeat runs, and task-specific verifiers.

## Repository-level findings

### Fixed: non-standard top-level frontmatter

Six internal modules used `user-invocable: false` as a top-level field. The
canonical specification permits only `name`, `description`, `license`,
`compatibility`, `metadata`, and experimental `allowed-tools`.

The modules now use namespaced string metadata:

```yaml
metadata:
  mhingston.internal: "true"
  mhingston.owner-agent: "pr-review"
  mhingston.user-invocable: "false"
```

This metadata is descriptive, not an authorization boundary. Each internal skill
retains a fail-closed invocation contract and refuses work without the owning
agent's exact orchestration context. Harness-specific visibility should be
generated from metadata rather than added to canonical frontmatter.

### Fixed: active-context size

`repository-ontology/SKILL.md` was 662 lines. It has been reduced to the core
selection and modelling workflow. Formal ontology detail and output schemas now
live in two directly linked references loaded only when required.

### Added: repeatable validation

`.github/workflows/validate-skills.yml` now:

- installs the official reference validator at a pinned upstream revision;
- validates every top-level skill directory;
- rejects `SKILL.md` files above the repository's 500-line policy;
- runs the deterministic Git-history collector tests.

### Added: calibrated deterministic history analysis

`git-archaeologist` previously mixed mechanical Git counts with unsupported
claims about dangerous files, bus factor, departures, velocity, team health, and
operational stability. It now separates signals from interpretation and includes
a standard-library, read-only JSON collector with representative and failure-case
tests.

## Per-skill result

| Skill | Result | Audit outcome |
| --- | --- | --- |
| `adopt` | Pass | Description is discriminative; mechanism-transfer workflow has explicit evidence, fit, reversibility, and rejection rules. Detailed scoring remains in a direct reference. |
| `audit-me` | Pass | Strong scope, human-responsibility boundary, prioritisation, pilot, and deployment-ready output contract. |
| `coach-me` | Improved | Removed frozen research statistics and the use of Git prose as a proxy for AI prompting. The benchmark is refreshed from its canonical source, direct session evidence is primary, and sample/transfer caveats are explicit. |
| `create-pr` | Improved | Removed the repository-specific Jira base URL and made work-item links conditional on a verified source. Added portable compatibility and preserved idempotency, risk-map freshness, and human-verdict boundaries. |
| `explain-diff` | Fixed and focused | Replaced invalid top-level runtime metadata, retained fail-closed ownership, and reduced duplicated prose while preserving causal investigation, safe self-contained HTML, interaction, validation, and unanswered human explain-back. |
| `git-archaeologist` | Reworked | Replaced overclaiming heuristics with evidence-calibrated signals, corroboration steps, interpretation limits, a deterministic script, and tests. |
| `human-verdict-gate` | Fixed and focused | Replaced invalid top-level runtime metadata and retained revision pinning, risk-map completeness, unanswered human fields, readiness statuses, and no-verdict boundary. |
| `implement-ticket` | Fixed | Moved internal visibility data under canonical metadata. RED/GREEN evidence, isolated execution, scope, and orchestrator ownership remain unchanged. |
| `lsp-config` | Pass | Clear use/avoid conditions, fast and full paths, additive merge invariants, script requirements, error handling, and verification loop. Runtime requirements are already explicit in the active instructions. |
| `programmatic-tool-calling` | Pass | Strong bounded-stage selection, harness routing, authorization, evidence preservation, failure controls, and matched-evaluation guidance. |
| `record-verdict` | Fixed and focused | Replaced invalid top-level runtime metadata and retained exact-revision binding, human-only judgement fields, schema/template resources, safe serialization, idempotent persistence, and no-merge boundary. |
| `refine-ticket` | Fixed | Moved internal visibility data under canonical metadata. Readiness rubric validation, one-question refinement, tracker ownership, and structured return states remain unchanged. |
| `repository-ontology` | Refactored | Reduced active instructions below the context ceiling and split formal modelling and machine-readable output contracts into direct references. Added explicit tooling compatibility and stop conditions. |
| `review` | Pass | Strong immutable scope, proportionate dimensions, independent passes, falsification, evidence-calibrated findings, and revision-bound risk map. |
| `session-lessons` | Pass | Strong longitudinal evidence unit, correlation controls, qualification thresholds, lifecycle, routing, and promotion gate. |
| `skill-creator` | Improved | Now documents the complete canonical frontmatter set, namespaced metadata strategy, official validator command, progressive disclosure, script contracts, and matched evaluation. |
| `split-work` | Fixed | Moved internal visibility data under canonical metadata. Vertical-slice, publication-target, acyclic graph, and no-tracker-write boundaries remain unchanged. |
| `teach-me` | Pass | Strong progressive references, explicit local-state disclosure, deterministic scheduler boundary, exact script invocation, fallback, receipts, and bundled maintenance tests. |

## Description audit

All 18 descriptions now:

- identify the capability rather than merely naming a topic;
- state realistic trigger situations;
- include important near-miss or ownership boundaries where needed;
- remain below the 1024-character limit;
- match the parent directory name through their `name` field.

This is a qualitative review. Triggering precision should still be measured with
held-out positive prompts and difficult near misses before descriptions are
aggressively optimized.

## Script audit

### `lsp-config/scripts/detect-languages.mjs`

Passes the script-quality review:

- self-contained catalogue and documented Node.js requirement;
- explicit arguments and JSON output;
- recoverable scan errors and fatal exit behaviour;
- bounded traversal depth and ignored-directory policy;
- instructions describe exactly when and how to run it.

A future change to a catalogue entry should continue to update both the
human-readable catalogue and embedded script entry, then test a representative
repository and an edge case.

### `teach-me/scripts/*`

Passes the package review:

- scripts have explicit invocation from `SKILL.md`;
- deterministic state and scheduler responsibilities are separated from model
  judgement;
- fallback behaviour is documented;
- dedicated state and engine tests already exist;
- third-party attribution is bundled.

### `git-archaeologist/scripts/analyse-history.py`

Added during this audit:

- standard-library Python and Git only;
- parameterized repository, revision, time window, and result limit;
- argument-array Git execution without shell interpolation;
- JSON success and failure contracts;
- shallow-history and empty-window warnings;
- explicit interpretation limits;
- synthetic-repository and prerequisite-failure tests.

## Evaluation status and recommended next work

The repository now describes good evaluation practice through `skill-creator`,
but most skills do not yet have committed evaluation cases or measured baselines.
The highest-value next evaluation work is:

1. **Description activation** — positive, negative, and hard near-miss prompts for
   overlapping engineering skills such as `review`, `create-pr`, `adopt`,
   `repository-ontology`, and `git-archaeologist`.
2. **Internal routing** — confirm public requests activate owning agents rather
   than internal modules across each supported harness.
3. **Behavioural lift** — matched old/new or no-skill comparisons for
   `git-archaeologist`, `coach-me`, and `repository-ontology` with deterministic
   checks plus human review.
4. **Cross-harness portability** — run the same cases in every harness where the
   repository is expected to operate; do not assume triggering or tool behaviour
   transfers.

Add evaluation fixtures only after the target harness, model, verifier, and
success criteria are explicit. Avoid committing a nominal eval suite that merely
checks whether the skill was mentioned.

## Acceptance criteria

The audit is complete when:

- every top-level skill passes pinned `skills-ref` validation;
- no canonical skill contains a non-standard top-level frontmatter field;
- every active `SKILL.md` is at most 500 lines;
- every internal module fails closed without owner-agent context;
- every bundled script has declared requirements, actionable failures, and a
  representative test path;
- the repository does not claim matched behavioural evaluation that was not run.
