/**
 * Style Dictionary v4+ Configuration
 * Design Tokens Platform - PHASE 2
 * 
 * Multi-platform token export:
 * - Web: CSS custom properties + JavaScript/TypeScript
 * - Tailwind: Preset configuration
 * - iOS: Swift enums
 * - Android: Kotlin objects
 * - Storybook: Addon integration
 */

import { fileHeader } from 'style-dictionary/utils';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default {
  // Source tokens
  source: ['01-tokens/tokens.dtcg.json'],

  // Build output directories
  platforms: {
    // ============================================
    // WEB — CSS + JavaScript/TypeScript
    // ============================================
    web: {
      transformGroup: 'web',
      buildPath: 'build/web/',
      files: [
        {
          destination: 'css/tokens.css',
          format: 'css/variables',
          options: {
            outputReferences: true
          }
        },
        {
          destination: 'css/tokens-with-metadata.css',
          format: 'css/variables-with-metadata',
          filter: (token) => token.$extensions?.metadata
        },
        {
          destination: 'js/tokens.js',
          format: 'javascript/es6',
          options: {
            outputReferences: true
          }
        },
        {
          destination: 'js/tokens.d.ts',
          format: 'typescript/es6-declarations',
          options: {
            outputReferences: true
          }
        },
        {
          destination: 'json/tokens.json',
          format: 'json/nested',
          options: {
            outputReferences: true
          }
        }
      ]
    },

    // ============================================
    // TAILWIND — Preset Configuration
    // ============================================
    tailwind: {
      transformGroup: 'web',
      buildPath: 'build/tailwind/',
      files: [
        {
          destination: 'tailwind.config.js',
          format: 'tailwind/config',
          options: {
            outputReferences: true
          }
        }
      ]
    },

    // ============================================
    // iOS — Swift Enums
    // ============================================
    ios: {
      transformGroup: 'ios',
      buildPath: 'build/ios/',
      files: [
        {
          destination: 'DesignTokens.swift',
          format: 'ios/swift/enum.swift',
          options: {
            outputReferences: true,
            accessControl: 'public'
          }
        }
      ]
    },

    // ============================================
    // Android — Kotlin Objects
    // ============================================
    android: {
      transformGroup: 'android',
      buildPath: 'build/android/',
      files: [
        {
          destination: 'kotlin/DesignTokens.kt',
          format: 'android/kotlin/object',
          options: {
            outputReferences: true,
            package: 'com.designmd.tokens'
          }
        },
        {
          destination: 'resources/values/design_tokens.xml',
          format: 'android/resources',
          options: {
            outputReferences: true
          }
        }
      ]
    },

    // ============================================
    // Storybook — Addon Integration
    // ============================================
    storybook: {
      transformGroup: 'web',
      buildPath: 'build/storybook/',
      files: [
        {
          destination: 'theme.js',
          format: 'storybook/theme',
          options: {
            outputReferences: true
          }
        },
        {
          destination: 'manager-head.html',
          format: 'storybook/manager-head',
          options: {
            outputReferences: true
          }
        }
      ]
    }
  },

  // ============================================
  // TRANSFORM GROUPS
  // ============================================
  transformGroups: {
    web: [
      'attribute/cti',
      'name/cti/kebab',
      'time/seconds',
      'content/icon',
      'size/rem',
      'color/hex',
      'stroke/weightToCss',
      'opacity/float',
      'fontFamily/css',
      'fontWeight/css',
      'fontSize/css',
      'lineHeight/css',
      'letterSpacing/css',
      'shadow/css',
      'border/css',
      'borderRadius/css',
      'motion/css',
      'tokenMetadata/web',
      'tokenName/web'
    ],
    ios: [
      'attribute/cti',
      'name/cti/camelCase',
      'time/seconds',
      'content/icon',
      'size/pt',
      'color/hex8ios',
      'stroke/weightToIos',
      'opacity/float',
      'fontFamily/ios',
      'fontWeight/ios',
      'fontSize/ios',
      'lineHeight/ios',
      'letterSpacing/ios',
      'shadow/ios',
      'border/ios',
      'borderRadius/ios',
      'motion/ios',
      'tokenMetadata/ios',
      'tokenName/ios'
    ],
    android: [
      'attribute/cti',
      'name/cti/camelCase',
      'time/seconds',
      'content/icon',
      'size/dp',
      'color/hex8android',
      'stroke/weightToAndroid',
      'opacity/float',
      'fontFamily/android',
      'fontWeight/android',
      'fontSize/android',
      'lineHeight/android',
      'letterSpacing/android',
      'shadow/android',
      'border/android',
      'borderRadius/android',
      'motion/android',
      'tokenMetadata/android',
      'tokenName/android'
    ]
  },

  // ============================================
  // CUSTOM TRANSFORMS
  // ============================================
  transforms: {
    // Metadata Transform — Add token metadata to output
    'tokenMetadata/web': {
      type: 'attribute',
      transformer: (token) => {
        const metadata = token.$extensions?.metadata || {};
        return {
          ...token.attributes,
          metadata: {
            element: metadata.element || [],
            attribute: metadata.attribute || '',
            purpose: metadata.purpose || '',
            category: metadata.category || 'primitive',
            wcagLevel: metadata.wcag_level || 'AA',
            brands: metadata.brands || {},
            coverage: metadata.coverage || {}
          }
        };
      }
    },
    'tokenMetadata/ios': {
      type: 'attribute',
      transformer: (token) => {
        const metadata = token.$extensions?.metadata || {};
        return {
          ...token.attributes,
          metadata: {
            element: metadata.element || [],
            attribute: metadata.attribute || '',
            purpose: metadata.purpose || '',
            wcagLevel: metadata.wcag_level || 'AA'
          }
        };
      }
    },
    'tokenMetadata/android': {
      type: 'attribute',
      transformer: (token) => {
        const metadata = token.$extensions?.metadata || {};
        return {
          ...token.attributes,
          metadata: {
            element: metadata.element || [],
            attribute: metadata.attribute || '',
            purpose: metadata.purpose || '',
            wcagLevel: metadata.wcag_level || 'AA'
          }
        };
      }
    },

    // Name Transform — Hierarchical naming for multi-platform
    'tokenName/web': {
      type: 'name',
      transformer: (token) => {
        const parts = token.path.join('-');
        return `--${parts}`;
      }
    },
    'tokenName/ios': {
      type: 'name',
      transformer: (token) => {
        const parts = token.path.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('');
        return parts;
      }
    },
    'tokenName/android': {
      type: 'name',
      transformer: (token) => {
        const parts = token.path.map(p => p.toUpperCase()).join('_');
        return parts;
      }
    }
  },

  // ============================================
  // CUSTOM FORMATS
  // ============================================
  formats: {
    // CSS with Metadata Comments
    'css/variables-with-metadata': {
      parser: ['attribute/cti'],
      formatter: function (options) {
        return function (dictionary, config) {
          let output = `${fileHeader({ file: config.file })}\n\n:root {\n`;
          
          dictionary.allTokens.forEach((token) => {
            const metadata = token.$extensions?.metadata;
            if (metadata) {
              output += `  /* ${metadata.purpose} • ${metadata.element.join(', ')} */\n`;
            }
            output += `  ${token.name}: ${token.value};\n`;
          });

          output += '\n}\n';
          return output;
        };
      }
    },

    // Tailwind Config Format
    'tailwind/config': {
      parser: ['attribute/cti'],
      formatter: function (options) {
        return function (dictionary, config) {
          let colorTokens = {};
          let spacingTokens = {};
          let fontTokens = {};

          dictionary.allTokens.forEach((token) => {
            if (token.type === 'color') {
              colorTokens[token.name] = token.value;
            } else if (token.type === 'spacing' || token.type === 'dimension') {
              spacingTokens[token.name] = token.value;
            } else if (token.type === 'fontSize' || token.type === 'fontFamily') {
              fontTokens[token.name] = token.value;
            }
          });

          return `export default {
  theme: {
    extend: {
      colors: ${JSON.stringify(colorTokens, null, 2)},
      spacing: ${JSON.stringify(spacingTokens, null, 2)},
      fontFamily: ${JSON.stringify(fontTokens, null, 2)}
    }
  }
};\n`;
        };
      }
    },

    // iOS Swift Enum
    'ios/swift/enum.swift': {
      parser: ['attribute/cti'],
      formatter: function (options) {
        return function (dictionary, config) {
          let output = `${fileHeader({ file: config.file })}\n\nimport UIKit\n\n`;
          output += `public enum DesignTokens {\n`;

          // Group by category
          const categories = {};
          dictionary.allTokens.forEach((token) => {
            const category = token.type || 'other';
            if (!categories[category]) {
              categories[category] = [];
            }
            categories[category].push(token);
          });

          for (const [category, tokens] of Object.entries(categories)) {
            output += `\n  // MARK: - ${category.toUpperCase()}\n`;
            tokens.forEach((token) => {
              output += `  public static let ${token.name} = "${token.value}"\n`;
            });
          }

          output += `}\n`;
          return output;
        };
      }
    },

    // Android Kotlin Object
    'android/kotlin/object': {
      parser: ['attribute/cti'],
      formatter: function (options) {
        return function (dictionary, config) {
          let output = `${fileHeader({ file: config.file })}\n\n`;
          output += `package ${options.package || 'com.designmd.tokens'}\n\n`;
          output += `object DesignTokens {\n`;

          // Group by category
          const categories = {};
          dictionary.allTokens.forEach((token) => {
            const category = token.type || 'other';
            if (!categories[category]) {
              categories[category] = [];
            }
            categories[category].push(token);
          });

          for (const [category, tokens] of Object.entries(categories)) {
            output += `\n  // ${category.toUpperCase()}\n`;
            tokens.forEach((token) => {
              output += `  const val ${token.name} = "${token.value}"\n`;
            });
          }

          output += `}\n`;
          return output;
        };
      }
    },

    // Storybook Theme
    'storybook/theme': {
      parser: ['attribute/cti'],
      formatter: function (options) {
        return function (dictionary, config) {
          const colors = {};
          dictionary.allTokens
            .filter(t => t.type === 'color')
            .forEach((token) => {
              colors[token.name] = token.value;
            });

          return `import { create } from '@storybook/theming';\n\n` +
            `export default create({\n` +
            `  base: 'light',\n` +
            `  colorPrimary: '${colors['color-action'] || '#5CD314'}',\n` +
            `  colorSecondary: '${colors['color-info'] || '#3B82F6'}',\n` +
            `  appBg: '${colors['background-surface'] || '#FFFFFF'}',\n` +
            `  appContentBg: '${colors['background-surface'] || '#FFFFFF'}',\n` +
            `  appBorderColor: '${colors['border-light'] || '#E5E7EB'}',\n` +
            `  textColor: '${colors['text-primary'] || '#1F2937'}',\n` +
            `  textInverseColor: '${colors['background-surface'] || '#FFFFFF'}',\n` +
            `  barBg: '${colors['background-surface'] || '#FFFFFF'}',\n` +
            `  barTextColor: '${colors['text-primary'] || '#1F2937'}',\n` +
            `  barSelectedColor: '${colors['color-action'] || '#5CD314'}',\n` +
            `  brandTitle: 'Design.MD',\n` +
            `  brandUrl: 'https://design.md',\n` +
            `  fontBase: '"Inter", "system-ui", "-apple-system", "sans-serif"',\n` +
            `  fontCode: '"Fira Code", "monospace"'\n` +
            `});\n`;
        };
      }
    },

    // Storybook Manager Head
    'storybook/manager-head': {
      parser: ['attribute/cti'],
      formatter: function (options) {
        return function (dictionary, config) {
          return `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">\n`;
        };
      }
    }
  }
};
