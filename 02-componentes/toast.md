# Toast (Notificación)

Notificación breve y no bloqueante que se auto-anuncia sin robar el foco. Ideal para confirmaciones, advertencias, mensajes de estado.

## Cuándo usarlo
- Confirmación de acción (guardado, eliminación).
- Mensajes de estado breves (cargando, completado, error).
- Notificaciones no críticas que no requieren interacción inmediata.

## Cuándo NO usarlo
- Errores críticos (usa modal).
- Información que requiere confirmación (usa dialog).
- Contenido largo (usa card/panel).

## Variantes
| Variante | Uso |
| --- | --- |
| Success | Acción completada exitosamente |
| Error | Algo salió mal, requiere atención |
| Warning | Advertencia no bloqueante |
| Info | Información neutra |

## Estados
- [x] Default · Hover · Focus (si contiene acciones) · Exiting (fade out)

## Accesibilidad (WCAG 2.2 AA)
- Region con `aria-live="polite"` anuncia al lector de pantalla.
- No roba foco (usuario puede continuar navegando).
- Contenido anunciado automáticamente (sin requerir Tab).
- Desaparece automáticamente después de 4-5 segundos.
- Si tiene acciones (ej: "Deshacer"), Button navegable por Tab.

## Comportamiento e interacción
- Aparece en esquina (usualmente inferior derecha en desktop, superior en móvil).
- Se anuncia automáticamente a lectores de pantalla.
- Hover pausa el temporizador de desaparición.
- Desaparece automáticamente después de 4 segundos.
- Click o cierre manual lo elimina antes de tiempo.
- Múltiples toasts se apilan verticalmente.

## Tokens utilizados
`color.background` · `color.on-background` · `color.success` · `color.danger` · `color.warning` · `radius.md` · `space.3` · `space.4` · `motion.base`

## Do's & Don'ts

**✔ Do**
- Mensaje breve y claro (máx. 1-2 líneas).
- Región aria-live para auto-anunciarse.
- Desaparece automáticamente (4-5 segundos).
- Hover pausa desaparición si usuario necesita leerlo.
- Icono + color clara (no solo color).

**❌ Don't**
- Mensaje confuso o ambiguo.
- Sin aria-live (no se anuncia a AT).
- Desaparece demasiado rápido (< 3 seg).
- Solo color para indicar tipo (rojo ≠ error, verde ≠ éxito para daltónicos).
- Toasts que roben foco innecesariamente.

## Código HTML
```html
<!-- Región aria-live (presente antes de inyectar toasts) -->
<div id="toast-region" class="toast-region" aria-live="polite"></div>

<!-- Toast inyectado dinámicamente con JavaScript -->
<div class="toast toast-success">
  <span aria-hidden="true">✔</span> Cambios guardados correctamente
</div>

<div class="toast toast-error">
  <span aria-hidden="true">✖</span> Error al guardar
</div>

<div class="toast toast-warning">
  <span aria-hidden="true">⚠</span> Cambio será permanente
</div>
```

## CSS
```css
.toast-region {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  max-width: 20rem;
}

.toast {
  background: var(--color-on-background);
  color: var(--color-background);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  animation: toastSlideIn var(--motion-base) ease-out;
  box-shadow: var(--shadow-md);
}

.toast-success { background: var(--color-success); }
.toast-error { background: var(--color-danger); }
.toast-warning { background: var(--color-warning); }

@keyframes toastSlideIn {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}
```

## JavaScript
```javascript
function showToast(message, type = 'info', duration = 4000) {
  const region = document.getElementById('toast-region');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  region.appendChild(toast);
  
  let timer = setTimeout(() => removeToast(toast), duration);
  
  // Pausar desaparición en hover
  toast.addEventListener('mouseenter', () => clearTimeout(timer));
  toast.addEventListener('mouseleave', () => {
    timer = setTimeout(() => removeToast(toast), duration / 2);
  });
  
  function removeToast(el) {
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 300);
  }
}

// Uso
showToast('✔ Cambios guardados', 'success', 4000);
showToast('✖ Error al guardar', 'error', 5000);
```

## Contrato ARIA
- Región con `aria-live="polite"` (anuncio no interrumpido).
- Contenido anunciado automáticamente al insertarse en DOM.
- No requiere `aria-label` en región (live ya proporciona contexto).
- Icono con `aria-hidden="true"` si es puramente visual.

## Contrato de teclado
- **No requiere navegación** si es solo notificación.
- **Si tiene acciones** (ej: botón "Deshacer"): Tab lo navega.
- **Auto-dismiss** no interrumpe navegación del usuario.

## Temporizadores
- **Mínimo 4 segundos**: Permite lectura completa + acción (Deshacer).
- **Máximo 6 segundos**: Permite lectura sin distraer indefinidamente.
- **Hover pausa**: Si usuario necesita más tiempo para leer.
- **Múltiples**: Apilan sin bloquear interacción.

## WCAG 2.2 AA
- **1.4.3 Contraste (mínimo)**: 4.5:1 para texto en toast (según color de fondo).
- **2.1.2 Sin trampa de teclado**: Toast no atrapa foco (permite navegación normal).
- **2.5.2 Tamaño de objetivo**: Si tiene botones de acción, mínimo 44×44px.
- **4.1.3 Mensajes de estado**: aria-live="polite" comunica cambios a AT.
- **2.2.3 Sin límite de tiempo (excepto esencial)**: Toast es esencial, pero 4+ seg permite lectura.
