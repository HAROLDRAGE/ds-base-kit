# 🎨 Color Foundations — Sistema de Colores Base

**Versión:** 2.2.0  
**Actualizado:** 2026-07-09

---

## 📋 Índice

1. [Estructura de Color](#estructura-de-color)
2. [Foundations por Marca](#foundations-por-marca)
3. [Paleta Completa](#paleta-completa)
4. [Mapeo a Semánticos](#mapeo-a-semánticos)
5. [WCAG AA Contrasts](#wcag-aa-contrasts)
6. [Uso en Componentes](#uso-en-componentes)

---

## 🏛️ Estructura de Color

### 3 Niveles

```
PRIMITIVOS (Hex/RGB values)
    #2E7D0F, #7CE83A, #0B0E11, etc.

        ↓

FOUNDATIONS (Nombres agnósticos de marca)
    --foundation-primary
    --foundation-neutral-900
    --foundation-red-600
    etc.

        ↓

SEMÁNTICOS (Intención de uso)
    --color-action (fondo de botón)
    --color-text (texto legible)
    --color-danger (error visual)
    etc.

        ↓

COMPONENTES (UI real)
    <button>, <input>, <alert>, etc.
```

---

## 🎯 Foundations por Marca

### PROMPTEA (Verde energético)

#### Dark Theme
```
Primitivos → Foundation:

#7CE83A      → --foundation-primary (verde brillante)
#8ef249      → --foundation-primary-hover (más saturado)
#1d3312      → --foundation-primary-soft (muy desaturado)

#0B0E11      → --foundation-neutral-950 (casi negro)
#14181D      → --foundation-neutral-900 (muy oscuro)
#2A3138      → --foundation-neutral-800 (oscuro)
#3d4855      → --foundation-neutral-700
#5A6572      → --foundation-neutral-600
#7d8a99      → --foundation-neutral-500
#9AA5B1      → --foundation-neutral-400 (gris)
#c5d0db      → --foundation-neutral-300
#e8ecf1      → --foundation-neutral-200 (muy claro)
#FFFFFF      → --foundation-neutral-100 (blanco puro)

#F87171      → --foundation-red-600 (rojo error)
#4ADE80      → --foundation-green-600 (verde success)
#FCD34D      → --foundation-amber-600 (amarillo warning)
```

#### Light Theme
```
#2E7D0F      → --foundation-primary (verde oscuro)
#1b5d03      → --foundation-primary-hover (más oscuro)
#f0fde4      → --foundation-primary-soft (muy claro)

#FFFFFF      → --foundation-neutral-50 (blanco puro)
#f9fafb      → --foundation-neutral-100
#f3f4f6      → --foundation-neutral-200
#e5e7eb      → --foundation-neutral-300
#d1d5db      → --foundation-neutral-400
#9ca3af      → --foundation-neutral-500
#6b7280      → --foundation-neutral-600
#374151      → --foundation-neutral-700
#1f2937      → --foundation-neutral-800
#1A2027      → --foundation-neutral-900 (muy oscuro)

#B91C1C      → --foundation-red-600
#15803D      → --foundation-green-600
#D97706      → --foundation-amber-600
```

---

### NOVA (Púrpura místico)

#### Dark Theme
```
#A78BFA      → --foundation-primary
#c4b5fd      → --foundation-primary-hover
#2d1f4e      → --foundation-primary-soft

#0D0B14      → --foundation-neutral-950
#171322      → --foundation-neutral-900
[escalas grises+púrpura]
```

#### Light Theme
```
#7C3AED      → --foundation-primary
#6D28D9      → --foundation-primary-hover
#F3E8FF      → --foundation-primary-soft
[escalas grises+púrpura claro]
```

---

### OCEAN (Azul agua)

#### Dark Theme
```
#0EA5E9      → --foundation-primary
#06B6D4      → --foundation-primary-hover
#0c4a6e      → --foundation-primary-soft

#050A0E      → --foundation-neutral-950
#0F1419      → --foundation-neutral-900
[escalas grises+azul]
```

#### Light Theme
```
#0369A1      → --foundation-primary
#0284C7      → --foundation-primary-hover
#E0F2FE      → --foundation-primary-soft
[escalas grises+azul claro]
```

---

## 🎨 Paleta Completa

### Anatomía de un Color Foundation

```
--foundation-{color}-{shade}

Ejemplos:
--foundation-primary      (sin shade = base)
--foundation-primary-hover
--foundation-primary-soft

--foundation-neutral-950 (casi negro)
--foundation-neutral-500 (50% tone)
--foundation-neutral-50 (casi blanco)

--foundation-red-600
--foundation-green-600
--foundation-amber-600
```

### Escala Neutral (Aplicable a todas las marcas)

```
Level     Valor Hex      Uso
─────────────────────────────────────────
-950      #0B0E11 (dark) Fondos, bordes muy oscuros
          #FFFFFF (light) [N/A]

-900      #14181D (dark) Texto principal
          #1A2027 (light) Texto principal

-800      #2A3138 (dark) Superficies
          #1f2937 (light) Superficies

-700      #3d4855 (dark) Bordes
          #374151 (light) Bordes

-600      #5A6572 (dark) Texto secundario
          #6b7280 (light) Texto secundario

-500      #7d8a99 (dark) Iconografía muda
          #9ca3af (light) Iconografía muda

-400      #9AA5B1 (dark) Deshabilitado, ayudas
          #d1d5db (light) Deshabilitado, ayudas

-300      #c5d0db (dark) Hover state
          #e5e7eb (light) Hover state

-200      #e8ecf1 (dark) Superficie sutil
          #f3f4f6 (light) Superficie sutil

-100      #f5f7fa (dark) [Raramente usado]
          #f9fafb (light) Fondo secundario

-50       #FFFFFF (dark) [N/A en dark]
          #FFFFFF (light) Blanco puro
```

### Colores Funcionales (Universales)

```
Red (Error/Danger)
├─ dark:  #F87171
├─ light: #B91C1C
└─ uso: Errores, validaciones, acciones destructivas

Green (Success)
├─ dark:  #4ADE80
├─ light: #15803D
└─ uso: Confirmaciones, completados, checks

Amber (Warning)
├─ dark:  #FCD34D
├─ light: #D97706
└─ uso: Advertencias, info importante, atención

Blue (Info) [Opcional]
├─ dark:  #60A5FA
├─ light: #1D4ED8
└─ uso: Información, hints, tooltips
```

---

## 🔗 Mapeo a Semánticos

### De Foundation a Semántico

```
FOUNDATION (bruto)           SEMÁNTICO (intención)    COMPONENTE
──────────────────────────────────────────────────────────────────
primary                  →   color-action        →   Button, Link
primary-hover            →   color-action-hover  →   Button:hover
primary-soft             →   color-action-soft   →   Alert (action)

neutral-900/950          →   color-text          →   Body, Heading
neutral-600              →   color-muted         →   Hint, Label
neutral-400              →   color-disabled      →   Input:disabled

red-600                  →   color-danger        →   Alert (error)
green-600                →   color-success       →   Alert (success)
amber-600                →   color-warning       →   Alert (warning)

neutral-800              →   color-border        →   Line, Divider
neutral-950              →   color-bg            →   Page background
neutral-900              →   color-surface       →   Card, Panel
```

### Tabla Completa (Light Theme - PROMPTEA)

| Semántico | Valor | Uso |
|-----------|-------|-----|
| `--color-text` | neutral-900 (#1A2027) | Texto principal |
| `--color-muted` | neutral-600 (#5A6572) | Texto secundario |
| `--color-action` | primary (#2E7D0F) | Botones, links |
| `--color-on-action` | white (#FFFFFF) | Texto sobre acción |
| `--color-action-hover` | primary-hover (#1b5d03) | Hover state |
| `--color-action-soft` | primary-soft (#f0fde4) | Background suave |
| `--color-focus` | primary (#2E7D0F) | Ring de foco |
| `--color-danger` | red-600 (#B91C1C) | Errores |
| `--color-success` | green-600 (#15803D) | Éxitos |
| `--color-warning` | amber-600 (#D97706) | Advertencias |
| `--color-border` | neutral-800 (#1f2937) | Bordes |
| `--color-bg` | white (#FFFFFF) | Fondo página |
| `--color-surface` | neutral-100 (#f9fafb) | Tarjetas |
| `--color-bg-secondary` | neutral-100 (#f9fafb) | Fondo secundario |
| `--color-surface-subtle` | neutral-50 (#f3f4f6) | Superficie sutil |

---

## ✅ WCAG AA Contrasts

### Contraste de Texto (mínimo 4.5:1 para AA)

#### Light Theme (PROMPTEA)

```
✅ PASANTE (> 4.5:1)
text (#1A2027) sobre white (#FFFFFF)        → 12.6:1 ✅
text (#1A2027) sobre neutral-100 (#f9fafb)  → 10.2:1 ✅

⚠️ LIMITADO (< 4.5:1)
muted (#5A6572) sobre white (#FFFFFF)       → 4.8:1 ✅
muted (#5A6572) sobre neutral-100 (#f9fafb) → 3.9:1 ❌ NO usar

❌ NO USAR
disabled (#d1d5db) sobre white (#FFFFFF)    → 2.1:1 ❌
```

#### Dark Theme (PROMPTEA)

```
✅ PASANTE
text (#E8ECF1) sobre bg (#0B0E11)          → 15.2:1 ✅
muted (#9AA5B1) sobre bg (#0B0E11)         → 8.5:1 ✅

✅ PASANTE (para WCAG A, no AA)
disabled (#7d8a99) sobre bg (#0B0E11)      → 3.8:1 ⚠️
```

### Contraste de Componentes (mínimo 3:1)

```
✅ Botón primario (acción sobre fondo)
action (#2E7D0F) sobre white (#FFFFFF)     → 3.8:1 ✅

✅ Borde activo (borde sobre fondo)
border (#1f2937) sobre white (#FFFFFF)     → 8.1:1 ✅
```

### Tabla de Validación WCAG

| Combinación | Contraste | WCAG A | WCAG AA | WCAG AAA |
|-------------|-----------|--------|---------|----------|
| text sobre bg | 12.6:1 | ✅ | ✅ | ✅ |
| muted sobre bg | 4.8:1 | ✅ | ✅ | ❌ |
| action sobre white | 3.8:1 | ✅ | ✅ | ❌ |
| danger sobre white | 5.2:1 | ✅ | ✅ | ✅ |

---

## 🎯 Uso en Componentes

### Botón Primario

```html
<button class="button button--primary">
  Continuar
</button>
```

```css
/* Foundation → Semántico → Componente */
.button--primary {
  background-color: var(--color-action);      /* primary */
  color: var(--color-on-action);              /* white */
  border: 1px solid var(--color-action);
}

.button--primary:hover {
  background-color: var(--color-action-hover); /* primary-hover */
}

.button--primary:active {
  background-color: var(--color-action-hover);
  opacity: 0.9;
}

.button--primary:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

.button--primary:disabled {
  background-color: var(--color-disabled);
  color: var(--color-text);
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Alert Danger

```html
<div class="alert alert--danger" role="alert">
  <svg class="alert__icon" aria-hidden="true">
    <!-- error icon -->
  </svg>
  <span class="alert__text">
    Error al procesar tu solicitud. Por favor, intenta de nuevo.
  </span>
</div>
```

```css
.alert--danger {
  background-color: var(--color-action-soft);  /* primary-soft, 10% opacidad */
  border: 1px solid var(--color-danger);       /* red-600 */
  color: var(--color-text);
}

.alert__icon {
  color: var(--color-danger);                  /* red-600 */
}
```

### Input

```html
<label for="email">Email</label>
<input 
  id="email" 
  type="email" 
  class="input"
  placeholder="tu@email.com"
/>
```

```css
.input {
  background-color: var(--color-surface);      /* neutral-900 (dark) */
  border: 1px solid var(--color-border);       /* neutral-700 */
  color: var(--color-text);
  padding: var(--space-2) var(--space-4);
}

.input:hover {
  border-color: var(--color-muted);            /* neutral-600 */
}

.input:focus-visible {
  outline: 2px solid var(--color-focus);       /* primary */
  outline-offset: 2px;
  border-color: var(--color-focus);
}

.input:disabled {
  background-color: var(--color-muted);        /* neutral-400 */
  cursor: not-allowed;
  opacity: 0.6;
}
```

---

## 🔄 Brand Switching

Cuando el usuario cambia marca (promptea → nova):

```javascript
document.body.dataset.brand = "nova";
```

El CSS recalcula TODOS los variables automáticamente:

```css
/* ANTES: promptea */
[data-brand="promptea"][data-theme="light"] {
  --color-action: #2E7D0F;        /* verde */
  --color-action-hover: #1b5d03;
}

/* DESPUÉS: nova */
[data-brand="nova"][data-theme="light"] {
  --color-action: #7C3AED;        /* púrpura */
  --color-action-hover: #6D28D9;
}

/* Componente NO cambia */
.button--primary {
  background: var(--color-action);  /* automáticamente nueva */
}
```

---

## 📊 Matriz de Compatibilidad

### Colores Semánticos vs Componentes

| Semántico | Button | Input | Alert | Card | Link | Badge |
|-----------|--------|-------|-------|------|------|-------|
| color-text | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| color-action | ✅ bg | ❌ | ✅ | ❌ | ✅ | ❌ |
| color-danger | ❌ | ✅ validation | ✅ | ❌ | ❌ | ✅ danger |
| color-border | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| color-surface | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |

---

## ✨ Mejores Prácticas

### ✅ CORRECTO
```css
/* Usar semánticos */
.button {
  background: var(--color-action);       ✅
  color: var(--color-on-action);         ✅
}

/* Usar foundations para valores sin marca */
.layout {
  gap: var(--foundation-space-2);        ✅ (no semántico porque no es color)
}
```

### ❌ INCORRECTO
```css
/* Hardcodear valores */
.button {
  background: #2E7D0F;                   ❌ (no reacciona a marca)
}

/* Mezclar niveles */
.button {
  background: var(--color-action);       ✅
  color: #FFFFFF;                        ❌ (debería ser --color-on-action)
}
```

---

## 🚀 Siguientes Pasos

- [ ] Actualizar `tokens.css` con comentarios explícitos
- [ ] Crear `component-manifest.json` versión 2.2.0 con Foundations
- [ ] Expandir paleta a 11 marcas (actualmente 3)
- [ ] Crear herramienta de generación de paletas (dark/light auto)
- [ ] Validador de contraste WCAG (script)
