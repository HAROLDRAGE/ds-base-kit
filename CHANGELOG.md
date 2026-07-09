# Changelog

Todos los cambios notables de este sistema se documentan aquí.
Formato: [Keep a Changelog](https://keepachangelog.com/es/1.1.0/) · Versionado: [SemVer](https://semver.org/lang/es/).

## [2.3.0] — 2026-07-09

### Added
- PHASE 4: scripts de gobernanza para ciclo de desuso, matriz de cobertura y monitor de salud.
- Evidencia trazable de PHASE 4 en `index.html`, con enlaces a sus scripts y reportes generados.
- Scripts npm: `tokens:deprecate`, `tokens:coverage`, `tokens:health` y `tokens:govern`.
- Metadata DTCG reproducible para los 72 tokens hoja: intención de uso, cobertura de cinco plataformas, variantes white-label y contexto WCAG.
- Exportador local de Web, Tailwind, iOS, Android y Storybook que funciona sin requerir una descarga de dependencias.
- Explorador de tokens en la portada: filtro, valores de la marca/tema activo y copia de referencias CSS.
- Catálogo completo DTCG en la portada, con vistas de marca/tema activos y de los 72 tokens.
- Flujo de CI sin dependencias npm para exportar tokens, con controles bloqueantes de esquema, lint, pruebas y gobernanza.

### Changed
- La portada muestra evidencia diferenciada de exportación multi-plataforma, cobertura declarada y evaluación WCAG aplicable.
- Las métricas de salud reflejan los 72 valores DTCG con metadata completa y 42 colores evaluables que superan AA.
- La portada deja de exponer nombres internos de etapas y presenta el sistema como una biblioteca de producto.
- README, manifiesto y pruebas distinguen explícitamente los 72 tokens DTCG, los 95 tokens semánticos declarados, los 160 tokens estructurados heredados y las 240 variables CSS.

## [2.1.0] — 2026-07-09

### Added
- **Sistema de Layout Responsive:** 6 breakpoints (xs, sm, md, lg, xl, 2xl) optimizados para móvil, tablet y desktop.
- **Tokens de Layout:** 16 nuevos tokens CSS para breakpoints, grid columns, touch targets, densidades y safe areas.
- **Guía Android (Material Design 3):** Conversión de tokens a dp, color dinámico, navegación, safe areas, haptics.
- **Guía iOS (Human Interface Guidelines):** Puntos (pt), Dynamic Island, vibrancy, navegación swipe-back, haptic feedback.
- **Guía Web:** Media queries, grid/flexbox, imágenes responsivas, Core Web Vitals, accesibilidad.
- **Documentación:** Archivo `01-tokens/LAYOUT.md` (350+ líneas) con ejemplos, mapeos plataforma-específicos, código Swift/Kotlin.
- Nuevas secciones HTML interactivas: #layouts, #android, #ios, #web con tablas de referencia y demos.
- Safe areas dinámicas para iOS notch y Android DisplayCutout: `env(safe-area-inset-*)` + classes `.safe-area-*`.

### Changed
- `component-manifest.json`: versión 2.0.0 → 2.1.0 (20 nuevos tokens de layout).
- `index.html`: v2.0.0 → v2.1.0; Meta viewport ahora incluye `viewport-fit=cover`.
- `tokens.css`: +85 líneas de utilidades responsive, safe areas y densidades.
- Sidebar actualizado con links a nuevos apartados: Layouts, Android, iOS, Web.

### Reference
- **Breakpoints:** 320px (xs) → 480px (sm) → 768px (md) → 1024px (lg) → 1280px (xl) → 1536px (2xl)
- **Touch targets:** 44px (iOS/web) = 44 pt iOS = 44 dp Android (mapeado a 48 dp Material Design 3)
- **Safe areas:** Dynamic Island (top), home indicator (bottom), DisplayCutout (Android)

## [2.0.0] — 2026-07-09

### Added
- **Expansión completa de tokens:** 90+ variables CSS (tipografía, espaciados, bordes, sombras, motion).
- **Nuevas secciones de sistema:** Tipografía, Espaciados, Bordes, Sombras, Motion (5 secciones interactivas).
- **Presets de tipografía:** h1–h6, body (lg/base/sm/xs), label (6 pesos, 4 line heights, 4 letter spacing).
- **Escala de espaciados:** 11 niveles (0–64px) con visualización de barras.
- **Bordes y radios:** 7 presets radius + 4 widths + 3 estilos.
- **Sistema de sombras:** 5 niveles (sm–2xl) con demostración de elevación.
- **Motion & transitions:** 3 duraciones (120–400ms) + 4 easing functions con demo interactivo.
- **Documentación:** `EXPANSION-v2.0.0.md` con mapeos de tokens y ejemplos.

### Changed
- `component-manifest.json`: versión 1.2.0 → 2.0.0 (80+ nuevos tokens).
- `tokens.css`: 200 líneas → 480 líneas (completamente regenerado).
- Descripción de sistema: "minimal" → "producción-ready".

### Fixed
- URL externa removida: `ds-base-kit.tess.page` → eliminado completamente.
- Manifest desacoplado de referencias externas.

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
- Publicación en https://github.com/HAROLDRAGE/ds-base-kit

### Changed
- `component-manifest.json` 1.0.0 → 1.1.0 (adiciones compatibles).
- `AGENT-CONTRACT.md` 1.0.0 → 1.1.0.

## [1.0.0] — 2026-07-01

### Added
- Manifiesto inicial: tokens semánticos, 6 componentes, reglas del sistema.
- Contratos de operación 00–07.
- White label: marcas promptea, nova, ocean × temas dark, light.