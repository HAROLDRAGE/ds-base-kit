# Sistema de Tipografía — Design.MD White Label v2.0.0

## Escala de Tipografía

### Font Families

#### Base (San-serif)
```
Font: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', etc.
Uso: Toda la interfaz, cuerpo de texto, headings
```

#### Monospace
```
Font: 'Fira Code', 'Courier New', 'Courier'
Uso: Código, snippets técnicos, números secuenciales
```

---

## Pesos de Fuente

| Variable | Valor | Uso |
|----------|-------|-----|
| `--typography-font-weight-light` | 300 | Textos menos enfatizados |
| `--typography-font-weight-regular` | 400 | Cuerpo estándar |
| `--typography-font-weight-medium` | 500 | Énfasis moderado, labels |
| `--typography-font-weight-semibold` | 600 | Énfasis fuerte, botones |
| `--typography-font-weight-bold` | 700 | Muy enfatizado, headings |
| `--typography-font-weight-extrabold` | 800 | Máximo énfasis, títulos principales |

---

## Tamaños de Fuente

| Token | Valor | Componentes |
|-------|-------|-------------|
| `--typography-size-xs` | 0.75rem (12px) | Badges, ayudas, notas pequeñas |
| `--typography-size-sm` | 0.875rem (14px) | Labels, pequeños textos |
| `--typography-size-base` | 1rem (16px) | Cuerpo estándar de texto |
| `--typography-size-lg` | 1.125rem (18px) | Subtítulos, introducción |
| `--typography-size-xl` | 1.25rem (20px) | Heading grande |
| `--typography-size-2xl` | 1.5rem (24px) | Heading mayor |
| `--typography-size-3xl` | 1.875rem (30px) | h3 |
| `--typography-size-4xl` | 2.25rem (36px) | h2 |
| `--typography-size-5xl` | 3rem (48px) | h1 |

---

## Headings Preestablecidos (h1-h6)

```css
/* h1: Display — Muy grande */
font-size: 3rem (48px);
font-weight: 800;
line-height: 1.2;
letter-spacing: -0.02em;

/* h2: Grande — Títulos principales */
font-size: 2.25rem (36px);
font-weight: 700;
line-height: 1.3;
letter-spacing: -0.01em;

/* h3: Mediano — Subtítulos */
font-size: 1.875rem (30px);
font-weight: 700;
line-height: 1.4;
letter-spacing: 0;

/* h4: Base elevado */
font-size: 1.5rem (24px);
font-weight: 600;
line-height: 1.4;

/* h5: Pequeño */
font-size: 1.25rem (20px);
font-weight: 600;
line-height: 1.5;

/* h6: Minimal */
font-size: 1.125rem (18px);
font-weight: 500;
line-height: 1.5;
text-transform: uppercase;
letter-spacing: 0.05em;
```

---

## Presets de Cuerpo de Texto

### Body Large
```
Size: 1.125rem (18px)
Weight: 400
Line Height: 1.75
Uso: Párrafos enfatizados, introducciones
```

### Body Base
```
Size: 1rem (16px)
Weight: 400
Line Height: 1.5
Uso: Cuerpo estándar de texto
```

### Body Small
```
Size: 0.875rem (14px)
Weight: 400
Line Height: 1.5
Uso: Textos secundarios, descripciones
```

### Body XS
```
Size: 0.75rem (12px)
Weight: 400
Line Height: 1.5
Uso: Notas, ayudas, meta-información
```

---

## Line Heights (Interlineado)

| Token | Valor | Uso |
|-------|-------|-----|
| `--typography-line-height-tight` | 1.2 | Headings compactos, display |
| `--typography-line-height-normal` | 1.5 | Cuerpo estándar |
| `--typography-line-height-relaxed` | 1.75 | Párrafos largos, mejor legibilidad |
| `--typography-line-height-loose` | 2 | Muy espaciado, poesía, accesibilidad |

---

## Letter Spacing (Espaciado entre letras)

| Token | Valor | Uso |
|-------|-------|-----|
| `--typography-letter-spacing-tight` | -0.02em | Display headings, textos densos |
| `--typography-letter-spacing-normal` | 0 | Estándar |
| `--typography-letter-spacing-wide` | 0.05em | Labels, uppercase |
| `--typography-letter-spacing-wider` | 0.1em | Mayúsculas enfatizado, títulos |

---

## Espaciado Scale

| Token | Valor (px) | Valor (rem) | Uso |
|-------|-----------|-----------|-----|
| `--space-0` | 0px | 0 | Sin espaciado |
| `--space-1` | 4px | 0.25rem | Separación mínima icono-texto |
| `--space-2` | 8px | 0.5rem | Interno compacto |
| `--space-3` | 12px | 0.75rem | Interno de controles |
| `--space-4` | 16px | 1rem | Padding estándar |
| `--space-5` | 20px | 1.25rem | Espaciado medio |
| `--space-6` | 24px | 1.5rem | Entre bloques |
| `--space-8` | 32px | 2rem | Entre secciones |
| `--space-10` | 40px | 2.5rem | Separación grande |
| `--space-12` | 48px | 3rem | Separación muy grande |
| `--space-16` | 64px | 4rem | Separación entre secciones principales |

---

## Border Radius

| Token | Valor | Uso |
|-------|-------|-----|
| `--radius-none` | 0 | Sin redondeo |
| `--radius-sm` | 4px | Badges, inputs pequeños |
| `--radius-md` | 8px | Botones, inputs |
| `--radius-lg` | 12px | Tarjetas, modales |
| `--radius-xl` | 16px | Paneles grandes |
| `--radius-2xl` | 20px | Componentes prominentes |
| `--radius-pill` | 999px | Pills, avatares, botones redondos |

---

## Border Widths

| Token | Valor | Uso |
|-------|-------|-----|
| `--border-width-hairline` | 0.5px | Divisores sutiles |
| `--border-width-thin` | 1px | Bordes estándar |
| `--border-width-base` | 2px | Bordes destacados, focus |
| `--border-width-thick` | 4px | Énfasis en bordes, separadores |

---

## Shadows (Elevación)

```css
--shadow-sm:   0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md:   0 4px 6px -1px rgb(0 0 0 / 0.1), 
               0 2px 4px -2px rgb(0 0 0 / 0.1);
--shadow-lg:   0 10px 15px -3px rgb(0 0 0 / 0.1), 
               0 4px 6px -4px rgb(0 0 0 / 0.1);
--shadow-xl:   0 20px 25px -5px rgb(0 0 0 / 0.1), 
               0 8px 10px -6px rgb(0 0 0 / 0.1);
--shadow-2xl:  0 25px 50px -12px rgb(0 0 0 / 0.25);
```

**Uso:**
- `shadow-sm`: Elevación mínima (hover leve)
- `shadow-md`: Elevación media (tarjetas, dropdowns)
- `shadow-lg`: Elevación grande (modales)
- `shadow-xl`: Elevación muy grande (popovers)
- `shadow-2xl`: Elevación máxima (full-screen overlays)

---

## Motion & Transitions

### Duraciones

| Token | Valor | Uso |
|-------|-------|-----|
| `--motion-fast` | 120ms | Hover, focus, cambios rápidos |
| `--motion-base` | 240ms | Aparición, expansión, estándar |
| `--motion-slow` | 400ms | Transiciones complejas, animaciones |

### Easing Functions

```css
--motion-easing-linear:    linear;                          /* Constante */
--motion-easing-in:        cubic-bezier(0.4, 0, 1, 1);      /* Suave entrada */
--motion-easing-out:       cubic-bezier(0, 0, 0.2, 1);      /* Suave salida */
--motion-easing-in-out:    cubic-bezier(0.4, 0, 0.2, 1);    /* Entrada y salida */
```

---

## Media & Images

### Aspect Ratios

```css
--media-aspect-square:     1 / 1;        /* Cuadrado */
--media-aspect-video:      16 / 9;       /* Panorámico */
--media-aspect-3-2:        3 / 2;        /* Fotografía estándar */
```

### Object Fit

```css
--media-object-fit-cover:   cover;       /* Rellenar sin distorsión */
--media-object-fit-contain: contain;     /* Ajustar dentro */
```

---

## Ejemplos de Uso

### Heading h1
```html
<h1>Título Principal</h1>
<!-- Automáticamente aplica: 3rem, 800, 1.2 line-height, -0.02em spacing -->
```

### Párrafo con clase body-lg
```html
<p class="body-lg">Texto más grande para introducciones</p>
```

### Botón con padding estándar
```html
<button class="btn px-4 py-2">Enviar</button>
<!-- px-4 = padding-left: 16px; padding-right: 16px -->
```

### Tarjeta con sombra y redondeo
```html
<div class="card rounded-lg shadow-md p-6">
  <!-- Aplica: border-radius 12px, sombra media, padding 24px -->
</div>
```

---

## Tokens de Color Semánticos

### Colores Base (Marca-independiente en `:root`)
- `--color-bg`: Fondo base de página
- `--color-surface`: Tarjetas, paneles, inputs
- `--color-text`: Texto principal
- `--color-muted`: Texto secundario
- `--color-action`: Acciones, enlaces, foco
- `--color-border`: Bordes y divisores
- `--color-danger`: Errores (siempre + icono + palabra)
- `--color-success`: Confirmaciones (siempre + icono + palabra)

### Extensiones por Marca
- `--color-bg-secondary`: Fondo alternativo
- `--color-surface-subtle`: Fondo muy sutil
- `--color-action-hover`: Estado hover del action
- `--color-action-soft`: Fondo suave del action
- `--color-warning`: Advertencias
- `--color-text-secondary`: Texto de apoyo

---

## Accesibilidad

- **Contrastes**: Mínimo 4.5:1 para texto, 3:1 para UI
- **Line height**: Mínimo 1.5 para legibilidad
- **Motion**: Respetar `prefers-reduced-motion`
- **Estado visual**: Nunca solo con color (siempre + icono + palabra)
- **Focus visible**: Anillo de foco obligatorio (2px, color action)

---

## Versionado

- **Versión**: 2.0.0
- **Última actualización**: 2026-07-09
- **Cambios**: Agregados tokens de tipografía, línea de altura, espaciado ampliado, bordes, sombras, motion, media
