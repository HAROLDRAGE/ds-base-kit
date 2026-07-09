# Table (Tabla)

Presentación de datos tabulares comparables y accesibles. **Solo para datos, nunca para layout.**

## Cuándo usarlo
- Mostrar datos en filas y columnas (comparativas, precios, listados).
- Datos que requieren análisis lado a lado.

## Cuándo NO usarlo
- Para maquetar layout (usa grid/flexbox en CSS).
- Para datos no relacionados (usa cards en su lugar).

## Variantes
| Variante | Uso |
| --- | --- |
| Básica | Datos simples sin acciones |
| Con acciones | Filas con botones de editar/eliminar |
| Condensada | Datos densos, espacios reducidos |
| Striped | Filas alternadas para legibilidad |
| Hover | Resaltar fila en hover |

## Estados
- [x] Default · Hover (fila) · Focus (navegable) · Sortable · Empty state · Loading

## Accesibilidad (WCAG 2.2 AA)
- **Estructura**: `<caption>` + `<thead>` + `<tbody>` obligatorios.
- **Alcance**: `th` con `scope="col"` (encabezados de columna) y `scope="row"` (etiquetas de fila).
- **Navegable**: Wrapper scrollable con `tabindex="0"` + `role="region"` + `aria-label`.
- **Anunciado**: Lector de pantalla anuncia relaciones fila-columna automáticamente.

## Comportamiento e interacción
- Flechas ↑↓ hacen scroll vertical en tablas largas.
- Flechas ←→ hacen scroll horizontal si es necesario.
- Tab enfoca el wrapper · Luego flechas navegan.
- Enter en filas con acciones (botones, links) los ejecuta.

## Tokens utilizados
`color.border` · `color.surface` · `color.on-surface` · `space.2` · `space.3` · `motion.base`

## Do's & Don'ts

**✔ Do**
- Usar `<caption>` para describir la tabla.
- `th scope="col"` en encabezados, `scope="row"` en etiquetas de fila.
- Wrapper con `role="region"` + `aria-label` si scrollable.
- Datos complejos en `<thead>` / `<tbody>`.

**❌ Don't**
- Tablas para layout o diseño.
- Celdas merged (`colspan`/`rowspan`) sin `scope` correcto.
- Todas las celdas `<td>` sin contexto de encabezado.
- Contenido solo visual (iconos sin etiquetas).

## Código HTML
```html
<div class="table-wrap" tabindex="0" role="region" aria-label="Comparativa de planes">
  <table>
    <caption class="sr-only">Comparativa de planes de precios</caption>
    <thead>
      <tr>
        <th scope="col">Plan</th>
        <th scope="col">Precio</th>
        <th scope="col">Estado</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <th scope="row">Básico</th>
        <td>$0</td>
        <td><span class="badge ok">Activo</span></td>
      </tr>
      <tr>
        <th scope="row">Pro</th>
        <td>$9.900</td>
        <td><span class="badge ok">Activo</span></td>
      </tr>
      <tr>
        <th scope="row">Enterprise</th>
        <td>Contactar</td>
        <td><span class="badge warn">Beta</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

## Contrato ARIA
- `<caption>` describe la tabla o está oculto con `.sr-only`.
- `<th scope="col">` para encabezados de columna.
- `<th scope="row">` para etiquetas de fila (si la primera columna es identificador).
- Wrapper scrollable: `tabindex="0"` + `role="region"` + `aria-label`.

## Contrato de teclado
- **Tab**: Enfoca el wrapper (si tiene contenido interactivo).
- **Flechas ↑↓**: Scroll vertical (si está activado).
- **Flechas ←→**: Scroll horizontal (para tablas anchas).
- **Enter / Espacio**: Activan acciones en celdas interactivas (botones, links).

## WCAG 2.2 AA
- **1.3.1 Información y relaciones**: Estructura semántica con `scope`.
- **1.4.10 Reflow**: Scrollable sin perder contexto.
- **2.1.1 Teclado**: Navegable completamente por teclado.
- **4.1.2 Nombre, rol, valor**: `caption` + `scope` = contexto claro.
