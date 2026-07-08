# Campo

Unidad completa de formulario: label + input + ayuda/error. Siempre composición, nunca input solo.

## Cuándo usarlo
- Formularios: cada campo siempre es una molécula field.
- Labels visibles y asociados al input.

## Cuándo NO usarlo
- Input suelto sin label → agrega un label.
- Formularios muy complejos con subgrupos: considera agrupar fields en fieldset.

## Anatomía
```
<div class="field">
  <label for="email">Correo</label>
  <input id="email" type="email" aria-describedby="email-help" />
  <p id="email-help" class="help">Usaremos este correo para contactarte.</p>
</div>
```

## Variantes
| Variante | Uso |
| --- | --- |
| Default | Input sin mensaje adicional |
| With Help | Input + texto de ayuda (gris claro) |
| With Error | Input + mensaje de error (color.danger + icono ⚠) |

## Estados
- [x] Default · Focus · Disabled · Error

## Accesibilidad
- **Label siempre visible:** asociado con `for`/`id`.
- **Aria-describedby:** vincula input al párrafo de ayuda/error.
- **Error con icono + palabra:** nunca solo color rojo.
- **Orden lógico:** tabulación va label → input → siguiente campo.
- **Disabled:** atributo `disabled` en input + texto gris (color.muted).

## Comportamiento e interacción
- Click en label → foco en input.
- Focus en input → borde de `color.focus`.
- Blur con error → muestra mensaje debajo.
- Help text siempre visible.

## Tokens
`color.text` · `color.muted` · `color.danger` · `space.2` · `space.3` · `space.4` · `radius.md`

## Do's & Don'ts
- ✅ Label siempre visible.
- ❌ Placeholder como único label.
- ✅ Error con ⚠ + texto: "Email inválido".
- ❌ Solo campo rojo sin mensaje.

## Código

```html
<!-- Default -->
<div class="field">
  <label for="name">Nombre completo</label>
  <input id="name" type="text" />
</div>

<!-- With Help -->
<div class="field">
  <label for="password">Contraseña</label>
  <input id="password" type="password" aria-describedby="pwd-help" />
  <p id="pwd-help" class="help">Mín. 8 caracteres, 1 mayúscula, 1 número.</p>
</div>

<!-- With Error -->
<div class="field error">
  <label for="email">Correo</label>
  <input id="email" type="email" aria-describedby="email-error" />
  <p id="email-error" class="error">⚠ Correo inválido o ya registrado.</p>
</div>

<!-- Disabled -->
<div class="field">
  <label for="readonly">Campo deshabilitado</label>
  <input id="readonly" type="text" disabled value="Lectura" />
</div>
```

## Props
- `for` en label (string): ID del input.
- `id` en input (string): único en la página.
- `aria-describedby` en input (string): ID del párrafo de ayuda/error.
- `disabled` en input (boolean): deshabilita entrada.
- `type` en input (string): "text", "email", "password", "search", etc.
- `class` en contenedor (string): "field" o "field error".
