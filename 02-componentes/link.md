# Enlace

Navegación a otra vista o recurso externo. No ejecuta acciones.

## Cuándo usarlo
- Navegar a otra página dentro del producto.
- Enlaces externos en documentación.
- Referencias dentro de un párrafo o lista.

## Cuándo NO usarlo
- Para ejecutar una acción (guardar, enviar) → usa un botón.
- Para abrir un menú → usa un botón con aria-haspopup.

## Anatomía
```
<a href="/destino" class="link">Texto autoexplicativo</a>
```

## Variantes
| Variante | Uso |
| --- | --- |
| Inline | Dentro de un párrafo o lista (subrayado continuo) |
| Standalone | Fuera de contexto, botón de navegación (puede ir sin subrayado en hover) |

## Estados
- [x] Default · Hover · Focus · Visited

## Accesibilidad
- **Texto autoexplicativo:** nunca "clic aquí" ni "aquí". Incluir contexto: "Ver documentación", "Leer política de privacidad".
- **Subrayado visible en párrafos:** en inline, subrayado siempre visible para cumplir 4.5:1 texto.
- **Foco visible:** outline de `color.focus` con offset.
- **Rel externo:** `rel="external"` o `rel="noopener noreferrer"` si es `target="_blank"`.

## Comportamiento e interacción
- Click → navega a `href`.
- Enter (teclado) → navega.
- Visitado → color más tenue (usar `:visited` con contraste ≥ 3:1).
- Sin JavaScript requerido.

## Tokens
`color.action` · `motion.fast`

## Do's & Don'ts
- ✅ Texto descriptivo: "Ver componente de botón".
- ❌ Texto genérico: "clic aquí".
- ✅ Subrayado visible en párrafos.
- ❌ Subrayado solo en hover.

## Código

```html
<!-- Inline en párrafo -->
<p>Lee la <a href="/docs">guía de componentes</a> para más detalles.</p>

<!-- Standalone -->
<a href="/inicio" class="link standalone">Volver a inicio</a>

<!-- Externo -->
<a href="https://ejemplo.com" rel="external" target="_blank">
  Ver ejemplo (abre en ventana nueva)
</a>
```

## Props HTML
- `href` (string, requerido): destino.
- `rel` (string): "external", "noopener noreferrer".
- `target` (string): "_blank" para abrir en nueva ventana.
- `class` (string): "link" o "link standalone".
