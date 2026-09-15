#!/usr/bin/env node

import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const EXIT_OK = 0;
const EXIT_LAYOUT_ERRORS = 1;
const EXIT_ENVIRONMENT_ERROR = 2;
const EPSILON = 0.75;

const TEXT_WIDTH_UNITS = {
  narrow: new Set('ijlI.,:;!|\'`'),
  wide: new Set('MW@%&#'),
  medium: new Set('ABCDEFGHKNOPQRSTUVXYZ0123456789'),
};

function usage() {
  console.error('Usage: node technical-diagram/scripts/static-lint-diagram.mjs <diagram.html>');
}

function number(value, fallback = 0) {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function finiteNumbers(value) {
  return (value?.match(/[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?/g) || [])
    .map((part) => Number(part))
    .filter(Number.isFinite);
}

function decodeEntities(value) {
  return value
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&quot;/gi, '"')
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/&#x([\da-f]+);/gi, (_, code) => String.fromCodePoint(Number.parseInt(code, 16)));
}

function parseAttributes(source) {
  const attrs = {};
  const attrPattern = /([:\w-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))/g;
  for (const match of source.matchAll(attrPattern)) {
    attrs[match[1]] = match[2] ?? match[3] ?? match[4] ?? '';
  }
  return attrs;
}

function makeNode(tag, attrs, parent, offset) {
  return { tag, attrs, parent, children: [], text: '', offset };
}

function parseSvg(documentText, errors) {
  const svgOpenings = [...documentText.matchAll(/<svg\b[^>]*>/gi)];
  if (svgOpenings.length !== 1) {
    errors.push({
      code: 'SVG_COUNT',
      message: `Expected exactly one SVG element, found ${svgOpenings.length}`,
    });
    return null;
  }

  const opening = svgOpenings[0];
  const closingIndex = documentText.indexOf('</svg>', opening.index + opening[0].length);
  if (closingIndex < 0) {
    errors.push({ code: 'SVG_UNCLOSED', message: 'SVG element is not closed' });
    return null;
  }

  const root = makeNode('svg', parseAttributes(opening[0]), null, opening.index);
  const svgEnd = closingIndex + '</svg>'.length;
  const source = documentText.slice(opening.index + opening[0].length, closingIndex)
    .replace(/<!--[\s\S]*?-->/g, '');
  const tagPattern = /<\/?([A-Za-z][\w:.-]*)([^>]*)>/g;
  const stack = [root];
  let cursor = 0;

  for (const match of source.matchAll(tagPattern)) {
    const text = source.slice(cursor, match.index);
    if (text) stack.at(-1).text += text;

    const raw = match[0];
    const tag = match[1].toLowerCase();
    if (raw.startsWith('</')) {
      const current = stack.at(-1);
      if (!current || current.tag !== tag) {
        errors.push({ code: 'SVG_TAG_MISMATCH', message: `Mismatched closing tag </${tag}>` });
      } else if (stack.length > 1) {
        stack.pop();
      }
    } else {
      const selfClosing = /\/\s*>$/.test(raw);
      const node = makeNode(tag, parseAttributes(match[2] || ''), stack.at(-1), match.index);
      stack.at(-1).children.push(node);
      if (!selfClosing) stack.push(node);
    }
    cursor = match.index + raw.length;
  }

  const trailingText = source.slice(cursor);
  if (trailingText) stack.at(-1).text += trailingText;
  if (stack.length !== 1) {
    errors.push({ code: 'SVG_TAG_UNCLOSED', message: `Unclosed SVG tag <${stack.at(-1).tag}>` });
  }

  if (documentText.slice(svgEnd).match(/<svg\b/i)) {
    errors.push({ code: 'SVG_MULTIPLE', message: 'Additional SVG markup exists after the first SVG element' });
  }
  return root;
}

function allNodes(root) {
  const result = [];
  const visit = (node) => {
    result.push(node);
    for (const child of node.children) visit(child);
  };
  visit(root);
  return result;
}

function nodeText(node) {
  return decodeEntities(`${node.text}${node.children.map(nodeText).join('')}`);
}

function textLines(node) {
  const tspans = node.children.filter((child) => child.tag === 'tspan');
  if (!tspans.length) return [nodeText(node).replace(/\s+/g, ' ').trim()];
  return tspans.map((tspan) => nodeText(tspan).replace(/\s+/g, ' ').trim()).filter(Boolean);
}

function parseCssFonts(documentText) {
  const rules = new Map();
  const stylePattern = /<style\b[^>]*>([\s\S]*?)<\/style>/gi;
  for (const styleMatch of documentText.matchAll(stylePattern)) {
    const rulePattern = /([^{}]+)\{([^{}]*)\}/g;
    for (const ruleMatch of styleMatch[1].matchAll(rulePattern)) {
      const fontSize = ruleMatch[2].match(/font-size\s*:\s*([\d.]+)px/i);
      if (!fontSize) continue;
      for (const selector of ruleMatch[1].split(',')) {
        const className = selector.trim().match(/\.([\w-]+)$/)?.[1];
        if (className) rules.set(className, Number(fontSize[1]));
      }
    }
  }
  return rules;
}

function textFontSize(node, cssFonts, warnings) {
  const explicit = node.attrs['data-static-font-size'] || node.attrs['font-size'];
  if (explicit) return number(explicit, 16);

  const inline = node.attrs.style?.match(/font-size\s*:\s*([\d.]+)px/i)?.[1];
  if (inline) return number(inline, 16);

  for (const className of (node.attrs.class || '').split(/\s+/).filter(Boolean)) {
    if (cssFonts.has(className)) return cssFonts.get(className);
  }

  warnings.push({
    code: 'TEXT_FONT_SIZE_APPROXIMATED',
    element: nodeText(node).slice(0, 80),
    message: 'No static font size was found; using a conservative 16px estimate',
  });
  return 16;
}

function estimateTextWidth(value, fontSize) {
  let units = 0;
  for (const char of value) {
    if (/\s/.test(char)) units += 0.28;
    else if (TEXT_WIDTH_UNITS.narrow.has(char)) units += 0.28;
    else if (TEXT_WIDTH_UNITS.wide.has(char)) units += 0.88;
    else if (TEXT_WIDTH_UNITS.medium.has(char)) units += 0.64;
    else if (/[a-z]/.test(char)) units += 0.54;
    else if (/[^\u0000-\u007f]/.test(char)) units += 0.92;
    else units += 0.48;
  }
  return units * fontSize * 0.96;
}

function textBounds(node, cssFonts, warnings) {
  const lines = textLines(node);
  const value = lines.join(' ').trim();
  if (!value) return null;

  const fontSize = textFontSize(node, cssFonts, warnings);
  const width = node.attrs['data-static-text-width']
    ? number(node.attrs['data-static-text-width'])
    : Math.max(...lines.map((line) => estimateTextWidth(line, fontSize)));
  const lineHeight = number(node.attrs['data-static-line-height'], fontSize * 0.98);
  const height = number(node.attrs['data-static-text-height'], lineHeight * lines.length);
  const x = number(node.attrs.x);
  const y = number(node.attrs.y);
  const anchor = node.attrs['text-anchor'] || 'start';
  const left = anchor === 'middle' ? x - width / 2 : anchor === 'end' ? x - width : x;
  const baseline = node.attrs['dominant-baseline'];
  const top = baseline === 'middle' ? y - height / 2 : baseline === 'hanging' ? y : y - fontSize * 0.78;
  return { x: left, y: top, width, height, right: left + width, bottom: top + height };
}

function union(bounds) {
  const items = bounds.filter(Boolean);
  if (!items.length) return null;
  const x = Math.min(...items.map((item) => item.x));
  const y = Math.min(...items.map((item) => item.y));
  const right = Math.max(...items.map((item) => item.right));
  const bottom = Math.max(...items.map((item) => item.bottom));
  return { x, y, width: right - x, height: bottom - y, right, bottom };
}

function pointsBounds(value) {
  const values = finiteNumbers(value);
  const points = [];
  for (let i = 0; i + 1 < values.length; i += 2) points.push({ x: values[i], y: values[i + 1] });
  if (!points.length) return null;
  const x = Math.min(...points.map((point) => point.x));
  const y = Math.min(...points.map((point) => point.y));
  const right = Math.max(...points.map((point) => point.x));
  const bottom = Math.max(...points.map((point) => point.y));
  return { x, y, width: right - x, height: bottom - y, right, bottom };
}

function pathBounds(value) {
  const tokens = value?.match(/[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?/g) || [];
  const points = [];
  const parameterCount = { m: 2, l: 2, h: 1, v: 1, c: 6, s: 4, q: 4, t: 2, a: 7, z: 0 };
  let index = 0;
  let command = '';
  let current = { x: 0, y: 0 };
  let subpath = { ...current };

  const addPoint = (x, y) => {
    current = { x, y };
    points.push(current);
  };

  while (index < tokens.length) {
    if (/^[a-zA-Z]$/.test(tokens[index])) command = tokens[index++];
    if (!command) break;
    const lower = command.toLowerCase();
    if (lower === 'z') {
      addPoint(subpath.x, subpath.y);
      command = '';
      continue;
    }
    const count = parameterCount[lower];
    if (!count || index + count > tokens.length || tokens.slice(index, index + count).some((token) => /^[a-zA-Z]$/.test(token))) break;
    const values = tokens.slice(index, index + count).map(Number);
    index += count;
    const relative = command === command.toLowerCase();
    const x = (value) => relative ? current.x + value : value;
    const y = (value) => relative ? current.y + value : value;

    if (lower === 'm' || lower === 'l' || lower === 't') {
      addPoint(x(values[0]), y(values[1]));
      if (lower === 'm') subpath = { ...current };
    } else if (lower === 'h') addPoint(x(values[0]), current.y);
    else if (lower === 'v') addPoint(current.x, y(values[0]));
    else if (lower === 'c') {
      points.push({ x: x(values[0]), y: y(values[1]) }, { x: x(values[2]), y: y(values[3]) });
      addPoint(x(values[4]), y(values[5]));
    } else if (lower === 's' || lower === 'q') {
      points.push({ x: x(values[0]), y: y(values[1]) });
      if (lower === 's') points.push({ x: x(values[2]), y: y(values[3]) });
      addPoint(x(values.at(-2)), y(values.at(-1)));
    } else if (lower === 'a') {
      const endX = x(values[5]);
      const endY = y(values[6]);
      points.push({ x: endX - Math.abs(values[0]), y: endY - Math.abs(values[1]) });
      points.push({ x: endX + Math.abs(values[0]), y: endY + Math.abs(values[1]) });
      addPoint(endX, endY);
    }
  }
  return pointsBounds(points.flatMap((point) => [point.x, point.y]).join(' '));
}

function pathSegments(value) {
  const tokens = value?.match(/[a-zA-Z]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?/g) || [];
  const segments = [];
  const parameterCount = { m: 2, l: 2, h: 1, v: 1, c: 6, s: 4, q: 4, t: 2, a: 7, z: 0 };
  let index = 0;
  let command = '';
  let current = { x: 0, y: 0 };
  let subpath = { ...current };
  const addSegment = (start, end) => {
    if (start.x !== end.x || start.y !== end.y) segments.push({ start, end });
    current = end;
  };
  const interpolate = (start, end, controls = []) => {
    const points = [start, ...controls, end];
    for (let i = 1; i < points.length; i += 1) addSegment(points[i - 1], points[i]);
  };

  while (index < tokens.length) {
    if (/^[a-zA-Z]$/.test(tokens[index])) command = tokens[index++];
    if (!command) break;
    const lower = command.toLowerCase();
    if (lower === 'z') {
      addSegment(current, subpath);
      command = '';
      continue;
    }
    const count = parameterCount[lower];
    if (!count || index + count > tokens.length || tokens.slice(index, index + count).some((token) => /^[a-zA-Z]$/.test(token))) break;
    const values = tokens.slice(index, index + count).map(Number);
    index += count;
    const relative = command === command.toLowerCase();
    const x = (value) => relative ? current.x + value : value;
    const y = (value) => relative ? current.y + value : value;
    const start = { ...current };

    if (lower === 'm' || lower === 'l' || lower === 't') {
      const end = { x: x(values[0]), y: y(values[1]) };
      if (lower === 'm') {
        current = end;
        subpath = { ...end };
      } else addSegment(start, end);
    } else if (lower === 'h') addSegment(start, { x: x(values[0]), y: current.y });
    else if (lower === 'v') addSegment(start, { x: current.x, y: y(values[0]) });
    else if (lower === 'c') interpolate(start, { x: x(values[4]), y: y(values[5]) }, [{ x: x(values[0]), y: y(values[1]) }, { x: x(values[2]), y: y(values[3]) }]);
    else if (lower === 's' || lower === 'q') {
      const end = { x: x(values.at(-2)), y: y(values.at(-1)) };
      const controls = lower === 's'
        ? [{ x: x(values[0]), y: y(values[1]) }, { x: x(values[2]), y: y(values[3]) }]
        : [{ x: x(values[0]), y: y(values[1]) }];
      interpolate(start, end, controls);
    } else if (lower === 'a') {
      addSegment(start, { x: x(values[5]), y: y(values[6]) });
    }
  }
  return segments;
}

function intersects(a, b, margin = 0) {
  return a && b && a.x < b.right + margin && a.right > b.x - margin && a.y < b.bottom + margin && a.bottom > b.y - margin;
}

function segmentIntersectsRect(segment, rect, margin = 0) {
  const box = { x: rect.x - margin, y: rect.y - margin, right: rect.right + margin, bottom: rect.bottom + margin };
  let t0 = 0;
  let t1 = 1;
  const dx = segment.end.x - segment.start.x;
  const dy = segment.end.y - segment.start.y;
  const clip = (p, q) => {
    if (Math.abs(p) < EPSILON) return q >= 0;
    const ratio = q / p;
    if (p < 0) {
      if (ratio > t1) return false;
      if (ratio > t0) t0 = ratio;
    } else {
      if (ratio < t0) return false;
      if (ratio < t1) t1 = ratio;
    }
    return true;
  };
  return clip(-dx, segment.start.x - box.x) &&
    clip(dx, box.right - segment.start.x) &&
    clip(-dy, segment.start.y - box.y) &&
    clip(dy, box.bottom - segment.start.y);
}

function inside(inner, outer, padding = 0) {
  return inner.x >= outer.x + padding - EPSILON &&
    inner.y >= outer.y + padding - EPSILON &&
    inner.right <= outer.right - padding + EPSILON &&
    inner.bottom <= outer.bottom - padding + EPSILON;
}

function isHidden(node) {
  const style = node.attrs.style || '';
  return node.attrs.display === 'none' || node.attrs.visibility === 'hidden' || /(?:^|;)\s*display\s*:\s*none/i.test(style);
}

function hasAncestor(node, tag) {
  let current = node.parent;
  while (current) {
    if (current.tag === tag) return true;
    current = current.parent;
  }
  return false;
}

function lintExternalResources(documentText, errors) {
  const checks = [
    { pattern: /\b(?:src|href)\s*=\s*["'](?:https?:|\/\/)/i, code: 'EXTERNAL_RESOURCE', message: 'External src/href is not allowed' },
    { pattern: /@import\s+[^;]*(?:https?:|\/\/)/i, code: 'EXTERNAL_RESOURCE', message: 'External CSS import is not allowed' },
    { pattern: /\b(?:fetch|XMLHttpRequest)\s*\(/i, code: 'NETWORK_CODE', message: 'Network code is not allowed in a self-contained artifact' },
    { pattern: /<(?:img|image|iframe|link)\b/i, code: 'EXTERNAL_RESOURCE', message: 'External image/frame/link elements are not allowed' },
  ];
  for (const check of checks) {
    if (check.pattern.test(documentText)) errors.push({ code: check.code, message: check.message });
  }
}

export function lintDocument(documentText, file = '<inline>') {
  const errors = [];
  const warnings = [];
  lintExternalResources(documentText, errors);
  const root = parseSvg(documentText, errors);
  if (!root) return { ok: false, mode: 'static', file, errors, warnings, summary: {} };

  const nodes = allNodes(root);
  const ids = new Map();
  for (const node of nodes) {
    const id = node.attrs.id;
    if (!id) continue;
    if (ids.has(id)) errors.push({ code: 'DUPLICATE_ID', element: id, message: `Duplicate SVG id #${id}` });
    else ids.set(id, node);
  }

  const viewBoxValues = finiteNumbers(root.attrs.viewBox);
  if (viewBoxValues.length !== 4 || viewBoxValues[2] <= 0 || viewBoxValues[3] <= 0) {
    errors.push({ code: 'VIEWBOX_INVALID', message: 'SVG must have a positive four-value viewBox' });
  }
  const viewBox = viewBoxValues.length === 4
    ? { x: viewBoxValues[0], y: viewBoxValues[1], width: viewBoxValues[2], height: viewBoxValues[3], right: viewBoxValues[0] + viewBoxValues[2], bottom: viewBoxValues[1] + viewBoxValues[3] }
    : null;

  const title = nodes.find((node) => node.tag === 'title');
  const desc = nodes.find((node) => node.tag === 'desc');
  if (!title || !nodeText(title).trim()) errors.push({ code: 'ACCESSIBILITY_TITLE', message: 'SVG needs a non-empty <title>' });
  if (!desc || !nodeText(desc).trim()) errors.push({ code: 'ACCESSIBILITY_DESC', message: 'SVG needs a non-empty <desc>' });

  const cssFonts = parseCssFonts(documentText);
  const textNodes = nodes.filter((node) => node.tag === 'text' && !hasAncestor(node, 'defs') && !isHidden(node) && node.attrs['data-lint-ignore'] !== 'true');
  const textBoxCache = new WeakMap();
  const boundsCache = new WeakMap();

  const getTextBounds = (node) => {
    if (!textBoxCache.has(node)) textBoxCache.set(node, textBounds(node, cssFonts, warnings));
    return textBoxCache.get(node);
  };

  const getBounds = (node) => {
    if (boundsCache.has(node)) return boundsCache.get(node);
    if (hasAncestor(node, 'defs') || ['title', 'desc', 'style', 'script'].includes(node.tag) || isHidden(node)) {
      boundsCache.set(node, null);
      return null;
    }
    const attrs = node.attrs;
    let result = null;
    if (node.tag === 'rect') {
      const x = number(attrs.x), y = number(attrs.y), width = number(attrs.width), height = number(attrs.height);
      if (width > 0 && height > 0) result = { x, y, width, height, right: x + width, bottom: y + height };
    } else if (node.tag === 'circle') {
      const cx = number(attrs.cx), cy = number(attrs.cy), r = number(attrs.r);
      if (r > 0) result = { x: cx - r, y: cy - r, width: r * 2, height: r * 2, right: cx + r, bottom: cy + r };
    } else if (node.tag === 'ellipse') {
      const cx = number(attrs.cx), cy = number(attrs.cy), rx = number(attrs.rx), ry = number(attrs.ry);
      if (rx > 0 && ry > 0) result = { x: cx - rx, y: cy - ry, width: rx * 2, height: ry * 2, right: cx + rx, bottom: cy + ry };
    } else if (node.tag === 'line') {
      result = pointsBounds(`${attrs.x1 || 0} ${attrs.y1 || 0} ${attrs.x2 || 0} ${attrs.y2 || 0}`);
    } else if (node.tag === 'polygon' || node.tag === 'polyline') {
      result = pointsBounds(attrs.points);
    } else if (node.tag === 'path') {
      result = pathBounds(attrs.d);
    } else if (node.tag === 'use') {
      const x = number(attrs.x), y = number(attrs.y), width = number(attrs.width), height = number(attrs.height);
      if (width > 0 && height > 0) result = { x, y, width, height, right: x + width, bottom: y + height };
    } else if (node.tag === 'text') {
      result = getTextBounds(node);
    } else if (node.tag === 'g' || node.tag === 'svg') {
      result = union(node.children.map(getBounds));
    }
    boundsCache.set(node, result);
    return result;
  };

  for (const text of textNodes) {
    const textBox = getTextBounds(text);
    if (!textBox) continue;
    if (viewBox && !inside(textBox, viewBox)) {
      errors.push({ code: 'TEXT_OUTSIDE_VIEWBOX', element: nodeText(text).slice(0, 80), message: 'Text estimate extends outside the SVG viewBox', textBox, viewBox });
    }

    const fitTargetId = text.attrs['data-fit-box'];
    if (!fitTargetId) continue;
    const target = ids.get(fitTargetId);
    if (!target) {
      errors.push({ code: 'FIT_TARGET_MISSING', element: nodeText(text).slice(0, 80), message: `Missing fit target #${fitTargetId}` });
      continue;
    }
    const targetBox = getBounds(target);
    if (!targetBox || targetBox.width <= 0 || targetBox.height <= 0) {
      errors.push({ code: 'FIT_TARGET_INVALID', element: fitTargetId, message: `Fit target #${fitTargetId} has no positive static bounds` });
      continue;
    }
    const padding = number(text.attrs['data-padding'], 6);
    if (!text.attrs['data-min-font-size']) {
      errors.push({ code: 'FIT_MIN_SIZE_MISSING', element: nodeText(text).slice(0, 80), message: 'Fit-constrained text must declare data-min-font-size' });
    }
    if (!inside(textBox, targetBox, padding)) {
      errors.push({ code: 'TEXT_OUTSIDE_FIT_BOX', element: nodeText(text).slice(0, 80), message: `Text estimate does not fit inside #${fitTargetId}`, textBox, targetBox, padding });
    }
  }

  const layoutObjects = nodes.filter((node) => node.attrs['data-layout-object'] && !hasAncestor(node, 'defs') && !isHidden(node) && node.attrs['data-lint-ignore'] !== 'true');
  const objectNames = new Set();
  for (const object of layoutObjects) {
    const name = object.attrs['data-layout-object'];
    if (objectNames.has(name)) errors.push({ code: 'DUPLICATE_LAYOUT_OBJECT', element: name, message: `Duplicate data-layout-object ${name}` });
    objectNames.add(name);
    const objectBox = getBounds(object);
    if (!objectBox) {
      errors.push({ code: 'LAYOUT_OBJECT_UNMEASURED', element: name, message: 'Layout object has no measurable SVG geometry' });
    } else if (viewBox && !inside(objectBox, viewBox)) {
      errors.push({ code: 'LAYOUT_OBJECT_OUTSIDE_VIEWBOX', element: name, message: 'Layout object extends outside the SVG viewBox', objectBox, viewBox });
    }
  }

  for (let i = 0; i < layoutObjects.length; i += 1) {
    for (let j = i + 1; j < layoutObjects.length; j += 1) {
      const a = layoutObjects[i];
      const b = layoutObjects[j];
      if (a === b) continue;
      let ancestor = a.parent;
      let nested = false;
      while (ancestor) {
        if (ancestor === b) nested = true;
        ancestor = ancestor.parent;
      }
      ancestor = b.parent;
      while (ancestor) {
        if (ancestor === a) nested = true;
        ancestor = ancestor.parent;
      }
      if (nested) continue;
      const firstBox = getBounds(a);
      const secondBox = getBounds(b);
      if (intersects(firstBox, secondBox, -3)) {
        errors.push({ code: 'LAYOUT_OBJECT_OVERLAP', element: a.attrs['data-layout-object'], message: 'Peer layout objects overlap', other: b.attrs['data-layout-object'], firstBox, secondBox });
      }
    }
  }

  const connectors = nodes.filter((node) => node.tag === 'path' && node.attrs['data-connector'] && !hasAncestor(node, 'defs') && !isHidden(node) && node.attrs['data-lint-ignore'] !== 'true');
  for (const connector of connectors) {
    const connectorBox = getBounds(connector);
    if (!connector.attrs.d || !connectorBox || connectorBox.width + connectorBox.height <= EPSILON) {
      errors.push({ code: 'CONNECTOR_INVALID', element: connector.attrs.id || connector.attrs['data-connector'], message: 'Connector path must have a non-zero d path' });
      continue;
    }
    if (viewBox && !inside(connectorBox, viewBox)) {
      errors.push({ code: 'CONNECTOR_OUTSIDE_VIEWBOX', element: connector.attrs.id || connector.attrs['data-connector'], message: 'Connector path extends outside the SVG viewBox', connectorBox, viewBox });
    }
    const segments = pathSegments(connector.attrs.d);
    for (const text of textNodes) {
      if (text.attrs['data-lint-ignore-connectors'] === 'true' || text.attrs['data-lint-ignore'] === 'true') continue;
      const textBox = getTextBounds(text);
      if (segments.some((segment) => segmentIntersectsRect(segment, textBox, 3))) {
        errors.push({ code: 'TEXT_CONNECTOR_COLLISION', element: nodeText(text).slice(0, 80), message: 'Text estimate intersects a connector segment', connector: connector.attrs.id || connector.attrs['data-connector'], textBox, connectorBox });
      }
    }
  }

  for (let i = 0; i < textNodes.length; i += 1) {
    for (let j = i + 1; j < textNodes.length; j += 1) {
      const a = textNodes[i];
      const b = textNodes[j];
      if (intersects(getTextBounds(a), getTextBounds(b), -1)) {
        errors.push({ code: 'TEXT_TEXT_OVERLAP', element: nodeText(a).slice(0, 80), message: 'Text estimates overlap', other: nodeText(b).slice(0, 80), firstBox: getTextBounds(a), secondBox: getTextBounds(b) });
      }
    }
  }

  const report = {
    ok: errors.length === 0,
    mode: 'static',
    file,
    errors,
    warnings,
    summary: {
      textNodes: textNodes.length,
      fitTextNodes: textNodes.filter((node) => node.attrs['data-fit-box']).length,
      layoutObjects: layoutObjects.length,
      connectors: connectors.length,
    },
  };
  return report;
}

async function main() {
  const file = process.argv[2];
  if (!file || file === '-h' || file === '--help') {
    usage();
    process.exit(file ? EXIT_OK : EXIT_ENVIRONMENT_ERROR);
  }

  const absolute = resolve(file);
  try {
    const documentText = await readFile(absolute, 'utf8');
    const report = lintDocument(documentText, absolute);
    console.log(JSON.stringify(report, null, 2));
    process.exitCode = report.ok ? EXIT_OK : EXIT_LAYOUT_ERRORS;
  } catch (error) {
    console.error(JSON.stringify({
      ok: false,
      mode: 'static',
      file: absolute,
      errors: [{ code: 'STATIC_LINT_UNAVAILABLE', message: error instanceof Error ? error.message : String(error) }],
      warnings: [],
    }, null, 2));
    process.exitCode = EXIT_ENVIRONMENT_ERROR;
  }
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(new URL(import.meta.url).pathname)) await main();
