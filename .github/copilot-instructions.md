# Instrucciones para GitHub Copilot — Design.MD White Label

- Lee `05-agentes/component-manifest.json` como fuente única de verdad antes de sugerir UI.
- Cumple los contratos de `05-agentes/AGENT-CONTRACT.md` (00-08).
- Sugiere solo tokens semánticos (`var(--color-action)`), nunca valores crudos hex/px/ms.
- Incluye todos los estados de componente y accesibilidad WCAG 2.2 AA (foco visible, icono + palabra).
- White label: `data-brand` / `data-theme`; nunca codifiques colores de una marca.
- No inventes componentes ni tokens fuera del manifiesto: propone extenderlo vía PR versionado.
