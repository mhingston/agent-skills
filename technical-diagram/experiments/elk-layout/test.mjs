#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { generate, metricBoxes, reportAccepted } from './auto-layout.mjs';

const root = dirname(fileURLToPath(import.meta.url));
const load = async (name) => JSON.parse(await readFile(resolve(root, 'fixtures', name + '.json'), 'utf8'));
const linear = await load('linear');
const first = await generate(linear);
const second = await generate(linear);
assert.deepEqual(first.report.nodes, second.report.nodes, 'same input must produce deterministic coordinates');
assert.equal(first.report.metrics.nodeOverlaps, 0, 'ELK must not overlap peer nodes');
assert.equal(first.report.metrics.foreignConnectorLabelOverlaps, 0, 'labels cannot hide unrelated routed edges');
assert.equal(reportAccepted(first.report), true, 'one acceptance gate for CLI and benchmark');
assert.equal(reportAccepted({ ...first.report, metrics: {
  ...first.report.metrics, foreignConnectorLabelOverlaps: 1 } }), false,
'crossing another edge must reject a candidate');
assert.equal(reportAccepted({ ...first.report, metrics: {
  ...first.report.metrics, labelOverlaps: 1 } }), false,
'label plate overlap must reject even the edited candidate');
assert.equal(first.report.metrics.edgeCount, linear.edges.length, 'semantic edges cannot be added or dropped');
assert.equal((first.html.match(/data-connector=/g) || []).length, linear.edges.length);
for (const edge of linear.edges) {
  assert.match(first.html, new RegExp('data-edge-kind="' + edge.kind + '"'));
  assert.equal(first.report.edgeKinds[edge.id], edge.kind, 'report must retain edge kinds');
}
assert.equal((first.html.match(/data-node-id=/g) || []).length, linear.nodes.length);
const styles = new Set();
for (const kind of ['primary', 'secondary', 'failure', 'control', 'feedback']) {
  const changed = structuredClone(linear);
  changed.edges[0].kind = kind;
  const result = await generate(changed);
  const path = result.html.match(/<path data-connector="request"[^>]*>/)?.[0];
  assert.ok(path, 'edge retains its stable ID: ' + kind);
  assert.match(path, new RegExp('data-edge-kind="' + kind + '"'));
  styles.add((path.match(/stroke="([^"]+)"/)?.[1] || '') + '/' +
    (path.match(/stroke-dasharray="([^"]+)"/)?.[1] || 'solid'));
}
assert.equal(styles.size, 5, 'all five semantic relationships need distinguishable static treatments');
assert.match(first.html, /window\.__diagramLayoutReport/, 'must preserve canonical browser gate');
assert.doesNotMatch(first.html, /<script[^>]+src=/, 'output cannot require hosted JavaScript');
assert.doesNotMatch(first.html, /<link\b/, 'output cannot require remote CSS');
assert.equal(first.report.staticLint.ok, true,
  'generated linear artifact must pass existing preflight: ' + first.report.staticLint.errors.join(', '));

const malicious = structuredClone(linear);
malicious.nodes[0].label = '<img src=x>';
const escaped = await generate(malicious);
assert.match(escaped.html, /&lt;img src=x&gt;/);
assert.doesNotMatch(escaped.html, /<img src=x>/);

const broken = structuredClone(linear);
broken.edges[0].to = 'not-a-node';
await assert.rejects(() => generate(broken), /known nodes/, 'unknown endpoints must fail closed');
const sequence = await load('sequence');
await assert.rejects(() => generate(sequence), /fixed-rail path/,
  'sequence layouts must stay editorial');
// A flat layout cannot assert an unsafe ownership boundary around nonmembers.
const badGroup = structuredClone(linear);
badGroup.groups = [{ id: 'misleading', detail: 'Noncontiguous', members: ['client', 'reply'] }];
await assert.rejects(() => generate(badGroup), /would enclose non-members/,
  'a rectangle must never visually claim ownership over non-members');
const clustered = await generate(await load('cluster'));
assert.equal(reportAccepted(clustered.report), true, 'safe nearby groups remain supported');
assert.match(clustered.html, /data-group-members="sharda,shardb"/);

// Test the connector-to-label check independently of whatever ELK happens to route.
const syntheticScene = { edges: [
  { id: 'owned', from: 'a', to: 'b', kind: 'primary', label: 'label' },
  { id: 'other', from: 'b', to: 'c', kind: 'secondary' }
] };
const synthetic = {
  nodes: {
    a: { x: 0, y: 0, width: 40, height: 40 },
    b: { x: 240, y: 0, width: 40, height: 40 },
    c: { x: 240, y: 200, width: 40, height: 40 }
  },
  edges: {
    owned: {
      label: { x: 90, y: 5, width: 50, height: 20 },
      sections: [[{ x: 40, y: 15 }, { x: 240, y: 15 }]]
    },
    other: {
      label: null,
      sections: [[{ x: 260, y: 40 }, { x: 260, y: 200 }]]
    }
  }
};
assert.equal(metricBoxes(synthetic, syntheticScene).foreignConnectorLabelOverlaps, 0,
  'label may cover its own connector only');
synthetic.edges.other.sections = [[{ x: 110, y: -20 }, { x: 110, y: 60 }]];
assert.equal(metricBoxes(synthetic, syntheticScene).foreignConnectorLabelOverlaps, 1,
  'foreign connector intersecting label plate must be detected');
const tooLong = structuredClone(linear);
tooLong.nodes[0].label = 'an excessively long descriptive diagram label';
await assert.rejects(() => generate(tooLong), /Shorten node label/);

console.log('ELK prototype: geometry, group semantics, edge kinds, connector-label collisions, refusals and offline preflight passed');
