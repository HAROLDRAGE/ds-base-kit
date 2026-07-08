# Botón

Acción interactiva que dispara una operación.

## Cuándo usarlo
- Acciones que ejecutan algo (guardar, enviar).

## Cuándo NO usarlo
- Para navegar entre páginas → usa un enlace.

## Variantes
| Variante | Uso |
| --- | --- |
| Primary | Acción principal (1 por vista) |
| Secondary | Acción de apoyo |
| Ghost | Acción terciaria |
| Danger | Acción destructiva |

## Estados
- [x] Default · Hover · Focus · Active · Disabled · Loading

## Accesibilidad
- Operable con teclado (Enter / Espacio); foco visible ≥ 3:1.
- `aria-busy="true"` en loading; `aria-label` si es solo icono.

## Tokens
`color.action` · `color.on-action` · `radius.md` · `space.3` · `space.4` · `motion.fast`

## Do's & Don'ts
- ✅ Un solo botón primario por vista.
- ❌ Múltiples primarios compitiendo por atención.
