#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { runInNewContext } from 'node:vm';
import { lintSceneDocument, validateScene } from './scene-schema.mjs';
import { lintDocument } from './static-lint-diagram.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const template = await readFile(resolve(here, '../assets/diagram-template.html'), 'utf8');
const manifestMatch = template.match(/<script type="application\/json" id="diagram-scene">([\s\S]*?)<\/script>/);
assert.ok(manifestMatch, 'example scene manifest is embedded in the offline template');
const original = JSON.parse(manifestMatch[1]);
const requestFlow = JSON.parse(await readFile(resolve(here, '../fixtures/scene/request-tool-flow.json'), 'utf8'));
const clone = () => JSON.parse(JSON.stringify(original));
const replaceManifest = (scene) => template.replace(manifestMatch[1], '\n' +
  JSON.stringify(scene).replace(/</g, '\\u003c') + '\n  ');
const expectedError = (scene, code) => {
  const report = validateScene(scene);
  assert.equal(report.ok, false, 'malformed scene must be rejected');
  assert.ok(report.errors.some((error) => error.code === code),
    code + ' not found in ' + JSON.stringify(report.errors));
};

assert.equal(validateScene(original).ok, true);
assert.equal(validateScene(requestFlow).ok, true);
assert.equal(requestFlow.steps.length, 3);
assert.equal(lintSceneDocument(template).ok, true);
assert.ok(lintSceneDocument(template.replace('id="scene-next"', 'id="missing-next"'))
  .errors.some((error) => error.code === 'SCENE_CONTROLS'));

assert.equal(lintSceneDocument('<svg aria-label="plain"></svg>').mode, 'legacy');
assert.ok(lintSceneDocument(template.replace('data-scene-node="actor"', 'data-scene-node="other"'))
  .errors.some((error) => error.code === 'SCENE_BINDING'));
assert.ok(lintSceneDocument(template.replace('data-scene-node="actor"', 'data-scene-node="app"'))
  .errors.some((error) => error.code === 'SCENE_BINDING'));
const duplicateManifest = template.replace('</main>', '</main>' + manifestMatch[0]);
assert.ok(lintSceneDocument(duplicateManifest)
  .errors.some((error) => error.code === 'SCENE_MANIFEST'));

const badKind = clone(); badKind.edges[0].kind = 'unknown';
expectedError(badKind, 'SCENE_EDGE_KIND');
assert.ok(lintDocument(replaceManifest(badKind)).errors.some((error) => error.code === 'SCENE_EDGE_KIND'));
const badEdge = clone(); badEdge.edges[0].to = 'missing';
expectedError(badEdge, 'SCENE_EDGE_ENDPOINT');
const badStep = clone(); badStep.steps[0].nodes = ['missing'];
expectedError(badStep, 'SCENE_REFERENCE_UNKNOWN');
const duplicate = clone(); duplicate.nodes[1].id = duplicate.nodes[0].id;
expectedError(duplicate, 'SCENE_DUPLICATE_ID');
const noHighlight = clone(); noHighlight.steps[0].nodes = []; noHighlight.steps[0].edges = [];
expectedError(noHighlight, 'SCENE_EMPTY_STEP');
const badGroup = clone(); badGroup.groups = [{ id: 'zone', members: ['missing'] }];
expectedError(badGroup, 'SCENE_REFERENCE_UNKNOWN');
assert.ok(lintSceneDocument(template.replace('"The caller initiates a request."', '"<script>alert(1)</script>"'))
  .errors.some((error) => error.code === 'SCENE_UNSAFE_JSON'));
const safeText = clone();
safeText.nodes[0].detail = '<img src=x onerror=alert(1)>';
assert.equal(lintSceneDocument(replaceManifest(safeText)).ok, true,
  'JSON escaped text is supported; runtime must insert it as text only');

// Exercise the actual inline browser script using a minimal no-network DOM stub.
// This catches behavioural regressions without requiring Playwright in deterministic CI.
const scripts = [...template.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const runtime = scripts.find((match) => match[1].includes('Scene v1 is optional'))?.[1];
assert.ok(runtime, 'self-contained runtime must be present in the template');

class Element {
  constructor(attributes = {}) {
    this.attributes = { ...attributes };
    this.children = [];
    this.listeners = new Map();
    this.classes = new Set();
    this.classList = {
      add: (name) => this.classes.add(name),
      remove: (...names) => names.forEach((name) => this.classes.delete(name)),
      contains: (name) => this.classes.has(name)
    };
    this.textContent = '';
    this.hidden = true;
    this.disabled = false;
  }
  getAttribute(name) { return this.attributes[name] ?? null; }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  removeAttribute(name) { delete this.attributes[name]; }
  append(child) { this.children.push(child); }
  addEventListener(name, fn) { this.listeners.set(name, fn); }
  fire(name, event = {}) { this.listeners.get(name)?.(event); }
}
function execute(scene, options = {}) {
  const elements = Object.fromEntries([
    ...scene.nodes.map((n) => [n.id, new Element({ 'data-scene-node': n.id })]),
    ...scene.edges.map((e) => [e.id, new Element({ 'data-scene-edge': e.id })]),
    ...(scene.groups || []).map((g) => [g.id, new Element({ 'data-scene-group': g.id })])
  ]);
  const svg = {
    querySelectorAll(selector) {
      const attr = selector.match(/^\[(data-scene-(?:node|edge|group))\]$/)?.[1];
      if (attr) return Object.values(elements).filter((e) => e.getAttribute(attr) !== null);
      return Object.values(elements);
    }
  };
  const artifact = new Element();
  artifact.querySelector = () => svg;
  const panel = new Element();
  const ids = Object.fromEntries([
    'scene-notes', 'scene-previous', 'scene-next', 'scene-show-all',
    'scene-count', 'scene-description'
  ].map((id) => [id, new Element()]));
  panel.querySelector = (selector) => ids[selector.slice(1)] ?? null;
  const manifest = new Element();
  manifest.textContent = options.rawJson ? JSON.stringify(scene) : JSON.stringify(scene).replace(/</g, '\\u003c');
  const document = {
    getElementById: (id) => id === 'diagram-scene' && !options.legacy ? manifest : id === 'diagram-walkthrough' ? panel : null,
    querySelector: () => artifact,
    createElement: () => new Element(),
    createElementNS: () => new Element()
  };
  const window = {};
  runInNewContext(runtime, { document, window });
  return { window, artifact, panel, ids, elements };
}

const flow = execute(requestFlow);
assert.equal(flow.window.__diagramSceneReport.ok, true);
flow.ids['scene-next'].fire('click');
flow.ids['scene-next'].fire('click');
assert.equal(flow.elements['tool-result'].classList.contains('scene-active'), true);
assert.equal(flow.elements.answer.classList.contains('scene-muted'), true);

const initial = execute(original);
assert.equal(initial.window.__diagramSceneReport.ok, true);
assert.equal(initial.panel.hidden, false);
assert.equal(initial.ids['scene-next'].disabled, false);
assert.equal(initial.ids['scene-previous'].disabled, true);
assert.equal(initial.ids['scene-count'].textContent, 'Full diagram');
assert.equal(initial.artifact.getAttribute('data-scene-step'), null);
initial.ids['scene-next'].fire('click');
assert.equal(initial.ids['scene-count'].textContent, 'Step 1 of 3');
assert.equal(initial.elements.actor.classList.contains('scene-active'), true);
assert.equal(initial.elements.store.classList.contains('scene-muted'), true);
initial.ids['scene-next'].fire('click');
assert.equal(initial.artifact.getAttribute('data-scene-step'), 'process-step');
initial.panel.fire('keydown', { key: 'ArrowRight', preventDefault() {} });
assert.equal(initial.ids['scene-next'].disabled, true);
initial.ids['scene-show-all'].fire('click');
assert.equal(initial.artifact.getAttribute('data-scene-step'), null);
assert.equal(initial.elements.store.classList.contains('scene-muted'), false);

const malicious = execute(safeText);
assert.equal(malicious.window.__diagramSceneReport.ok, true);
assert.ok(malicious.ids['scene-notes'].children.some((row) => row.textContent.includes('<img src=')));
assert.equal(malicious.ids['scene-notes'].children.some((row) => row.children.length), false,
  'notes use textContent, never HTML parsing');

const rawNotes = execute(safeText, { rawJson: true });
assert.equal(rawNotes.window.__diagramSceneReport.ok, false);
assert.equal(rawNotes.panel.hidden, true);

const invalid = execute(badKind);
assert.equal(invalid.window.__diagramSceneReport.ok, false);
assert.equal(invalid.panel.hidden, true);
assert.equal(invalid.artifact.getAttribute('data-scene-step'), null);

const legacy = execute(original, { legacy: true });
assert.equal(legacy.window.__diagramSceneReport.mode, 'legacy');
assert.equal(legacy.panel.hidden, true);
console.log('technical-diagram scene schema and interactive runtime: ok');
