# ⚡ Movimiento Foundations — Transiciones y Animaciones

**Versión:** 2.2.0  | **Actualizado:** 2026-07-09

---

## 🏛️ Estructura

```
FOUNDATIONS
├─ Duración (timing)
│  ├─ fast (120ms)
│  ├─ base (240ms)
│  └─ slow (400ms)
│
└─ Easing (aceleración)
   ├─ linear (constante)
   ├─ in (aceleración)
   ├─ out (desaceleración)
   └─ in-out (natural)

    ↓

SEMÁNTICOS
├─ motion-button-transition
├─ motion-modal-entrance
└─ motion-dropdown-exit

    ↓

COMPONENTES
├─ Button, Modal, Dropdown
```

---

## ⏱️ Duración

### Escala

| Token | Valor | Uso |
|-------|-------|-----|
| `--foundation-motion-fast` | 120ms | Hover, focus, feedback inmediato |
| `--foundation-motion-base` | 240ms | Transiciones estándar |
| `--foundation-motion-slow` | 400ms | Animaciones complejas |

### Principio: Respuesta Rápida

```
User acción (click)
    ↓
120ms → Feedback visual (fast)
    ↓
User percibe respuesta instantánea (< 100ms = inmediato)
```

**Regla de oro:** < 100ms = instantáneo, 100-300ms = rápido, > 300ms = lento

### Uso por Interacción

```css
/* Hover - debe ser muy rápido */
.button:hover {
  transition: background-color var(--foundation-motion-fast);  /* 120ms */
}

/* Cambio de tema - puede ser medio */
body.theme-change {
  transition: background-color var(--foundation-motion-base);  /* 240ms */
}

/* Animación de entrada - puede ser más lenta */
@keyframes slideIn {
  from { transform: translateY(-100%); }
  to { transform: translateY(0); }
}

.modal {
  animation: slideIn var(--foundation-motion-slow) ease-out;  /* 400ms */
}
```

---

## 🎯 Easing Functions

### Tipos

| Token | Valor CSS | Comportamiento | Uso |
|-------|-----------|-----------------|-----|
| `--foundation-motion-easing-linear` | `linear` | Cambio constante | Indicadores de progreso |
| `--foundation-motion-easing-in` | `cubic-bezier(0.4, 0, 1, 1)` | Empieza lento, acelera | Salidas, collapses |
| `--foundation-motion-easing-out` | `cubic-bezier(0, 0, 0.2, 1)` | Empieza rápido, desacelera | Entradas, opens |
| `--foundation-motion-easing-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Aceleración + desaceleración | Transiciones naturales |

### Visualización

```
Linear: ─────────────────  (constante)
        /

In:     ________/          (empieza lento, acelera)
                /

Out:    /________          (empieza rápido, desacelera)
       /

In-Out: _____/\_____       (aceleración + desaceleración)
             /   \
```

### Reglas

```
Entrada (elemento aparece)
  → Usar ease-OUT (empieza rápido, termina lento = natural)

Salida (elemento desaparece)
  → Usar ease-IN (empieza lento, termina rápido = rápido)

Estado a estado (cambio dentro del viewport)
  → Usar ease-IN-OUT (natural en ambas direcciones)
```

---

## 🎬 Composiciones Semánticas

### Button Hover

```css
.button {
  transition: 
    background-color var(--foundation-motion-fast) var(--foundation-motion-easing-out),
    box-shadow var(--foundation-motion-fast) var(--foundation-motion-easing-out),
    transform var(--foundation-motion-fast) var(--foundation-motion-easing-out);
}

.button:hover {
  background-color: var(--color-action-hover);
  box-shadow: var(--foundation-shadow-sm);
  transform: translateY(-2px);  /* Pequeño levantamiento */
}
```

### Modal Entrance

```css
@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal {
  animation: modalSlideIn var(--foundation-motion-base) var(--foundation-motion-easing-out);
}
```

### Dropdown Open/Close

```css
.dropdown-menu {
  opacity: 0;
  transform: translateY(-8px);
  pointer-events: none;
  transition: 
    opacity var(--foundation-motion-fast) var(--foundation-motion-easing-out),
    transform var(--foundation-motion-fast) var(--foundation-motion-easing-out);
}

.dropdown-menu.open {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
```

### Color Change (Theme Switch)

```javascript
// Cambiar tema
document.body.dataset.theme = "dark";
```

```css
/* CSS transitions automáticas con motion-base */
body {
  transition: background-color var(--foundation-motion-base) var(--foundation-motion-easing-in-out);
}

[data-theme="dark"] {
  --color-bg: #0B0E11;
  --color-text: #E8ECF1;
}

[data-theme="light"] {
  --color-bg: #FFFFFF;
  --color-text: #1A2027;
}
```

---

## 🔄 Transiciones vs Animaciones

### Transición (Cambio de estado A → B)

```css
/* Cuando propiedad CSS cambia, animar la transición */
.button {
  background-color: var(--color-action);
  transition: background-color 120ms ease-out;
}

.button:hover {
  background-color: var(--color-action-hover);  /* La transición se aplica automáticamente */
}
```

### Animación (Secuencia keyframes)

```css
/* Secuencia predefinida de frames */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading {
  animation: spin 1s linear infinite;
}
```

---

## 🚫 Cosas a Evitar

### ❌ Movimiento Lento
```css
/* MALO: 1 segundo es demasiado para hover */
.button {
  transition: all 1s ease-in-out;
}

/* BUENO */
.button {
  transition: background-color var(--foundation-motion-fast) var(--foundation-motion-easing-out);
}
```

### ❌ Movimiento Inconsistente
```css
/* MALO: Sin coherencia */
.button { transition: 100ms; }
.card { transition: 250ms; }
.modal { transition: 350ms; }

/* BUENO */
.button { transition: var(--foundation-motion-fast); }
.card { transition: var(--foundation-motion-base); }
.modal { transition: var(--foundation-motion-slow); }
```

### ❌ Animar TODO
```css
/* MALO: Animar properties que no importan */
.button {
  transition: all 240ms ease-out;  /* includes width, height, etc */
}

/* BUENO: Solo lo que cambia visualmente */
.button {
  transition: background-color var(--foundation-motion-fast);
}
```

---

## 🎨 Respeto Preferencias

### Prefers Reduced Motion

```css
/* Respetar preferencia de sistema */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
  }
}
```

**¿Por qué?** Usuarios con vestibular disorders o fotosensibilidad.

---

## 📊 Matriz de Movimiento

| Componente | Duración | Easing | Propiedades |
|------------|----------|--------|-------------|
| Button hover | fast (120ms) | ease-out | background, shadow, transform |
| Input focus | fast (120ms) | ease-out | border-color, shadow |
| Modal entrance | base (240ms) | ease-out | opacity, transform |
| Dropdown toggle | fast (120ms) | ease-out | opacity, transform |
| Theme switch | base (240ms) | ease-in-out | background, color |
| Page transition | slow (400ms) | ease-in-out | opacity, transform |

---

## ✅ Checklist

- ✅ Duraciones: fast (120ms), base (240ms), slow (400ms)
- ✅ Easing: linear, in, out, in-out
- ✅ No usar valores hardcodeados (250ms, 500ms, etc)
- ✅ Respetar prefers-reduced-motion
- ✅ Transiciones < 300ms para feedback inmediato
- ✅ Animaciones pueden ser más lentas (> 400ms)
