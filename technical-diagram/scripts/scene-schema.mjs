/**
 * Technical diagram scene v1: semantic validation, independent of layout.
 * Browser runtime validates the same contract before enabling controls.
 */
export const SCENE_EDGE_KINDS = Object.freeze(['primary', 'secondary', 'failure', 'control', 'feedback']);
const ID = /^[a-z][a-z0-9_-]{0,63}$/;
const isObject = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);

export function validateScene(scene, bindings = null) {
  const errors = [];
  const fail = (code, message) => errors.push({ code, message });
  if (!isObject(scene) || scene.version !== 1) {
    fail('SCENE_VERSION', 'A scene must be an object with version: 1');
    return { ok: false, errors };
  }
  if (!Array.isArray(scene.nodes) || !Array.isArray(scene.edges) ||
      !Array.isArray(scene.steps) || (scene.groups !== undefined && !Array.isArray(scene.groups))) {
    fail('SCENE_COLLECTIONS', 'nodes, edges and steps must be arrays; groups is an optional array');
    return { ok: false, errors };
  }

  const seen = new Set();
  const index = { nodes: new Set(), edges: new Set(), groups: new Set(), steps: new Set() };
  const register = (item, collection) => {
    if (!isObject(item) || typeof item.id !== 'string' || !ID.test(item.id)) {
      fail('SCENE_ID', 'Invalid ID in ' + collection);
      return false;
    }
    if (seen.has(item.id)) {
      fail('SCENE_DUPLICATE_ID', 'Duplicate ID: ' + item.id);
      return false;
    }
    seen.add(item.id);
    index[collection].add(item.id);
    return true;
  };
  const text = (value, field, max, required = false) => {
    if (value === undefined && !required) return;
    if (typeof value !== 'string' || !value.trim() || value.length > max) {
      fail('SCENE_TEXT', field + ' must be nonempty plain text (max ' + max + ' characters)');
    }
  };
  const references = (values, indexName, field, requireNonempty = false) => {
    if (values === undefined && !requireNonempty) return;
    if (!Array.isArray(values) || (requireNonempty && !values.length)) {
      fail('SCENE_REFERENCES', field + ' must be a nonempty array');
      return;
    }
    const used = new Set();
    for (const value of values) {
      if (typeof value !== 'string' || !index[indexName].has(value)) {
        fail('SCENE_REFERENCE_UNKNOWN', field + ' references unknown ' + indexName + ' ID: ' + String(value));
      } else if (used.has(value)) {
        fail('SCENE_REFERENCE_DUPLICATE', field + ' repeats ' + value);
      }
      used.add(value);
    }
  };

  for (const node of scene.nodes) {
    if (!register(node, 'nodes')) continue;
    text(node.label, 'node ' + node.id + ' label', 120);
    text(node.detail, 'node ' + node.id + ' detail', 500);
  }
  for (const edge of scene.edges) {
    if (!register(edge, 'edges')) continue;
    if (!SCENE_EDGE_KINDS.includes(edge.kind)) fail('SCENE_EDGE_KIND', 'Invalid kind on edge ' + edge.id);
    if (!index.nodes.has(edge.from) || !index.nodes.has(edge.to)) {
      fail('SCENE_EDGE_ENDPOINT', 'Edge ' + edge.id + ' must connect known nodes');
    }
    text(edge.label, 'edge ' + edge.id + ' label', 120);
    text(edge.detail, 'edge ' + edge.id + ' detail', 500);
  }
  for (const group of scene.groups || []) {
    if (!register(group, 'groups')) continue;
    text(group.detail, 'group ' + group.id + ' detail', 500);
    references(group.members, 'nodes', 'group ' + group.id + ' members', true);
  }
  if (!scene.steps.length) fail('SCENE_STEPS', 'An interactive scene needs at least one step');
  for (const step of scene.steps) {
    if (!register(step, 'steps')) continue;
    text(step.title, 'step ' + step.id + ' title', 120, true);
    text(step.description, 'step ' + step.id + ' description', 500, true);
    references(step.nodes, 'nodes', 'step ' + step.id + ' nodes');
    references(step.edges, 'edges', 'step ' + step.id + ' edges');
    references(step.groups, 'groups', 'step ' + step.id + ' groups');
    if (!(step.nodes?.length || step.edges?.length || step.groups?.length)) {
      fail('SCENE_EMPTY_STEP', 'Step ' + step.id + ' must highlight at least one object');
    }
  }
  if (bindings) {
    for (const collection of ['nodes', 'edges', 'groups']) {
      for (const id of index[collection]) {
        if (bindings[collection]?.get(id) !== 1) {
          fail('SCENE_BINDING', 'Expected exactly one data-scene-' + collection.slice(0, -1) + ' binding for ' + id);
        }
      }
      for (const [id, count] of bindings[collection] || []) {
        if (!index[collection].has(id) || count !== 1) {
          fail('SCENE_BINDING', 'Unknown or duplicate visual binding: ' + id);
        }
      }
    }
  }
  return { ok: errors.length === 0, errors };
}

const marker = /<([a-z][\w:-]*)\b([^>]*\bdata-scene-(node|edge|group)\s*=\s*["']([^"']+)["'][^>]*)>/gi;
const manifestPattern = /<script\b(?=[^>]*\bid\s*=\s*["']diagram-scene["'])(?=[^>]*\btype\s*=\s*["']application\/json["'])[^>]*>([\s\S]*?)<\/script\s*>/gi;

export function lintSceneDocument(html) {
  const matches = [...html.matchAll(manifestPattern)];
  const hasMarkers = /\bdata-scene-(?:node|edge|group)\s*=/.test(html);
  if (!matches.length && !hasMarkers) return { ok: true, errors: [], mode: 'legacy' };
  const errors = [];
  if (matches.length !== 1) {
    errors.push({ code: 'SCENE_MANIFEST', message: 'Exactly one application/json diagram-scene manifest is required' });
    return { ok: false, errors };
  }
  // JSON placed inside a script element must escape '<' as \u003c to avoid early tag termination.
  if (matches[0][1].includes('<')) {
    errors.push({ code: 'SCENE_UNSAFE_JSON', message: 'Escape literal < characters as JSON unicode escapes' });
  }
  let scene;
  try { scene = JSON.parse(matches[0][1]); } catch (error) {
    errors.push({ code: 'SCENE_JSON', message: String(error.message) });
    return { ok: false, errors };
  }
  const bindings = { nodes: new Map(), edges: new Map(), groups: new Map() };
  for (const match of html.matchAll(marker)) {
    const collection = { node: 'nodes', edge: 'edges', group: 'groups' }[match[3]];
    const id = match[4];
    bindings[collection].set(id, (bindings[collection].get(id) || 0) + 1);
  }
  errors.push(...validateScene(scene, bindings).errors);
  return { ok: errors.length === 0, errors, mode: 'scene-v1' };
}
