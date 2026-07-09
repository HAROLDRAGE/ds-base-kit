# 📏 Espaciado Foundations — Sistema de Distancias Base

**Versión:** 2.2.0  
**Actualizado:** 2026-07-09

---

## 🏛️ Estructura

```
PRIMITIVOS (valores brutos)
  4px, 8px, 12px, 16px, etc.

      ↓

FOUNDATIONS (escala agnóstica)
  --foundation-space-1 → 4px
  --foundation-space-2 → 8px
  --foundation-space-4 → 16px

      ↓

SEMÁNTICOS (propósito definido)
  --space-button-padding-y → space-2 (8px)
  --space-button-padding-x → space-4 (16px)
  --space-component-gap → space-2 (8px)

      ↓

COMPONENTES
  Button, Card, Input, etc.
```

---

## 🔢 Escala Base

### 4px Magic Number

```
Todos los espacios son múltiplos de 4px

4px × 1 = 4px
4px × 2 = 8px
4px × 3 = 12px
4px × 4 = 16px  ← Base estándar
4px × 5 = 20px
4px × 8 = 32px
4px × 10 = 40px
4px × 12 = 48px
4px × 16 = 64px
```

**¿Por qué 4px?**
- ✅ Divisible por 2 (criatura perfecta para grillas)
- ✅ Compatible con resoluciones retina (4px = 2×2 pixels)
- ✅ Escalable: 4×6 = 24px, 4×16 = 64px
- ✅ Flexible para mobile (44px touch target = 4×11)

---

## 📊 Tabla de Espaciado

### Completa con Propósito

```
Token              Valor    Tipo        Uso Típico
─────────────────────────────────────────────────────────────
--space-0          0px      nill        Reset
--space-1          4px      tiny        Mínimo
--space-2          8px      small       Espaciado estándar pequeño
--space-3          12px     small-med   Separación ligera
--space-4          16px     base        ⭐ Padding estándar
--space-5          20px     medium      Spacing generoso
--space-6          24px     medium      Padding agresivo
--space-8          32px     large       Separación componentes
--space-10         40px     large       Separación grandes
--space-12         48px     xl          Separación secciones
--space-16         64px     2xl         Separación mayor
```

---

## 🎯 Patrones de Uso

### 1. Padding (Espacio Interior)

#### Button
```
Tamaño    Padding Y    Padding X    Total
─────────────────────────────────────────
Small     space-1      space-2      4px 8px
Base      space-2      space-4      8px 16px  ← Standard
Large     space-3      space-6      12px 24px
```

```html
<button class="button button--base">Click</button>
```

```css
.button--base {
  padding: var(--space-2) var(--space-4);   /* 8px 16px */
}

.button--small {
  padding: var(--space-1) var(--space-2);   /* 4px 8px */
}
```

#### Card
```css
.card {
  padding: var(--space-4) var(--space-6);   /* 16px 24px */
}
```

#### Input
```css
.input {
  padding: var(--space-2) var(--space-4);   /* 8px 16px */
}
```

### 2. Gap (Espaciado entre elementos)

#### Flex Container
```html
<div class="flex-container">
  <button>Item 1</button>
  <button>Item 2</button>
  <button>Item 3</button>
</div>
```

```css
.flex-container {
  display: flex;
  gap: var(--space-2);   /* 8px entre items */
}
```

#### Grid Container
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);   /* 16px entre filas y columnas */
}
```

### 3. Margin (Separación Externa)

#### Entre Secciones
```html
<section class="section">...</section>
<section class="section">...</section>
```

```css
.section {
  margin-bottom: var(--space-12);  /* 48px separación */
}

.section:last-child {
  margin-bottom: 0;  /* No margin en último */
}
```

#### Entre Componentes
```css
.component {
  margin-bottom: var(--space-8);  /* 32px */
}
```

### 4. Spacing Simétrico

```css
/* Centro + igual a todos lados */
.centered-content {
  margin: auto;
  padding: var(--space-6);  /* 24px todos los lados */
}

/* Square shape */
.square {
  width: var(--space-16);   /* 64px × 64px */
  height: var(--space-16);
}
```

### 5. Spacing Asimétrico

```css
/* Más espacio abajo que arriba */
.title {
  margin-top: var(--space-4);     /* 16px */
  margin-bottom: var(--space-8);  /* 32px */
}

/* Padding diferente horizontal vs vertical */
.alert {
  padding: var(--space-4) var(--space-6);  /* 16px top/bottom, 24px left/right */
}
```

---

## 📐 Uso por Componente

### Button
```
Pequeño:   2 × 8  = 2px padding
Mediano:   8 × 16 = 8px padding
Grande:    12 × 24 = 12px padding
```

### Card
```
Padding:   16px (space-4)
Interno gap: 8px (space-2) entre elementos
```

### Modal
```
Padding:   24px (space-6)
Header gap: 16px (space-4)
Footer gap: 8px (space-2) entre botones
```

### Alert
```
Padding:   8px 16px (space-2 space-4)
Icon + Text gap: 12px (space-3)
```

### Dropdown/Menu
```
Item padding: 8px 12px (space-2 space-3)
Item gap: 0px (items se tocan)
```

---

## 🔄 Responsive Spacing

### Principio: Reducir en Mobile

```css
/* Mobile (default) */
.section {
  padding: var(--space-4);  /* 16px */
  margin-bottom: var(--space-8);  /* 32px */
}

/* Tablet: media query */
@media (min-width: 768px) {
  .section {
    padding: var(--space-6);  /* 24px */
    margin-bottom: var(--space-10);  /* 40px */
  }
}

/* Desktop: media query */
@media (min-width: 1024px) {
  .section {
    padding: var(--space-8);  /* 32px */
    margin-bottom: var(--space-12);  /* 48px */
  }
}
```

### Vertical Rhythm

Mantener consistencia vertical:

```css
body {
  line-height: 1.5;
  font-size: 1rem;  /* 16px */
}

/* Vertical rhythm = 1rem × 1.5 = 24px */
h2 {
  margin-top: var(--space-6);    /* 24px (1 rhythm) */
  margin-bottom: var(--space-4); /* 16px */
}

p {
  margin-bottom: var(--space-6); /* 24px (1 rhythm) */
}
```

---

## 🎯 Patrones Comunes

### Stack (Vertical)
```css
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);  /* 16px entre items */
}
```

### Inline (Horizontal)
```css
.inline {
  display: flex;
  gap: var(--space-2);  /* 8px entre items */
}
```

### Cluster (Wrapping)
```css
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);  /* 12px entre items */
  align-items: center;
}
```

### Sidebar Layout
```css
.sidebar-layout {
  display: flex;
  gap: var(--space-6);  /* 24px entre sidebar y main */
}

.sidebar {
  flex: 0 0 250px;
}

.main {
  flex: 1;
}
```

### Grid Cards
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-6);  /* 24px entre cards */
}
```

---

## 🚫 Cosas a Evitar

### ❌ No Mezclar Espacios Arbitrarios
```css
/* MALO */
.card {
  padding: 15px;       /* No es múltiplo de 4 */
  margin: 23px;        /* Arbitrario */
  gap: 5px;            /* No existe en escala */
}

/* BUENO */
.card {
  padding: var(--space-4);     /* 16px */
  margin: var(--space-6);      /* 24px */
  gap: var(--space-2);         /* 8px */
}
```

### ❌ No Ignorar Escala
```css
/* MALO */
.section {
  gap: 30px;  /* No existe en escala (no es múltiplo de 4) */
}

/* BUENO */
.section {
  gap: var(--space-8);  /* 32px, cercano a 30px pero en escala */
}
```

### ❌ No Espaciar Inconsistentemente
```css
/* MALO: Botones con espaciado inconsistente */
.button-group button + button {
  margin-left: 10px;
}

/* BUENO: Usar gap */
.button-group {
  display: flex;
  gap: var(--space-2);  /* 8px consistente */
}
```

---

## 📊 Matriz de Componentes

| Componente | Padding | Gap | Margin |
|------------|---------|-----|--------|
| Button | 8/16 | N/A | 0 |
| Input | 8/16 | N/A | 0 |
| Card | 24 | 16 | 24 |
| Alert | 8/16 | 12 | 0 |
| Badge | 4/8 | N/A | 0 |
| Modal | 24 | 16 | 0 |
| Dropdown | 8/12 | 0 | 0 |
| Tooltip | 8/12 | N/A | 0 |
| Section | Responsive | N/A | 48 |
| Container | 16-32 | N/A | 0 |

---

## ✨ Mejores Prácticas

### ✅ CORRECTO
```css
.component {
  padding: var(--space-4);
  margin-bottom: var(--space-6);
  gap: var(--space-2);
}
```

### ❌ INCORRECTO
```css
.component {
  padding: 15px;
  margin-bottom: 20px;
  gap: 7px;
}
```

---

## 🚀 Siguientes Pasos

- [ ] Crear utility classes para spacing (`.p-4`, `.m-6`, `.gap-2`)
- [ ] Validar consistencia de spacing en todos los componentes
- [ ] Documentar spacing por breakpoint (mobile vs desktop)
- [ ] Crear guidelines de "white space" (espacios vacíos)
