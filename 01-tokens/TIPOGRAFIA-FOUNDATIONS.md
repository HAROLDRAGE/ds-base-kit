# 📝 Tipografía Foundations — Sistema de Fuentes Base

**Versión:** 2.2.0  
**Actualizado:** 2026-07-09

---

## 🏛️ Estructura

```
FOUNDATIONS (agnósticos de marca)
├─ Familias de fuente (font-stack)
├─ Pesos (weights: 300-800)
├─ Tamaños (escala modulada)
├─ Line heights (espaciado vertical)
├─ Letter spacing (espaciado horizontal)
└─ Line clamp (truncado)

    ↓

SEMÁNTICOS (composiciones con propósito)
├─ typography-heading-h1 (size + weight + line-height)
├─ typography-heading-h2
├─ typography-body-base
└─ typography-label

    ↓

COMPONENTES
├─ <h1>, <h2>, <p>, <label>, <button>
└─ Presets predefinidos
```

---

## 🔤 Familias de Fuente

### Foundation: Font Family Base

```css
--foundation-font-family-base: 
  -apple-system,           /* macOS */
  BlinkMacSystemFont,      /* macOS Chrome */
  'Segoe UI',              /* Windows */
  'Roboto',                /* Android */
  'Oxygen',                /* Linux */
  'Ubuntu',                /* Linux */
  'Cantarell',             /* GNOME */
  'Fira Sans',             /* Firefox */
  'Droid Sans',            /* Android */
  'Helvetica Neue',        /* Fallback */
  sans-serif;              /* Final fallback */
```

**Propósito:** Sistema font-stack que se ve bien en todas las plataformas sin necesidad de @import de Google Fonts. Garantiza legibilidad y humanismo.

**Usa en:**
- ✅ Cuerpo de texto
- ✅ Headings
- ✅ Labels, placeholders
- ✅ Botones, inputs

### Foundation: Font Family Mono

```css
--foundation-font-family-mono:
  'Fira Code',              /* Hermosa, open source */
  'SF Mono',                /* macOS */
  'Courier New',            /* Fallback */
  'Courier',                /* Windows */
  monospace;                /* Final fallback */
```

**Propósito:** Tipografía monoespaciada para código, snippets, valores técnicos.

**Usa en:**
- ✅ `<code>` inline
- ✅ `<pre>` bloques
- ✅ Componentes técnicos (terminal, editor)
- ✅ Valores numéricos que necesitan alineación

---

## ⚖️ Pesos (Font Weights)

### Escala Universal

```
Level        Weight  CSS Value   Uso Típico
────────────────────────────────────────────────────────
Light        300     font-weight: 300  Texto desenfatizado
Regular      400     font-weight: 400  Cuerpo estándar
Medium       500     font-weight: 500  Énfasis moderado
Semibold     600     font-weight: 600  Énfasis fuerte
Bold         700     font-weight: 700  Muy enfatizado
Extrabold    800     font-weight: 800  Máximo énfasis
```

### Combinaciones Recomendadas

```
Heading H1 + Body
├─ H1: Extrabold (800) + Large (3rem)
└─ Body: Regular (400) + Base (1rem)
└─ Contraste visual: 8x tamaño + 2x weight

Label + Input
├─ Label: Medium (500) + Small (0.875rem)
└─ Input: Regular (400) + Base (1rem)
└─ Contraste visual: Jerarquía clara sin abrupto

Button (importante)
├─ Semibold (600)
└─ Garantiza clickability visual

Quote (menos importante)
├─ Light (300) o Regular (400)
└─ Crea contraste de jerarquía
```

---

## 📏 Tamaños (Font Sizes)

### Escala Modulada (base 1rem = 16px)

```
Level      Tamaño     Px     Escala    Uso Típico
──────────────────────────────────────────────────────
xs         0.75rem    12px   ÷ 1.33    Badges, hints
sm         0.875rem   14px   ÷ 1.14    Labels, small
base       1rem       16px   base      Cuerpo estándar
lg         1.125rem   18px   × 1.13    Subtítulos
xl         1.25rem    20px   × 1.25    Headings medianos
2xl        1.5rem     24px   × 1.5     Headings grandes
3xl        1.875rem   30px   × 1.88    H3
4xl        2.25rem    36px   × 2.25    H2
5xl        3rem       48px   × 3       H1
```

**Relación:** Cada nivel es ~12% más grande que el anterior (ratio ≈ 1.12).

### Uso por Componente

| Componente | Tamaño | Peso | Uso |
|------------|--------|------|-----|
| **H1** | 5xl (3rem) | Extrabold (800) | Título página |
| **H2** | 4xl (2.25rem) | Bold (700) | Sección principal |
| **H3** | 3xl (1.875rem) | Bold (700) | Subsección |
| **H4** | 2xl (1.5rem) | Semibold (600) | Subsección pequeña |
| **Body** | base (1rem) | Regular (400) | Párrafo estándar |
| **Small** | sm (0.875rem) | Regular (400) | Texto pequeño |
| **Label** | sm (0.875rem) | Medium (500) | Labels de input |
| **Badge** | xs (0.75rem) | Medium (500) | Etiquetas |
| **Button** | base (1rem) | Semibold (600) | Texto de botón |
| **Hint** | xs (0.75rem) | Regular (400) | Texto de ayuda |

---

## 📐 Line Heights (Espaciado Vertical)

### Escala

```
Level       Value   Uso Típico
─────────────────────────────────────
tight       1.2     Headings compactos
normal      1.5     Cuerpo estándar
relaxed     1.75    Párrafos largos
loose       2.0     Texto muy espaciado
```

### Cálculo

```
Line Height = text-size × line-height-value

Ejemplo:
H1 (3rem) × 1.2 = 3.6rem espaciado entre líneas
Body (1rem) × 1.5 = 1.5rem espaciado entre líneas
```

### Por Tipo de Contenido

| Contenido | Line Height | Por qué |
|-----------|-------------|---------|
| Headings (H1-H3) | 1.2 - 1.3 | Compacto, visual |
| Subtítulos | 1.4 | Más abierto |
| Body (párrafos) | 1.5 - 1.6 | Legible, estándar web |
| Párrafos muy largos | 1.75 | Menos cansador para leer |
| Poetry/Art | 2.0 | Muy espaciado |

---

## 🎯 Letter Spacing (Espaciado Horizontal)

### Escala

```
Level     Value      Uso Típico
─────────────────────────────────────
tight     -0.02em    Headings impactantes
normal    0em        Estándar
wide      0.05em     Labels, small caps
wider     0.1em      Énfasis, títulos
```

### Aplicación

```
Headings (impactante)
  letter-spacing: -0.02em    (más apretado)

Body (legible)
  letter-spacing: 0em        (normal)

Labels (legibilidad)
  letter-spacing: 0.05em     (ligeramente abierto)

Small Caps / Énfasis
  letter-spacing: 0.1em      (muy abierto)
```

---

## 🎨 Presets Semánticos (Composiciones)

### Headings

```css
--typography-heading-h1: 
  font-size: var(--foundation-typography-size-5xl);     /* 3rem */
  font-weight: var(--foundation-typography-weight-extrabold); /* 800 */
  line-height: var(--foundation-typography-line-height-tight); /* 1.2 */
  letter-spacing: -0.02em;

--typography-heading-h2:
  font-size: var(--foundation-typography-size-4xl);     /* 2.25rem */
  font-weight: var(--foundation-typography-weight-bold); /* 700 */
  line-height: 1.3;
  letter-spacing: -0.01em;

--typography-heading-h3:
  font-size: var(--foundation-typography-size-3xl);     /* 1.875rem */
  font-weight: var(--foundation-typography-weight-bold); /* 700 */
  line-height: 1.4;
  letter-spacing: 0;

--typography-heading-h4:
  font-size: var(--foundation-typography-size-2xl);     /* 1.5rem */
  font-weight: var(--foundation-typography-weight-semibold); /* 600 */
  line-height: 1.4;
```

### Body Presets

```css
--typography-body-lg:
  font-size: var(--foundation-typography-size-lg);      /* 1.125rem */
  font-weight: var(--foundation-typography-weight-regular); /* 400 */
  line-height: var(--foundation-typography-line-height-relaxed); /* 1.75 */

--typography-body-base:
  font-size: var(--foundation-typography-size-base);    /* 1rem */
  font-weight: var(--foundation-typography-weight-regular); /* 400 */
  line-height: var(--foundation-typography-line-height-normal); /* 1.5 */

--typography-body-sm:
  font-size: var(--foundation-typography-size-sm);      /* 0.875rem */
  font-weight: var(--foundation-typography-weight-regular); /* 400 */
  line-height: var(--foundation-typography-line-height-normal); /* 1.5 */
```

### Label Preset

```css
--typography-label:
  font-size: var(--foundation-typography-size-sm);      /* 0.875rem */
  font-weight: var(--foundation-typography-weight-medium); /* 500 */
  line-height: var(--foundation-typography-line-height-normal); /* 1.5 */
  letter-spacing: 0.05em;
  text-transform: uppercase;  /* opcional */
```

### Code Preset

```css
--typography-code:
  font-family: var(--foundation-font-family-mono);
  font-size: 0.875rem;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0;
```

---

## 🧮 Uso en Componentes

### HTML Semántico + CSS

```html
<h1>Título Principal</h1>
<p>Párrafo de cuerpo.</p>
<label for="email">Email</label>
<code>const x = 42;</code>
```

```css
h1 {
  font-size: var(--typography-size-5xl);
  font-weight: var(--typography-weight-extrabold);
  line-height: var(--typography-line-height-tight);
}

p {
  font: var(--typography-body-base);
}

label {
  font: var(--typography-label);
}

code {
  font-family: var(--foundation-font-family-mono);
  font-size: 0.875rem;
}
```

### Component: Button

```html
<button class="button button--primary">
  Click me
</button>
```

```css
.button {
  font-family: var(--foundation-font-family-base);
  font-size: var(--typography-size-base);        /* 1rem */
  font-weight: var(--typography-weight-semibold); /* 600 */
  line-height: var(--typography-line-height-normal); /* 1.5 */
}
```

### Component: Card Title

```html
<div class="card">
  <h2 class="card__title">Tarjeta</h2>
  <p class="card__description">Descripción...</p>
</div>
```

```css
.card__title {
  font-size: var(--typography-size-xl);          /* 1.25rem */
  font-weight: var(--typography-weight-semibold); /* 600 */
  line-height: var(--typography-line-height-normal); /* 1.5 */
}

.card__description {
  font: var(--typography-body-base);
  color: var(--color-muted);
}
```

---

## 🔄 Responsividad

### Escala Adaptativa (Recomendado)

```css
/* Mobile */
h1 {
  font-size: 1.875rem;  /* 3xl en lugar de 5xl */
  line-height: 1.3;
}

body {
  font-size: 1rem;  /* No cambiar */
}

/* Desktop (media query) */
@media (min-width: 1024px) {
  h1 {
    font-size: 3rem;  /* 5xl */
    line-height: 1.2;
  }
}
```

**Principio:** NO cambiar `font-size: base` entre breakpoints. Cambiar solo headings.

---

## ✨ Mejores Prácticas

### ✅ CORRECTO
```html
<h1>Título</h1>
<h2>Subtítulo</h2>
<p>Párrafo</p>
```

```css
h1 { font: var(--typography-heading-h1); }
h2 { font: var(--typography-heading-h2); }
p  { font: var(--typography-body-base); }
```

### ❌ INCORRECTO
```html
<div class="h1">Título con div</div>
<span class="heading">Pero es importante</span>
```

```css
/* Violate semantic HTML */
/* No usar font-size hardcodeado */
.h1 { font-size: 48px; }
```

---

## 📊 Matriz de Correspondencia

| Semántico | Size | Weight | Line Height | Uso |
|-----------|------|--------|-------------|-----|
| heading-h1 | 5xl | 800 | 1.2 | `<h1>` |
| heading-h2 | 4xl | 700 | 1.3 | `<h2>` |
| heading-h3 | 3xl | 700 | 1.4 | `<h3>` |
| body-lg | lg | 400 | 1.75 | Large intro |
| body-base | base | 400 | 1.5 | Párrafos |
| body-sm | sm | 400 | 1.5 | Small text |
| label | sm | 500 | 1.5 | Labels |
| code | sm | 400 | 1.5 | `<code>` |

---

## 🚀 Siguientes Pasos

- [ ] Crear fuente variable si es posible (mejor performance)
- [ ] Validar contraste de color con tamaños pequeños
- [ ] Crear guidelines para headings en mobile
- [ ] Documentar font-size cambios por breakpoint
