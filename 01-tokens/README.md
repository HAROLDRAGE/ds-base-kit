# 📚 Tokens Foundations — Sistema Completo

**Versión:** 2.2.0  | **Estructura:** Primitivos → Foundations → Semánticos → Componentes

---

## 🗂️ Índice de Documentación

### 🏛️ Conceptos Base
- [FOUNDATIONS.md](./FOUNDATIONS.md) — **LÉE PRIMERO** — Conceptualización de 3 capas de tokens

### 🎨 Foundations por Categoría

#### 1. 🎨 **Color**
- [COLORES-FOUNDATIONS.md](./COLORES-FOUNDATIONS.md)
  - Paletas por marca (Promptea, Nova, Ocean)
  - Light/Dark themes
  - Mapeo a semánticos (color-action, color-text, etc.)
  - WCAG AA contrast validation
  - Uso en componentes (Button, Alert, Input)

#### 2. 📝 **Tipografía**
- [TIPOGRAFIA-FOUNDATIONS.md](./TIPOGRAFIA-FOUNDATIONS.md)
  - Familias (base, mono)
  - Pesos (300-800)
  - Tamaños (escala 0.75rem - 3rem)
  - Line heights y letter spacing
  - Presets semánticos (h1-h6, body, label, code)
  - Uso en componentes

#### 3. 📏 **Espaciado**
- [ESPACIADO-FOUNDATIONS.md](./ESPACIADO-FOUNDATIONS.md)
  - Escala 4px (base 4)
  - 11 niveles (0px - 64px)
  - Patrones: padding, margin, gap
  - Responsive adjustments
  - Stack, inline, cluster, grid, sidebar layouts

#### 4. 🔲 **Bordes**
- [BORDES-FOUNDATIONS.md](./BORDES-FOUNDATIONS.md)
  - Ancho: hairline, thin, base, thick
  - Radio: none, sm, md, lg, xl, 2xl, pill
  - Uso por componente (Button=md, Card=lg, etc.)
  - Estados (hover, focus, disabled)

#### 5. 🌙 **Sombras**
- [SOMBRAS-FOUNDATIONS.md](./SOMBRAS-FOUNDATIONS.md)
  - Escala: sm, md, lg, xl, 2xl
  - Opacidades: 5%, 10%, 25%
  - Jerarquía visual
  - Estados (normal, hover, active)
  - Dark vs Light theme

#### 6. ⚡ **Movimiento**
- [MOVIMIENTO-FOUNDATIONS.md](./MOVIMIENTO-FOUNDATIONS.md)
  - Duración: fast (120ms), base (240ms), slow (400ms)
  - Easing: linear, in, out, in-out
  - Transiciones vs animaciones
  - Motion feedback
  - Respeto a prefers-reduced-motion

#### 7. 📐 **Layout**
- [LAYOUT-FOUNDATIONS.md](./LAYOUT-FOUNDATIONS.md)
  - Breakpoints: xs, sm, md, lg, xl, 2xl
  - Grid columns por viewport
  - Touch targets: 44px (mobile), 32px (desktop)
  - Safe areas (notch devices)
  - Density (compact, normal, comfortable)
  - Patrones de layout

#### 8. 🎨 **Iconografía**
- [ICONOGRAFIA-FOUNDATIONS.md](./ICONOGRAFIA-FOUNDATIONS.md)
  - Tamaños: xs, sm, md, lg, xl
  - Stroke: thin, base, thick
  - Color: inherit, currentColor, explicit
  - Alineamiento y responsividad
  - Accesibilidad WCAG

---

## 🔄 Arquitectura de Capas

```
NIVEL 1: PRIMITIVOS
   valores brutos: #2E7D0F, 4px, 1rem, cubic-bezier(...)
           ↓
NIVEL 2: FOUNDATIONS
   tokens agnósticos: --foundation-primary, --foundation-space-4
           ↓
NIVEL 3: SEMÁNTICOS
   tokens con propósito: --color-action, --space-button-padding-y
           ↓
NIVEL 4: COMPONENTES
   UI real: <button>, <card>, <input>
```

---

## 📊 Tabla de Correspondencia

### Capa 1: PRIMITIVOS
```
#2E7D0F         (color hex promptea)
4px             (distancia base)
1rem            (tamaño de fuente)
cubic-bezier... (función de animación)
```

### Capa 2: FOUNDATIONS
```
--foundation-primary: #2E7D0F
--foundation-space-4: 16px
--foundation-typography-size-base: 1rem
--foundation-motion-easing-out: cubic-bezier(...)
```

### Capa 3: SEMÁNTICOS
```
--color-action: var(--foundation-primary)
--space-button-padding-x: var(--foundation-space-4)
--typography-body-base: var(--foundation-typography-size-base)
--motion-button-transition: var(--foundation-motion-fast) var(--foundation-motion-easing-out)
```

### Capa 4: COMPONENTES
```css
.button--primary {
  background: var(--color-action);
  padding: 0 var(--space-button-padding-x);
  font-size: var(--typography-body-base);
  transition: background var(--motion-button-transition);
}
```

---

## 🎯 Fundamentos Documentados

### Colores
| Tipo | Count | Status |
|------|-------|--------|
| Primarios (1 por marca) | 3 | ✅ |
| Neutros (escala -900 a -50) | 11 | ✅ |
| Funcionales (rojo, verde, amarillo) | 9 | ✅ |
| Extended (hover, soft, secondary) | 10+ | ✅ |
| **Total** | **33+** | **✅** |

### Tipografía
| Tipo | Count | Status |
|------|-------|--------|
| Familias | 2 | ✅ |
| Pesos | 6 | ✅ |
| Tamaños | 9 | ✅ |
| Line Heights | 4 | ✅ |
| Letter Spacing | 4 | ✅ |
| Presets (h1-6, body, label) | 10 | ✅ |
| **Total** | **35+** | **✅** |

### Espaciado
| Tipo | Count | Status |
|------|-------|--------|
| Escala (0-16) | 11 | ✅ |
| Padding patterns | 5 | ✅ |
| Gap patterns | 4 | ✅ |
| Margin patterns | 3 | ✅ |
| **Total** | **23** | **✅** |

### Bordes
| Tipo | Count | Status |
|------|-------|--------|
| Ancho | 4 | ✅ |
| Radio | 7 | ✅ |
| Combinaciones | 8+ | ✅ |
| **Total** | **19+** | **✅** |

### Sombras
| Tipo | Count | Status |
|------|-------|--------|
| Escala | 5 | ✅ |
| Por tema (dark/light) | 5 | ✅ |
| **Total** | **5** | **✅** |

### Movimiento
| Tipo | Count | Status |
|------|-------|--------|
| Duración | 3 | ✅ |
| Easing | 4 | ✅ |
| Presets (button, modal, etc.) | 5+ | ✅ |
| **Total** | **12+** | **✅** |

### Layout
| Tipo | Count | Status |
|------|-------|--------|
| Breakpoints | 6 | ✅ |
| Touch targets | 2 | ✅ |
| Safe areas | 4 | ✅ |
| Density | 3 | ✅ |
| **Total** | **15** | **✅** |

### Iconografía
| Tipo | Count | Status |
|------|-------|--------|
| Tamaños | 5 | ✅ |
| Stroke | 3 | ✅ |
| Color strategies | 5 | ✅ |
| **Total** | **13** | **✅** |

---

## 🚀 Uso Rápido

### Para Diseñadores
1. Lee [FOUNDATIONS.md](./FOUNDATIONS.md) para conceptos
2. Lee [COLORES-FOUNDATIONS.md](./COLORES-FOUNDATIONS.md) para paleta
3. Lee [TIPOGRAFIA-FOUNDATIONS.md](./TIPOGRAFIA-FOUNDATIONS.md) para fuentes
4. Usa tokens semánticos en Figma: `--color-action`, `--space-4`, etc.

### Para Desarrolladores
1. Lee [FOUNDATIONS.md](./FOUNDATIONS.md) para arquitectura
2. Inspecciona [tokens.css](./tokens.css) para valores brutos
3. Usa tokens en CSS: `background: var(--color-action);`
4. Consulta la categoría específica para detalles

### Para Managers/Stakeholders
1. Lee sección "Arquitectura de Capas" de [FOUNDATIONS.md](./FOUNDATIONS.md)
2. Mira tabla de correspondencia aquí
3. Verifica documentación es exhaustiva: **33+ colores, 35+ tipografía, 23 espaciado, 5 sombras, 12 movimiento, 15 layout, 13 iconografía**

---

## 📋 Validation Checklist

- ✅ Todos los Foundations documentados (8 categorías)
- ✅ Cada Foundation tiene: descripción, escala, uso, ejemplos
- ✅ Cada Foundation mapea a tokens semánticos
- ✅ Cada semántico mapea a componentes
- ✅ Colores con validación WCAG AA
- ✅ Espaciado en escala 4px (múltiplos)
- ✅ Bordes y radios por componente
- ✅ Sombras con jerarquía clara
- ✅ Movimiento respetuoso (prefers-reduced-motion)
- ✅ Layout responsive (mobile-first)
- ✅ Iconografía accesible

---

## 🔗 Archivos Relacionados

- [COLORES.md](./COLORES.md) — Guía semántica de colores (legacy)
- [ESPACIADO.md](./ESPACIADO.md) — Guía semántica de espaciado (legacy)
- [tokens.css](./tokens.css) — Implementación CSS (todas las capas)
- [tokens.json](./tokens.json) — Exportación JSON
- [../05-agentes/component-manifest.json](../05-agentes/component-manifest.json) — SSOT de sistema

---

**Última actualización:** 2026-07-09  
**Versión:** 2.2.0
