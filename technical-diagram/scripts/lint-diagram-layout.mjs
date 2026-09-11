#!/usr/bin/env node

import { access } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const EXIT_LAYOUT_ERRORS = 1;
const EXIT_ENVIRONMENT_ERROR = 2;

function usage() {
  console.error('Usage: node technical-diagram/scripts/lint-diagram-layout.mjs <diagram.html>');
}

async function loadBrowserAdapter() {
  try {
    const { chromium } = await import('playwright');
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1600, height: 900 } });
    const page = await context.newPage();
    return {
      page,
      close: async () => {
        await context.close();
        await browser.close();
      },
      driver: 'playwright'
    };
  } catch (playwrightError) {
    try {
      const puppeteer = await import('puppeteer');
      const browser = await puppeteer.launch({ headless: true });
      const page = await browser.newPage();
      await page.setViewport({ width: 1600, height: 900 });
      return {
        page,
        close: async () => browser.close(),
        driver: 'puppeteer'
      };
    } catch (puppeteerError) {
      const error = new Error(
        'No usable browser driver found. Install Playwright or Puppeteer in the authoring harness, ' +
        'or inspect window.__diagramLayoutReport in another browser-backed renderer.'
      );
      error.cause = { playwrightError, puppeteerError };
      throw error;
    }
  }
}

async function waitForReport(page, driver) {
  if (driver === 'playwright') {
    await page.waitForFunction(() => Boolean(window.__diagramLayoutReport), null, { timeout: 10000 });
    return page.evaluate(() => window.__diagramLayoutReport);
  }

  await page.waitForFunction(() => Boolean(window.__diagramLayoutReport), { timeout: 10000 });
  return page.evaluate(() => window.__diagramLayoutReport);
}

async function gotoFile(page, driver, url) {
  if (driver === 'playwright') {
    await page.goto(url, { waitUntil: 'load' });
    return;
  }
  await page.goto(url, { waitUntil: 'load' });
}

async function main() {
  const file = process.argv[2];
  if (!file || file === '-h' || file === '--help') {
    usage();
    process.exit(file ? 0 : EXIT_ENVIRONMENT_ERROR);
  }

  const absolute = resolve(file);
  try {
    await access(absolute);
  } catch {
    console.error(JSON.stringify({
      ok: false,
      errors: [{ code: 'FILE_NOT_FOUND', message: `Diagram not found: ${absolute}` }],
      warnings: []
    }, null, 2));
    process.exit(EXIT_ENVIRONMENT_ERROR);
  }

  let adapter;
  try {
    adapter = await loadBrowserAdapter();
    await gotoFile(adapter.page, adapter.driver, pathToFileURL(absolute).href);
    const report = await waitForReport(adapter.page, adapter.driver);
    const output = {
      ...report,
      driver: adapter.driver,
      file: absolute
    };
    console.log(JSON.stringify(output, null, 2));
    process.exitCode = report?.errors?.length ? EXIT_LAYOUT_ERRORS : 0;
  } catch (error) {
    console.error(JSON.stringify({
      ok: false,
      errors: [{
        code: 'LAYOUT_LINT_UNAVAILABLE',
        message: error instanceof Error ? error.message : String(error)
      }],
      warnings: []
    }, null, 2));
    process.exitCode = EXIT_ENVIRONMENT_ERROR;
  } finally {
    if (adapter) {
      await adapter.close().catch(() => {});
    }
  }
}

await main();
