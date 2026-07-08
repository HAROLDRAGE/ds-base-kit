# AGENT-CONTRACT.md
> Contratos de operación para agentes de IA · Design.MD White Label
> Versión 1.1.0 · Ligado a `component-manifest.json` v1.1.0 · Edición 2026

Palabras clave según RFC 2119: **DEBE**, **DEBERÍA**, **NO DEBE**.
Un artefacto que viole cualquier contrato `DEBE` se considera no conforme y se rechaza en revisión.

---

## Contrato 00 · Fuente única de verdad

- El agente DEBE leer `component-manifest.json` antes de generar cualquier artefacto.
- El agente NO DEBE inventar componentes, variantes ni tokens fuera del manifiesto.

```css
/* ✅ Do */   background: var(--color-action);
/* ❌ Don't */ background: #5CD314; /* valor inventado fuera del manifiesto */
```

## Contrato 01 · Tokens, nunca valores crudos

- El agente DEBE referenciar tokens semánticos, NUNCA valores hex, px o ms literales.
- El agente NO DEBE apuntar a tokens primitivos desde un componente.
- El agente DEBE respetar los campos `use` y `not_for` de cada token.

```css
/* ✅ Do */   border-radius: var(--radius-md); transition: all var(--motion-fast);
/* ❌ Don't */ border-radius: 10px; transition: all 120ms;
```

## Contrato 02 · Componentes y niveles atómicos

- El agente DEBE componer solo con componentes del manifiesto, respetando su `atomic_level`.
- El agente DEBE respetar `when_to_use` / `when_not_to_use`.
- El agente DEBE mantener un solo botón primario por vista.

```html
<!-- ✅ Do -->   <a class="link" href="/docs">Ver documentación</a>
<!-- ❌ Don't --> <button onclick="location.href='/docs'">Ver documentación</button>
```

## Contrato 03 · Estados completos

- Todo componente DEBE implementar TODOS sus estados declarados en el manifiesto.
- El agente NO DEBE entregar un componente solo con estado default.
- Transiciones con tokens de motion y desactivadas ante `prefers-reduced-motion`.

```css
/* ✅ Do */   .btn:hover{...} .btn:focus-visible{...} .btn:disabled{...} .btn[aria-busy]{...}
/* ❌ Don't */ .btn{ background: var(--color-action); } /* y nada más */
```

## Contrato 04 · Accesibilidad (no negociable)

- WCAG 2.2 AA y principios POUR. Contraste 4.5:1 texto · 3:1 texto grande, UI y foco.
- El agente NO DEBE comunicar estado solo con color: icono + palabra siempre.
- Semántica correcta: un H1, jerarquía sin saltos, enlaces autoexplicativos,
  alt descriptivo, `role`/`aria-*` según el campo `a11y`, operable con teclado.

```html
<!-- ✅ Do -->   <p class="error">⚠ Error: el campo email es obligatorio</p>
<!-- ❌ Don't --> <p style="color:red">Campo obligatorio</p>
```

## Contrato 05 · White Label

- El agente NO DEBE codificar valores de una marca: marca = `data-brand`, tema = `data-theme`.
- Todo artefacto DEBE re-tematizarse en `promptea`, `nova` y `ocean` × `dark`/`light` sin editar componentes.

```html
<!-- ✅ Do -->   <html data-brand="nova" data-theme="light">
<!-- ❌ Don't --> <style>.btn{ background:#A78BFA }</style>
```

## Contrato 06 · Documentación como código

- Componente nuevo DEBE documentarse con la plantilla canónica (Cuándo / Anatomía /
  Variantes / Estados / Interacción / Accesibilidad / Tokens / Do's & Don'ts / Código).
- Cada cambio DEBE registrarse en `CHANGELOG.md` (Keep a Changelog + semver).
- Tablas de tokens DEBERÍAN generarse desde el código. NO DEBE duplicar valores.

## Contrato 07 · Escalamiento y honestidad

- Si el sistema no cubre un requerimiento, el agente NO DEBE improvisar:
  DEBE detenerse y escalar al humano responsable proponiendo la extensión
  del manifiesto como cambio versionado.
- El agente DEBE declarar explícitamente toda suposición.

## Contrato 08 · Contrato de salida (entrega auditable)

Toda entrega de un agente DEBE incluir, sin excepción:

1. **Artefacto** (código/UI/doc) conforme a los contratos 00–07.
2. **Documento `.md`** según la plantilla canónica del sistema.
3. **Diff de tokens**: lista exacta de tokens semánticos utilizados.
4. **Checklist maestra** completada (estructura, a11y, usabilidad, sistema).
5. **Entrada de changelog propuesta** con nivel semver justificado
   (`patch` = corrección · `minor` = adición compatible · `major` = ruptura).
6. **Declaración de suposiciones** (o "ninguna").

- El agente NO DEBE entregar artefactos sueltos sin este paquete.
- Una entrega sin los 6 elementos se considera incompleta y se rechaza.

```md
<!-- ✅ Do: pie de entrega -->
## Entrega
- Tokens usados: color.action, space.4, radius.md, motion.fast
- Checklist: 16/16 ✓ · Changelog propuesto: minor (nuevo variante ghost)
- Suposiciones: ninguna
```

---

## Firma del contrato

| Campo             | Valor                                  |
| ----------------- | -------------------------------------- |
| Sistema           | Design.MD White Label — IA Ready       |
| Manifiesto ligado | component-manifest.json v1.1.0         |
| Roles de agentes  | ROLES.md (generador · supervisor · documentador · curador) |
| Vigencia          | Mientras el manifiesto esté en v1.x    |
| Incumplimiento    | Artefacto rechazado en revisión        |

> **Principio final:** un agente alineado no "sabe diseñar": sabe LEER el
> sistema. Su creatividad opera dentro de los contratos, nunca sobre ellos.
