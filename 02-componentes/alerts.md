# Alerts — Mensajes de estado

## Cuándo usarlo

Para comunicar estado del sistema de forma persistente: éxito, información, advertencia o error.
Nunca es el único canal de información crítica.

## Anatomía

```
[Icono] [Título] [Descripción]
```

- **Icono:** Refuerza el estado (✓, ℹ, ⚠, ✖)
- **Título:** Estado o acción (Éxito, Info, Advertencia, Error)
- **Descripción:** Contexto adicional

## Variantes

- **Success** (`role="status"`) — Operación completada
- **Info** (`role="status"`) — Información general
- **Warning** (`role="status"`) — Precaución, sin bloqueo
- **Danger** (`role="alert"`) — Error crítico, requiere acción

## Estados

- Default (visible)
- Cerrada (si tiene botón close)

## Accesibilidad

✅ **Do:**
- Icono + palabra + color (triple codificación)
- `role="alert"` solo para errores críticos
- `role="status"` con `aria-live="polite"` para éxito/info
- Descripción clara del problema y acción sugerida

❌ **Don't:**
- Comunicar estado solo con color
- Usar `role="alert"` para mensajes informativos
- Iconos sin texto descriptivo

## Tokens

- `color.success` / `color.warning` / `color.danger` — Colores de estado
- `space.3` / `space.4` — Padding interno
- `radius.md` — Border radius
- `motion.fast` — Transiciones (si aparece/desaparece)

## Contrato WCAG 2.2 AA

- **1.4.1 Use of Color:** No comuniques estado solo con color
- **4.1.3 Status Messages:** Los anuncios de estado usan `role="status"` o `role="alert"`
- **1.4.11 Non-text Contrast (3:1):** Icono + fondo tienen contraste suficiente

## Código

```html
<!-- Success -->
<div class="alert success" role="status" aria-live="polite">
  ✔ <strong>Éxito:</strong> cambios guardados.
</div>

<!-- Danger -->
<div class="alert danger" role="alert">
  ✖ <strong>Error:</strong> no se pudo procesar el pago.
</div>
```
