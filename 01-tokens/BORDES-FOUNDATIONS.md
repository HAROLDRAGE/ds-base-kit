# 🔲 Bordes Foundations — Radio y Grosor de Bordes

**Versión:** 2.2.0  | **Actualizado:** 2026-07-09

---

## 🏛️ Estructura

```
FOUNDATIONS
├─ Ancho (border-width)
│  ├─ hairline (0.5px)
│  ├─ thin (1px)
│  ├─ base (2px)
│  └─ thick (4px)
│
└─ Radio (border-radius)
   ├─ none (0px)
   ├─ sm (4px)
   ├─ md (8px)
   ├─ lg (12px)
   ├─ xl (16px)
   ├─ 2xl (20px)
   └─ pill (999px)

    ↓

SEMÁNTICOS
├─ radius-button → md
├─ radius-card → lg
└─ border-width-input → thin

    ↓

COMPONENTES
├─ Button, Input, Card, Modal, Badge
```

---

## 📐 Border Width (Ancho de Borde)

### Escala

| Token | Valor | Uso |
|-------|-------|-----|
| `--foundation-border-width-hairline` | 0.5px | Divisores sutiles |
| `--foundation-border-width-thin` | 1px | Bordes normales |
| `--foundation-border-width-base` | 2px | Bordes destacados |
| `--foundation-border-width-thick` | 4px | Bordes muy visibles |

### Uso por Componente

```css
/* Input (borde normal) */
.input {
  border: var(--foundation-border-width-thin);
}

/* Alert (borde destacado) */
.alert {
  border-left: var(--foundation-border-width-base);
}

/* Divider (línea sutil) */
.divider {
  border-top: var(--foundation-border-width-hairline);
}

/* Card (borde importante) */
.card {
  border: var(--foundation-border-width-thin);
}
```

---

## 🔘 Border Radius (Radio de Esquinas)

### Escala

| Token | Valor | Forma | Uso |
|-------|-------|-------|-----|
| `--foundation-radius-none` | 0px | Cuadrado | UI rígida |
| `--foundation-radius-sm` | 4px | Muy ligero | Subtle |
| `--foundation-radius-md` | 8px | Redondeado | ⭐ Default |
| `--foundation-radius-lg` | 12px | Muy redondeado | Elevación |
| `--foundation-radius-xl` | 16px | Muy muy redondeado | Modales |
| `--foundation-radius-2xl` | 20px | Máximo | Contenedores |
| `--foundation-radius-pill` | 999px | Circular | Botones redondos |

### Uso por Componente

| Componente | Radio | Ejemplo |
|------------|-------|---------|
| Button | md (8px) | Botón rectangular |
| Input | md (8px) | Campo de texto |
| Card | lg (12px) | Tarjeta elevada |
| Modal | lg (12px) | Diálogo flotante |
| Badge | pill (999px) | Etiqueta redonda |
| Alert | md (8px) | Notificación |
| Dropdown | md (8px) | Menú desplegable |
| Tooltip | sm (4px) | Sugerencia |
| Avatar | pill (999px) | Foto circular |

### Ejemplos CSS

```css
/* Button con radio mediano */
.button {
  border-radius: var(--foundation-radius-md);  /* 8px */
}

/* Card con radio grande */
.card {
  border-radius: var(--foundation-radius-lg);  /* 12px */
}

/* Avatar circular */
.avatar {
  border-radius: var(--foundation-radius-pill);  /* 999px */
  width: var(--space-12);
  height: var(--space-12);
  overflow: hidden;
}

/* Modal flotante con radio máximo */
.modal {
  border-radius: var(--foundation-radius-lg);  /* 12px */
}

/* Badge con pill shape */
.badge {
  border-radius: var(--foundation-radius-pill);  /* 999px */
  padding: var(--space-1) var(--space-2);
}
```

---

## 🎯 Combinaciones

### Redondeado + Borde

```css
/* Card elegante */
.card {
  border: var(--foundation-border-width-thin);
  border-radius: var(--foundation-radius-lg);
  border-color: var(--color-border);
}

/* Input con énfasis en focus */
.input:focus-visible {
  border: var(--foundation-border-width-base);
  border-radius: var(--foundation-radius-md);
  border-color: var(--color-focus);
}
```

### Diferentes Radios por Lado

```css
/* Sólo esquinas superiores redondeadas */
.dropdown-menu {
  border-radius: 
    var(--foundation-radius-md)
    var(--foundation-radius-md)
    0
    0;
}

/* Todo redondeado excepto abajo */
.popover {
  border-radius:
    var(--foundation-radius-lg)
    var(--foundation-radius-lg)
    0
    0;
}
```

---

## 📊 Estado de Bordes

### Hover
```css
.card:hover {
  border-color: var(--color-muted);
  border-width: var(--foundation-border-width-thin);
}
```

### Focus
```css
.input:focus-visible {
  border-width: var(--foundation-border-width-base);
  border-color: var(--color-focus);
  outline: none;
}
```

### Disabled
```css
.input:disabled {
  border-color: var(--color-disabled);
  opacity: 0.5;
}
```

---

## ✅ Checklist

- ✅ Todos los bordes usan values de `--foundation-border-width-*`
- ✅ Todos los radios usan values de `--foundation-radius-*`
- ✅ Consistencia: Button = Input = Badge (radio)
- ✅ Card, Modal = radio mayor para jerarquía
- ✅ No usar valores hardcodeados (5px, 10px, etc.)
