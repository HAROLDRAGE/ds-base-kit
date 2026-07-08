"""Linting de diseño: valida el manifiesto contra el schema y el contraste WCAG 2.2 AA."""
import json, sys
from jsonschema import validate

MANIFEST = json.load(open("05-agentes/component-manifest.json", encoding="utf-8"))
SCHEMA = json.load(open("05-agentes/manifest.schema.json", encoding="utf-8"))
validate(MANIFEST, SCHEMA)
print("schema: OK — manifiesto conforme")

def lum(h):
    h = h.lstrip("#"); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

CHECKS = [("text","bg",4.5),("text","surface",4.5),("muted","bg",4.5),("action","bg",3.0),
          ("on-action","action",4.5),("focus","bg",3.0),("danger","bg",4.5),("success","bg",4.5)]
fails = 0
for brand, themes in MANIFEST["tokens"]["values"].items():
    for theme, t in themes.items():
        for a, b, req in CHECKS:
            r = ratio(t[a], t[b])
            if r < req:
                fails += 1
                print(f"FALLA {brand}/{theme} {a} sobre {b}: {r:.2f} < {req}")
print("contraste: OK — todas las verificaciones pasan" if fails == 0 else f"contraste: {fails} fallas")
sys.exit(1 if fails else 0)
