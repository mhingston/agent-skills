# Optional scene v1 and interactive walkthroughs

Use this reference only when the user wants an exploratory or step-by-step diagram. Static diagrams must continue to work without a scene manifest, walkthrough controls, or JavaScript.

## Authoring contract

The semantic scene is distinct from geometry: the agent determines which actors and interactions are supported by evidence; SVG/template code determines where they are drawn. Scene IDs are stable across revisions (do not reuse an existing ID for a different object). The scene must not invent edges, execution order, persistence, retries, or security boundaries.

- A single inline `<script type="application/json" id="diagram-scene">` contains the versioned scene; it must never load external resources. Escape raw `<` as the JSON escape `\u003c` when serializing user-derived content to avoid closing the script element. Use `JSON.stringify(scene).replace(/</g, '\\u003c')` in an authoring script.
- Each declared node has exactly one SVG element with `data-scene-node="node-id"`. Edges and optional groups similarly use `data-scene-edge` and `data-scene-group`. The existing `data-layout-object`, `data-connector`, and `data-fit-box` layout annotations remain independent and required where applicable.
- Each ID is unique across nodes, edges, groups and steps; IDs use ASCII lowercase letters first, then lowercase letters, numbers, underscores or hyphens, maximum 64 characters.
- Nodes: `{ "id": "app", "label": "App", "detail": "Validates input" }` (label/detail optional). Edges: `{ "id": "call", "from": "app", "to": "api", "kind": "primary" }`, with optional `label` and `detail`.
- Edge `kind` must be `primary`, `secondary`, `failure`, `control`, or `feedback` and must accurately describe the relationship. Group objects have `{ "id": "zone", "members": ["app", "api"], "detail": "Trust boundary" }` and may be omitted entirely.
- Steps are ordered objects with `id`, nonempty `title`, nonempty `description`, and one or more references in `nodes`, `edges`, or `groups`. Every reference must resolve. Steps highlight what the walkthrough is explaining; they do **not** assert execution order beyond source evidence.
- Titles, labels, descriptions and notes are plain text, not HTML. The runtime inserts them using `textContent` rather than `innerHTML`.

See `fixtures/scene/request-tool-flow.json` for a three-stage semantic scene and `assets/diagram-template.html` for a complete standalone HTML/SVG example with visual bindings and controls.

## Progressive interaction

Keep the SVG fully visible by default (and when JavaScript is disabled). Only enable the controls after successful manifest and visual-binding validation; otherwise leave the static SVG untouched and report the failure. The default view is **Show all**. Steps mark relevant nodes/edges/groups and mute unrelated bound elements. Previous / Next and Left / Right arrow keys navigate; Show all restores the static view.

Use native button controls, visible focus indicators, a live description, and a reduced-motion fallback. Supplemental descriptions appear in a disclosure list in addition to SVG hover titles and keyboard-focusable elements; do not make hover the only route to factual information. Keep the entire diagram legible in static screenshots and SVG/PNG exports: a walkthrough is an enhancement, never a hidden source of necessary information.

Do not put executable inline scripts, remote fonts, CDN assets, network requests, local storage, or tracking in the delivered artifact. Do not depend on Sketchy or any MCP server for the file to open.

## Verification

Run `node technical-diagram/scripts/test-scene-walkthrough.mjs` for deterministic schema/interaction tests, then `node technical-diagram/scripts/verify-diagram.mjs path/to/diagram.html` for the existing geometry/offline contract. The static linter now rejects invalid scene manifests and broken bindings; legacy diagrams without scene markup are still supported.

Manually verify keyboard focus order, arrow navigation, notes accessibility, mobile/touch operation, reduced motion, the no-JavaScript full-graph fallback, and SVG/PNG export in a real browser. These manual checks are not implied by a Node-only test pass.
