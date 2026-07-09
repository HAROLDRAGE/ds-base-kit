# 🌙 Sombras Foundations — Elevación y Profundidad

**Versión:** 2.2.0  | **Actualizado:** 2026-07-09

---

## 🏛️ Estructura

```
FOUNDATIONS (agnósticos de marca)
├─ Shadow scale (sm → 2xl)
├─ Opacity predefinida
└─ Valores box-shadow

    ↓

SEMÁNTICOS (intención)
├─ shadow-button (sm, hover)
├─ shadow-card (md, base)
└─ shadow-modal (xl, flotante)

    ↓

COMPONENTES
├─ Button, Card, Modal, Dropdown, Tooltip
```

---

## 🔦 Escala de Sombras

### Foundation Values

| Token | Valor CSS | Opacidad | Uso |
|-------|-----------|----------|-----|
| `--foundation-shadow-sm` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | 5% | Subtle |
| `--foundation-shadow-md` | `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)` | 10% | Normal |
| `--foundation-shadow-lg` | `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)` | 10% | Elevado |
| `--foundation-shadow-xl` | `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)` | 10% | Muy elevado |
| `--foundation-shadow-2xl` | `0 25px 50px -12px rgb(0 0 0 / 0.25)` | 25% | Flotante |

### Propósito de Cada Nivel

```
sm    (5% opacidad)   → Bordes sutiles, divisores
md    (10% opacidad)  → Tarjetas base, componentes normales
lg    (10% opacidad)  → Tarjetas elevadas, popovers
xl    (10% opacidad)  → Modales, menús flotantes
2xl   (25% opacidad)  → Modales grandes, tooltips críticos
```

---

## 🎯 Uso por Componente

### Button (shadow-sm)
```css
.button {
  box-shadow: none;  /* Sin sombra por defecto */
}

.button:hover {
  box-shadow: var(--foundation-shadow-sm);  /* Sutil elevación */
}

.button:active {
  box-shadow: 0 0 0 2px var(--color-focus);  /* Ring en lugar de shadow */
}
```

### Card (shadow-md)
```css
.card {
  box-shadow: var(--foundation-shadow-md);  /* Normal */
  border-radius: var(--foundation-radius-lg);
  background: var(--color-surface);
}

.card:hover {
  box-shadow: var(--foundation-shadow-lg);  /* Elevación en hover */
}
```

### Dropdown (shadow-lg)
```css
.dropdown-menu {
  box-shadow: var(--foundation-shadow-lg);  /* Flotante */
  position: absolute;
  z-index: 10;
}
```

### Modal (shadow-xl)
```css
.modal {
  box-shadow: var(--foundation-shadow-xl);  /* Muy flotante */
  position: fixed;
  z-index: 100;
  background: var(--color-surface);
  border-radius: var(--foundation-radius-lg);
}

.modal::backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}
```

### Tooltip (shadow-md)
```css
.tooltip {
  box-shadow: var(--foundation-shadow-md);  /* Sutil elevación */
  position: absolute;
  background: var(--color-text);
  color: var(--color-on-action);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--foundation-radius-md);
  z-index: 50;
}
```

### Alert (shadow-sm o none)
```css
.alert {
  box-shadow: none;  /* Sin sombra, solo color de borde */
  border-left: var(--foundation-border-width-base);
  border-radius: var(--foundation-radius-md);
  padding: var(--space-3) var(--space-4);
}
```

---

## 🌍 Tema Dark vs Light

### El Secreto: Same Shadow, Diferente Opacidad

En **light theme**: sombras son oscuras (opacidad 5-25%)
```css
/* light */
[data-theme="light"] {
  --foundation-shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}
```

En **dark theme**: sombras más fuertes (opacidad mayor)
```css
/* dark */
[data-theme="dark"] {
  --foundation-shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.25);
}
```

**¿Por qué?** En dark mode, fondos oscuros necesitan sombras más visibles para contraste.

---

## 🎨 Estados

### Normal → Hover → Active

```css
.card {
  box-shadow: var(--foundation-shadow-md);  /* Normal */
  transition: box-shadow var(--motion-base);
}

.card:hover {
  box-shadow: var(--foundation-shadow-lg);  /* Elevación */
}

.card:active {
  box-shadow: var(--foundation-shadow-sm);  /* Menos elevación, click feedback */
}
```

### Focus Visible

```css
.button:focus-visible {
  box-shadow: 0 0 0 3px var(--color-focus);  /* Ring, no shadow */
  outline: none;
}
```

---

## 🚫 Cosas a Evitar

### ❌ Sombras Arbitrarias
```css
/* MALO */
.card {
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);  /* Valor custom */
}

/* BUENO */
.card {
  box-shadow: var(--foundation-shadow-md);
}
```

### ❌ Sombras sin Intención
```css
/* MALO: Shadow sin coherencia */
.button {
  box-shadow: var(--foundation-shadow-xl);  /* Demasiado para un botón */
}

/* BUENO */
.button:hover {
  box-shadow: var(--foundation-shadow-sm);  /* Sutil feedback */
}
```

---

## 📊 Matriz de Componentes

| Componente | Base | Hover | Active | Z-index |
|------------|------|-------|--------|---------|
| Button | none | sm | sm | auto |
| Input | none | sm | sm | auto |
| Card | md | lg | md | auto |
| Modal | xl | xl | xl | 100 |
| Dropdown | lg | lg | lg | 50 |
| Tooltip | md | md | md | 50 |
| Alert | none | none | none | auto |
| Badge | none | none | none | auto |

---

## ✅ Checklist

- ✅ Sombras escaladas: sm → md → lg → xl → 2xl
- ✅ Opacidades consistentes (5%, 10%, 25%)
- ✅ No usar box-shadow hardcodeado
- ✅ Shadow = feedback visual de elevación
- ✅ Transición suave entre estados (motion token)
