#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const templatePath = resolve(here, '../assets/diagram-template.html');
const template = await readFile(templatePath, 'utf8');

assert.match(template, /window\.__diagramLayoutReport/,
  'template must expose the runtime layout report');
assert.match(template, /data-fit-box=/,
  'template must demonstrate fit-constrained text');
assert.match(template, /data-connector=/,
  'template must mark connectors for collision linting');
assert.match(template, /data-layout-object=/,
  'template must mark peer layout objects');
assert.match(template, /TEXT_OUTSIDE_FIT_BOX/,
  'template must fail text that cannot fit its declared box');
assert.match(template, /TEXT_CONNECTOR_COLLISION/,
  'template must detect text/connector collisions');
assert.match(template, /TEXT_TEXT_OVERLAP/,
  'template must detect overlapping text');
assert.match(template, /LAYOUT_OBJECT_OVERLAP/,
  'template must detect overlapping peer layout objects');

console.log('technical-diagram layout contract: ok');
