# Modal — Diálogo modal

## Cuándo usarlo

Para acciones que requieren confirmación o entrada de datos crítica.
No es recomendable para mensajes que no requieren respuesta inmediata.

## Anatomía

```
┌──────────────────────────┐
│ [Título]                 │
├──────────────────────────┤
│ [Contenido]              │
├──────────────────────────┤
│ [Cancelar] [OK]          │
└──────────────────────────┘
```

- **Backdrop:** Oscurece fondo (inerte, clicable para cerrar)
- **Modal:** Dialog con aria-modal
- **Título:** H4 identificando la acción
- **Contenido:** Contexto y confirmación
- **Acciones:** Botones primarios y secundarios

## Variantes

- **Confirmación:** "¿Estás seguro?"
- **Destructivo:** Alerta roja, lenguaje claro del riesgo
- **Entrada:** Formulario dentro del modal

## Estados

- Cerrado (backdrop hidden)
- Abierto (backdrop visible, focus trap activo)
- Hover/Focus (en botones)

## Accesibilidad

✅ **Do:**
- `role="dialog"` + `aria-modal="true"`
- `aria-labelledby` apunta al título
- Trap de focus: solo elementos interactivos dentro
- Escape cierra el modal
- Foco retorna al elemento que lo abrió
- Alt text en imágenes de advertencia

❌ **Don't:**
- Cerrar modal sin confirmar en acciones destructivas
- Focus que escapa del modal
- Semántica solo con color (ej: rojo = peligro)
- Modal sin forma clara de cerrarlo

## Tokens

- `color.bg` — Background del modal
- `color.danger` — Botones destructivos
- `radius.lg` — Border radius
- `shadow.md` — Sombra del modal
- `space.4` / `space.6` — Padding
- `motion.base` — Transición de aparición

## Contrato WCAG 2.2 AA

- **2.1.1 Keyboard:** Todas las funciones (Escape, Enter, Tab trap)
- **1.4.1 Use of Color:** Botón destructivo tiene icono + palabra
- **2.4.3 Focus Order:** Trap de focus dentro del modal

## Código

```html
<div class="modal-backdrop" id="modal-bg" hidden>
  <div 
    class="modal" 
    role="dialog" 
    aria-modal="true" 
    aria-labelledby="modal-title"
  >
    <h4 id="modal-title">¿Eliminar 3 archivos?</h4>
    <p>Esta acción no se puede deshacer.</p>
    <div class="row end">
      <button class="btn secondary" onclick="closeModal()">Cancelar</button>
      <button class="btn danger" onclick="confirmDelete()">⚠ Eliminar</button>
    </div>
  </div>
</div>

<script>
function closeModal() {
  document.getElementById('modal-bg').hidden = true;
  // Retornar foco al elemento que abrió el modal
}
function openModal() {
  document.getElementById('modal-bg').hidden = false;
  // Focus trap: Tab solo entre botones
}
</script>
```
