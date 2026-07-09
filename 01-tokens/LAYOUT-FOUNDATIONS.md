# 📐 Layout Foundations — Responsive y Estructura

**Versión:** 2.2.0  | **Actualizado:** 2026-07-09

---

## 🏛️ Estructura

```
FOUNDATIONS
├─ Breakpoints (responsive)
│  ├─ xs (320px)
│  ├─ sm (480px)
│  ├─ md (768px)
│  ├─ lg (1024px)
│  ├─ xl (1280px)
│  └─ 2xl (1536px)
│
├─ Grid (columnas)
├─ Touch targets (WCAG)
└─ Safe areas (notch devices)

    ↓

SEMÁNTICOS
├─ layout-container-max-width
├─ layout-touch-target-mobile
└─ layout-breakpoint-md

    ↓

COMPONENTES
├─ Container, Grid, Flexbox
```

---

## 📱 Breakpoints

### Escala Standard

| Token | Valor | Device | Cols |
|-------|-------|--------|------|
| `--layout-breakpoint-xs` | 320px | Mobile pequeño | 1 |
| `--layout-breakpoint-sm` | 480px | Mobile grande | 1-2 |
| `--layout-breakpoint-md` | 768px | Tablet | 2-3 |
| `--layout-breakpoint-lg` | 1024px | Desktop pequeño | 3-4 |
| `--layout-breakpoint-xl` | 1280px | Desktop | 3-4 |
| `--layout-breakpoint-2xl` | 1536px | Desktop grande | 4-6 |

### Devices

```
xs   320px   → iPhone SE (2020), old phones
sm   480px   → Modern smartphones (landscape)
md   768px   → iPad mini, tablets
lg   1024px  → iPad Pro, desktop pequeño
xl   1280px  → Desktop estándar
2xl  1536px  → Desktop grande, 4K displays
```

### Mobile-First Approach

```css
/* DEFAULT: Mobile (xs) */
.container {
  width: 100%;
  padding: var(--space-4);
}

/* Tablet (md) */
@media (min-width: 768px) {
  .container {
    padding: var(--space-6);
  }
}

/* Desktop (lg) */
@media (min-width: 1024px) {
  .container {
    max-width: var(--layout-container-max-width);
    margin: 0 auto;
  }
}
```

---

## 🎯 Container & Grid

### Max Width

```css
--layout-container-max-width: 1280px;
```

```html
<div class="container">
  <!-- Contenido con máximo 1280px ancho -->
</div>
```

```css
.container {
  max-width: var(--layout-container-max-width);
  margin-left: auto;
  margin-right: auto;
  padding: var(--layout-container-padding);
}
```

### Grid Columns por Breakpoint

| Breakpoint | Columnas | Uso |
|-----------|----------|-----|
| xs | 1 | Stack vertical |
| sm | 1-2 | A veces lado a lado |
| md | 2-3 | Layout normal |
| lg | 3-4 | Layout rico |
| xl | 4 | Layout muy rico |

```css
/* Mobile */
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}

/* Tablet */
@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## 🖱️ Touch Targets (WCAG)

### Escala

| Plataforma | Valor | Regla WCAG |
|-----------|-------|-----------|
| Mobile | 44px × 44px | WCAG 2.1 AAA |
| Desktop | 32px × 32px | WCAG 2.1 AA |

**¿Por qué?** Dedos son más grandes que cursores. 44px es el mínimo para evitar misclicks.

### Uso

```css
/* Button en mobile */
@media (max-width: 767px) {
  .button {
    min-height: var(--layout-touch-target-mobile);  /* 44px */
    min-width: var(--layout-touch-target-mobile);
    padding: var(--space-3) var(--space-4);
  }
}

/* Button en desktop */
@media (min-width: 1024px) {
  .button {
    min-height: var(--layout-touch-target-desktop);  /* 32px */
    min-width: auto;
    padding: var(--space-2) var(--space-4);
  }
}
```

---

## 📐 Padding & Margins por Viewport

### Container Padding

```
Mobile (xs):   16px (space-4)
Tablet (md):   24px (space-6)
Desktop (lg):  32px (space-8)
```

```css
/* Mobile */
.container {
  padding: 0 var(--space-4);
}

/* Tablet+ */
@media (min-width: 768px) {
  .container {
    padding: 0 var(--space-6);
  }
}

/* Desktop+ */
@media (min-width: 1024px) {
  .container {
    padding: 0 var(--space-8);
  }
}
```

### Vertical Rhythm por Viewport

```css
/* Mobile */
section {
  margin-bottom: var(--space-8);  /* 32px */
  padding-top: var(--space-8);
}

/* Desktop */
@media (min-width: 1024px) {
  section {
    margin-bottom: var(--space-12);  /* 48px */
    padding-top: var(--space-12);
  }
}
```

---

## 🎭 Safe Areas (iPhone Notch)

### Tokens

```css
--layout-safe-area-inset-top: env(safe-area-inset-top, 0px);
--layout-safe-area-inset-right: env(safe-area-inset-right, 0px);
--layout-safe-area-inset-bottom: env(safe-area-inset-bottom, 0px);
--layout-safe-area-inset-left: env(safe-area-inset-left, 0px);
```

### Uso

```css
/* Sticky header respetando notch */
header {
  padding-top: calc(var(--space-4) + var(--layout-safe-area-inset-top));
  padding-left: calc(var(--space-4) + var(--layout-safe-area-inset-left));
  padding-right: calc(var(--space-4) + var(--layout-safe-area-inset-right));
}

/* Sticky footer */
footer {
  padding-bottom: calc(var(--space-4) + var(--layout-safe-area-inset-bottom));
}
```

---

## 🧮 Density (Compactibilidad)

### Scales

```css
--layout-density-compact: 1.0       /* 100% tamaño */
--layout-density-normal: 1.25       /* 125% tamaño */
--layout-density-comfortable: 1.5   /* 150% tamaño */
```

### Uso (Opcional)

```css
/* Interfaz compacta (datos densos) */
body.density-compact {
  --multiplier: var(--layout-density-compact);
}

/* Interfaz normal (por defecto) */
body.density-normal {
  --multiplier: var(--layout-density-normal);
}

/* Elemento con aplicación de density */
.list-item {
  padding: calc(var(--space-2) * var(--multiplier)) var(--space-4);
}
```

---

## 🎨 Patrones de Layout

### Sidebar Layout

```html
<div class="sidebar-layout">
  <aside class="sidebar">Sidebar</aside>
  <main class="main-content">Main</main>
</div>
```

```css
.sidebar-layout {
  display: flex;
  gap: var(--space-6);
}

.sidebar {
  flex: 0 0 250px;
  display: none;  /* Hidden on mobile */
}

@media (min-width: 1024px) {
  .sidebar {
    display: block;
  }
}

.main-content {
  flex: 1;
  min-width: 0;  /* Prevenir overflow */
}
```

### Centered Container

```css
.container {
  max-width: var(--layout-container-max-width);
  margin-left: auto;
  margin-right: auto;
  padding: 0 var(--space-4);
}

@media (min-width: 1024px) {
  .container {
    padding: 0 var(--space-6);
  }
}
```

### Responsive Grid

```css
.grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## 🎯 Validación Responsive

### Test Sizes

```
Mobile:     375px (iPhone X)
Tablet:     768px (iPad)
Desktop:    1440px (27" monitor)
```

### Checklist

- ✅ Texto legible en mobile (mín 16px)
- ✅ Touch targets 44px×44px en mobile
- ✅ Máximo ancho 1280px en desktop
- ✅ Padding consistente por breakpoint
- ✅ Safe areas respetadas

---

## ✅ Checklist

- ✅ Breakpoints: xs, sm, md, lg, xl, 2xl
- ✅ Mobile-first approach (default es xs)
- ✅ Touch targets 44px en mobile
- ✅ Container max-width 1280px
- ✅ Padding adaptativo por breakpoint
- ✅ Safe areas para notched devices
