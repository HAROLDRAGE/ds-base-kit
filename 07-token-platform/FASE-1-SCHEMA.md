# FASE 1 — SCHEMA DE METADATA DE TOKENS
> Machine-Readable Token Metadata Schema v1.0  
> Basado en: DTCG, FASE-0-AUDIT.md, AGENT-CONTRACT.md

---

## 📋 Schema JSON (07-token-platform/token-metadata.schema.json)

```json
{
  "$schema": "http://json-schema.org/draft-2020-12/schema",
  "$id": "https://ds-base-kit.local/schemas/token-metadata/v1.0",
  "title": "Design.MD Token Metadata Schema",
  "description": "Machine-readable metadata para razonamiento de agentes IA sobre tokens semánticos",
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "required": [
        "category",
        "element",
        "attribute",
        "purpose",
        "prominence",
        "state"
      ],
      "properties": {
        "category": {
          "type": "string",
          "enum": ["primitive", "foundation", "semantic", "component"],
          "description": "Layer del token en la arquitectura"
        },
        "element": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "button", "link", "input", "badge", "card", "alert", "dropdown",
              "modal", "tabs", "accordion", "breadcrumb", "tooltip", "toast",
              "navbar", "field", "table", "pagination", "progress",
              "navbar-bottom", "avatar", "checkbox", "radio", "switch",
              "slider", "date-picker", "snackbar", "bar-chart", "line-chart",
              "pie-chart"
            ]
          },
          "description": "Componentes que usan este token"
        },
        "attribute": {
          "type": "string",
          "enum": [
            "color", "background", "border", "text", "padding", "margin",
            "gap", "radius", "shadow", "transition", "animation", "font-size",
            "font-weight", "line-height", "letter-spacing", "width", "height",
            "opacity", "z-index", "stroke"
          ],
          "description": "Propiedad CSS que aplica este token"
        },
        "purpose": {
          "type": "string",
          "enum": [
            "primary", "secondary", "danger", "success", "warning", "info",
            "action", "neutral", "muted", "disabled", "focus", "hover",
            "active", "visited", "placeholder", "border", "bg", "text",
            "accent", "surface", "overlay"
          ],
          "description": "Intención de diseño (semántica de negocio)"
        },
        "prominence": {
          "type": "string",
          "enum": ["high", "medium", "low"],
          "description": "Importancia visual del token"
        },
        "size": {
          "type": "string",
          "enum": ["xs", "sm", "md", "lg", "xl", "2xl", "3xl"],
          "description": "Escala de tamaño (spacing, typography, etc.)"
        },
        "speed": {
          "type": "string",
          "enum": ["slow", "normal", "fast"],
          "description": "Velocidad (solo para motion tokens)"
        },
        "state": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "default", "hover", "active", "focus", "focus-visible",
              "disabled", "loading", "error", "success", "warning",
              "visited", "pressed", "expanded", "collapsed"
            ]
          },
          "description": "Estados en los que este token es aplicable"
        },
        "index": {
          "type": "integer",
          "minimum": 1,
          "description": "Posición en escala (para spacing, typography, etc.)"
        },
        "wcag_level": {
          "type": "string",
          "enum": ["A", "AA", "AAA"],
          "description": "Nivel de conformidad WCAG validado"
        },
        "brands": {
          "type": "object",
          "properties": {
            "promptea": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$|^[a-z0-9-]+$" },
            "nova": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$|^[a-z0-9-]+$" },
            "ocean": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$|^[a-z0-9-]+$" }
          },
          "description": "Overrides por brand"
        },
        "themes": {
          "type": "object",
          "properties": {
            "light": { "type": "string" },
            "dark": { "type": "string" }
          },
          "description": "Overrides por theme"
        },
        "deprecated": {
          "type": "boolean",
          "default": false,
          "description": "¿Está deprecado?"
        },
        "deprecation_date": {
          "type": "string",
          "format": "date",
          "description": "Cuándo se deprecó"
        },
        "removal_date": {
          "type": "string",
          "format": "date",
          "description": "Cuándo se removerá"
        },
        "replacement": {
          "type": "string",
          "description": "Token de reemplazo recomendado"
        },
        "aliases": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Nombres alternativos válidos (backward compat)"
        },
        "css_var_name": {
          "type": "string",
          "description": "Nombre derivado de CSS custom property"
        },
        "js_export_name": {
          "type": "string",
          "description": "Nombre derivado para export JS/TS"
        }
      }
    }
  }
}
```

---

## 🔄 Regla Generativa de Nombres (Name Transform)

**Del schema al nombre final:**

```
$[SYSTEM]-[CATEGORY]-[ELEMENT]?-[CONCEPT]?-[ATTRIBUTE]-[SIZE|SPEED]?-[STATE]?

Dónde:
  SYSTEM       = "mds" (Design System prefix)
  CATEGORY     = "primitive" | "foundation" | "semantic" | "component"
  ELEMENT      = elemento del componente (optional, ej: "button")
  CONCEPT      = propósito (ej: "action", "primary")
  ATTRIBUTE    = propiedad CSS (ej: "color", "padding")
  SIZE/SPEED   = escala (ej: "md", "fast")
  STATE        = estado (ej: "hover", "disabled")
```

**Ejemplos derivados automáticamente:**

| Schema | Nombre Final | Uso |
|--------|-------------|-----|
| `{ category: "semantic", element: ["button"], attribute: "color", purpose: "action", state: ["default", "hover"] }` | `--mds-semantic-button-action-color` | Color de botón primario |
| `{ category: "semantic", element: ["button"], attribute: "color", purpose: "action", state: ["hover"] }` | `--mds-semantic-button-action-color-hover` | Color hover de botón |
| `{ category: "primitive", attribute: "spacing", index: 4, size: "md" }` | `--mds-primitive-space-4` | 16px (escala base) |
| `{ category: "foundation", attribute: "font-weight", purpose: "bold" }` | `--mds-foundation-font-weight-bold` | Weight 700 |

**Validación:** Un PR que use `--my-custom-blue` en lugar de un token del schema será rechazado automáticamente por el Agent Linter.

---

## 📝 Evolución de tokens.dtcg.json (W3C DTCG con $extensions)

**Antes (actual):**
```json
{
  "color": {
    "action": {
      "$type": "color",
      "$value": "#5CD314",
      "$description": "Acciones principales, enlaces, foco"
    }
  }
}
```

**Después (con metadata machine-readable):**
```json
{
  "color": {
    "action": {
      "$type": "color",
      "$value": "#5CD314",
      "$description": "Acciones principales, enlaces, foco",
      "$extensions": {
        "metadata": {
          "category": "semantic",
          "element": ["button", "link", "input"],
          "attribute": "color",
          "purpose": "action",
          "prominence": "high",
          "state": ["default", "hover", "focus"],
          "wcag_level": "AA",
          "brands": {
            "promptea": "#5CD314",
            "nova": "#7C3AED",
            "ocean": "#0284C7"
          },
          "themes": {
            "light": "#5CD314",
            "dark": "#7ED321"
          },
          "deprecated": false,
          "aliases": ["--semantic-action-color"],
          "css_var_name": "--mds-semantic-color-action",
          "js_export_name": "colorAction"
        },
        "wcag": {
          "promptea-light": { "contrast_ratio": 4.52, "level": "AA" },
          "promptea-dark": { "contrast_ratio": 5.11, "level": "AAA" },
          "nova-light": { "contrast_ratio": 4.73, "level": "AA" },
          "nova-dark": { "contrast_ratio": 5.33, "level": "AAA" },
          "ocean-light": { "contrast_ratio": 4.65, "level": "AA" },
          "ocean-dark": { "contrast_ratio": 5.04, "level": "AAA" }
        },
        "usage": {
          "components": ["Button", "Link", "Input"],
          "patterns": ["formularios", "navegación"],
          "count_usages": 47
        }
      }
    }
  }
}
```

---

## 🔗 Backward Compatibility (NO romper consumidores)

**Garantía:** Los nombres de tokens actuales siguen siendo válidos.

| Consumidor | Actual | Nuevo | Compatible |
|------------|--------|-------|-----------|
| CSS web | `var(--color-action)` | `var(--mds-semantic-color-action)` | ✅ AMBOS válidos |
| Agentes | Lee `component-manifest.json` | Lee `tokens.dtcg.json` + metadata | ✅ Mejor inferencia |
| JS/TS | `import { colorAction }` | Agregado: `import { mdsSemanticColorAction }` | ✅ AMBOS válidos |

**Estrategia:**
1. Mantener tokens actuales en `tokens.css` (sin cambios de nombre)
2. Generar TAMBIÉN nuevas references derivadas del schema
3. Crear mapping entre nombres antiguos ↔ nuevos en `tokens.aliases.json`
4. En FASE 2, Style Dictionary puede exportar ambos

---

## ✅ Validación del Schema

**Script de validación (07-token-platform/validate-schema.py):**

```python
#!/usr/bin/env python3
"""Valida que tokens.dtcg.json cumpla el schema."""

import json
import jsonschema
from pathlib import Path

def validate():
    with open("token-metadata.schema.json") as f:
        schema = json.load(f)
    
    with open("../01-tokens/tokens.dtcg.json") as f:
        tokens = json.load(f)
    
    # Validator por cada token
    for path, token in flatten_dtcg(tokens):
        if "$extensions" in token and "metadata" in token["$extensions"]:
            try:
                jsonschema.validate(
                    token["$extensions"],
                    schema["properties"]["metadata"]
                )
            except jsonschema.ValidationError as e:
                print(f"❌ FALLO en {path}: {e.message}")
                return False
    
    print("✅ Todos los tokens validan contra schema")
    return True

if __name__ == "__main__":
    exit(0 if validate() else 1)
```

---

**FASE 1 Entregables:**
1. ✅ `token-metadata.schema.json` — Schema JSON completo
2. ✅ Regla de name transform (derivación automática)
3. ✅ `tokens.dtcg.json` migrado con `$extensions`
4. ✅ `validate-schema.py` en scripts
5. ✅ `tokens.aliases.json` para backward compat
