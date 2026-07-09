# Link (Enlace)

Componente de navegación que lleva a otro documento, sección o recurso externo. Siempre claramente identificable y accesible.

## Cuándo usarlo / Cuándo NO usarlo

### ✅ Usar para:
- Navegación a otra página
- Enlaces internos a secciones
- Referencias a recursos externos
- Acciones secundarias que NO son formularios

### ❌ NO usar para:
- Acciones de formulario (usar `<button>`)
- Descargas de archivos (usar `<button>` con download attr)
- Navegación principal (usar componente `navbar`)

---

## Anatomía

```html
<a href="/destino" class="link">Ir a recurso</a>
```

Partes:
1. **Texto del enlace** → debe ser descriptivo ("Más información", NO "click aquí")
2. **Color** → `--color-action` (cambia por tema/marca)
3. **Indicador visual** → subrayado (color) o icono
4. **Focus ring** → visible en todos los estados

---

## Variantes

### Link Estándar (inline)

```html
<a href="#" class="link">Enlace estándar</a>
```

- Color semántico `--color-action`
- Subrayado en hover
- Sin decoración en reposo (tema)

### Link Deshabilitado

```html
<a href="#" aria-disabled="true" class="link link--disabled">
  Enlace deshabilitado
</a>
```

- Color: `--color-muted`
- No clickeable (cursor: not-allowed)
- Contraste > 4.5:1

---

## Estados

| Estado | Apariencia | Cursor | ARIA |
|--------|-----------|--------|------|
| **Default** | `color-action`, sin decoración | pointer | N/A |
| **Hover** | Subrayado + color más oscuro | pointer | N/A |
| **Focus** | Focus ring visible (2px) | pointer | N/A |
| **Visited** | Color ligeramente diferente (opcional) | pointer | N/A |
| **Active** (durante click) | Escala/opacidad reducida | pointer | `aria-current="page"` si es página actual |
| **Disabled** | `color-muted`, no clickeable | not-allowed | `aria-disabled="true"` |

---

## Comportamiento e Interacción

1. **Click:** Navega a href
2. **Keyboard (Tab):** Navega con Tab, activable con Enter
3. **Página actual:** Usa `aria-current="page"` para indicar que es la sección actual
4. **Enlaces externos:** Opcional añadir icono + atributo `target="_blank"` + `rel="noopener noreferrer"`

```html
<!-- Página actual -->
<a href="/inicio" aria-current="page">Inicio</a>

<!-- Enlace externo -->
<a href="https://ejemplo.com" target="_blank" rel="noopener noreferrer">
  Sitio externo <span aria-label="abre en nueva pestaña">🔗</span>
</a>
```

---

## Accesibilidad

### ♿ Requerimientos WCAG 2.2 AA

- ✅ **Texto descriptivo:** "Ir a producto" NO "click aquí"
- ✅ **Color + indicador:** NO solo color (usa subrayado o icono)
- ✅ **Focus visible:** Siempre, 2px+ outline
- ✅ **Contraste:** 4.5:1 mínimo contra fondo
- ✅ **Keyboard:** Tab, Enter para activar
- ✅ **Links externos:** Indicar con icono + `target="_blank"` requiere `rel="noopener"`
- ✅ **Skip links:** Primera opción de navegación en la página

### Atributos ARIA

```html
<!-- Enlace que abre nueva pestaña -->
<a href="..." target="_blank" rel="noopener" aria-label="Ir a sitio (abre nueva pestaña)">
  Sitio externo
</a>

<!-- Página actual/activa -->
<a href="/servicios" aria-current="page">Servicios</a>

<!-- Enlace deshabilitado -->
<a href="#" aria-disabled="true">No disponible</a>
```

---

## Tokens Utilizados

| Token | Propiedad | Valor Ejemplo |
|-------|-----------|--------------|
| `--color-action` | color | Según marca y tema activos |
| `--color-action-hover` | color (hover) | Según marca y tema activos |
| `--color-muted` | color (disabled) | Tema-dependiente |
| `--focus-color` | outline color | Tema-dependiente |
| `--space-1` | margin (si hay icono) | `var(--space-1)` |

---

## Do's & Don'ts

### ✅ DO:
```html
<!-- Texto claro y descriptivo -->
<a href="/blog/article-1">Leer artículo sobre cómo empezar</a>

<!-- Con icono externo para nuevas pestañas -->
<a href="https://recurso.com" target="_blank" rel="noopener">
  Más información <span aria-hidden="true">↗</span>
</a>

<!-- Página actual siempre indicada -->
<nav>
  <a href="/inicio">Inicio</a>
  <a href="/servicios" aria-current="page">Servicios</a>
  <a href="/contacto">Contacto</a>
</nav>
```

### ❌ DON'T:
```html
<!-- ❌ Texto genérico sin contexto -->
<a href="/blog/123">Leer más</a>
<a href="...">click aquí</a>

<!-- ❌ Solo color para diferenciar -->
<a href="#" style="color: var(--color-action)">Sin subrayado</a>

<!-- ❌ Links que se ven como botones pero no son semánticos -->
<div class="link-button" onclick="...">Acción</div>

<!-- ❌ Abrir pestaña sin indicar -->
<a href="externo.com" target="_blank">Ir a sitio</a>
```

---

## Código / Props

### HTML

```html
<a href="/pagina" class="link">Ir a página</a>

<!-- Con modifiers -->
<a href="/pagina" class="link link--disabled" aria-disabled="true">
  No disponible
</a>

<a href="/external" target="_blank" rel="noopener" class="link">
  Recurso externo <span aria-hidden="true">↗</span>
</a>
```

### CSS

```css
.link {
  color: var(--color-action);
  text-decoration: none;
  cursor: pointer;
  transition: color var(--motion-base);
  position: relative;
}

.link:hover {
  color: var(--color-action-hover);
  text-decoration: underline;
}

.link:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  border-radius: 2px;
}

.link:visited {
  color: var(--color-action);  /* o modificar ligeramente */
}

.link[aria-disabled="true"] {
  color: var(--color-muted);
  pointer-events: none;
  cursor: not-allowed;
  text-decoration: none;
}

.link[aria-current="page"] {
  font-weight: var(--typography-font-weight-semibold);
  border-bottom: 2px solid var(--color-action);
}
```

---

## Referencias

- 📄 **Manifest:** `05-agentes/component-manifest.json`
- 🎨 **Tokens:** `01-tokens/COLORES.md`, `01-tokens/ESPACIADO.md`
- ♿ **WCAG:** https://www.w3.org/WAI/WCAG22/Understanding/link-purpose
- 📘 **MDN:** https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a
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
