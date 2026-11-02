#!/usr/bin/env node
/**
 * Reproducible geometry/proxy benchmark; NOT a paired human quality experiment.
 * Manual controls are existing, non-matched fixtures.
 */
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { lintDocument } from '../../scripts/static-lint-diagram.mjs';
import { generate, reportAccepted } from './auto-layout.mjs';
const root = dirname(fileURLToPath(import.meta.url));
const out = resolve(process.argv[2] || resolve(root, 'out'));
await mkdir(out, { recursive: true });
const names = ['linear', 'fallback', 'branchy-loop', 'cluster'];
const results = {};
for (const name of names) {
  const scene = JSON.parse(await readFile(resolve(root, 'fixtures', name + '.json'), 'utf8'));
  try {
    const result = await generate(scene);
    await writeFile(resolve(out, name + '.html'), result.html);
    results[name] = { status: reportAccepted(result.report) ? 'pass' : 'needs-repair', ...result.report };
  } catch (error) {
    results[name] = { status: 'rejected', error: String(error.message) };
  }
}
const linear = JSON.parse(await readFile(resolve(root, 'fixtures/linear.json'), 'utf8'));
const original = await generate(linear);
const edited = structuredClone(linear);
edited.nodes.push({ id: 'audit', label: 'Audit sink' });
edited.edges.push({ id: 'audit-publish', from: 'worker', to: 'audit', kind: 'secondary' });
edited.steps[0].nodes.push('audit');
edited.steps[0].edges.push('audit-publish');
try {
  const changed = await generate(edited, original.report);
  results['linear-edit'] = { status: reportAccepted(changed.report) ? 'pass' : 'needs-repair', ...changed.report };
  await writeFile(resolve(out, 'linear-edit.html'), changed.html);
} catch (error) { results['linear-edit'] = { status: 'rejected', error: String(error.message) }; }

const controls = {};
for (const [name, relative] of Object.entries({
  'branchy-loop-editorial': '../../fixtures/layout/bubble-sort.html',
  'sequence-editorial': '../../fixtures/layout/http-sequence.html',
})) {
  const html = await readFile(resolve(root, relative), 'utf8');
  const report = lintDocument(html);
  controls[name] = { staticLintPass: report.ok, errorCount: report.errors.length,
    note: 'Existing hand-authored control, NOT a matched semantic-scene baseline' };
}
const sequence = JSON.parse(await readFile(resolve(root, 'fixtures/sequence.json'), 'utf8'));
let sequenceDecision = 'unexpected-acceptance';
try { await generate(sequence); } catch (error) {
  sequenceDecision = String(error.message).includes('fixed-rail') ? 'editorial-retained' : 'unexpected-rejection';
}
const attempts = Object.values(results);
const summary = {
  totalPrototypes: attempts.length,
  passes: attempts.filter((r) => r.status === 'pass').length,
  needsRepair: attempts.filter((r) => r.status === 'needs-repair').length,
  rejected: attempts.filter((r) => r.status === 'rejected').length,
  staticErrorCount: attempts.reduce((n, r) => n + (r.staticLint?.errors?.length || 0), 0),
  layoutMilliseconds: attempts.filter((r) => Number.isFinite(r.layoutMs)).map((r) => r.layoutMs),
  repairEffortMinutes: null,
  humanAuthoringLatencyMinutes: null,
  visualQualityRating: null,
  reason: 'No paired manually produced versions of the same scenes; do not claim improvement.',
};
const report = {
  experiment: 'ELK author-time layout Phase 2',
  defaultBackend: 'editorial',
  sequenceDecision,
  results, controls, summary,
};
await writeFile(resolve(out, 'benchmark.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ output: out, summary, sequenceDecision, results:
  Object.fromEntries(Object.entries(results).map(([name, r]) => [name, { status: r.status,
    metrics: r.metrics || null, staticErrors: r.staticLint?.errors || null,
    layoutMs: r.layoutMs ?? null, stability: r.stability || null }])) }, null, 2));
if (sequenceDecision !== 'editorial-retained' ||
    !controls['sequence-editorial'].staticLintPass ||
    !controls['branchy-loop-editorial'].staticLintPass ||
    summary.rejected || summary.needsRepair) process.exitCode = 1;
