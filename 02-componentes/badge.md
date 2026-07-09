# Badge — Indicador de estado o contador

## Cuándo usarlo

Para indicar estado o mostrar contadores de forma compacta.
Nunca debe ser el único canal de información crítica.

## Anatomía

```
[Icono o número] [Etiqueta]
```

- **Contenido:** Número, palabra o símbolo breve
- **Contexto:** Siempre dentro de un control (button, card, etc.)

## Variantes

- **Default** — Estado neutral
- **Ok** — Éxito/activo
- **Warning** — Pendiente/cautela
- **Error** — Crítico/vencido

## Estados

- Default (visible)
- En botones con focus
- En elementos activos

## Accesibilidad

✅ **Do:**
- Incluir el contador en `aria-label` del control contenedor
- Texto + color para comunicar estado
- Badge adjunto a un control interactivo

❌ **Don't:**
- Badge como único indicador de información crítica
- Contadores sin nombre accesible
- Color como único diferenciador

## Tokens

- `color.action-soft` — Background
- `color.action-hover` — Text
- `space.2` — Padding
- `radius.full` — Forma píldora

## Contrato WCAG 2.2 AA

- **1.4.3 Contrast Minimum (4.5:1 for text):** Badge tiene contraste suficiente
- **1.3.1 Info and Relationships:** El significado está en el aria-label del contenedor

## Código

```html
<!-- En un botón -->
<button aria-label="Notificaciones, 4 sin leer">
  🔔 Notificaciones
  <span class="badge">4</span>
</button>

<!-- Estado -->
<span class="badge ok">Activo</span>
<span class="badge warn">Pendiente</span>
<span class="badge err">Vencido</span>
```
