# Dropdown — Menú desplegable

## Cuándo usarlo

Para agrupar acciones secundarias o filtros sin ocupar espacio permanente.
Alternativa a botones secundarios cuando hay muchas opciones.

## Anatomía

```
[Botón de disparo ▾]
├─ [Opción 1]
├─ [Opción 2]
└─ [Opción 3]
```

- **Botón:** Dispara el menú (aria-haspopup, aria-expanded)
- **Menú:** Lista de opciones (role="menu")
- **Items:** Botones dentro del menú (role="menuitem")

## Variantes

- **Acciones:** Operaciones sobre un elemento
- **Filtro:** Opciones de selección (radio buttons internos)
- **Con peligro:** Última opción en rojo (destructiva)

## Estados

- Cerrado (menú oculto)
- Abierto (menú visible)
- Hover (items)
- Focus (ítem activo)
- Disabled (opción deshabilitada)

## Accesibilidad

✅ **Do:**
- `aria-haspopup="true"` en botón de disparo
- `aria-expanded` indica si está abierto
- `role="menu"` + `role="menuitem"` para navegación por teclado
- Escape cierra el menú
- Arrow keys navegan items
- Enter/Space activan el item

❌ **Don't:**
- Menú que no se cierra con Escape
- Items no accesibles por teclado
- Diferencial solo por color en opciones peligrosas

## Tokens

- `color.bg` — Background del menú
- `color.text` — Texto de items
- `color.danger` — Color de opción destructiva
- `radius.md` — Border radius
- `shadow.md` — Sombra del menú
- `space.1` / `space.2` — Padding items

## Contrato WCAG 2.2 AA

- **2.4.3 Focus Order:** Navegación lógica con teclado
- **1.4.1 Use of Color:** No comuniques destrucción solo con color
- **2.1.1 Keyboard:** Todas las funciones accesibles por teclado

## Código

```html
<div class="dropdown">
  <button 
    class="btn secondary" 
    aria-haspopup="true" 
    aria-expanded="false" 
    aria-controls="menu1"
    onclick="toggleMenu(this)"
  >
    Acciones ▾
  </button>
  <ul class="dropdown-menu" id="menu1" role="menu" hidden>
    <li role="none"><button role="menuitem">Editar</button></li>
    <li role="none"><button role="menuitem">Duplicar</button></li>
    <li role="none"><button role="menuitem" class="danger">Eliminar</button></li>
  </ul>
</div>
```
