# Design.MD White Label — IA Ready

> Sistema de diseño white label documentado en Markdown, operable por humanos
> y agentes de IA. 3 marcas (promptea, nova, ocean) × 2 temas (dark, light).
> Basado en Design.MD · Edición 2026 · v1.3.0

**Repositorio:** https://github.com/haroldrage/ds-base-kit

## Quick Start

### Humanos
```bash
git clone https://github.com/haroldrage/ds-base-kit
cd ds-base-kit
open index.html   # documentación navegable, buscador y selector de marca/tema
```

### Agentes externos
1. Leer `05-agentes/component-manifest.json` — qué existe
2. Operar bajo `05-agentes/AGENT-CONTRACT.md` — cómo actuar
3. Consultar `QUICK-START.md` para comandos y flujos

### Claude Code (Agent Skill)
```bash
cp -r 06-skills/ds-guardian ~/.claude/skills/
```
`CLAUDE.md`, `.cursorrules` y `.github/copilot-instructions.md` ya vienen en la raíz.

## Validación (linting de diseño)
```bash
pip install jsonschema
python scripts/validate.py   # schema + 48 verificaciones de contraste WCAG 2.2 AA
```
El workflow `.github/workflows/validate.yml` lo ejecuta en cada push y PR.

## Estructura
```
00-fundamentos/  01-tokens/  02-componentes/  03-patrones/
04-plantillas/   05-agentes/ (manifiesto · schema · contratos · roles)
06-skills/ds-guardian/       scripts/validate.py
```

## Licencia y créditos
Material derivado de Design.MD — promptea.cl · Edición 2026.
