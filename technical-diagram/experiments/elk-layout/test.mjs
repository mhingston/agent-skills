#!/usr/bin/env node
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { generate } from './auto-layout.mjs';

const root = dirname(fileURLToPath(import.meta.url));
const load = async (name) => JSON.parse(await readFile(resolve(root, 'fixtures', name + '.json'), 'utf8'));
const linear = await load('linear');
const first = await generate(linear);
const second = await generate(linear);
assert.deepEqual(first.report.nodes, second.report.nodes, 'same input must produce deterministic coordinates');
assert.equal(first.report.metrics.nodeOverlaps, 0, 'ELK must not overlap peer nodes');
assert.equal(first.report.metrics.edgeCount, linear.edges.length, 'semantic edges cannot be added or dropped');
assert.equal((first.html.match(/data-connector=/g) || []).length, linear.edges.length);
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
await assert.rejects(() => generate(await load('sequence')), /fixed-rail path/,
  'sequence layouts must stay editorial');
const tooLong = structuredClone(linear);
tooLong.nodes[0].label = 'an excessively long descriptive diagram label';
await assert.rejects(() => generate(tooLong), /Shorten node label/);

console.log('ELK prototype: deterministic flow, semantic edges, escaping, refusals and offline preflight passed');
