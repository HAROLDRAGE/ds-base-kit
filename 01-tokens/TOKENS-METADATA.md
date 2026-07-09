# Tokens Metadata Schema v2.3.0
> Machine-Readable Design Tokens with Semantic and Governance Information

---

## Overview

Starting with **v2.3.0**, all design tokens include machine-readable metadata that enables:

- ✅ **Automated validation** (WCAG, brand coverage, platform coverage)
- ✅ **Agent reasoning** (Schema Validator, Generator, Migration Assistant, Diff Reporter)
- ✅ **Enterprise governance** (deprecation policy, coverage matrix, compliance)
- ✅ **White label support** (brand overrides, theme variants)
- ✅ **Backward compatibility** (aliases, symlinks, migration path)

---

## Structure

### Token Anatomy

Each token in `tokens.dtcg.json` now includes:

```json
{
  "color": {
    "action": {
      "$value": "#5CD314",
      "$type": "color",
      "$extensions": {
        "metadata": {
          "element": ["button", "link", "input"],
          "attribute": "color",
          "purpose": "action",
          "category": "semantic",
          "wcag_level": "AA",
          "contrast_ratio": 4.5,
          "state": ["default", "hover", "active"],
          "brands": {
            "promptea": { "light": "#5CD314", "dark": "#7CFC00" },
            "nova": { "light": "#7C3AED", "dark": "#A78BFA" },
            "ocean": { "light": "#0284C7", "dark": "#38BDF8" }
          },
          "deprecation": { "deprecated": false },
          "related_tokens": ["color-action-hover"],
          "design_decision": "Primary action color for main CTAs",
          "figma_linked": true,
          "aliases": ["color-primary"],
          "tags": ["interactive", "primary"],
          "coverage": {
            "web": true,
            "ios": true,
            "android": true,
            "tailwind": true,
            "storybook": true
          }
        }
      }
    }
  }
}
```

### Metadata Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `element` | `string[]` | ✅ | UI elements this token applies to (button, link, input, etc.) |
| `attribute` | `string` | ✅ | CSS attribute (color, background-color, margin, etc.) |
| `purpose` | `string` | ✅ | Semantic purpose (action, success, warning, danger, info, etc.) |
| `category` | `string` | ✅ | primitive \| semantic \| component |
| `wcag_level` | `string` | ❌ | A \| AA \| AAA (default: AA) |
| `contrast_ratio` | `number` | ❌ | Min contrast ratio for color tokens |
| `state` | `string[]` | ❌ | Component states (default, hover, active, focus, disabled, etc.) |
| `brands` | `object` | ❌ | Brand overrides {brand: {theme: value}} |
| `deprecation` | `object` | ❌ | {deprecated, removal_date, replacement, reason} |
| `related_tokens` | `string[]` | ❌ | Dependent or related tokens |
| `design_decision` | `string` | ❌ | Reasoning for this token's values |
| `figma_linked` | `boolean` | ❌ | Is this synced with Figma tokens? |
| `aliases` | `string[]` | ❌ | Alternative names for backward compatibility |
| `tags` | `string[]` | ❌ | Searchable tags (interactive, primary, etc.) |
| `coverage` | `object` | ❌ | Platform coverage {web, ios, android, tailwind, storybook} |

---

## Valid Enums

### Purposes
```
action, success, warning, danger, info, neutral,
background, surface, text, border, focus, disabled,
heading, body, caption, code, label, button,
xs, sm, md, lg, xl, 2xl
```

### Categories
```
primitive (base values)
semantic (intent-based)
component (UI-specific)
```

### States
```
default, hover, active, focus, disabled, error, success, warning, loading
```

### Attributes (for CSS)
```
color, background-color, border-color, border-radius, border-width,
margin, padding, gap, inset, font-size, font-weight, line-height,
letter-spacing, text-decoration, box-shadow, opacity
```

### Platforms
```
web (CSS, JS/TS, Tailwind)
ios (Swift)
android (Kotlin)
storybook (Addon integration)
```

---

## Validation Rules

### Pre-Commit Hook
All commits are validated for:

1. ✅ **Required fields** (element, attribute, purpose, category)
2. ✅ **Valid enums** (no misspelled values)
3. ✅ **WCAG compliance** (contrast ratios match level)
4. ✅ **Brand coverage** (all brands + themes present)
5. ✅ **Platform coverage** (all platforms defined)
6. ✅ **Deprecation integrity** (if deprecated, has replacement)

### Pre-Push Validation
Additional checks before merge:

1. ✅ **No hardcoded values** (only token references)
2. ✅ **Aliases resolve** (backward compat checked)
3. ✅ **No circular dependencies** (tokens don't reference themselves)
4. ✅ **Figma sync status** (if figma_linked=true, matches Figma)

### Validación por agentes
When used by agents:

1. ✅ **Token Schema Validator** — Metadata structure + WCAG + coverage
2. ✅ **Token Generator** — Proposes semantic tokens from components
3. ✅ **Migration Assistant** — Detects hardcoded values → suggests tokens
4. ✅ **Token Diff Reporter** — Changelog generation + breaking change detection

---

## Backward Compatibility

### Aliases (v2.2.1 → v2.3.0)

Old name → New path:
```json
"color-action" → "color.semantic.action"
"color-success" → "color.semantic.success"
"spacing-md" → "spacing.primitive.md"
```

Defined in `tokens.aliases.json`:
```json
{
  "color": {
    "action": "color.semantic.action"
  }
}
```

### Migration Path

**Aliases activos:** los nombres anteriores permanecen disponibles cuando están definidos en el catálogo.
```javascript
// Old way still works:
import { colorAction } from "tokens.js";

// New way (better):
import { mdsSemanticColorAction } from "tokens.dtcg.js";
```

Los cambios de alias se gestionan mediante metadata de desuso y validación automatizada.
```javascript
// Old way generates warning:
// Warning: "colorAction" alias deprecated, use "mdsSemanticColorAction"
import { colorAction } from "tokens.js";
```

## White Label (Brands)

### Brand-Specific Overrides

All color tokens support 3 brands × 2 themes:

```json
{
  "color": {
    "action": {
      "$value": "#5CD314",  // Promptea light default
      "$extensions": {
        "metadata": {
          "brands": {
            "promptea": { "light": "#5CD314", "dark": "#7CFC00" },
            "nova": { "light": "#7C3AED", "dark": "#A78BFA" },
            "ocean": { "light": "#0284C7", "dark": "#38BDF8" }
          }
        }
      }
    }
  }
}
```

### Using in CSS

```css
:root[data-brand="promptea"][data-theme="light"] {
  --color-action: #5CD314;
}

:root[data-brand="nova"][data-theme="light"] {
  --color-action: #7C3AED;
}

:root[data-brand="ocean"][data-theme="light"] {
  --color-action: #0284C7;
}
```

### Using in JavaScript

```javascript
const getBrandToken = (tokenPath, brand, theme) => {
  const brands = tokens.color.action.$extensions.metadata.brands;
  return brands[brand]?.[theme] || tokens.color.action.$value;
};

const actionColor = getBrandToken("color.action", "nova", "light");
// → "#7C3AED"
```

---

## Deprecation Policy

### Marking a Token as Deprecated

```json
{
  "color": {
    "old-action": {
      "$value": "#5CD314",
      "$extensions": {
        "metadata": {
          "deprecation": {
            "deprecated": true,
            "replacement": "color.action",
            "removal_date": "2026-10-09",
            "reason": "Renamed to follow naming convention"
          }
        }
      }
    }
  }
}
```

### Ciclo de desuso

1. **Marcado:** el token se declara como obsoleto con reemplazo y fecha de retirada.
   - ✅ Still exports and functions
   - ⚠️ Agents warn consumers
   - 📋 Release notes explain migration

2. **Alias:** se conserva una ruta de compatibilidad durante el periodo definido.
   - ✅ Token still exported
   - ✅ Alias created: `old-action` → `color.action`
   - 🤖 Migration script available: `npm run tokens:migrate --from-deprecated`

3. **Retirada:** la eliminación se considera un cambio incompatible y se documenta en el changelog.
   - ✅ Token removed from exports
   - ❌ Alias gone
   - 💥 Breaking change (major version bump)

---

## WCAG Compliance

All color tokens declare their accessibility level:

### Level A (Minimum)
- Contrast ratio: ≥ 3:1
- For large text only (18pt+)

### Level AA (Standard)
- Contrast ratio: ≥ 4.5:1
- Recommended for normal text
- **Default in ds-base-kit**

### Level AAA (Enhanced)
- Contrast ratio: ≥ 7:1
- For critical information
- Used for text-primary, text-secondary

### Validation

```python
# In validate-schema.py:
def validate_wcag_compliance(token_path: str, token: Dict) -> bool:
    wcag_level = token.get("wcag_level", "AA")
    contrast_ratio = token.get("contrast_ratio", 0)
    
    min_ratios = {"A": 3, "AA": 4.5, "AAA": 7}
    required = min_ratios[wcag_level]
    
    if contrast_ratio < required:
        raise ValidationError(f"Contrast {contrast_ratio} < {required}")
```

---

## Scripts & Tools

### Validation Scripts

| Script | Purpose | Trigger |
|--------|---------|---------|
| `validate-schema.py` | Validate tokens against schema | Manual, pre-commit |
| `agents/token-schema-validator.py` | Validación por agente | CI/CD |
| `agents/token-generator.py` | Propuesta de tokens semánticos | Manual, comentario de PR |
| `agents/token-migrate.py` | Detección de valores hardcodeados | CI/CD |
| `agents/token-diff-reporter.py` | Informe de cambios | CI/CD |

### Running Validations

```bash
# Full validation
python3 scripts/validate-schema.py

# Validación por agentes
python3 scripts/agents/token-schema-validator.py --full

# Pre-commit hook (auto)
# (runs validate-schema.py + agents/token-schema-validator.py)

# Pre-push hook (auto)
# (runs full tests + token-diff reporter)
```

---

## Examples

### Adding a New Semantic Color

```json
{
  "color": {
    "new-interactive": {
      "$value": "#2E7D0F",
      "$type": "color",
      "$extensions": {
        "metadata": {
          "element": ["button", "link", "checkbox"],
          "attribute": "color",
          "purpose": "action",
          "category": "semantic",
          "wcag_level": "AA",
          "contrast_ratio": 5.2,
          "state": ["default", "hover", "focus", "active"],
          "brands": {
            "promptea": { "light": "#2E7D0F", "dark": "#4ADE80" },
            "nova": { "light": "#059669", "dark": "#6EE7B7" },
            "ocean": { "light": "#0891B2", "dark": "#06B6D4" }
          },
          "design_decision": "New interactive color for enhanced accessibility",
          "figma_linked": true,
          "aliases": ["interactive-primary"],
          "tags": ["interactive", "primary"],
          "coverage": {
            "web": true,
            "ios": true,
            "android": true,
            "tailwind": true,
            "storybook": true
          }
        }
      }
    }
  }
}
```

### Deprecating a Token

```json
{
  "color": {
    "legacy-color": {
      "$value": "#FF0000",
      "$type": "color",
      "$extensions": {
        "metadata": {
          "deprecation": {
            "deprecated": true,
            "replacement": "color.danger",
            "removal_date": "2026-10-09",
            "reason": "Replaced by standardized color.danger"
          }
        }
      }
    }
  }
}
```

---

## Integration with Agents

### How Agents Use Metadata

**Token Schema Validator Agent:**
```python
# Validates metadata structure
agent.validate_metadata_required_fields("color.action", metadata)
agent.validate_wcag_compliance("color.action", token)
agent.validate_brand_coverage("color.action", metadata)
```

**Agente generador de tokens:**
```python
# Proposes new semantic tokens
agent.suggest_semantic_token(
    element="button",
    state="hover",
    purpose="action",
    category="component"
)
```

**Asistente de migración:**
```python
# Detects hardcoded values
agent.find_hardcoded_colors()
agent.suggest_token_replacement("#5CD314", "color.action")
```

**Generador de diferencias de tokens:**
```python
# Generates changelog
agent.generate_diff("v2.2.1", "v2.3.0")
# Output: TOKENS-CHANGELOG.md
```

---

## Referencias operativas

- **Catálogo DTCG:** [tokens.dtcg.json](tokens.dtcg.json)
- **Esquema de metadata:** [token-metadata.schema.json](token-metadata.schema.json)
- **Validación:** [validate-schema.py](../scripts/validate-schema.py)
- **Contratos para agentes:** [AGENT-CONTRACT.md](../05-agentes/AGENT-CONTRACT.md)
- **Estado de salud:** [TOKENS-HEALTH.md](../TOKENS-HEALTH.md)

**Versión:** 2.3.0
**Estado:** 🟢 Validado
**Actualización:** 2026-07-09
