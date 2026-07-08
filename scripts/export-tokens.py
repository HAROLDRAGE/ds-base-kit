#!/usr/bin/env python3
"""
Exportador de tokens: genera CSS, JavaScript, JSON y SCSS desde component-manifest.json
Uso: python3 scripts/export-tokens.py [--format css|js|json|scss] [--output path]
"""
import json
import sys
from pathlib import Path

MANIFEST = json.load(open("05-agentes/component-manifest.json", encoding="utf-8"))

def export_css(tokens_values):
    """Exporta tokens como CSS custom properties."""
    css = """/* Design.MD White Label — Tokens CSS
 * Generado automáticamente desde component-manifest.json
 * Uso: import en HTML o CSS principal, NO editar a mano
 */

:root {
  /* Tokens semánticos (primitivos, cero marca) */
"""
    # Agregar tokens primitivos
    for token_name, token_def in MANIFEST["tokens"]["semantic"].items():
        if "value" in token_def:
            css += f"  --{token_name.replace('.', '-')}: {token_def['value']};\n"
    
    css += "}\n\n"
    
    # Agregar tokens con valores por marca/tema
    for brand, themes in tokens_values.items():
        for theme, colors in themes.items():
            css += f"[data-brand=\"{brand}\"][data-theme=\"{theme}\"] {{\n"
            for color_name, color_value in colors.items():
                css += f"  --color-{color_name.replace('_', '-')}: {color_value};\n"
            css += "}\n\n"
    
    return css

def export_js(tokens_values):
    """Exporta tokens como objeto JavaScript (ESM)."""
    js = """// Design.MD White Label — Tokens JavaScript
// Generado automáticamente desde component-manifest.json
// Uso: import { tokens } from './tokens.js'

export const semanticTokens = {
"""
    
    for token_name, token_def in MANIFEST["tokens"]["semantic"].items():
        if "value" in token_def:
            clean_name = token_name.replace(".", "_")
            js += f"  {clean_name}: '{token_def['value']}', // {token_def.get('use', '')}\n"
    
    js += "};\n\n"
    js += "export const brandTokens = " + json.dumps(tokens_values, indent=2) + ";\n\n"
    js += """export default {
  semantic: semanticTokens,
  brands: brandTokens,
};
"""
    return js

def export_json(tokens_values):
    """Exporta tokens como JSON estructurado."""
    output = {
        "version": MANIFEST["version"],
        "timestamp": "2026-07-08",
        "semantic": {},
        "brands": tokens_values
    }
    
    for token_name, token_def in MANIFEST["tokens"]["semantic"].items():
        output["semantic"][token_name] = {
            "value": token_def.get("value", "computed by brand/theme"),
            "type": token_def.get("type", "color" if "color" in token_name else "dimension"),
            "use": token_def.get("use", ""),
            "not_for": token_def.get("not_for", "")
        }
    
    return json.dumps(output, indent=2, ensure_ascii=False)

def export_scss(tokens_values):
    """Exporta tokens como SCSS mixins."""
    scss = """// Design.MD White Label — Tokens SCSS
// Generado automáticamente desde component-manifest.json
// Uso: @include brand-tokens('promptea', 'dark')

// Tokens semánticos (siempre disponibles)
"""
    
    for token_name, token_def in MANIFEST["tokens"]["semantic"].items():
        if "value" in token_def:
            scss += f"${token_name.replace('.', '_')}: {token_def['value']};\n"
    
    scss += """

// Mixin para cambiar marca y tema
@mixin brand-tokens($brand, $theme) {
  $tokens: #{inspect(map-get($brands, $brand))};
  $theme-map: map-get($tokens, $theme);
  
  @each $token-name, $token-value in $theme-map {
    --color-#{str-replace($token-name, '_', '-')}: #{$token-value};
  }
}

// Mapa de marcas (para acceso programático)
$brands: (
"""
    
    for brand, themes in tokens_values.items():
        scss += f"  '{brand}': (\n"
        for theme, colors in themes.items():
            scss += f"    '{theme}': (\n"
            for color_name, color_value in colors.items():
                scss += f"      '{color_name}': '{color_value}',\n"
            scss += "    ),\n"
        scss += "  ),\n"
    
    scss += """);

// Uso en componentes:
// .button {
//   background: var(--color-action);
//   color: var(--color-on-action);
// }
"""
    return scss

def main():
    tokens_values = MANIFEST["tokens"]["values"]
    
    format_requested = "css"  # default
    output_path = None
    
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--format" and i + 1 < len(sys.argv[1:]):
            format_requested = sys.argv[i + 2]
        elif arg == "--output" and i + 1 < len(sys.argv[1:]):
            output_path = sys.argv[i + 2]
    
    if format_requested == "css":
        content = export_css(tokens_values)
        default_path = "01-tokens/tokens.css"
    elif format_requested == "js":
        content = export_js(tokens_values)
        default_path = "01-tokens/tokens.js"
    elif format_requested == "json":
        content = export_json(tokens_values)
        default_path = "01-tokens/tokens.json"
    elif format_requested == "scss":
        content = export_scss(tokens_values)
        default_path = "01-tokens/tokens.scss"
    else:
        print(f"Formato desconocido: {format_requested}")
        sys.exit(1)
    
    output_file = output_path or default_path
    Path(output_file).write_text(content, encoding="utf-8")
    print(f"✅ {format_requested.upper()} exportado a {output_file}")

if __name__ == "__main__":
    main()
