# 🎨 Iconografía Foundations — Sistema de Íconos

**Versión:** 2.2.0  | **Actualizado:** 2026-07-09

---

## 🏛️ Estructura

```
FOUNDATIONS
├─ Tamaños (iconografía)
│  ├─ xs (16px)
│  ├─ sm (20px)
│  ├─ md (24px)
│  ├─ lg (32px)
│  └─ xl (48px)
│
├─ Stroke (grosor de línea)
│  ├─ thin (1px)
│  ├─ base (1.5px)
│  └─ thick (2px)
│
└─ Color
   ├─ inherit (del contenedor)
   ├─ currentColor (CSS variable)
   └─ explicit (definido)

    ↓

SEMÁNTICOS
├─ icon-size-button
├─ icon-size-input
└─ icon-stroke-normal

    ↓

COMPONENTES
├─ Button, Input, Alert, Link
```

---

## 📏 Tamaños

### Escala

| Token | Valor | Uso |
|-------|-------|-----|
| `--foundation-icon-size-xs` | 16px | Inline en texto, badges |
| `--foundation-icon-size-sm` | 20px | Labels, inputs, buttons pequeños |
| `--foundation-icon-size-md` | 24px | Botones estándar, cards |
| `--foundation-icon-size-lg` | 32px | Headings, secciones |
| `--foundation-icon-size-xl` | 48px | Secciones grandes, avatares |

### Mapeo a Componentes

| Componente | Tamaño | Ejemplo |
|-----------|--------|---------|
| Button pequeño | xs (16px) | `<button>` with icon |
| Button normal | md (24px) | `<button>` with icon |
| Input icon | sm (20px) | Search, email, etc. |
| Alert icon | sm (20px) | Error, success, warning |
| Card icon | md (24px) | Descripción de tarjeta |
| Section icon | lg (32px) | Feature section |
| Avatar | xl (48px) | User profile |
| Inline icon | xs (16px) | Dentro de texto |

---

## 🎨 Stroke (Grosor de Línea)

### Escala

| Token | Valor | Tipo | Uso |
|-------|-------|------|-----|
| `--foundation-icon-stroke-thin` | 1px | Línea fina | Iconos grandes |
| `--foundation-icon-stroke-base` | 1.5px | Línea normal | ⭐ Estándar |
| `--foundation-icon-stroke-thick` | 2px | Línea gruesa | Énfasis |

### Por Tamaño

```
Tamaño   Stroke Recomendado
─────────────────────────────
xs       thin (1px)
sm       base (1.5px)
md       base (1.5px)
lg       base (1.5px) o thin
xl       thin (1px)
```

---

## 🎯 Uso en Componentes

### Button con Icono

```html
<button class="button button--primary">
  <svg class="button__icon" aria-hidden="true">
    <!-- icon -->
  </svg>
  <span class="button__text">Click me</span>
</button>
```

```css
.button__icon {
  width: var(--foundation-icon-size-md);   /* 24px */
  height: var(--foundation-icon-size-md);
  stroke-width: var(--foundation-icon-stroke-base); /* 1.5px */
  color: currentColor;  /* Del button */
  margin-right: var(--space-2);
}
```

### Input con Icono

```html
<div class="input-group">
  <svg class="input__icon" aria-hidden="true">
    <!-- search icon -->
  </svg>
  <input 
    type="text" 
    class="input" 
    placeholder="Buscar..."
  />
</div>
```

```css
.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input__icon {
  position: absolute;
  left: var(--space-3);
  width: var(--foundation-icon-size-sm);   /* 20px */
  height: var(--foundation-icon-size-sm);
  stroke-width: var(--foundation-icon-stroke-base);
  color: var(--color-muted);
  pointer-events: none;
}

.input {
  padding-left: var(--space-8);  /* Espacio para icono */
}
```

### Alert con Icono

```html
<div class="alert alert--danger" role="alert">
  <svg class="alert__icon" aria-hidden="true">
    <!-- error icon -->
  </svg>
  <div class="alert__content">
    <p class="alert__title">Error</p>
    <p class="alert__message">Algo salió mal.</p>
  </div>
</div>
```

```css
.alert__icon {
  flex-shrink: 0;
  width: var(--foundation-icon-size-sm);   /* 20px */
  height: var(--foundation-icon-size-sm);
  stroke-width: var(--foundation-icon-stroke-base);
  color: var(--color-danger);
  margin-right: var(--space-3);
}
```

### Link con Icono

```html
<a href="/page" class="link">
  <span class="link__text">Ir a página</span>
  <svg class="link__icon" aria-hidden="true">
    <!-- arrow icon -->
  </svg>
</a>
```

```css
.link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  color: var(--color-action);
  text-decoration: none;
}

.link__icon {
  width: var(--foundation-icon-size-xs);   /* 16px */
  height: var(--foundation-icon-size-xs);
  stroke-width: var(--foundation-icon-stroke-thin);
  transition: transform var(--motion-fast);
}

.link:hover .link__icon {
  transform: translateX(2px);
}
```

---

## 🎨 Color de Íconos

### Opciones

```css
/* Opción 1: Heredar color */
.icon {
  color: inherit;  /* Del contenedor padre */
}

/* Opción 2: Usar CSS variable (recomendado) */
.icon {
  color: currentColor;  /* Usa color CSS del elemento */
}

/* Opción 3: Explícito */
.icon {
  color: var(--color-action);
}

/* Opción 4: Muted */
.icon--muted {
  color: var(--color-muted);
}

/* Opción 5: Danger/Warning */
.icon--danger {
  color: var(--color-danger);
}
.icon--warning {
  color: var(--color-warning);
}
```

### Estados

```css
.button {
  color: var(--color-text);
}

.button__icon {
  color: currentColor;  /* Automáticamente color del button */
}

.button:hover {
  color: var(--color-action);
  /* Icon color cambia con button automáticamente */
}

.button:disabled {
  color: var(--color-disabled);
  /* Icon color cambia con button automáticamente */
}
```

---

## 📐 Alineamiento

### Centrado Vertical (Flex)

```css
.flex-center {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
```

### Alineamiento en Línea de Base

```css
/* Para íconos dentro de texto */
.icon--inline {
  display: inline-block;
  vertical-align: -2px;  /* Pequeño ajuste */
}
```

---

## 🔄 Responsividad

### Tamaños Adaptables

```css
/* Mobile */
.button__icon {
  width: var(--foundation-icon-size-sm);   /* 20px */
  height: var(--foundation-icon-size-sm);
}

/* Desktop */
@media (min-width: 1024px) {
  .button__icon {
    width: var(--foundation-icon-size-md);  /* 24px */
    height: var(--foundation-icon-size-md);
  }
}
```

### Visibilidad Selectiva

```css
/* Mostrar icono solo en mobile */
.icon-mobile {
  display: inline;
}

@media (min-width: 1024px) {
  .icon-mobile {
    display: none;
  }
}

/* Mostrar icono solo en desktop */
.icon-desktop {
  display: none;
}

@media (min-width: 1024px) {
  .icon-desktop {
    display: inline;
  }
}
```

---

## ♿ Accesibilidad

### Íconos Decorativos

```html
<!-- aria-hidden para íconos sin significado -->
<button class="button">
  <svg class="button__icon" aria-hidden="true">
    <!-- icon -->
  </svg>
  <span>Click me</span>
</button>
```

### Íconos Significativos

```html
<!-- Sin aria-hidden si el ícono comunica algo -->
<button class="button">
  <svg class="button__icon" role="img" aria-label="Cerrar">
    <!-- close icon -->
  </svg>
</button>
```

### Contraste WCAG

```
Requerimiento: Color icono vs fondo ≥ 3:1

✅ Oscuro sobre claro
❌ Gris sobre blanco (muy bajo contraste)
✅ Usar --color-action sobre --color-bg
```

---

## 🚫 Cosas a Evitar

### ❌ Tamaños Arbitrarios
```css
/* MALO */
.icon {
  width: 23px;
  height: 23px;
}

/* BUENO */
.icon {
  width: var(--foundation-icon-size-sm);   /* 20px */
  height: var(--foundation-icon-size-sm);
}
```

### ❌ Colores Hardcodeados
```css
/* MALO */
.icon {
  color: #2E7D0F;
}

/* BUENO */
.icon {
  color: currentColor;  /* Hereda del contenedor */
}

/* O explícito */
.icon {
  color: var(--color-action);
}
```

### ❌ Stroke Inconsistente
```css
/* MALO */
svg {
  stroke-width: 1px;  /* Variable por SVG */
}

/* BUENO */
svg {
  stroke-width: var(--foundation-icon-stroke-base);
}
```

---

## 📊 Matriz de Componentes

| Componente | Tamaño | Stroke | Color |
|-----------|--------|--------|-------|
| Button | md (24px) | base | currentColor |
| Input | sm (20px) | base | muted → action |
| Alert | sm (20px) | base | danger/warning |
| Link | xs (16px) | thin | action |
| Card icon | md (24px) | base | action |
| Avatar | xl (48px) | thin | auto |
| Badge | xs (16px) | base | explicit |

---

## ✅ Checklist

- ✅ Tamaños: xs, sm, md, lg, xl
- ✅ Stroke: thin, base, thick
- ✅ Color: currentColor o explícito
- ✅ Alineamiento correcto (vertical-center)
- ✅ Accesibilidad: aria-hidden donde corresponde
- ✅ Responsive: tamaños adaptables
- ✅ Contraste WCAG AA (≥ 3:1)
