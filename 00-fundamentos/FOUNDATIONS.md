# 🎨 Foundations — Sistema de Diseño Base

**Versión:** 2.2.0  
**Estado:** ✅ Definición exhaustiva de capas de tokens

---

## 📐 ¿Qué son Foundations?

**Foundations** es la capa base del sistema de tokens. Define las **decisiones de diseño fundamentales** sin contexto de aplicación: colores, tipografía, espaciado, bordes, sombras, movimiento.

```
PRIMITIVOS (Raw Values)
    ↓ (se combinan en)
FOUNDATIONS (Base Tokens)
    ↓ (se aplican como)
SEMÁNTICOS (Intención de Uso)
    ↓ (se componen en)
COMPONENTES (UI)
```

---

## 🏛️ Las 3 Capas de Tokens

### 1️⃣ **PRIMITIVOS** — Valores brutos, sin contexto

**¿Qué son?**  
Números, porcentajes, códigos hex, valores CSS puros. NO tienen nombre semántico.

**Ejemplos:**
```css
/* Valores brutos — sin contexto */
0.75rem      /* tamaño */
0.75          /* opacidad */
#0B0E11       /* color hex */
4px           /* distancia */
0.4, 0, 1, 1  /* curve de animación */
```

**Cuándo usarlos:**
- ❌ **Nunca directamente en componentes**
- ✅ Solo como base para Foundations
- ✅ En scripts de generación de tokens

### 2️⃣ **FOUNDATIONS** — Tokens base, sin marca

**¿Qué son?**  
Tokens **agnósticos de marca**, que definen la estructura pero no el color específico.

**Categorías:**

#### 🎨 **Colores Foundations**
```css
/* NO son color-action, color-text (esos son semánticos)
   SON bloques de color nombrados por valor/rol */

--foundation-color-primary: <color>    /* Color principal del sistema */
--foundation-color-secondary: <color>  /* Color secundario */
--foundation-color-neutral-900: <color> /* Neutral muy oscuro (para dark) */
--foundation-color-neutral-50: <color>  /* Neutral muy claro (para light) */
```

**Propósito:** Permitir que cada marca (promptea, nova, ocean) defina sus propios colores primarios, pero todos usen la misma **estructura de token**.

#### 📝 **Tipografía Foundations**
```css
--foundation-font-family-base: <font-stack>
--foundation-font-family-mono: <font-stack>
--foundation-font-weight-light: 300
--foundation-font-weight-regular: 400
--foundation-font-weight-bold: 700
--foundation-typography-size-base: 1rem
--foundation-typography-line-height-normal: 1.5
```

**Propósito:** Define las **familias y escalas**, pero sin intención de uso. Un heading puede ser cualquier tamaño.

#### 📏 **Espaciado Foundations**
```css
--foundation-space-0: 0px
--foundation-space-1: 4px
--foundation-space-2: 8px
--foundation-space-4: 16px  /* base = 4px × 4 */
```

**Propósito:** Escala uniforme, base 4px. Todos los componentes comparten la misma escala.

#### 🔲 **Bordes Foundations**
```css
--foundation-border-width-thin: 1px
--foundation-border-width-base: 2px
--foundation-radius-sm: 4px
--foundation-radius-md: 8px
```

#### 🌙 **Sombras Foundations**
```css
--foundation-shadow-sm: 0 1px 2px ...
--foundation-shadow-md: 0 4px 6px ...
```

#### ⚡ **Movimiento Foundations**
```css
--foundation-motion-fast: 120ms
--foundation-motion-base: 240ms
--foundation-motion-easing-in-out: cubic-bezier(...)
```

---

### 3️⃣ **SEMÁNTICOS** — Tokens con intención de uso

**¿Qué son?**  
Tokens que **aplican decisiones de Foundations a un propósito específico**.

**Ejemplos:**
```css
/* Semántico = Foundations + Intención */
--color-text: var(--foundation-color-neutral-900)  /* usar para texto */
--color-action: var(--foundation-color-primary)    /* usar para acciones */
--color-danger: var(--foundation-color-red-600)    /* usar para errores */
--space-button-padding: var(--foundation-space-2) var(--foundation-space-4)
--typography-heading-h1: ...
```

**Propósito:** Los **componentes SOLO usan tokens semánticos**. Proporcionan garantía de:
- ✅ Uso correcto (no confundir color de texto con color de acción)
- ✅ Coherencia (todos los botones usan el mismo espacio)
- ✅ Flexibilidad (cambiar tema sólo actualiza semánticos)

---

## 🎯 Foundations Organizados por Categoría

### 1. **Color Foundations**

#### Estructura
```
├─ Primarios (1 por marca)
│  ├─ primary (color marca, ej: verde para promptea)
│  ├─ primary-hover (más saturado o más oscuro)
│  └─ primary-soft (versión muy desaturada)
│
├─ Neutros (para contrast)
│  ├─ neutral-900/800/700...100 (escala completa, más oscuro a más claro)
│  ├─ neutral-50 (casi blanco)
│  └─ neutral-950 (casi negro)
│
├─ Funcionales (rojo, verde, amarillo para estados)
│  ├─ red-600, green-600, amber-600
│  └─ Versiones hover/soft de cada uno
│
└─ Especiales
   ├─ focus-ring (color del anillo de foco)
   └─ success, warning, error (pueden mapear a rojo/verde/amarillo)
```

#### Por Marca
```
PROMPTEA
├─ primary: #2E7D0F (verde oscuro light)
├─ primary: #7CE83A (verde brillante dark)
└─ primeros: neutrales grises

NOVA
├─ primary: #A78BFA (púrpura claro)
└─ primeros: neutrales púrpura-tinted

OCEAN
├─ primary: #0EA5E9 (azul agua)
└─ primeros: neutrales azul-tinted
```

#### Intención de Uso en Semánticos
```
Color Semántico          → Mapea a Foundation
--color-text             → neutral-900 (light) o neutral-50 (dark)
--color-action           → primary (marca)
--color-action-hover     → primary-hover
--color-danger           → red-600
--color-success          → green-600
--color-warning          → amber-600
```

---

### 2. **Tipografía Foundations**

#### Familias (Sin marca)
```
--foundation-font-family-base
  = -apple-system, BlinkMacSystemFont, 'Segoe UI', ...
  Propósito: Legible, humanista, accesible en web

--foundation-font-family-mono
  = 'Fira Code', 'Courier New', ...
  Propósito: Código, snippets, componentes técnicos
```

#### Weights (Estructura universal)
```
Light        300  → Texto muy desenfatizado
Regular      400  → Cuerpo estándar
Medium       500  → Énfasis moderado (labels)
Semibold     600  → Énfasis fuerte (botones, subtítulos)
Bold         700  → Muy enfatizado (headings)
Extrabold    800  → Máximo énfasis (títulos h1)
```

#### Tamaños (Escala modulada, base 1rem)
```
xs      0.75rem   (12px)  → badges, hints
sm      0.875rem  (14px)  → labels, small text
base    1rem      (16px)  → cuerpo estándar
lg      1.125rem  (18px)  → subtítulos
xl      1.25rem   (20px)  → headings medianos
...
5xl     3rem      (48px)  → heading h1
```

#### Line Heights (Según contenido)
```
tight    1.2   → Headings compactos
normal   1.5   → Cuerpo estándar
relaxed  1.75  → Párrafos largos
loose    2.0   → Muy espaciado
```

#### Intención de Uso en Semánticos
```
--typography-heading-h1
  = size-5xl (3rem) +
    weight-extrabold (800) +
    line-height-tight (1.2)

--typography-body-base
  = size-base (1rem) +
    weight-regular (400) +
    line-height-normal (1.5)
```

---

### 3. **Espaciado Foundations**

#### Escala (Base 4px, múltiplos)
```
0   → 0px      (sin espacio)
1   → 4px      (mínimo)
2   → 8px      (pequeño)
3   → 12px     (mediano-pequeño)
4   → 16px     (base, estándar)
5   → 20px     (mediano)
6   → 24px     (mediano-grande)
8   → 32px     (grande)
10  → 40px     (muy grande)
12  → 48px     (extra grande)
16  → 64px     (máximo)
```

#### Propósito
- ✅ Consistencia: Todos los espacios son múltiplos de 4px
- ✅ Escala: Crecimiento predecible
- ✅ Memoria: Fácil de recordar

#### Intención de Uso en Semánticos
```
--space-button-padding    → 2 4  (8px 16px)
--space-card-padding      → 4 6  (16px 24px)
--space-component-gap     → 2    (8px entre elementos)
--space-section-margin    → 12   (48px entre secciones)
```

---

### 4. **Bordes Foundations**

#### Ancho
```
hairline  0.5px  → Bordes muy sutiles (divisores)
thin      1px    → Bordes normales
base      2px    → Bordes destacados
thick     4px    → Bordes muy importantes
```

#### Radio (Esquinas)
```
none      0px    → Cuadrado
sm        4px    → Ligeramente redondeado
md        8px    → Redondeado (default)
lg        12px   → Muy redondeado
xl        16px   → Muy muy redondeado
2xl       20px   → Máximo redondeado
pill      999px  → Circular (botones redondos)
```

#### Intención de Uso en Semánticos
```
--radius-button      → md (8px)
--radius-input       → md (8px)
--radius-card        → lg (12px)
--radius-modal       → lg (12px)
--radius-badge       → pill (999px)
```

---

### 5. **Sombras Foundations**

#### Escala
```
sm    → 1px 2px, opacidad 5%   (sutil)
md    → 4px 6px, opacidad 10%  (normal)
lg    → 10px 15px, opacidad 10% (elevado)
xl    → 20px 25px, opacidad 10% (muy elevado)
2xl   → 25px 50px, opacidad 25% (flotante)
```

#### Propósito
- Crear jerarquía visual (elevación)
- Indicar interactividad
- Separar componentes

#### Intención de Uso en Semánticos
```
--shadow-button       → sm (hover)
--shadow-card         → md (base)
--shadow-modal        → xl (flotante)
--shadow-tooltip      → md (flotante)
```

---

### 6. **Movimiento Foundations**

#### Duración
```
fast    120ms   → Feedback inmediato (hover, focus)
base    240ms   → Transiciones estándar
slow    400ms   → Animaciones complejas
```

#### Easing
```
linear     → Cambio constante
in         → Aceleración (empieza lento)
out        → Desaceleración (termina lento)
in-out     → Aceleración + desaceleración (natural)
```

#### Intención de Uso en Semánticos
```
--motion-button-transition  → fast ease-out
--motion-modal-entrance     → base ease-in-out
--motion-dropdown-exit      → fast ease-out
```

---

### 7. **Layout Foundations**

#### Breakpoints (Responsividad)
```
xs   320px   → Móvil pequeño
sm   480px   → Móvil grande
md   768px   → Tablet
lg   1024px  → Desktop pequeño
xl   1280px  → Desktop
2xl  1536px  → Desktop grande
```

#### Grid
```
mobile       1 col   → Móvil
tablet       2 cols  → Tablet
desktop      3 cols  → Desktop
```

#### Touch Targets (WCAG)
```
mobile       44px × 44px  → Dedos (recomendado)
desktop      32px × 32px  → Mouse
```

#### Contenedor
```
max-width    1280px  → Máximo ancho contenido
padding      16px    → Padding lateral en móvil
```

---

### 8. **Iconografía Foundations**

#### Tamaños
```
xs   16px  → Inline en texto, badges
sm   20px  → Labels, inputs
md   24px  → Botones estándar
lg   32px  → Headings
xl   48px  → Secciones
```

#### Stroke
```
thin     1px   → Iconografía delgada
base     1.5px → Iconografía normal
thick    2px   → Iconografía gruesa
```

#### Color
```
Inherit      → Del contenedor
Current      → Color actual (CSS currentColor)
Explicit     → Color definido en foundation
```

#### Intención de Uso en Semánticos
```
--icon-size-button      → sm (20px)
--icon-size-input       → sm (20px)
--icon-size-heading     → lg (32px)
--icon-stroke-normal    → base (1.5px)
```

---

## 🔗 Relación Foundations → Semánticos → Componentes

### Ejemplo: Botón Primario

```
FOUNDATIONS (raw building blocks)
├─ primary color: #2E7D0F
├─ weight-semibold: 600
├─ space-2: 8px
├─ space-4: 16px
├─ radius-md: 8px
└─ motion-fast: 120ms

    ↓ APLICACIÓN SEMÁNTICA

SEMÁNTICOS (propósito definido)
├─ --color-action: var(--primary)          ← fondo
├─ --color-on-action: white                ← texto sobre fondo
├─ --space-button-padding-y: var(--space-2) ← padding vertical
├─ --space-button-padding-x: var(--space-4) ← padding horizontal
├─ --radius-button: var(--radius-md)
└─ --motion-button: var(--motion-fast) ease-out

    ↓ COMPOSICIÓN EN COMPONENTE

COMPONENTE: Button
```html
<button class="button button--primary">
  Acción
</button>
```

```css
.button--primary {
  background: var(--color-action);
  color: var(--color-on-action);
  padding: var(--space-button-padding-y) var(--space-button-padding-x);
  border-radius: var(--radius-button);
  transition: background var(--motion-button);
}

.button--primary:hover {
  background: var(--color-action-hover);
}
```
```

---

## 📊 Matriz de Correspondencia

| Categoría | Foundation | Semántico | Componente |
|-----------|-----------|-----------|-----------|
| **Color** | primary | color-action | Button, Link, Alert |
| **Color** | neutral-900 | color-text | Body, Heading, Label |
| **Tipo** | size-base | typography-body | Paragraph, Label |
| **Tipo** | weight-bold | typography-heading | H1-H6 |
| **Espacio** | space-4 | space-button-padding | Button, Input |
| **Espacio** | space-2 | space-component-gap | Flex/Grid |
| **Borde** | radius-md | radius-button | Button, Input |
| **Sombra** | shadow-md | shadow-card | Card, Dropdown |
| **Motion** | motion-fast | motion-button-transition | Hover, Focus |

---

## 🎨 Estructura en CSS

```css
:root {
  /* PRIMITIVOS (raw values, nunca usar directamente) */
  --primitive-size-base: 1rem;
  
  /* FOUNDATIONS (agnóstico de marca) */
  --foundation-font-family-base: system fonts;
  --foundation-space-4: 16px;
  --foundation-radius-md: 8px;
  --foundation-primary: (no definido en :root, varía por marca)
  
  /* Algunos Foundations SÍ tienen valor en :root */
  --foundation-motion-fast: 120ms;
  --foundation-motion-easing-out: cubic-bezier(...);
}

[data-brand="promptea"][data-theme="light"] {
  /* Foundations color para esta marca/tema */
  --foundation-primary: #2E7D0F;
  --foundation-neutral-900: #1A2027;
  
  /* SEMÁNTICOS (aplican Foundations) */
  --color-action: var(--foundation-primary);
  --color-text: var(--foundation-neutral-900);
}
```

---

## ✅ Checklist de Foundations

### En Documentación
- ✅ Cada Foundation tiene descripción de qué es
- ✅ Cada Foundation tiene ejemplos de valores
- ✅ Cada Foundation enumera casos de uso
- ✅ Cada Foundation mapea a token(s) semántico(s)

### En CSS
- ✅ Primitivos en comentarios documentados
- ✅ Foundations con prefijo `--foundation-`
- ✅ Semánticos sin prefijo o con prefijo `--color-`, `--space-`, etc.
- ✅ Comentarios explícitos separando capas

### En Manifest
- ✅ Estructura foundations separada de semánticos
- ✅ Cada Foundation con use/not_for
- ✅ Mapeo explícito a semánticos

---

## 🚀 Siguientes Pasos

1. ✅ Documentar qué son Foundations (este archivo)
2. 📝 Expandir cada categoría en archivos separados:
   - `COLORES-FOUNDATIONS.md`
   - `TIPOGRAFIA-FOUNDATIONS.md`
   - `ESPACIADO-FOUNDATIONS.md`
   - etc.
3. 🔧 Actualizar `component-manifest.json` con estructura de Foundations
4. 🎨 Actualizar `tokens.css` con comentarios de Foundations
5. 📊 Crear `FOUNDATIONS-MATRIX.json` con mapeo completo

---

## 📚 Referencias

- [COLORES.md](../01-tokens/COLORES.md) — Tokens de color semánticos
- [ESPACIADO.md](../01-tokens/ESPACIADO.md) — Tokens de espaciado semánticos
- [component-manifest.json](../05-agentes/component-manifest.json) — SSOT
- [tokens.css](../01-tokens/tokens.css) — Implementación CSS
