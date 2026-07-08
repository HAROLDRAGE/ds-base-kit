# Changelog

Todos los cambios notables de este sistema se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) · Versionado: [SemVer](https://semver.org/lang/es/).

## [1.2.0] — 2026-07-08

### Added
- Sección Quick Start: humanos, agentes externos y Claude Code / Cursor / Copilot.
- Agent Skill `ds-guardian` (formato Anthropic SKILL.md) en `06-skills/`.
- Sección Skills: catálogo de skills existentes (anthropics/skills, MCP, Figma) integrables al flujo.
- Botón al repositorio GitHub y descarga directa de `ds-base-kit.zip` desde el sitio.
- `CLAUDE.md`, `.cursorrules` y `.github/copilot-instructions.md`: una sola fuente de verdad para todos los agentes.
- CI de linting de diseño: `.github/workflows/validate.yml` + `scripts/validate.py` (schema + contraste WCAG).

### Changed
- Documentación HTML 1.1.0 → 1.2.0.

## [1.1.0] — 2026-07-08

### Added
- `AGENT-CONTRACT.md` Contrato 08: contrato de salida (entregas auditables en 6 partes).
- `manifest.schema.json`: validación automática del manifiesto (JSON Schema 2020-12).
- `llms.txt`: descubrimiento estándar para agentes LLM.
- `tokens.dtcg.json`: tokens en formato W3C Design Tokens Community Group.
- `ROLES.md`: matriz de roles de agentes (generador, supervisor, documentador, curador).
- Ejemplos Do/Don't ejecutables en cada contrato.
- Reporte de contraste automatizado: 48 verificaciones, 3 marcas × 2 temas, WCAG 2.2 AA.
- Búsqueda/filtro en la documentación HTML (test de 30 segundos).
- Componentes nuevos en manifiesto: `link`, `field`, `navbar`.
- Publicación en https://ds-base-kit.tess.page

### Changed
- `component-manifest.json` 1.0.0 → 1.1.0 (adiciones compatibles).
- `AGENT-CONTRACT.md` 1.0.0 → 1.1.0.

## [1.0.0] — 2026-07-01

### Added
- Manifiesto inicial: tokens semánticos, 6 componentes, reglas del sistema.
- Contratos de operación 00–07.
- White label: marcas promptea, nova, ocean × temas dark, light.