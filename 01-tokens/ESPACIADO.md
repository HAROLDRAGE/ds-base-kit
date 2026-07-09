# Sistema de Espaciado

> **Fuente única de verdad:** `01-tokens/tokens.css` + `component-manifest.json`

## Tabla de Contenidos
1. [Escala de Espaciado](#escala-de-espaciado)
2. [Cómo Usar](#cómo-usar)
3. [Tokens Disponibles](#tokens-disponibles)
4. [Mapeo a Componentes](#mapeo-a-componentes)
5. [Spacing Patterns](#spacing-patterns)

---

## Escala de Espaciado

Escala base: **4px** (múltiplos aritméticos).

| Token | Valor | Uso | Ejemplo |
|-------|-------|-----|---------|
| `--space-0` | 0px | Quitar espacios | No padding |
| `--space-1` | 4px | Micro spacing | Gap entre icono + texto |
| `--space-2` | 8px | Tight spacing | Padding en badge |
| `--space-3` | 12px | Compact spacing | Padding en button |
| `--space-4` | 16px | Base spacing | Padding estándar |
| `--space-5` | 20px | Comfortable spacing | Margin entre elementos |
| `--space-6` | 24px | Generous spacing | Padding en card, gap en grid |
| `--space-8` | 32px | Section spacing | Margin entre secciones |
| `--space-10` | 40px | Large spacing | Margin entre bloques |
| `--space-12` | 48px | Extra large | Margin top de headings |
| `--space-16` | 64px | Huge spacing | Section divider |

---

## Cómo Usar

### En CSS

```css
/* Padding */
.card {
  padding: var(--space-4);  /* 16px en todos lados */
}

/* Margin */
.section {
  margin-bottom: var(--space-8);  /* 32px abajo */
  margin-top: var(--space-12);    /* 48px arriba */
}

/* Gap (Flexbox/Grid) */
.button-group {
  display: flex;
  gap: var(--space-3);  /* 12px entre botones */
}

/* Combinaciones */
.button {
  padding: var(--space-2) var(--space-4);  /* 8px arriba/abajo, 16px lados */
}
```

### En HTML (inline con tokens)

```html
<!-- ✅ Usar tokens como inline styles (cuando no hay clase CSS) -->
<div style="padding: var(--space-4); margin-bottom: var(--space-6)">
  Contenido
</div>

<!-- ❌ Evitar: hard-coded values -->
<div style="padding: 16px; margin-bottom: 24px">
  Contenido
</div>
```

---

## Tokens Disponibles

### Espacios Primitivos (`:root`)

```css
:root {
  --space-0: 0px;       /* 0 */
  --space-1: 4px;       /* 1× base */
  --space-2: 8px;       /* 2× base */
  --space-3: 12px;      /* 3× base */
  --space-4: 16px;      /* 4× base */
  --space-5: 20px;      /* 5× base */
  --space-6: 24px;      /* 6× base */
  --space-8: 32px;      /* 8× base */
  --space-10: 40px;     /* 10× base */
  --space-12: 48px;     /* 12× base */
  --space-16: 64px;     /* 16× base */
}
```

### Propiedades Derivadas (específicas de componentes)

```css
/* Presets para componentes comunes */
--spacing-button-padding: var(--space-2) var(--space-4);        /* 8px, 16px */
--spacing-input-padding: var(--space-2) var(--space-3);         /* 8px, 12px */
--spacing-card-padding: var(--space-4);                          /* 16px */
--spacing-modal-padding: var(--space-6);                         /* 24px */
--spacing-section-gap: var(--space-6);                           /* 24px */
```

> **Nota:** Los presets no reemplazan los tokens básicos, son referencias.

---

## Mapeo a Componentes

### Componentes Atómicos

| Componente | Padding | Margin | Gap |
|-----------|---------|--------|-----|
| **Button** | `space-2` (v) + `space-4` (h) | `space-3` (margin-right) | N/A |
| **Badge** | `space-2` (v) + `space-3` (h) | `space-2` (margin-right) | N/A |
| **Input** | `space-2` (v) + `space-3` (h) | `space-4` (margin-bottom) | N/A |
| **Link** | `space-0` | `space-0` | N/A |
| **Tooltip** | `space-2` (v) + `space-3` (h) | `space-2` (offset) | N/A |
| **Alert** | `space-4` | `space-4` (margin-bottom) | `space-2` (gap icon-text) |

### Componentes Complejos

| Componente | Padding Interior | Margin Exterior | Gap Interno |
|-----------|-----------------|-----------------|------------|
| **Card** | `space-4` | `space-4` | `space-3` (entre elementos) |
| **Modal** | `space-6` | `space-0` | `space-4` (entre secciones) |
| **Navbar** | `space-4` | `space-0` | `space-4` (entre items) |
| **Table** | `space-3` (celdas) | `space-0` | `space-0` (sin gap, usa borders) |
| **Dropdown** | `space-3` (item) | `space-0` | `space-2` (entre items) |
| **Accordion** | `space-4` (panel) | `space-4` (entre paneles) | `space-3` (header gap) |

---

## Spacing Patterns

### Pattern 1: Padding Uniforme

```css
.card {
  padding: var(--space-4);  /* 16px en todos los lados */
}
```

**Uso:** Cards, modales, paneles simétricos.

### Pattern 2: Padding Asimétrico (Vertical ≠ Horizontal)

```css
.button {
  padding: var(--space-2) var(--space-4);  /* 8px v, 16px h */
}

/* O más explícito */
.button {
  padding-top: var(--space-2);
  padding-right: var(--space-4);
  padding-bottom: var(--space-2);
  padding-left: var(--space-4);
}
```

**Uso:** Botones, inputs, elementos comprimidos vertically.

### Pattern 3: Gap en Flex/Grid

```css
.button-group {
  display: flex;
  gap: var(--space-3);  /* Espaciado consistente */
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-6);  /* 24px entre cards */
}
```

**Uso:** Listas, grillas, grupos de elementos.

### Pattern 4: Margin para Separación de Bloques

```css
/* Entre secciones grandes */
section {
  margin-bottom: var(--space-12);  /* 48px separación */
}

/* Dentro de grupos */
.form-group {
  margin-bottom: var(--space-4);   /* 16px separación */
}

h2 + p {
  margin-top: var(--space-3);      /* 12px bajo heading */
}
```

**Uso:** Separación vertical entre bloques, jerarquía visual.

### Pattern 5: Composición de Espacios

```css
/* Dentro de un item de lista */
.list-item {
  padding: var(--space-4);
  display: flex;
  gap: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.list-item:not(:last-child) {
  margin-bottom: var(--space-2);  /* Compresión si hay border */
}
```

---

## Responsive Adjustments

Aunque los tokens NO cambian por breakpoint, **el uso sí puede variar:**

```css
/* Mobile: tight spacing */
@media (max-width: 640px) {
  .card {
    padding: var(--space-3);  /* 12px en móvil */
  }
  .card-grid {
    gap: var(--space-3);      /* 12px en móvil */
  }
}

/* Desktop: generous spacing */
@media (min-width: 1024px) {
  .card {
    padding: var(--space-6);  /* 24px en desktop */
  }
  .card-grid {
    gap: var(--space-6);      /* 24px en desktop */
  }
}
```

---

## Checklist de Uso Correcto

- ✅ Usa `var(--space-X)` siempre, nunca hard-code `16px`
- ✅ Mantén múltiplos de 4 (o usa los tokens definidos)
- ✅ Combina `padding` + `gap` en Flexbox/Grid
- ✅ Usa `margin` para separación entre **bloques distintos**
- ✅ Usa `padding` para espaciado **dentro de un componente**
- ✅ Escala responsive: cambiar `space-4` → `space-3` en mobile
- ✅ Documenta decisiones de spacing en patrones

- ❌ No mezcles padding + margin sin razón clara
- ❌ No uses `space-0` a menos que sea intencional
- ❌ No hard-codes valores como `16px`, usa tokens
- ❌ No olvides responsive: mismo spacing en móvil = demasiado tight

---

## Exportación

El sistema de espaciado se exporta en múltiples formatos:

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

- 📄 **Manifest:** `05-agentes/component-manifest.json` (tokens.semantic.space)
- 🎨 **CSS Activos:** `01-tokens/tokens.css`
- 📊 **Índice:** `index.html` → Sección "Tokens" (tabla interactiva)
- ♿ **Accesibilidad:** Mínimo `space-3` (12px) para touch targets (mobile)
