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
const cssSource = path.join(root, '01-tokens', 'tokens.css');
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

function cssPurpose(name) {
  const categories = [
    ['typography', 'Tipografía'],
    ['space', 'Espaciado'],
    ['radius', 'Radio de borde'],
    ['border', 'Borde'],
    ['shadow', 'Sombra'],
    ['motion', 'Movimiento'],
    ['media', 'Media'],
    ['heading', 'Jerarquía tipográfica'],
    ['body', 'Texto de cuerpo'],
    ['label', 'Etiqueta'],
    ['layout', 'Layout'],
    ['color', 'Color semántico'],
  ];
  const category = categories.find(([prefix]) => name.startsWith(`${prefix}-`));
  return category ? category[1] : 'Token genérico';
}

function extractCssTokens(css) {
  const tokens = [];
  const rules = css.matchAll(/([^{}]+)\{([^{}]*)\}/g);
  for (const match of rules) {
    const selector = match[1].trim();
    const declarations = match[2];
    const brandMatch = selector.match(/\[data-brand="([^"]+)"\]/);
    const themeMatch = selector.match(/\[data-theme="([^"]+)"\]/);
    const isRoot = selector.includes(':root') && !brandMatch && !themeMatch;
    if (!isRoot && (!brandMatch || !themeMatch)) continue;

    for (const declaration of declarations.matchAll(/--([a-z0-9-]+)\s*:\s*([^;]+);/gi)) {
      const name = declaration[1];
      tokens.push({
        name,
        cssName: `--${name}`,
        value: declaration[2].trim(),
        purpose: cssPurpose(name),
        brand: brandMatch?.[1] ?? null,
        theme: themeMatch?.[1] ?? null,
      });
    }
  }
  return tokens;
}

function write(relativePath, content) {
  const target = path.join(output, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, content);
}

function build() {
  const dtcg = JSON.parse(fs.readFileSync(source, 'utf8'));
  const tokens = flatten(dtcg);
  const genericTokens = extractCssTokens(fs.readFileSync(cssSource, 'utf8'));
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
  write('../assets/js/generic-tokens.js', `// Generated from 01-tokens/tokens.css\nwindow.GENERIC_TOKENS = ${JSON.stringify(genericTokens, null, 2)};\n`);

  write('tailwind/preset.js', `/** Generated from DTCG */\nexport default { theme: { extend: { designTokens: ${JSON.stringify(flat, null, 2)} } } };\n`);
  write('ios/Tokens.swift', `// Generated from DTCG\nimport Foundation\n\npublic enum DesignToken {\n${tokens.map((token) => `  public static let ${camelName(token)} = "${String(token.value).replaceAll('"', '\\"')}"`).join('\n')}\n}\n`);

  const colorTokens = tokens.filter((token) => token.type === 'color');
  write('android/values/tokens.xml', `<?xml version="1.0" encoding="utf-8"?>\n<resources>\n${colorTokens.map((token) => `  <color name="${androidName(token)}">${token.value}</color>`).join('\n')}\n</resources>\n`);
  write('android/Tokens.kt', `// Generated from DTCG\nobject DesignToken {\n${tokens.map((token) => `  const val ${androidName(token).toUpperCase()} = "${String(token.value).replaceAll('"', '\\"')}"`).join('\n')}\n}\n`);
  write('storybook/tokens.js', `// Generated from DTCG\nexport const designTokens = ${JSON.stringify(flat, null, 2)};\n`);

  const report = {
    generatedAt: new Date().toISOString(),
    source: '01-tokens/tokens.dtcg.json',
    tokenCount: tokens.length,
    genericCssSource: '01-tokens/tokens.css',
    genericCssTokenCount: genericTokens.length,
    platforms: ['web', 'tailwind', 'ios', 'android', 'storybook'],
  };
  write('build-report.json', `${JSON.stringify(report, null, 2)}\n`);
  console.log(`✅ Exported ${tokens.length} DTCG tokens and ${genericTokens.length} CSS tokens.`);
}

build();
if (watch) {
  console.log('👀 Watching DTCG and generic CSS token sources for changes…');
  [source, cssSource].forEach((file) => fs.watch(file, { persistent: true }, () => {
    try { build(); } catch (error) { console.error(`❌ Build failed: ${error.message}`); }
  }));
}
