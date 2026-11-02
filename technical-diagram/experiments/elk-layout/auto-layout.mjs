#!/usr/bin/env node
/**
 * Author-time ELK prototype; NEVER shipped as a runtime dependency in HTML.
 * The only inputs to the graph are validated scene-v1 nodes and edges.
 */
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { performance } from 'node:perf_hooks';
import { createRequire } from 'node:module';
import { validateScene } from '../../scripts/scene-schema.mjs';
import { lintDocument } from '../../scripts/static-lint-diagram.mjs';

const require = createRequire(import.meta.url);
const DIR = dirname(fileURLToPath(import.meta.url));
const PAPER = { width: 1600, height: 900, left: 52, top: 158, widthForGraph: 1496, heightForGraph: 662 };
const escape = (value) => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;')
  .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
const num = (v) => Number(v.toFixed(2));
const boxOverlap = (a, b) => a.x < b.x + b.width && a.x + a.width > b.x &&
  a.y < b.y + b.height && a.y + a.height > b.y;
const distance = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
const average = (values) => values.length ? num(values.reduce((a, b) => a + b, 0) / values.length) : null;

function validateInput(scene) {
  const result = validateScene(scene);
  const errors = result.errors.map((error) => error.message);
  for (const node of scene.nodes || []) {
    if (typeof node.label !== 'string' || !node.label.trim()) errors.push('Node ' + node.id + ' needs a visible label');
    if (node.label?.length > 24) errors.push('Shorten node label ' + node.id + ' (max 24 characters)');
  }
  if (scene.layout?.pattern === 'sequence') errors.push('Sequence diagrams stay on the editorial/fixed-rail path');
  if (errors.length) throw new Error(errors.join('; '));
}

function geometryOf(result, scene) {
  const nodes = Object.fromEntries(result.children.map((node) =>
    [node.id, { x: node.x, y: node.y, width: node.width, height: node.height }]));
  const edges = {};
  for (const edge of result.edges) {
    if (!edge.sections?.length) throw new Error('ELK returned no routed sections for edge ' + edge.id);
    const sections = edge.sections.map((section) => [section.startPoint, ...(section.bendPoints || []), section.endPoint]);
    const firstLabel = edge.labels?.[0];
    const label = firstLabel && Number.isFinite(firstLabel.x) && Number.isFinite(firstLabel.y)
      ? { x: firstLabel.x, y: firstLabel.y, width: firstLabel.width, height: firstLabel.height }
      : null;
    edges[edge.id] = { sections, label };
  }
  const groups = {};
  for (const group of scene.groups || []) {
    const members = group.members.map((id) => nodes[id]);
    const bounds = {
      x: Math.min(...members.map((b) => b.x)) - 18,
      y: Math.min(...members.map((b) => b.y)) - 35,
      width: Math.max(...members.map((b) => b.x + b.width)) - Math.min(...members.map((b) => b.x)) + 36,
      height: Math.max(...members.map((b) => b.y + b.height)) - Math.min(...members.map((b) => b.y)) + 53,
    };
    // A visual boundary is an ownership assertion, not mere decoration.
    // Until ELK is group-aware, reject convex bounds that enclose non-members.
    const membersSet = new Set(group.members);
    const intruders = Object.entries(nodes).filter(([id, box]) =>
      !membersSet.has(id) && boxOverlap(bounds, box)).map(([id]) => id);
    if (intruders.length) throw new Error(
      'Group ' + group.id + ' would enclose non-members: ' + intruders.join(', ') +
      '; use an editorial layout or a group-aware layout backend');
    groups[group.id] = bounds;
  }
  return { nodes, edges, groups };
}

// Inclusive line/rectangle clipping; orthogonal ELK routes are a subset.
function segmentIntersectsRect(from, to, box, padding = 3) {
  const xMin = box.x - padding, xMax = box.x + box.width + padding;
  const yMin = box.y - padding, yMax = box.y + box.height + padding;
  const dx = to.x - from.x, dy = to.y - from.y;
  const p = [-dx, dx, -dy, dy];
  const q = [from.x - xMin, xMax - from.x, from.y - yMin, yMax - from.y];
  let enter = 0, leave = 1;
  for (let i = 0; i < 4; i++) {
    if (Math.abs(p[i]) < 1e-8) {
      if (q[i] < 0) return false;
      continue;
    }
    const t = q[i] / p[i];
    if (p[i] < 0) enter = Math.max(enter, t);
    else leave = Math.min(leave, t);
    if (enter > leave) return false;
  }
  return true;
}

export function metricBoxes(geom, scene) {
  const nodeBoxes = Object.entries(geom.nodes).map(([id, box]) => ({ id, ...box }));
  const labels = scene.edges.flatMap((edge) => geom.edges[edge.id].label
    ? [{ id: edge.id, ...geom.edges[edge.id].label }] : []);
  let nodeOverlaps = 0;
  let labelOverlaps = 0;
  const foreignConnectorLabelCollisions = [];
  for (const label of labels) {
    for (const edge of scene.edges) {
      // A label can sit on its OWN connector. It cannot mask someone else's.
      if (edge.id === label.id) continue;
      const route = geom.edges[edge.id];
      if (route?.sections?.some((points) => points.slice(1).some((point, i) =>
        segmentIntersectsRect(points[i], point, label)))) {
        foreignConnectorLabelCollisions.push({ labelEdgeId: label.id, crossingEdgeId: edge.id });
      }
    }
  }
  for (let i = 0; i < nodeBoxes.length; i++) {
    for (let j = i + 1; j < nodeBoxes.length; j++) if (boxOverlap(nodeBoxes[i], nodeBoxes[j])) nodeOverlaps++;
  }
  for (let i = 0; i < labels.length; i++) {
    for (let j = i + 1; j < labels.length; j++) if (boxOverlap(labels[i], labels[j])) labelOverlaps++;
    for (const node of nodeBoxes) if (boxOverlap(labels[i], node)) labelOverlaps++;
  }
  return {
    nodeOverlaps, labelOverlaps,
    foreignConnectorLabelOverlaps: foreignConnectorLabelCollisions.length,
    foreignConnectorLabelCollisions,
    edgeBends: Object.values(geom.edges).reduce((sum, edge) =>
      sum + edge.sections.reduce((total, points) => total + Math.max(0, points.length - 2), 0), 0),
    labelledEdges: labels.length,
    nodeCount: nodeBoxes.length,
    edgeCount: scene.edges.length,
  };
}

function scaledGeometry(geom, scale) {
  const X = (x) => num(PAPER.left + x * scale);
  const Y = (y) => num(PAPER.top + y * scale);
  const rect = (b) => ({ x: X(b.x), y: Y(b.y), width: num(b.width * scale), height: num(b.height * scale) });
  return {
    nodes: Object.fromEntries(Object.entries(geom.nodes).map(([id, b]) => [id, rect(b)])),
    groups: Object.fromEntries(Object.entries(geom.groups).map(([id, b]) => [id, rect(b)])),
    edges: Object.fromEntries(Object.entries(geom.edges).map(([id, edge]) => [id, {
      sections: edge.sections.map((points) => points.map((p) => ({ x: X(p.x), y: Y(p.y) }))),
      label: edge.label && rect(edge.label),
    }])),
  };
}

async function layoutScene(scene, previous = null) {
  validateInput(scene);
  let ELK;
  try { ELK = require('elkjs/lib/elk.bundled.js'); }
  catch { throw new Error('Install author-time ELK dependency: cd technical-diagram/experiments/elk-layout && npm install'); }
  const elk = new ELK();
  const graph = {
    id: 'scene',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': scene.layout?.direction === 'down' ? 'DOWN' : 'RIGHT',
      'elk.edgeRouting': 'ORTHOGONAL',
      'elk.spacing.nodeNode': '64',
      'elk.layered.spacing.nodeNodeBetweenLayers': '90',
      'elk.layered.considerModelOrder.strategy': 'NODES_AND_EDGES',
      'elk.edgeLabels.placement': 'CENTER',
    },
    children: scene.nodes.map((node) => ({
      id: node.id, width: Math.max(202, Math.ceil(node.label.length * 13.5 + 42)), height: 82,
    })),
    edges: scene.edges.map((edge) => ({
      id: edge.id, sources: [edge.from], targets: [edge.to],
      labels: edge.label ? [{ id: 'label-' + edge.id, text: edge.label,
        width: Math.max(48, edge.label.length * 10.5 + 19), height: 31 }] : [],
    })),
  };
  const start = performance.now();
  const result = await elk.layout(graph);
  const layoutMs = num(performance.now() - start);
  const raw = geometryOf(result, scene);
  const scale = Math.min(1, PAPER.widthForGraph / result.width, PAPER.heightForGraph / result.height);
  if (scale < 0.74) throw new Error('Layout needs scale ' + scale.toFixed(2) +
    ', below legibility floor; simplify or use editorial layout');
  const geom = scaledGeometry(raw, scale);
  const metrics = metricBoxes(geom, scene);
  const shared = previous?.nodes
    ? Object.keys(geom.nodes).filter((id) => previous.nodes[id]) : [];
  const displacement = shared.map((id) => distance(geom.nodes[id], previous.nodes[id]));
  const report = {
    engine: 'elkjs', experimental: true, pattern: scene.layout?.pattern || 'flow',
    layoutMs, scale: num(scale), metrics,
    edgeKinds: Object.fromEntries(scene.edges.map((edge) => [edge.id, edge.kind])),
    groupMembers: Object.fromEntries((scene.groups || []).map((group) => [group.id, [...group.members]])),
    stability: { sharedNodes: shared.length, meanDisplacementPx: average(displacement) },
    nodes: Object.fromEntries(Object.entries(geom.nodes).map(([id, b]) => [id, { x: b.x, y: b.y }])),
  };
  return { geom, report };
}

const EDGE_STYLE = Object.freeze({
  primary: { stroke: '#111111', dash: '' },
  secondary: { stroke: '#111111', dash: '15 7' },
  failure: { stroke: '#d64b28', dash: '7 6' },
  control: { stroke: '#6525d1', dash: '2 7' },
  feedback: { stroke: '#17658a', dash: '14 5 3 5' },
});

export function reportAccepted(report) {
  return !!report.staticLint?.ok &&
    report.metrics?.nodeOverlaps === 0 &&
    report.metrics?.labelOverlaps === 0 &&
    report.metrics?.foreignConnectorLabelOverlaps === 0;
}

async function renderHtml(scene, geom) {
  const template = await readFile(resolve(DIR, '../../assets/diagram-template.html'), 'utf8');
  const gate = template.match(/<script>\s*\(\(\) => \{\s*const EPSILON = 0\.75;[\s\S]*?<\/script>/);
  if (!gate) throw new Error('Cannot find canonical rendered geometry gate in diagram-template.html');
  const title = scene.title || 'Technical diagram';
  if (title.length > 58) throw new Error('Title too long for slide canvas; shorten it');
  let shapes = '';
  for (const group of scene.groups || []) {
    const b = geom.groups[group.id];
    shapes += '<rect data-layout-group-id="' + escape(group.id) +
      '" data-group-members="' + escape(group.members.join(',')) +
      '" x="' + b.x + '" y="' + b.y + '" width="' + b.width +
      '" height="' + b.height + '" rx="16" fill="#f7f0ff" stroke="#6525d1" stroke-dasharray="10 8" stroke-width="2"/>';
    shapes += '<text x="' + (b.x + 14) + '" y="' + (b.y + 23) +
      '" font-size="17" font-weight="700">' + escape(group.detail || group.id) + '</text>';
  }
  for (const edge of scene.edges) {
    const route = geom.edges[edge.id];
    const style = EDGE_STYLE[edge.kind];
    const dash = style.dash ? ' stroke-dasharray="' + style.dash + '"' : '';
    const path = route.sections.map((points) => 'M ' + points.map((p) => p.x + ' ' + p.y).join(' L ')).join(' ');
    shapes += '<path data-connector="' + escape(edge.id) +
      '" data-edge-kind="' + escape(edge.kind) +
      '" data-edge-from="' + escape(edge.from) + '" data-edge-to="' + escape(edge.to) +
      '" role="img" aria-label="' + escape(edge.kind + ': ' + edge.from + ' to ' + edge.to +
        (edge.label ? ', ' + edge.label : '')) +
      '" d="' + path + '" fill="none" stroke="' + style.stroke +
      '" stroke-width="3" stroke-linecap="round"' + dash +
      ' marker-end="url(#arrow)"/>';
    const b = route.label;
    if (edge.label && b) {
      shapes += '<rect id="edge-label-' + escape(edge.id) + '" x="' + b.x + '" y="' + b.y +
        '" width="' + b.width + '" height="' + b.height + '" rx="5" fill="#fff"/>';
      shapes += '<text x="' + num(b.x + b.width / 2) + '" y="' + num(b.y + b.height / 2) +
        '" text-anchor="middle" dominant-baseline="middle" font-size="17" data-fit-box="edge-label-' +
        escape(edge.id) + '" data-padding="3" data-min-font-size="15" data-lint-ignore-connectors="true">' +
        escape(edge.label) + '</text>';
    }
  }
  for (const node of scene.nodes) {
    const b = geom.nodes[node.id];
    shapes += '<g data-layout-object="' + escape(node.id) +
      '" data-node-id="' + escape(node.id) + '">';
    shapes += '<rect id="node-' + escape(node.id) + '" x="' + b.x + '" y="' + b.y +
      '" width="' + b.width + '" height="' + b.height + '" rx="14" fill="#ddf8e9" stroke="#111" stroke-width="3"/>';
    shapes += '<text x="' + num(b.x + b.width / 2) + '" y="' + num(b.y + b.height / 2) +
      '" text-anchor="middle" dominant-baseline="middle" font-size="21" font-weight="700"' +
      ' data-fit-box="node-' + escape(node.id) + '" data-padding="10" data-min-font-size="15">' +
      escape(node.label) + '</text></g>';
  }
  // A visible legend documents the semantics of the different line patterns.
  // Keep it outside the topology canvas's graph area (max graph bottom 820).
  const kinds = Object.keys(EDGE_STYLE).filter((kind) => scene.edges.some((edge) => edge.kind === kind));
  kinds.forEach((kind, i) => {
    const x = 68 + i * 297, style = EDGE_STYLE[kind];
    const dash = style.dash ? ' stroke-dasharray="' + style.dash + '"' : '';
    shapes += '<path d="M ' + x + ' 862 L ' + (x + 42) +
      ' 862" fill="none" stroke="' + style.stroke + '" stroke-width="3" stroke-linecap="round"' + dash + '/>';
    shapes += '<text x="' + (x + 53) +
      '" y="868" font-size="18">' + escape(kind[0].toUpperCase() + kind.slice(1)) + '</text>';
  });
  return '<!doctype html><html lang="en"><head><meta charset="utf-8"/>' +
    '<meta name="viewport" content="width=device-width,initial-scale=1"/>' +
    '<title>' + escape(title) + '</title><style>' +
    '*{box-sizing:border-box}body{margin:0;padding:12px;background:#eee;font-family:Arial,sans-serif}' +
    '.artifact{margin:auto;max-width:1600px;background:white}svg{width:100%;height:auto;display:block}' +
    'text{fill:#111;font-family:Arial,sans-serif}</style></head><body>' +
    '<main class="artifact" aria-label="' + escape(title) + '">' +
    '<svg viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">' +
    '<title id="title">' + escape(title) + '</title><desc id="desc">' +
    escape(scene.description || 'Verified scene graph with automatically routed connections.') + '</desc>' +
    '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">' +
    '<path d="M0 0 L10 5 L0 10Z" fill="#111"/></marker></defs>' +
    '<text x="800" y="72" text-anchor="middle" font-size="32" font-weight="800">' + escape(title) +
    '</text>' + shapes + '</svg></main>' + gate[0] + '</body></html>';
}

export async function generate(scene, previous = null) {
  const { geom, report } = await layoutScene(scene, previous);
  const html = await renderHtml(scene, geom);
  const lint = lintDocument(html);
  report.staticLint = { ok: lint.ok, errors: lint.errors.map((e) => e.code), warnings: lint.warnings.length };
  return { html, report };
}

async function main(args) {
  if (args.length < 2 || args.includes('--help')) {
    console.error('Usage: node auto-layout.mjs scene.json output.html [--report report.json] [--previous previous-report.json]');
    process.exitCode = 2; return;
  }
  const [input, output] = args;
  const argument = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null; };
  const reportPath = argument('--report');
  const previousPath = argument('--previous');
  const scene = JSON.parse(await readFile(resolve(input), 'utf8'));
  const previous = previousPath ? JSON.parse(await readFile(resolve(previousPath), 'utf8')) : null;
  const { html, report } = await generate(scene, previous);
  if (reportPath) {
    await mkdir(dirname(resolve(reportPath)), { recursive: true });
    await writeFile(resolve(reportPath), JSON.stringify(report, null, 2) + '\n');
  }
  if (!reportAccepted(report)) {
    throw new Error('Layout rejected by preflight; ' + JSON.stringify(report.staticLint.errors) +
      ', metrics=' + JSON.stringify(report.metrics));
  }
  await mkdir(dirname(resolve(output)), { recursive: true });
  await writeFile(resolve(output), html);
  console.log(JSON.stringify({ output, ...report }, null, 2));
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2)).catch((error) => {
    console.error(error.message); process.exitCode = 1;
  });
}
