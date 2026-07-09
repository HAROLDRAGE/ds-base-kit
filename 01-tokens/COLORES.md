# Sistema de Colores

> **Fuente única de verdad:** `01-tokens/tokens.css` + `component-manifest.json`

## Tabla de Contenidos
1. [Colores Semánticos](#colores-semánticos)
2. [Colores Extendidos](#colores-extendidos)
3. [Mapeo a Componentes](#mapeo-a-componentes)
4. [Modo Oscuro/Claro](#modo-oscurooscuro)
5. [Accesibilidad WCAG](#accesibilidad-wcag)
6. [Uso Correcto](#uso-correcto)

---

## Colores Semánticos

Los colores semánticos definen **intención** no apariencia. Se aplican automáticamente según marca + tema.

| Token | Use | NOT For | Ejemplo |
|-------|-----|---------|---------|
| `--color-bg` | Fondo base de página | Texto, énfasis | Body background |
| `--color-surface` | Tarjetas, paneles, inputs | Texto, fondos grandes | Card background |
| `--color-text` | Texto principal | Fondos | Párrafos, labels |
| `--color-muted` | Texto secundario, ayudas | Texto crítico | Hints, meta, deshabilitado |
| `--color-action` | Acciones: botones, enlaces, foco | Fondos extensos | Links, btn-primary, focus ring |
| `--color-on-action` | Icono/texto sobre `--color-action` | Otros fondos | Icon en btn-primary |
| `--color-focus` | Anillo de foco visible (outline) | Decoración | Focus ring (4px) |
| `--color-danger` | Errores (siempre + icono + palabra) | Énfasis genérico | Error state, validation |
| `--color-success` | Confirmaciones (siempre + icono + palabra) | Énfasis genérico | Success toast, check |
| `--color-warning` | Advertencias (siempre + icono + palabra) | Énfasis genérico | Warning badge |
| `--color-border` | Bordes, divisores | Texto | Input border, hr |

---

## Colores Extendidos

Refinamientos para casos específicos (derivados de semánticos):

| Token | Propósito | Dónde Usarlo |
|-------|-----------|-------------|
| `--color-bg-secondary` | Fondo alternativo (striping) | Table rows alternos, lista items |
| `--color-action-hover` | Hover del color de acción | Botón hover, link hover |
| `--color-action-soft` | Fondo soft de acción (baja emphasis) | Secondary button background |
| `--color-action-disabled` | Acción deshabilitada | Botón disabled state |
| `--color-text-inverse` | Texto sobre fondo oscuro | Modal/overlay |
| `--color-border-strong` | Borde enfatizado | Inputs focused, dividers importantes |

---

## Mapeo a Componentes

### Componentes Atómicos

| Componente | Tokens Usados | Notas |
|-----------|---------------|-------|
| **Button (Primary)** | `--color-action`, `--color-on-action`, `--color-action-hover` | Cambio de color según tema/marca automático |
| **Button (Secondary)** | `--color-action-soft`, `--color-action`, `--color-border` | Borde + fondo light |
| **Input** | `--color-surface`, `--color-border`, `--color-action` (focus), `--color-danger` (error) | Borde se oscurece en focus |
| **Link** | `--color-action`, `--color-action-hover` | Subrayado en hover (accesibilidad) |
| **Badge** | `--color-action-soft`, `--color-action` | Fondo light + texto action |
| **Alert** | `--color-danger`, `--color-warning`, `--color-success` (siempre con icon) | Fondo + border + text |
| **Toast** | `--color-success`, `--color-warning`, `--color-danger` | Overlay sobre `--color-bg` |

### Componentes Complejos

| Patrón | Tokens Usados | Notas |
|--------|---------------|-------|
| **Modal** | `--color-bg-secondary` (backdrop), `--color-bg` (panel) | Contraste alto en fondo |
| **Table** | `--color-bg`, `--color-bg-secondary` (striping), `--color-border` | Alt rows = `secondary` |
| **Navbar** | `--color-surface`, `--color-text`, `--color-action` | Barra fija con fondo |
| **Card** | `--color-surface`, `--color-border`, `--color-text` | Sutil elevation |

---

## Modo Oscuro/Claro

Los colores cambian automáticamente con `data-theme`:

```html
<!-- Light (default) -->
<html data-theme="light" data-brand="promptea">

<!-- Dark -->
<html data-theme="dark" data-brand="promptea">
```

**Ejemplo:**
```css
/* Primitivos: sin cambio */
:root {
  --color-action: var(--green-600);  /* siempre verde */
}

/* Light theme (default) */
:root {
  --color-bg: #FFFFFF;
  --color-text: #111827;
}

/* Dark theme */
[data-theme="dark"] {
  --color-bg: #0F172A;
  --color-text: #F1F5F9;
}
```

---

## Accesibilidad WCAG

### Contrastes Mínimos (AA)

| Combinación | Ratio | Status |
|-------------|-------|--------|
| `text` sobre `bg` | 7:1+ | ✅ AAA |
| `action` sobre `bg` | 4.5:1+ | ✅ AA |
| `muted` sobre `bg` | 4.5:1+ | ✅ AA |
| `danger` sobre `bg` | 4.5:1+ | ✅ AA (siempre + icon) |

### Reglas

1. **Nunca uses color solo para significado:**
   ```html
   <!-- ❌ MAL -->
   <p style="color: var(--color-danger)">Error</p>

   <!-- ✅ BIEN -->
   <p role="alert" style="color: var(--color-danger)">
     <span aria-hidden="true">⚠️</span> Error: Campo requerido
   </p>
   ```

2. **Siempre incluye icono + palabra:**
   - Errores: 🚫 + "Error"
   - Éxito: ✅ + "Éxito"
   - Advertencia: ⚠️ + "Advertencia"

3. **Focus ring siempre visible:**
   ```css
   button:focus-visible {
     outline: 2px solid var(--color-focus);
     outline-offset: 2px;
   }
   ```

---

## Uso Correcto

### ✅ CORRECTO

```html
<!-- Button Primary -->
<button style="background: var(--color-action); color: var(--color-on-action)">
  Guardar
</button>

<!-- Link with proper contrast -->
<a href="#" style="color: var(--color-action)">Más información</a>

<!-- Error con contexto -->
<div role="alert">
  <span style="color: var(--color-danger)">🚫 Validación:</span>
  <p>El email es inválido</p>
</div>

<!-- Input disabled -->
<input disabled style="background: var(--color-surface); color: var(--color-muted)">
```

### ❌ INCORRECTO

```html
<!-- ❌ Color solo (sin icono/palabra) -->
<p style="color: var(--color-danger)">Falla</p>

<!-- ❌ Baja accesibilidad -->
<span style="color: #8B8B8B; background: white">Texto poco visible</span>

<!-- ❌ Hard-coded hex en lugar de tokens -->
<button style="background: #5CD314">Guardar</button>

<!-- ❌ Colores sin considerar tema oscuro -->
<div style="background: white">Siempre blanco, mal en dark mode</div>
```

---

## Valores por Marca × Tema

Las 3 marcas (Promptea, Nova, Ocean) × 2 temas (Light, Dark) = **6 variaciones**.

Ejemplo: **Promptea Light** vs **Ocean Dark**

| Propiedad | Promptea (Light) | Ocean (Dark) |
|-----------|-----------------|------------|
| `--color-action` | `#5CD314` (verde) | `#0284C7` (azul) |
| `--color-bg` | `#FFFFFF` | `#0F172A` |
| `--color-text` | `#111827` | `#F1F5F9` |

**Cambio en tiempo real:**
```javascript
// JavaScript
document.documentElement.dataset.brand = "ocean";
document.documentElement.dataset.theme = "dark";
// → Todos los var(--color-*) actualizan automáticamente
```

---

## Exportación

Los colores se exportan en múltiples formatos:

- **CSS:** `01-tokens/tokens.css` ✅
- **JSON:** `01-tokens/tokens.json` ✅
- **SCSS:** `01-tokens/tokens.scss` ✅
- **DTCG:** `01-tokens/tokens.dtcg.json` ✅

Regenerar con:
```bash
npm run export-tokens
```

---

## Referencias

- 📄 **Manifest:** `05-agentes/component-manifest.json` (tokens.semantic section)
- 🎨 **CSS Activos:** `01-tokens/tokens.css`
- 📊 **Índice:** `index.html` → Sección "Tokens" (tabla interactiva)
- ♿ **Accesibilidad:** WCAG 2.2 AA mínimo en todas las combinaciones
