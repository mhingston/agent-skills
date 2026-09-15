#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { lintDocument } from './static-lint-diagram.mjs';
import { readFile } from 'node:fs/promises';

const EXIT_OK = 0;
const EXIT_LAYOUT_ERRORS = 1;
const EXIT_ENVIRONMENT_ERROR = 2;
const here = resolve(fileURLToPath(new URL('.', import.meta.url)));

function usage() {
  console.error('Usage: node technical-diagram/scripts/verify-diagram.mjs <diagram.html>');
}

function runNode(script, args) {
  return new Promise((resolveResult) => {
    const child = spawn(process.execPath, [script, ...args], { stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (chunk) => { stdout += chunk; });
    child.stderr.on('data', (chunk) => { stderr += chunk; });
    child.on('error', (error) => resolveResult({ exitCode: EXIT_ENVIRONMENT_ERROR, stdout, stderr: String(error) }));
    child.on('close', (exitCode) => resolveResult({ exitCode: exitCode ?? EXIT_ENVIRONMENT_ERROR, stdout, stderr }));
  });
}

function parseJson(value) {
  try {
    return JSON.parse(value.trim());
  } catch {
    return null;
  }
}

async function main() {
  const file = process.argv[2];
  if (!file || file === '-h' || file === '--help') {
    usage();
    process.exit(file ? EXIT_OK : EXIT_ENVIRONMENT_ERROR);
  }

  const absolute = resolve(file);
  let staticResult;
  try {
    staticResult = lintDocument(await readFile(absolute, 'utf8'), absolute);
  } catch (error) {
    console.log(JSON.stringify({
      ok: false,
      file: absolute,
      checks: { static: { status: 'unavailable', error: String(error?.message || error) }, rendered: { status: 'not-run' } },
      errors: [{ code: 'STATIC_LINT_UNAVAILABLE', message: String(error?.message || error) }],
      warnings: [],
    }, null, 2));
    process.exitCode = EXIT_ENVIRONMENT_ERROR;
    return;
  }

  if (!staticResult.ok) {
    console.log(JSON.stringify({
      ok: false,
      file: absolute,
      checks: { static: staticResult, rendered: { status: 'not-run', reason: 'static preflight failed' } },
      errors: staticResult.errors,
      warnings: staticResult.warnings,
    }, null, 2));
    process.exitCode = EXIT_LAYOUT_ERRORS;
    return;
  }

  const browserResult = await runNode(resolve(here, 'lint-diagram-layout.mjs'), [absolute]);
  const rendered = parseJson(browserResult.stdout) || parseJson(browserResult.stderr);
  if (browserResult.exitCode === EXIT_OK && rendered) {
    console.log(JSON.stringify({
      ok: true,
      file: absolute,
      checks: { static: staticResult, rendered: { ...rendered, status: 'pass' } },
      errors: [],
      warnings: [...staticResult.warnings, ...(rendered.warnings || [])],
    }, null, 2));
    process.exitCode = EXIT_OK;
    return;
  }

  if (browserResult.exitCode === EXIT_LAYOUT_ERRORS && rendered) {
    console.log(JSON.stringify({
      ok: false,
      file: absolute,
      checks: { static: staticResult, rendered: { ...rendered, status: 'fail' } },
      errors: rendered.errors || [{ code: 'LAYOUT_ERRORS', message: 'Rendered layout lint failed' }],
      warnings: [...staticResult.warnings, ...(rendered.warnings || [])],
    }, null, 2));
    process.exitCode = EXIT_LAYOUT_ERRORS;
    return;
  }

  console.log(JSON.stringify({
    ok: false,
    file: absolute,
    checks: { static: staticResult, rendered: { status: 'unavailable', ...(rendered || {}) } },
    errors: [{ code: 'RENDERED_LINT_UNAVAILABLE', message: 'Static preflight passed, but browser-backed rendered lint was unavailable' }],
    warnings: staticResult.warnings,
  }, null, 2));
  process.exitCode = EXIT_ENVIRONMENT_ERROR;
}

await main();
