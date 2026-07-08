# Patrón · Modales

Diálogos que requieren decisión o atención. Bloquean contenido de fondo.

## Variantes

### Estándar
- Título + contenido + botones de acción.
- Tamaño mediano (400-600px).
- Cierre: botón X, Escape, clic fuera (opcional).

### Confirmación
- Pregunta binaria (Sí/No, Continuar/Cancelar).
- Botón principal (acción) vs secundario (cancelar).
- Un solo botón primario.

### Peligro (Destructivo)
- Advertencia roja.
- Confirmación doble (ej: escribir "ELIMINAR").
- Botón destruir en rojo (color.danger).

## Composición
```
modal (overlay oscuro + contenedor)
├── header
│  ├── Título (H2 o aria-labelledby)
│  └── Botón cerrar (X)
├── body (contenido)
└── footer
   ├── Botón secundario (Cancelar)
   └── Botón primario (Continuar / Eliminar)
```

## Accesibilidad
- **Role:** `role="dialog"` + `aria-modal="true"`.
- **Título:** `aria-labelledby="modal-title"` vinculado a H2.
- **Focus trap:** Tab recorre solo elementos dentro del modal; last → first.
- **Cierre:** Escape cierra el modal.
- **Fondo:** `<div class="modal-backdrop">` con fondo semitransparente.
- **Overlay:** `inert` en contenido de fondo (optional pero recomendado).

## Comportamiento e interacción
- Aparición: fade-in suave (`transition: opacity var(--motion-base)`).
- Click en botón principal → ejecuta acción + cierra.
- Click en cancelar → cierra sin ejecutar.
- Click fuera (backdrop) → cierra (configurable).
- Escape → cierra.

## Tokens
`color.surface` · `color.text` · `color.danger` · `space.4` · `space.5` · `radius.lg` · `motion.base`

## Ejemplo de implementación

```html
<!-- Estándar -->
<div class="modal-backdrop" open>
  <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
    <div class="modal-header">
      <h2 id="modal-title">Crear nuevo proyecto</h2>
      <button class="btn ghost" aria-label="Cerrar" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body">
      <p>Ingresa los detalles del proyecto...</p>
      <div class="field">
        <label for="proj-name">Nombre</label>
        <input id="proj-name" type="text" />
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn secondary" onclick="closeModal()">Cancelar</button>
      <button class="btn primary" onclick="createProject()">Crear</button>
    </div>
  </div>
</div>

<!-- Confirmación peligrosa -->
<div class="modal-backdrop" open>
  <div class="modal danger" role="dialog" aria-modal="true" aria-labelledby="danger-title">
    <div class="modal-header">
      <h2 id="danger-title">⚠ Eliminar cuenta</h2>
    </div>
    <div class="modal-body">
      <p>Esta acción es permanente y no se puede revertir.</p>
      <p>Escribe <strong>ELIMINAR</strong> para confirmar:</p>
      <input type="text" placeholder="ELIMINAR" id="confirm-text" />
    </div>
    <div class="modal-footer">
      <button class="btn secondary" onclick="closeModal()">Cancelar</button>
      <button class="btn danger" onclick="deleteAccount()" id="delete-btn" disabled>Eliminar permanentemente</button>
    </div>
  </div>
</div>
```

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--motion-base);
}

.modal-backdrop[open] {
  opacity: 1;
}

.modal {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  max-width: 600px;
  max-height: 90vh;
  overflow: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.modal-header, .modal-footer {
  display: flex;
  justify-content: space-between;
  padding: var(--space-5);
  border-bottom: 1px solid var(--color-border);
}

.modal-footer {
  border-bottom: none;
  border-top: 1px solid var(--color-border);
  gap: var(--space-3);
}

.modal-body {
  padding: var(--space-5);
}
```

## Do's & Don'ts
- ✅ Título claro y conciso.
- ❌ Modal sin título o muy genérico.
- ✅ Botón principal alineado a la acción (derecha).
- ❌ Orden de botones inconsistente.
- ✅ Focus trap dentro del modal.
- ❌ Tab escapa del modal.
- ✅ Advertencia visual (icono ⚠) en modales destructivos.
- ❌ Botón rojo sin contexto en modal normal.
