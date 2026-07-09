#!/usr/bin/env node
/**
 * Dependency-free DTCG exporter.
 * Generates the platform artifacts consumed by this repository even when an
 * external package registry is unavailable. Source of truth: tokens.dtcg.json.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, '01-tokens', 'tokens.dtcg.json');
const output = path.join(root, 'build');
const watch = process.argv.includes('--watch');

function flatten(value, prefix = []) {
  if (value && typeof value === 'object' && '$value' in value) {
    return [{ path: prefix, value: value.$value, type: value.$type, metadata: value.$extensions?.metadata ?? {} }];
  }
  if (!value || typeof value !== 'object') return [];
  return Object.entries(value)
    .filter(([key]) => !key.startsWith('$'))
    .flatMap(([key, child]) => flatten(child, [...prefix, key]));
}

function cssName(token) {
  return `--${token.path.join('-')}`;
}

function camelName(token) {
  return token.path
    .join('-')
    .replace(/-([a-z0-9])/g, (_, letter) => letter.toUpperCase())
    .replace(/[^a-zA-Z0-9]/g, '');
}

function androidName(token) {
  return token.path.join('_').replace(/[^a-zA-Z0-9_]/g, '_');
}

function write(relativePath, content) {
  const target = path.join(output, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, content);
}

function build() {
  const dtcg = JSON.parse(fs.readFileSync(source, 'utf8'));
  const tokens = flatten(dtcg);
  const flat = Object.fromEntries(tokens.map((token) => [token.path.join('.'), token.value]));

  write('web/css/tokens.css', `/* Generated from 01-tokens/tokens.dtcg.json */\n:root {\n${tokens.map((token) => `  ${cssName(token)}: ${token.value};`).join('\n')}\n}\n`);
  write('web/js/tokens.js', `// Generated from DTCG\nexport const tokens = ${JSON.stringify(flat, null, 2)};\nexport default tokens;\n`);
  write('web/ts/tokens.ts', `// Generated from DTCG\nexport const tokens = ${JSON.stringify(flat, null, 2)} as const;\nexport type TokenName = keyof typeof tokens;\n`);
  write('web/json/tokens.json', `${JSON.stringify({ tokens: flat }, null, 2)}\n`);
  write('../assets/js/dtcg-tokens.js', `// Generated from 01-tokens/tokens.dtcg.json\nwindow.DTCG_TOKENS = ${JSON.stringify(tokens.map((token) => ({
    name: token.path.join('.'),
    cssName: cssName(token),
    value: token.value,
    type: token.type,
    purpose: token.metadata.purpose || 'Token de diseño',
  })), null, 2)};\n`);

  write('tailwind/preset.js', `/** Generated from DTCG */\nexport default { theme: { extend: { designTokens: ${JSON.stringify(flat, null, 2)} } } };\n`);
  write('ios/Tokens.swift', `// Generated from DTCG\nimport Foundation\n\npublic enum DesignToken {\n${tokens.map((token) => `  public static let ${camelName(token)} = "${String(token.value).replaceAll('"', '\\"')}"`).join('\n')}\n}\n`);

  const colorTokens = tokens.filter((token) => token.type === 'color');
  write('android/values/tokens.xml', `<?xml version="1.0" encoding="utf-8"?>\n<resources>\n${colorTokens.map((token) => `  <color name="${androidName(token)}">${token.value}</color>`).join('\n')}\n</resources>\n`);
  write('android/Tokens.kt', `// Generated from DTCG\nobject DesignToken {\n${tokens.map((token) => `  const val ${androidName(token).toUpperCase()} = "${String(token.value).replaceAll('"', '\\"')}"`).join('\n')}\n}\n`);
  write('storybook/tokens.js', `// Generated from DTCG\nexport const designTokens = ${JSON.stringify(flat, null, 2)};\n`);

  const report = { generatedAt: new Date().toISOString(), source: '01-tokens/tokens.dtcg.json', tokenCount: tokens.length, platforms: ['web', 'tailwind', 'ios', 'android', 'storybook'] };
  write('build-report.json', `${JSON.stringify(report, null, 2)}\n`);
  console.log(`✅ Exported ${tokens.length} tokens to Web, Tailwind, iOS, Android and Storybook.`);
}

build();
if (watch) {
  console.log('👀 Watching token source for changes…');
  fs.watch(source, { persistent: true }, () => {
    try { build(); } catch (error) { console.error(`❌ Build failed: ${error.message}`); }
  });
}
