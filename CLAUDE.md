# CLAUDE.md — Design.MD White Label

Este repositorio es un sistema de diseño white label operable por agentes.

## Antes de generar cualquier artefacto
1. Lee `05-agentes/component-manifest.json` (fuente única de verdad).
2. Cumple `05-agentes/AGENT-CONTRACT.md` (contratos 00-08).
3. Skill disponible: `06-skills/ds-guardian/SKILL.md` (opcional).

## Reglas clave
- Solo tokens semánticos (`var(--color-action)`), nunca valores crudos.
- Estados completos en cada componente; WCAG 2.2 AA; estado nunca solo con color.
- Marca = `data-brand` (promptea | nova | ocean), tema = `data-theme` (dark | light).
- Si algo no existe en el manifiesto: escalar al humano, nunca improvisar.
- Toda entrega sigue el Contrato 08 (artefacto + doc + diff de tokens + checklist + changelog + suposiciones).

## Validación local
`pip install -r requirements-dev.txt && npm run validate`
