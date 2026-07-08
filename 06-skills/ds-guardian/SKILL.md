---
name: ds-guardian
description: >
  Genera y valida interfaces, componentes y documentación conformes al sistema
  Design.MD White Label (marcas promptea, nova, ocean × temas dark, light).
  Usar siempre que se pida crear UI, auditar accesibilidad o documentar
  componentes de este sistema de diseño.
---

# DS Guardian — skill del sistema Design.MD White Label

## Flujo obligatorio (en este orden)

1. Lee `05-agentes/component-manifest.json` — fuente única de verdad (tokens, componentes, reglas).
2. Opera bajo `05-agentes/AGENT-CONTRACT.md` — contratos 00-08 en lenguaje RFC 2119.
3. Verifica tu rol y permisos en `05-agentes/ROLES.md` antes de actuar.

## Reglas duras (no negociables)

- Solo tokens semánticos: `var(--color-action)`, `var(--space-4)` — NUNCA valores crudos (hex, px, ms).
- Todo componente implementa TODOS sus estados declarados: default, hover, focus, active, disabled, loading.
- WCAG 2.2 AA: contraste 4.5:1 texto / 3:1 UI y foco; el estado NUNCA se comunica solo con color (icono + palabra).
- White label: la marca vive en `data-brand` y el tema en `data-theme`; cero valores de marca en componentes.
- Un solo botón primario por vista. Navegación = link, acción = button.

## Contrato de salida (Contrato 08)

Toda entrega incluye: artefacto + doc `.md` (plantilla canónica) + diff de tokens usados +
checklist maestra completada + entrada de changelog propuesta (semver justificado) + declaración de suposiciones.

## Escalamiento

Si el manifiesto no cubre el requerimiento: DETENTE y propón la extensión al humano
responsable como cambio versionado. Nunca improvises tokens ni componentes.
