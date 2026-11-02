# ELK.js optional layout experiment — issue #167

This is an **author-time prototype**, not a new default or a shipped runtime
dependency. Static editorial diagrams, fixed-rail sequence diagrams, and the
existing verify-diagram.mjs command remain authoritative. Generated HTML
contains inline CSS, SVG, and the **canonical** browser layout-check script
extracted from assets/diagram-template.html; it never includes ELK.js, a CDN,
or an MCP client.

## Try it

Requires Node 18+ and npm with network access **only while installing the
experiment tool**. Delivered HTML requires no network.

~~~bash
cd technical-diagram/experiments/elk-layout
npm install --no-audit --no-fund --package-lock=false
npm test
npm run benchmark
node auto-layout.mjs fixtures/linear.json out/linear.html --report out/linear-report.json
# From repository root: retain the full verification gate:
node technical-diagram/scripts/verify-diagram.mjs technical-diagram/experiments/elk-layout/out/linear.html
~~~

Only flow, linear, fallback, branchy-loop, and cluster semantic scenes are
candidates. Setting layout.pattern to sequence is deliberately refused, leaving
existing fixed participant columns and interaction rows unchanged. There is
**no automatic fallback** that could silently change a diagram's semantics.

Input uses the Phase 1 scene-v1 JSON format with nodes, edges, steps, and optional
groups. Add title, description, optional layout.direction (right default,
down optional), and layout.pattern. Node and edge IDs, endpoints, edge kinds,
text labels, and group membership are carried through unchanged. Steps are
semantic metadata, but this experimental renderer produces a **static** diagram:
use the existing editorial path when a guided walkthrough is needed. Groups are
drawn as lightweight rectangles only when their bounding rectangle encloses
no nonmember node; otherwise the scene is rejected for editorial or group-aware
layout. Grouping never infers connectivity.

ELK.js 0.12.1 supplies layered ordering and orthogonal routing. Long labels,
oversized layouts, unknown endpoints, and sequence patterns fail rather than
silently omitting objects or shrinking below the readability floor.

## Measurements and limitations

Running benchmark.mjs [output_dir] produces HTML candidates and benchmark.json
for linear, fallback, branching loop, cluster and a linear graph with an added
audit branch. A sequence fixture remains a **negative** candidate, retained
under the editorial baseline. Static editorial controls include existing
HTTP-sequence and bubble-sort fixtures.

Measurements: ELK layout duration (not model generation latency), graph and
edge-label box overlaps, **foreign connector versus edge-label collisions**,
bend counts, static-lint failures, and displacement of
shared node IDs after an edit (in 1600x900 SVG pixel coordinates). Stability
is observed, not guaranteed, and displacement includes graph repacking.
The control diagrams are **not matched illustrations of these scenes**: their
error counts must not be interpreted as evidence of improvement.

Repair effort, human authoring latency, and visual quality remain null until
paired same-scene diagrams have been created and timed using both methods.
A meaningful comparison also needs blind 1-5 quality assessments, full and
thumbnail review, and final verify-diagram results.

## Known trade-offs

- The prototype uses plain rectangles, not the established editorial treatments;
  it should not replace infographic composition.
- Every edge retains its semantic kind, endpoints, and stable ID in SVG
  attributes, a distinguishable line pattern (including a visible legend),
  and report metadata. Edge kinds must not silently collapse to identical
  graphical meanings.
- ELK's edge labels are rendered where ELK places them. Their intentional
  contact with their own edge is exempted from connector/text lint; **every
  other** routed edge is tested against the label plate in geometry preflight.
  Label/label and label/node overlaps also reject output, including edited
  candidates. The copied browser gate cannot enforce per-connector exemptions,
  so this extra graph-level check is mandatory before treating it as a pass.
  Real-browser inspection and verification remain required.
- Generated HTML copies the canonical browser layout report script but
  does not constitute a verify-diagram pass on its own. Exit code 2 remains
  unverified, never pass.
- Output files under out/ are disposable; deleting this experiment leaves the
  normal skill untouched.
- ELK.js is pinned at 0.12.1 and uses EPL-2.0. Preserve upstream notices
  if redistributing the dependency, although no ELK code is bundled in diagrams:
  https://github.com/kieler/elkjs and https://www.eclipse.org/legal/epl-2.0/
- The conceptual separation of scene and deterministic geometry was informed
  by Sketchy; no Sketchy source code is incorporated.

## Promotion / stop rules

Keep the **editorial path as default**. An automatic renderer may become an
opt-in supported path only after matched cases demonstrate fewer manual layout
fixes or lower authoring costs with no semantic regressions, zero final geometry
errors, equal or better readability, and offline export. Discard it if that
evidence does not materialise. Deterministic script checks are not model/harness
behavioural evaluation.
