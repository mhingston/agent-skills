import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const SCRIPT = fileURLToPath(new URL("./detect-languages.mjs", import.meta.url));

async function withWorkspace(run) {
  const root = await mkdtemp(join(tmpdir(), "lsp-config-test-"));
  try {
    await run(root);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
}

function runDetector(workspaceRoot, cwd = process.cwd()) {
  const result = spawnSync(process.execPath, [SCRIPT, workspaceRoot], {
    cwd,
    encoding: "utf8",
  });

  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.equal(result.stderr, "");
  return JSON.parse(result.stdout);
}

test("detects representative languages while ignoring generated dependency directories", async () => {
  await withWorkspace(async (root) => {
    await mkdir(join(root, "src"), { recursive: true });
    await writeFile(join(root, "src", "app.ts"), "export const value = 1;\n");
    await writeFile(join(root, "src", "worker.py"), "print('ok')\n");
    await writeFile(join(root, "go.mod"), "module example.com/lsp-test\n");

    await mkdir(join(root, "node_modules", "ignored"), { recursive: true });
    await writeFile(join(root, "node_modules", "ignored", "should-not-count.rb"), "");

    const result = runDetector(root);

    assert.equal(result.workspaceRoot, resolve(root));
    assert.deepEqual(result.detectedKeys, ["go", "python", "typescript"]);
    assert.deepEqual(result.errors, []);
    assert.ok(result.ignoredDirectories.includes("node_modules"));
  });
});

test("resolves a relative workspace root and detects case-insensitive manifest names", async () => {
  await withWorkspace(async (parent) => {
    const workspace = join(parent, "workspace");
    await mkdir(workspace, { recursive: true });
    await writeFile(join(workspace, "Cargo.toml"), "[package]\nname = \"example\"\n");

    const result = runDetector("workspace", parent);

    assert.equal(result.workspaceRoot, resolve(workspace));
    assert.deepEqual(result.detectedKeys, ["rust"]);
    assert.deepEqual(result.errors, []);
  });
});

test("reports a missing workspace as a recoverable scan error", async () => {
  await withWorkspace(async (parent) => {
    const missing = join(parent, "missing");
    const result = runDetector(missing);

    assert.deepEqual(result.detectedKeys, []);
    assert.equal(result.errors.length, 1);
    assert.equal(result.errors[0].path, resolve(missing));
    assert.equal(typeof result.errors[0].message, "string");
    assert.ok(result.errors[0].message.length > 0);
  });
});
