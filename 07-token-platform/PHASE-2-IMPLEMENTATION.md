# Design Tokens Platform PHASE 2
> Multi-Platform Export using Style Dictionary v4+

---

## Overview

**PHASE 2** brings multi-platform token export to ds-base-kit, enabling developers to use design tokens natively on any platform:

- ✅ **Web:** CSS custom properties + JavaScript/TypeScript
- ✅ **Tailwind:** Preset configuration  
- ✅ **iOS:** Swift enums + UIColor extensions
- ✅ **Android:** Kotlin objects + Resource files
- ✅ **Storybook:** Theme customization + Manager head

### Architecture

```
tokens.dtcg.json (SSOT with metadata)
        ↓
Style Dictionary v4+ (config-driven)
        ↓
    Custom Transforms (metadata, naming, wcag)
        ↓
    Custom Formats (platform-specific output)
        ↓
build/ (multi-platform exports)
├── web/ (CSS, JS/TS, JSON)
├── tailwind/ (theme config)
├── ios/ (Swift)
├── android/ (Kotlin + XML)
└── storybook/ (theme + manager)
```

---

## Installation

### Prerequisites
- Node.js ≥ 18.0.0
- npm or yarn

### Setup

```bash
cd ds-base-kit

# Install dependencies
npm install

# Verify installation
npm run tokens:validate

# Build tokens for all platforms
npm run tokens:build
```

---

## Build System

### npm Scripts

| Command | Purpose | Output |
|---------|---------|--------|
| `npm run tokens:build` | Build all platforms | `build/` directory |
| `npm run tokens:build:watch` | Watch mode (live rebuild) | Continuous output |
| `npm run tokens:validate` | Validate + schema check | Pass/fail report |
| `npm run tokens:diff` | Generate changelog | `TOKENS-CHANGELOG.md` |
| `npm run tokens:migrate` | Detect + suggest migrations | Migration report |

### Example

```bash
# Single build
npm run tokens:build

# Output:
# ✅ web: 45ms
# ✅ tailwind: 12ms
# ✅ ios: 38ms
# ✅ android: 52ms
# ✅ storybook: 8ms

# Watch mode (auto-rebuild on token changes)
npm run tokens:build:watch
```

---

## Platform-Specific Exports

### 1. Web — CSS + JavaScript

**Location:** `build/web/`

#### CSS Output
```css
/* style-dictionary output */

:root {
  /* action • button, link, input */
  --color-action: #5CD314;
  
  /* success • alert, badge, icon */
  --color-success: #22C55E;
  
  /* spacing • any */
  --spacing-xs: 0.25rem;
}
```

#### JavaScript Output
```javascript
// ES6 module
export const colorAction = '#5CD314';
export const colorSuccess = '#22C55E';
export const spacingXs = '0.25rem';

// TypeScript definitions
export const colorAction: string;
export const colorSuccess: string;
export const spacingXs: string;
```

#### JSON Output
```json
{
  "color": {
    "action": "#5CD314",
    "success": "#22C55E"
  },
  "spacing": {
    "xs": "0.25rem"
  }
}
```

**Usage:**
```javascript
// CSS
<link rel="stylesheet" href="build/web/css/tokens.css">
.button { color: var(--color-action); }

// JavaScript
import { colorAction, spacingXs } from './build/web/js/tokens.js';
const buttonColor = colorAction; // #5CD314
```

---

### 2. Tailwind — Theme Configuration

**Location:** `build/tailwind/tailwind.config.js`

```javascript
export default {
  theme: {
    extend: {
      colors: {
        'color-action': '#5CD314',
        'color-success': '#22C55E',
        'color-danger': '#EF4444'
      },
      spacing: {
        'spacing-xs': '0.25rem',
        'spacing-sm': '0.5rem',
        'spacing-md': '1rem'
      }
    }
  }
};
```

**Usage:**
```bash
# Extend Tailwind config
module.exports = {
  presets: [require('./build/tailwind/tailwind.config.js')],
  // Additional config...
};
```

```html
<button class="text-color-action px-spacing-md py-spacing-sm">
  Click me
</button>
```

---

### 3. iOS — Swift Enums

**Location:** `build/ios/DesignTokens.swift`

```swift
import UIKit

public enum DesignTokens {
  // MARK: - Color
  public static let colorAction = "#5CD314"
  public static let colorSuccess = "#22C55E"
  public static let colorDanger = "#EF4444"
  
  // MARK: - Spacing
  public static let spacingXs = "0.25rem"
  public static let spacingMd = "1rem"
}
```

**Usage:**
```swift
import UIKit

class ViewController: UIViewController {
  override func viewDidLoad() {
    super.viewDidLoad()
    
    let button = UIButton()
    button.backgroundColor = UIColor(hex: DesignTokens.colorAction)
    button.contentEdgeInsets = UIEdgeInsets(
      top: 12,
      left: 16,
      bottom: 12,
      right: 16
    )
  }
}
```

---

### 4. Android — Kotlin Objects

**Location:** `build/android/kotlin/DesignTokens.kt`

```kotlin
package com.designmd.tokens

object DesignTokens {
  // COLOR
  const val COLOR_ACTION = "#5CD314"
  const val COLOR_SUCCESS = "#22C55E"
  const val COLOR_DANGER = "#EF4444"
  
  // SPACING
  const val SPACING_XS = "4dp"
  const val SPACING_MD = "16dp"
}
```

**Android XML Output:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<resources>
  <!-- Colors -->
  <color name="color_action">#5CD314</color>
  <color name="color_success">#22C55E</color>
  
  <!-- Dimensions -->
  <dimen name="spacing_xs">4dp</dimen>
  <dimen name="spacing_md">16dp</dimen>
</resources>
```

**Usage:**
```kotlin
// From Kotlin
val buttonColor = Color.parseColor(DesignTokens.COLOR_ACTION)

// From XML
<com.google.android.material.button.MaterialButton
  android:layout_margin="@dimen/spacing_md"
  app:backgroundTint="@color/color_action"
/>
```

---

### 5. Storybook — Theme Integration

**Location:** `build/storybook/theme.js`

```javascript
import { create } from '@storybook/theming';

export default create({
  base: 'light',
  colorPrimary: '#5CD314',
  colorSecondary: '#3B82F6',
  appBg: '#FFFFFF',
  appBorderColor: '#E5E7EB',
  textColor: '#1F2937',
  brandTitle: 'Design.MD',
  fontBase: '"Inter", system-ui, sans-serif'
});
```

**Usage in Storybook config:**
```javascript
// .storybook/manager.js
import { addons } from '@storybook/manager-api';
import theme from '../build/storybook/theme.js';

addons.setConfig({
  theme: theme
});
```

---

## Configuration

### style-dictionary.config.js

Main configuration file controlling all token builds.

#### Platforms Block
```javascript
platforms: {
  web: {
    transformGroup: 'web',
    buildPath: 'build/web/',
    files: [/* output files */]
  },
  ios: {
    transformGroup: 'ios',
    buildPath: 'build/ios/',
    files: [/* output files */]
  }
  // ... more platforms
}
```

#### Transform Groups
Pre-built sets of transforms for each platform:
- `web`: CSS/JS specific (kebab-case, hex colors, rem sizing)
- `ios`: Swift specific (camelCase, hex8 colors, pt sizing)
- `android`: Kotlin specific (UPPER_CASE, hex8 colors, dp sizing)

#### Custom Transforms
```javascript
transforms: {
  'tokenMetadata/web': { /* extracts metadata */ },
  'tokenName/web': { /* generates CSS var names */ },
  'tokenName/ios': { /* generates Swift enum names */ }
}
```

#### Custom Formats
```javascript
formats: {
  'css/variables-with-metadata': { /* CSS with metadata comments */ },
  'tailwind/config': { /* Tailwind preset */ },
  'ios/swift/enum.swift': { /* Swift enums */ },
  'android/kotlin/object': { /* Kotlin objects */ }
}
```

---

## Custom Transforms

### Token Metadata Transform

Extracts machine-readable metadata from `$extensions.metadata`:

```javascript
'tokenMetadata/web': {
  transformer: (token) => {
    const metadata = token.$extensions?.metadata || {};
    return {
      metadata: {
        element: metadata.element || [],
        attribute: metadata.attribute || '',
        purpose: metadata.purpose || '',
        category: metadata.category || 'primitive',
        wcagLevel: metadata.wcag_level || 'AA'
      }
    };
  }
}
```

**Usage:**
```javascript
// CSS output includes metadata in comments
/* action • button, link, input */
--color-action: #5CD314;

// Swift output preserves metadata
public static let colorAction = "#5CD314" // action, WCAG: AA
```

### Token Name Transform

Generates platform-specific naming conventions:

```javascript
'tokenName/web': {
  transformer: (token) => {
    return `--${token.path.join('-')}`; // --color-action
  }
},

'tokenName/ios': {
  transformer: (token) => {
    return token.path.map(p => 
      p.charAt(0).toUpperCase() + p.slice(1)
    ).join(''); // ColorAction
  }
},

'tokenName/android': {
  transformer: (token) => {
    return token.path.map(p => p.toUpperCase()).join('_'); // COLOR_ACTION
  }
}
```

### WCAG Compliance Transform

Validates and enforces WCAG compliance (coming in v2.3.1):

```javascript
'wcag/validate': {
  transformer: (token) => {
    const wcagLevel = token.$extensions?.metadata?.wcag_level || 'AA';
    const contrastRatio = token.$extensions?.metadata?.contrast_ratio || 0;
    
    // Validate contrast ratio meets level
    const minRatios = { A: 3, AA: 4.5, AAA: 7 };
    if (contrastRatio < minRatios[wcagLevel]) {
      console.warn(`Token ${token.path}: contrast below ${wcagLevel}`);
    }
  }
}
```

---

## Custom Formats

### CSS with Metadata
```css
/* Includes metadata comments alongside token values */

:root {
  /* action • button, link, input • WCAG: AA */
  --color-action: #5CD314;
}
```

### Tailwind Config
```javascript
export default {
  theme: {
    extend: {
      colors: { /* all color tokens */ },
      spacing: { /* all spacing tokens */ },
      fontFamily: { /* all font tokens */ }
    }
  }
};
```

### iOS Swift Enum
```swift
public enum DesignTokens {
  public static let colorAction = "#5CD314"
  // Swift-specific formatting + type safety
}
```

### Android Kotlin Object
```kotlin
object DesignTokens {
  const val COLOR_ACTION = "#5CD314"
  // Kotlin-specific formatting + package declaration
}
```

### Storybook Theme
```javascript
create({
  colorPrimary: '#5CD314', // Extracted from color.action token
  colorSecondary: '#3B82F6',
  // ... mapped to Storybook theme structure
});
```

---

## Workflow

### 1. Token Addition

Add new token to `01-tokens/tokens.dtcg.json`:
```json
{
  "color": {
    "new-token": {
      "$value": "#7C3AED",
      "$extensions": {
        "metadata": {
          "element": ["button"],
          "attribute": "background-color",
          "purpose": "action"
        }
      }
    }
  }
}
```

### 2. Validation

```bash
npm run tokens:validate

# Output:
# ✅ Metadata structure valid
# ✅ WCAG compliance checked
# ✅ Brand coverage verified
# ✅ Platform coverage confirmed
```

### 3. Build

```bash
npm run tokens:build

# Output:
# ✅ web: 45ms
# ✅ tailwind: 12ms
# ✅ ios: 38ms
# ✅ android: 52ms
# ✅ storybook: 8ms
```

### 4. Sync

Build outputs automatically synced to `01-tokens/`:
- `build/web/css/tokens.css` → `01-tokens/tokens.css`
- `build/web/js/tokens.js` → `01-tokens/tokens.js`
- `build/web/json/tokens.json` → `01-tokens/tokens.json`

### 5. Commit

```bash
git add 01-tokens/ build/
git commit -m "chore: update tokens (new color.new-token)"
git push origin main
```

Pre-commit hook validates new tokens automatically.

---

## Advanced Usage

### Watch Mode

Automatic rebuild on token changes:

```bash
npm run tokens:build:watch

# Terminal output:
# 📝 Tokens changed, rebuilding...
# ✅ web: 45ms
# ✅ tailwind: 12ms
# ... (auto-repeats on changes)
```

### Single Platform Build

Build only specific platform:

```bash
npm run tokens:build -- --platform=ios
# Only generates iOS Swift enums

npm run tokens:build -- --platform=tailwind
# Only generates Tailwind config
```

### Custom Transform/Format

Add custom transform in `style-dictionary.config.js`:

```javascript
transforms: {
  'myCustom/transform': {
    type: 'attribute',
    transformer: (token) => {
      // Custom logic here
      return token;
    }
  }
}
```

Then include in transformGroup:

```javascript
transformGroups: {
  web: [
    'attribute/cti',
    'myCustom/transform',
    // ... other transforms
  ]
}
```

---

## Troubleshooting

### Build Fails
```bash
npm run tokens:build

# Error: Cannot find module 'style-dictionary'
# Solution: npm install

# Error: Invalid token structure
# Solution: npm run tokens:validate (check for schema errors)
```

### Output Missing
```bash
# Check build directory
ls -la build/

# Check logs
cat logs/build-tokens.log

# Rebuild with verbose output
npm run tokens:build 2>&1 | tee build.log
```

### Platform-Specific Issues

**iOS:**
```bash
# Xcode cannot find DesignTokens.swift
# Solution: Add to Xcode project: File → Add Files → build/ios/DesignTokens.swift
```

**Android:**
```bash
# Gradle cannot find resources
# Solution: Ensure build/android/resources/values/ is in src/main/res/
```

---

## Next Steps (PHASE 3)

- ⏳ Token Generator Agent (proposes semantic tokens)
- ⏳ Migration Assistant Agent (detects hardcoded values)
- ⏳ Token Diff Reporter Agent (generates changelog)
- ⏳ Governance loop (Agent → Human → Merge)
- ⏳ CI/CD job: .github/workflows/validate-tokens.yml

---

## Reference

- **Config:** [style-dictionary.config.js](../style-dictionary.config.js)
- **Build Script:** [scripts/build-tokens.js](../scripts/build-tokens.js)
- **PHASE 1 Spec:** [07-token-platform/FASE-1-SCHEMA.md](../07-token-platform/FASE-1-SCHEMA.md)
- **PHASE 2 Spec:** [07-token-platform/FASE-2-STYLE-DICTIONARY.md](../07-token-platform/FASE-2-STYLE-DICTIONARY.md)

**Version:** 2.3.0 PHASE 2  
**Status:** 🟢 Production Ready  
**Last Updated:** 2026-07-09
