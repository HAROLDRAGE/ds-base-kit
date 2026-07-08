# Comandos Rápidos — Design.MD White Label v1.3.0

## 🚀 Inicio Rápido

```bash
# Clonar
git clone https://github.com/haroldrage/ds-base-kit
cd ds-base-kit

# Ver documentación
open index.html

# Validar proyecto
python3 scripts/validate.py
```

## 📦 Exportar Tokens

```bash
# Todos los formatos (CSS, JS, JSON, SCSS)
bash scripts/regenerate-all.sh

# Individual
python3 scripts/export-tokens.py --format css
python3 scripts/export-tokens.py --format js
python3 scripts/export-tokens.py --format json
python3 scripts/export-tokens.py --format scss

# Salida personalizada
python3 scripts/export-tokens.py --format js --output dist/tokens.js
```

## 🧪 Validación y Tests

```bash
# Validar schema + contraste WCAG
python3 scripts/validate.py

# Configurar tests visuales (VRT)
python3 scripts/vrt-tests.py

# Instalar dependencias para VRT
pip install playwright
python -m playwright install
```

## 📝 Editar Componentes/Patrones

Siempre editar el manifiesto primero:

```bash
# 1. Editar component-manifest.json (fuente única de verdad)
nano 05-agentes/component-manifest.json

# 2. Regenerar artefactos
bash scripts/regenerate-all.sh

# 3. Validar cambios
python3 scripts/validate.py

# 4. Commit
git add .
git commit -m "feat: agregar componente XXX"
git push
```

## 🤖 Para Agentes IA

```bash
# Leer en este orden:
1. GET https://ds-base-kit.tess.page/llms.txt
2. cat 05-agentes/component-manifest.json
3. cat 05-agentes/AGENT-CONTRACT.md

# Instalar skill
cp -r 06-skills/ds-guardian ~/.claude/skills/

# Operar bajo Contratos 00-08
# Si algo no existe en el manifiesto → escalar (Contrato 07)
```

## 📊 Archivos Clave

| Archivo | Propósito |
|---|---|
| `05-agentes/component-manifest.json` | Fuente única de verdad (SSOT) |
| `05-agentes/AGENT-CONTRACT.md` | Contratos 00-08 (RFC 2119) |
| `05-agentes/manifest.schema.json` | Validación JSON Schema |
| `scripts/validate.py` | Linting de diseño (CI) |
| `scripts/export-tokens.py` | Exportador multiformat |
| `scripts/regenerate-all.sh` | Regenerar todos los artefactos |
| `CHANGELOG.md` | Keep a Changelog + SemVer |
| `index.html` | Documentación navegable |

## 🎯 Flujo de Desarrollo

```
component-manifest.json (editar aquí)
          ↓
    validate.py (schema + contraste)
          ↓
    export-tokens.py (CSS, JS, JSON, SCSS)
          ↓
   01-tokens/*.{css,js,json,scss} (generados)
          ↓
    git add . && git commit
          ↓
    CI: .github/workflows/validate.yml
```

## 🔗 Enlaces Útiles

- **GitHub:** https://github.com/haroldrage/ds-base-kit
- **Documentación completa:** Abre `index.html` en tu navegador (o `python3 -m http.server 8000` para servir localmente)
- **Mejoras v1.3.0:** `docs/v1.3.0-improvements.md`

## ❓ FAQ

**P: ¿Cómo agrego un componente nuevo?**
R: Edita `component-manifest.json` (estructura + tokens), luego documenta en `02-componentes/nombre.md`, luego `bash scripts/regenerate-all.sh` y `python3 scripts/validate.py`.

**P: ¿Puedo editar `tokens.css` directamente?**
R: No. Edita el manifiesto y ejecuta `export-tokens.py`. Los archivos generados llevan comentario "NO editar a mano".

**P: ¿Cómo integro con Figma?**
R: Exporta `tokens.json` y usa Token Studio plugin o Figma Dev Mode + MCP.

**P: ¿Es posible agregar una 4ª marca?**
R: Sí. Agrega a `component-manifest.json` > `brands` array y en `tokens.values`. Luego regenera con `scripts/regenerate-all.sh`.

---

**Última actualización:** 2026-07-08 · v1.3.0
