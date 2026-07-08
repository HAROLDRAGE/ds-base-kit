# Changelog

Todos los cambios notables de este sistema se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) · Versionado: [SemVer](https://semver.org/lang/es/).

## [1.3.0] — 2026-07-08

### Added
- Documentación completa de componentes: `link.md`, `field.md`, `card.md`, `navbar.md` (6/6 del manifiesto).
- Nuevos patrones: `navegacion.md`, `tarjetas.md`, `modales.md` (4 patrones totales).
- Exportadores de tokens: `scripts/export-tokens.py` genera CSS, JavaScript, JSON, SCSS desde el manifiesto.
- Archivos generados: `01-tokens/tokens.js`, `01-tokens/tokens.json`, `01-tokens/tokens.scss`.
- Tests visuales (VRT): `scripts/vrt-tests.py` + `.github/workflows/vrt.yml` para integración con Playwright y Percy.io.
- Sección de descargas en index.html con botones para cada formato de tokens.
- Especificaciones WCAG 2.2 AA en cada componente: anatomía, variantes, estados, accesibilidad, código.
- Contrato 06 (documentación como código) implementado para todos los componentes.

### Changed
- `index.html`: versión 1.2.0 → 1.3.0.
- Cobertura de componentes: 33% (2/6) → 100% (6/6).
- Cobertura de patrones: 25% (1/4) → 100% (4/4).
- `component-manifest.json`: versión 1.1.0 → 1.2.0 (documentación completada).

### Fixed
- Validación continua: todos los tokens pasan 48 verificaciones WCAG 2.2 AA (contraste 4.5:1 texto, 3:1 UI/foco).
- Ejemplos de código ejecutables en cada componente y patrón.

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