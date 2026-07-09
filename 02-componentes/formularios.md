# Formularios

Entrada estructurada de datos: inputs de texto, emails, selects, checkboxes, radios, switches y validación.

## Cuándo usarlo
- Recopilar datos del usuario (login, registro, pedidos).
- Configuración y preferencias.
- Búsqueda y filtros.

## Cuándo NO usarlo
- Para acciones simples (usa botones).
- Para contenido de solo lectura (usa tablas o listas).

## Componentes incluidos
| Componente | Uso |
| --- | --- |
| Input text/email | Entrada de texto simple |
| Textarea | Texto largo multilínea |
| Select | Lista desplegable de opciones |
| Checkbox | Selección múltiple |
| Radio | Selección única excluyente |
| Switch/Toggle | Activar/desactivar booleano |

## Estados
- [x] Default · Hover · Focus · Filled · Invalid · Disabled · Loading

## Accesibilidad (WCAG 2.2 AA)
- **Labels asociados**: `<label for="id">` siempre vinculado y visible.
- **Validación clara**: Mensajes de error describen cómo corregir (no solo "Error").
- **Indicadores visuales**: Rojo/verde no son únicos (usa iconos + texto).
- **Fieldsets**: `<fieldset>` + `<legend>` para grupos (radios, checkboxes).
- **Mensajes de error**: `role="alert"` + `aria-describedby`.

## Comportamiento e interacción
- Tab navega entre campos.
- Enter envía el formulario (en `<button type="submit">`).
- Espacio alterna checkbox/switch.
- Flechas ↑↓ cambian opción en select/radios.
- Enter abre select en foco.
- Validación al enviar o bajo demanda (no en tiempo real).

## Tokens utilizados
`color.border` · `color.action` · `color.danger` · `radius.md` · `space.2` · `space.3` · `space.4` · `motion.fast`

## Do's & Don'ts

**✔ Do**
- Label visible y siempre asociado (`for="id"`).
- Validar al enviar; mostrar errores claros que expliquen cómo corregir.
- Fieldsets con legend para grupos de opciones.
- aria-describedby vinculando input con mensaje de error.

**❌ Don't**
- Labels ocultos (placeholders no son labels).
- Validación solo con color rojo (usa icono + texto).
- Cambiar valores mientras el usuario escribe (espera a envío).
- Inputs sin labels (accesibles deben tener etiqueta explícita).

## Código HTML
```html
<!-- Input con validación -->
<form onsubmit="return validateForm(event)">
  <div class="field">
    <label for="email">Correo electrónico *</label>
    <input 
      id="email" 
      type="email" 
      required 
      aria-describedby="email-err">
    <p id="email-err" class="field-error" role="alert" hidden>
      ✖ Ingresa un correo válido, ej: nombre@dominio.cl
    </p>
  </div>

  <!-- Radios agrupados -->
  <fieldset>
    <legend>Plan *</legend>
    <label class="choice">
      <input type="radio" name="plan" value="basic" checked>
      Básico
    </label>
    <label class="choice">
      <input type="radio" name="plan" value="pro">
      Pro
    </label>
  </fieldset>

  <!-- Checkbox -->
  <label class="choice">
    <input type="checkbox" required>
    Acepto los <a href="/terms">términos</a> *
  </label>

  <!-- Botón de envío -->
  <button class="btn primary" type="submit">Enviar</button>
</form>
```

## Contrato ARIA
- `<label for="id">` siempre presente y visible.
- `<fieldset>` + `<legend>` para agrupar radios/checkboxes.
- `aria-describedby="error-id"` vincula input con mensaje de error.
- `role="alert"` en mensajes de error.
- `aria-invalid="true"` cuando hay error (opcional pero recomendado).

## Contrato de teclado
- **Tab**: Navega entre campos en orden.
- **Shift+Tab**: Navega hacia atrás.
- **Enter**: En select abre dropdown; en formulario envía (button[type=submit]).
- **Espacio**: Alterna checkbox/switch/radio.
- **Flechas ↑↓**: Cambian opción en select/radios.
- **Foco visible**: ≥ 3:1 contraste.

## Validación
- **Client-side**: JavaScript con mensaje claro antes de enviar.
- **Server-side**: Siempre validar en servidor (nunca confiar solo en client).
- **Mensajes**: Describir qué está mal y cómo corregir (no solo "Error").
- **Persistencia**: Mantener valores si hay error (para corrección parcial).

## WCAG 2.2 AA
- **1.3.1 Información y relaciones**: Labels asociados, fieldsets con legend.
- **2.1.1 Teclado**: Todos los campos navegables y operables por teclado.
- **2.4.7 Foco visible**: Indicador visual claro en focus.
- **3.3.1 Identificación de errores**: Mensajes describen el error.
- **3.3.3 Sugerencia de errores**: Mensajes explican cómo corregir.
- **3.3.4 Prevención de errores**: Validación clara antes de envío (especialmente datos críticos).
- **4.1.2 Nombre, rol, valor**: aria-describedby, aria-invalid comunican estado a lectores de pantalla.
