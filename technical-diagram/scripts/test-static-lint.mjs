#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { lintDocument } from './static-lint-diagram.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const fixtureRoot = resolve(here, '../fixtures/layout');
const cases = [
  { file: 'warning-overflow.html', ok: false, error: 'TEXT_OUTSIDE_FIT_BOX' },
  { file: 'warning-fixed.html', ok: true },
  { file: 'connector-collision.html', ok: false, error: 'TEXT_CONNECTOR_COLLISION' },
  { file: 'connector-fixed.html', ok: true },
  { file: 'http-sequence.html', ok: true },
  { file: 'bubble-sort.html', ok: true },
];

for (const testCase of cases) {
  const file = resolve(fixtureRoot, testCase.file);
  const report = lintDocument(await readFile(file, 'utf8'), file);
  assert.equal(report.ok, testCase.ok, `${testCase.file}: unexpected static-lint result`);
  if (testCase.error) {
    assert.ok(report.errors.some((error) => error.code === testCase.error), `${testCase.file}: missing ${testCase.error}`);
  }
}

console.log(`technical-diagram static fixtures: ${cases.length} passed`);
