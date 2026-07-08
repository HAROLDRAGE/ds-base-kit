# Tarjeta

Superficie que agrupa contenido relacionado. Aísla y da jerarquía visual.

## Cuándo usarlo
- Agrupar contenido temático: producto, artículo, usuario, resultado.
- Crear ritmo visual en listados.
- Elevar un bloque de contenido.

## Cuándo NO usarlo
- Layout de página completo → usa una sección.
- Contenedor solo para aplicar espaciado → usa div con padding.

## Anatomía
```
<div class="card">
  <h3>Título</h3>
  <p>Contenido...</p>
  [opcional: link o botón al pie]
</div>
```

## Variantes
| Variante | Uso |
| --- | --- |
| Default | Contenido solo lectura |
| Interactive | Card es un botón/enlace; toda la tarjeta es clickeable |

## Estados
- [x] Default · Hover · Focus (si es interactiva)

## Accesibilidad
- **Card interactiva:** el contenedor es un `<a>` o tiene `role="button"` + `tabindex="0"`.
- **Foco en tarjeta:** no en elementos internos (captura foco).
- **Texto dentro:** jerarquía clara (H3, no H1 si es dentro de sección).
- **Si es interactiva:** un solo destino/acción principal dentro de la tarjeta.

## Comportamiento e interacción
- Hover (interactiva) → sombra o elevación.
- Focus (interactiva) → borde de `color.focus`.
- Sin interacción (default) → hover solo visual, sin cambio de cursor.

## Tokens
`color.surface` · `color.border` · `space.4` · `radius.lg` · `motion.fast`

## Do's & Don'ts
- ✅ Un destino principal por tarjeta.
- ❌ Múltiples botones dentro compitiendo.
- ✅ Contenido consistente en altura o flexible.
- ❌ Tarjeta vacía o sin contenido claro.

## Código

```html
<!-- Default (solo lectura) -->
<div class="card">
  <h3>Artículo destacado</h3>
  <p>Lorem ipsum dolor sit amet...</p>
  <span class="badge brand">Nuevo</span>
</div>

<!-- Interactive (enlace) -->
<a href="/productos/123" class="card interactive">
  <h3>Producto: Auriculares</h3>
  <p>Descripción del producto...</p>
  <span class="badge success">En stock</span>
</a>

<!-- Interactive (botón) -->
<button class="card interactive" onclick="abrirModal()">
  <h3>Acción: Crear nuevo elemento</h3>
  <p>Inicia un flujo de configuración...</p>
</button>
```

## Props
- `href` si es `<a>` (string).
- `onclick` o `data-action` si es `<button>`.
- `class` (string): "card" o "card interactive".
- Contenido interior: flexible, respeta estructura del contexto.
