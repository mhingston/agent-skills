# Phase 3 — matched technical-diagram evaluation (issue #168)

**State: NOT EVALUATED.** This directory describes an executable *evidence gate*, not
a claimed improvement. A passing deterministic tool suite and the Phase 2
`benchmark.json` are useful engineering checks, **not** matched model runs.

## Comparisons (do not mix baselines)

| Condition | Code revision | Renderer | Answers |
| --- | --- | --- | --- |
| **baseline** | `af79871d653991e3e05373c612c4392809ac25f4` (pre-Phase-1) | Existing editorial SVG | Did walkthrough/scene changes improve behaviour without stealing requests from adjacent skills? |
| **current** | Candidate PR head (record full SHA) | Editorial SVG, optional scene-v1 controls | What does the current skill actually deliver? |
| **candidate** | **Same SHA as current** | Opt-in ELK.js author-time renderer | Does auto-layout help on exactly the same semantic scene? |

The `baseline` here still includes `technical-diagram`, `eli5`, and
`codebase-walkthrough`. It is deliberately **not** the historical
"catalogue without technical-diagram" activation experiment. Never compare a
scene-v1 output with a completely absent skill to claim walkthrough lift.

For each `TD-E1`–`TD-E18` run baseline and current in clean, separate
contexts with the **same model, thinking effort, harness/version, permissions,
tool access, prompt text and artifact/browser support**. Each executed
baseline/current case must record matching `promptHash` and `controlsHash`.
The controls digest covers model/version/effort, harness/version, tools,
permissions and other non-renderer run settings, with unhashed values in the
trace. Any differences make the comparison inconclusive. Keep the competing
skills available in both conditions. Record skill-discovery traces where possible.
If activation is hidden, report `surrogate`, not `direct`: it will not satisfy
the routing gate.

For ELK use `linear`, `fallback`, `branchy-loop`, `cluster` and
`linear-edit` semantic scenes from `experiments/elk-layout/fixtures/`.
Generate an *editorial* version and an *ELK* version of each **from the same
normalised scene and the same starting evidence**. SHA-256 the canonical scene
JSON for each arm. If the same scene cannot be faithfully rendered by both,
record `BLOCKED`; do not substitute an unrelated legacy fixture.
Revisions of unchanged nodes should also record node-ID preservation and
coordinate displacement. The fixed-rail `sequence` scene is a negative
ELK control and must be rejected in favour of the editorial path.

## How to run

From the repository root:

```bash
node technical-diagram/scripts/assess-phase3.mjs --init /tmp/td-phase3.json
node technical-diagram/scripts/test-layout-contract.mjs
node technical-diagram/scripts/test-static-lint.mjs
node technical-diagram/scripts/test-scene-walkthrough.mjs
node technical-diagram/scripts/test-phase3.mjs
cd technical-diagram/experiments/elk-layout
npm install --no-audit --no-fund --package-lock=false
npm test && npm run benchmark
cd ../../..
```

Populate `/tmp/td-phase3.json` with *real* per-condition observations,
replacing every `NOT_RUN` with `PASS`, `FAIL` or `BLOCKED` **only after
the relevant test**. Set `revisions.current`, `candidate`, `suite`, and
`evaluator` to their actual full commits. `suite` identifies the revision
containing the tested prompts and rubric, `evaluator` the tested gate revision;
these are not necessarily equal to the runtime candidate. Preserve the
source prompts, responses, generated HTML/SVG, lint reports, browser screenshots,
grading sheets, discovery traces, and CI URLs under a stable artifact location.
Refer to those files in `proof`; do not put fabricated paths in receipts.

```bash
node technical-diagram/scripts/assess-phase3.mjs --assess /tmp/td-phase3.json
node technical-diagram/scripts/assess-phase3.mjs --strict /tmp/td-phase3.json
```

`--assess` checks structure and prints blockers/decisions; its successful exit
means **schema-valid**, not **evaluation passed**. `--strict` exits non-zero
unless the scene and ELK adoption gates are both satisfied. Missing checks,
unobservable routing, and unperformed browser or human tests remain blockers.
This evaluator does **not** execute a model, browser, screen reader or a human
grading session. It cannot turn reviewer-entered evidence into independently
verified behavioural proof.

## Receipt fields

The `--init` scaffold deliberately contains all 18 behavioural case pairs,
five ELK same-scene pairs, and a sequence-rejection control, each `NOT_RUN`.
Use the following contract when filling one `cases[].current` outcome:

```json
{
  "state": "PASS",
  "proof": "artifacts/<run-id>/TD-E13/current/trace-and-artifact-index.md",
  "promptHash": "sha256:<canonical-UTF8-prompt-digest>",
  "controlsHash": "sha256:<canonical-shared-harness-config-digest>",
  "route": "technical-diagram",
  "routeMethod": "direct",
  "checks": {
    "goal": "PASS",
    "semantic": "PASS",
    "legibility": "PASS",
    "offline": "PASS",
    "staticLint": "PASS",
    "browserLint": "PASS",
    "keyboard": "PASS",
    "screenReader": "PASS",
    "noJs": "PASS",
    "svgExport": "PASS",
    "hoverIndependent": "PASS"
  },
  "scores": {
    "semantic": 4,
    "legibility": 4
  }
}
```

This is **illustrative schema**, not a result. For `TD-E1`–`TD-E5` and
`TD-E9`–`TD-E12`, add 1–5 scores for `mechanism`, `hierarchy`,
`composition` and `style`. The assessor enforces a human median of at least
4 for TD-E1, TD-E2 and TD-E5 and a semantic/legibility floor of 3.
For TD-E6/E7 record `goal` and `boundary`; TD-E8 records `goal`.
For TD-E16 record `malformedRejected`, `fullDiagramFallback` and
`sceneLintReject` — rejecting malicious/malformed input is the **success**
condition. TD-E13/E14/E17/E18 have case-specific keyboard,
screen-reader, fallback, safe-text and export checks. Record each observed
browser and accessibility check as `PASS`, `FAIL`, `NOT_RUN` or
`BLOCKED`, with the browser driver, versions, screenshot/trace and reasons
for unavailable checks captured in the supporting artifacts.
A status is not automatically a pass because code exists for that check.

A `layouts[]` outcome has the same `state`/`proof` fields, plus:

- `sceneHash`: identical canonical semantic scene digest on both sides;
- `controlsHash`: identical non-renderer model/harness/permission/tool digest
  in both arms (only renderer option changes);
- `checks`: `semanticIds`, `staticLint`, `browserLint`, `offline`,
  `svgExport`, `fullSize`, `thumbnail`, `noOverlap` (each observed);
- `scores`: 1–5 human `semantic`, `legibility` and blind `quality`;
- `repairMinutes` and `authoringMinutes`: measured per-arm values, not
  ELK library runtime or guessed LLM token cost.

Attach numeric bend counts, cross-edge collisions, stable-ID drift in pixels,
lint error counts, viewport/driver metadata, and sample screenshots in the
underlying report. The assessor blocks promotion if any ELK grade worsens, any
final check fails, scenes differ, or no measured repair/authoring benefit exists.
The evidence record must still be examined by a human: `reviewerVerdict` is a
human decision, never an automatic approval.

## Manual grading (separate from lint)

Blind the renderer condition wherever possible. Ask a reviewer to view each
artifact at full size and a 25% thumbnail, then:

1. Identify the primary actor, outcome and first/next action in five seconds.
2. Trace one normal edge and one exception/fallback edge without the notes.
3. Identify any uncertain, replicated, or failed edge: was its meaning preserved?
4. Use keyboard only to move through steps and disclosures; test focus and
   the live announcement with a screen reader, with hover unavailable.
5. Disable JavaScript and network access, reload the HTML, and inspect the
   complete unmuted SVG. Export the SVG and open it independently.
6. Repeat after adding an independent service. Check unchanged IDs and
   recognisable placement; record actual displacement, not just "stable".

Keep **routing**, **semantic fidelity**, **static geometry**, **rendered
geometry**, **accessibility**, **user comprehension**, and **human effort** as
separate columns. Neither a VM-based DOM stub nor a clean static lint proves
keyboard/screen-reader behaviour, clipping under a real font, or comprehension.

## Decision and promotion

- **Scene ADOPT**: all 18 current cases observed, no adjacent-skill collisions,
  the required accessibility, browser and static checks performed and passing,
  semantic/legibility floors met, and no decline against pre-Phase-1 behaviour.
  Until then: `ITERATE`, `ROLLBACK`, or `NOT_EVALUATED`.
- **ELK ADOPT_OPT_IN**: five matched same-scene pairs and the rejected sequence
  control, **no** semantic/accessibility/offline/geometry/quality regression,
  and demonstrably lower authoring or repair effort. Do not make ELK the default.
- **KEEP_EXPERIMENTAL**: any incomplete evidence, worsening legibility or
  semantic result, missing browser checks, no measured benefit, or an invalid
  paired scene. Revert the experiment if repeated failures indicate it has no
  credible path to promotion.

The assessor returns conservative *recommendations*; a maintainer must make
the actual promotion, iteration or rollback decision. Keep the first Phase 3
PR as evaluation infrastructure only if the harness/browser/human trials have
not yet run. Never mark the issue completed solely because the new CI test passes.
