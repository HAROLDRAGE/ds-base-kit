# Pagination — Paginación

## Cuándo usarlo

Para dividir contenido largo en páginas navegables.
Alternativa a scroll infinito cuando el usuario necesita saltar a una página específica.

## Anatomía

```
[< Anterior] [1] [2] [3] ... [Siguiente >]
```

- **Anterior:** Botón al inicio
- **Números de página:** Enlaces o botones
- **Página actual:** Destacada (aria-current)
- **Siguiente:** Botón al final

## Variantes

- **Numerada:** 1, 2, 3...
- **Compacta:** Prev/Next solo (sin números)
- **Con salto:** Input para ir a página específica

## Estados

- Primera página (Anterior disabled)
- Página media (ambos activos)
- Última página (Siguiente disabled)
- Hover (enlaces/botones)
- Focus
- Página actual (aria-current)

## Accesibilidad

✅ **Do:**
- `<nav aria-label="Paginación">`
- Página actual con `aria-current="page"`
- Botones Anterior/Siguiente con aria-label descriptivos
- Disabled en botones inapropiados

❌ **Don't:**
- Números sin contexto
- Anterior/Siguiente sin estar disabled en límites
- Página actual como enlace

## Tokens

- `color.action` — Color de enlaces activos
- `color.bg` — Background página actual
- `space.1` / `space.2` — Padding
- `radius.md` — Border radius
- `motion.fast` — Hover transitions

## Contrato WCAG 2.2 AA

- **2.1.1 Keyboard:** Tab entre números y botones
- **2.4.8 Location:** El usuario sabe en qué página está
- **1.3.1 Info and Relationships:** aria-current comunica página actual

## Código

```html
<nav aria-label="Paginación">
  <button class="btn secondary" aria-label="Ir a página anterior">← Anterior</button>
  
  <a href="?page=1" class="page-link">1</a>
  <a href="?page=2" class="page-link" aria-current="page">2</a>
  <a href="?page=3" class="page-link">3</a>
  
  <button class="btn secondary" aria-label="Ir a página siguiente">Siguiente →</button>
</nav>
```
