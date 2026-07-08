# Input

Entrada de texto de una línea.

## Cuándo usarlo
- Texto corto: nombre, email, búsqueda.

## Cuándo NO usarlo
- Texto largo → textarea. Opciones cerradas → select.

## Estados
- [x] Default · Hover · Focus · Disabled · Error

## Accesibilidad
- Label siempre visible y asociado (`for`/`id`).
- Error: icono + mensaje vinculado con `aria-describedby`.

## Tokens
`color.surface` · `color.text` · `color.border` · `color.danger` · `space.3` · `radius.md`

## Do's & Don'ts
- ✅ Label visible sobre el campo.
- ❌ Placeholder como único label.
