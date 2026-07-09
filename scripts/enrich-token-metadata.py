#!/usr/bin/env python3
"""Completa metadata DTCG determinista para tokens existentes sin alterar valores.

La metadata se deriva de la ruta semántica y deja trazabilidad en
`$extensions.metadata.generated_from`. Los ratios se calculan solamente para
colores utilizados sobre una superficie conocida.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parent.parent
TOKENS_FILE = ROOT / "01-tokens" / "tokens.dtcg.json"
PLATFORMS = {"web": True, "tailwind": True, "ios": True, "android": True, "storybook": True}

COLOR_RULES = {
    "bg": ("background", "background", ["page", "layout"], False),
    "surface": ("surface", "background", ["card", "input", "panel"], False),
    "text": ("text", "color", ["text", "heading", "label"], True),
    "muted": ("neutral", "color", ["text", "help"], True),
    "action": ("action", "background-color", ["button", "link", "focus"], True),
    "on-action": ("text", "color", ["button", "link"], True),
    "focus": ("focus", "outline-color", ["focus-indicator"], True),
    "danger": ("danger", "color", ["alert", "field-error"], True),
    "success": ("success", "color", ["alert", "status"], True),
    "border": ("border", "border-color", ["divider", "card", "input"], False),
}


def leaves(value: Any, path: list[str] | None = None) -> Iterator[tuple[list[str], dict[str, Any]]]:
    path = path or []
    if isinstance(value, dict) and "$value" in value:
        yield path, value
    elif isinstance(value, dict):
        for key, child in value.items():
            if not key.startswith("$"):
                yield from leaves(child, path + [key])


def hex_to_rgb(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) / 255 for index in (0, 2, 4))


def luminance(value: str) -> float:
    channels = []
    for channel in hex_to_rgb(value):
        channels.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first: str, second: str) -> float:
    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return round((light + 0.05) / (dark + 0.05), 2)


def color_ratio(data: dict[str, Any], path: list[str]) -> float | None:
    brand, theme, role = path[1:4]
    colors = data["color"][brand][theme]
    value = colors[role]["$value"]
    if role in {"text", "muted", "action", "danger", "success", "focus"}:
        return contrast(value, colors["bg"]["$value"])
    if role == "on-action":
        return contrast(value, colors["action"]["$value"])
    return None


def brand_variants(data: dict[str, Any], role: str) -> dict[str, dict[str, str]]:
    """Return actual light/dark values for the same semantic color across brands."""
    return {
        brand: {
            theme: data["color"][brand][theme][role]["$value"]
            for theme in ("light", "dark")
        }
        for brand in ("promptea", "nova", "ocean")
    }


def shared_brand_variants() -> dict[str, dict[str, str]]:
    return {
        brand: {"light": "var(--shared-token)", "dark": "var(--shared-token)"}
        for brand in ("promptea", "nova", "ocean")
    }


def enrich(data: dict[str, Any]) -> int:
    updated = 0
    for path, token in leaves(data):
        token_type = token["$type"]
        metadata = token.setdefault("$extensions", {}).setdefault("metadata", {})
        if token_type == "color":
            role = path[-1]
            purpose, attribute, elements, assessable = COLOR_RULES[role]
            ratio = color_ratio(data, path)
            metadata.update({
                "element": elements,
                "attribute": attribute,
                "purpose": purpose,
                "category": "semantic",
                "wcag_level": "AA",
                "brands": brand_variants(data, role),
                "coverage": PLATFORMS.copy(),
                "contrast_assessable": assessable,
                "generated_from": "token-path-v1",
            })
            if ratio is not None:
                metadata["contrast_ratio"] = ratio
            else:
                metadata.pop("contrast_ratio", None)
        elif token_type == "dimension":
            metadata.update({
                "element": ["component", "layout"],
                "attribute": "padding" if "space" in path else "border-radius",
                "purpose": "md",
                "category": "semantic",
                "brands": shared_brand_variants(),
                "coverage": PLATFORMS.copy(),
                "generated_from": "token-path-v1",
            })
        elif token_type == "duration":
            metadata.update({
                "element": ["component", "transition"],
                "attribute": "transition-duration",
                "purpose": "neutral",
                "category": "semantic",
                "brands": shared_brand_variants(),
                "coverage": PLATFORMS.copy(),
                "generated_from": "token-path-v1",
            })
        updated += 1
    return updated


if __name__ == "__main__":
    data = json.loads(TOKENS_FILE.read_text())
    count = enrich(data)
    TOKENS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"✅ Enriched metadata for {count} existing DTCG tokens")
