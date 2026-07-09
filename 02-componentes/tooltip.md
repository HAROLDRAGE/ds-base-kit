# Tooltip — Pista contextual

## Cuándo usarlo

Para proporcionar información adicional sin saturar la interfaz.
Alternativa a aria-label cuando la explicación es larga.

## Anatomía

```
[Icono de ayuda] → [Contenido del tooltip]
                    (flotante, cerca del trigger)
```

- **Trigger:** Elemento que dispara el tooltip (botón, icono)
- **Contenido:** Texto breve y útil
- **Posicionamiento:** Arriba, abajo, izquierda o derecha

## Variantes

- **Info:** Explicación general
- **Ayuda:** Instrucción de uso
- **Error:** Validación en tiempo real

## Estados

- Oculto (default)
- Visible (hover o focus)
- Desapareciendo (después de delay)

## Accesibilidad

✅ **Do:**
- `aria-label` o `aria-describedby` en trigger
- Aparecer en hover Y en focus
- Desaparecer con Escape
- Contenido conciso (máx 2-3 líneas)
- Usar para información **secundaria** (no crítica)

❌ **Don't:**
- Tooltip como único descriptor de funcionalidad
- Información crítica solo en tooltip
- Tooltips que se solapan
- Sin forma de cerrar (Escape)

## Tokens

- `color.text` — Texto del tooltip
- `color.surface` — Background
- `space.2` / `space.3` — Padding
- `radius.md` — Border radius
- `shadow.md` — Sombra
- `motion.fast` — Aparición/desaparición

## Contrato WCAG 2.2 AA

- **1.3.1 Info and Relationships:** Información no duplicada en aria-label
- **2.5.5 Target Size:** El trigger es suficientemente grande (44×44px)
- **2.1.1 Keyboard:** Visible en focus, cerrable con Escape

## Código

```html
<!-- Botón con tooltip -->
<button 
  aria-label="Ayuda: explica cómo usar esta función"
  data-tooltip="Por favor ingresa un correo válido, ej: nombre@ejemplo.cl"
>
  ?
</button>

<!-- CSS para mostrar/ocultar -->
<style>
[data-tooltip]:hover::after {
  content: attr(data-tooltip);
  position: absolute;
  background: var(--color-surface);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  white-space: nowrap;
  pointer-events: none;
  z-index: 10;
}
</style>
```
