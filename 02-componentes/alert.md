# Alert

**Categoría:** Molecule | **Estado:** v2.2.0 | **Última actualización:** 2026-07-09

---

## 🎯 Cuándo Usarlo

### Casos de Uso

- Mensajes informativos que requieren atención
- Notificaciones de error, warning, success
- Feedback del sistema al usuario

### No Usarlo Para

- Para confirmaciones destructivas (usar Modal)
- Para notificaciones transitorias (usar Toast)
- Para contenido principal (usar Card)

---

## 📐 Anatomía

### Estructura

```html
<div class='alert alert--success'>
  <i class='icon icon-check'></i>
  <p class='alert__message'>Operación completada</p>
  <button class='alert__close' aria-label='Cerrar'>&times;</button>
</div>
```

### Partes Principales

- Trigger/Control
- Container
- Content

---

## 🎭 Estados

### Estados del Componente

| Estado | Descripción | Interacción |
|--------|-------------|------------|
| default | Descripción | Interacción |
| with-icon | Descripción | Interacción |
| dismissible | Descripción | Interacción |
| with-title | Descripción | Interacción |

### Ejemplos Visuales

Ver ejemplos en sección de código

---

## 🎨 Variaciones

### Por Tamaño

- Compacto: `var(--dimension-space-5)`
- Estándar: `var(--dimension-space-6)`

### Por Tipo/Intención

- Variantes según tipo: def

---

## ♿ Accesibilidad (WCAG 2.2 AA)

### Requisitos

- ✅ Contraste mínimo: 4.5:1 para texto, 3:1 para componentes
- ✅ Touch target: `var(--layout-touch-target-min)` en móvil y `var(--layout-touch-target-desktop)` en escritorio
- ✅ Teclado: Tab, Enter/Space, Escape accesibles
- ✅ Screen reader: aria-label, aria-describedby, role descriptivos
- ✅ Motion: Respeta prefers-reduced-motion

### Implementación


- Usar `role` descriptivo (button, alert, etc.)
- Incluir `aria-label` o `aria-describedby`
- Cumplir contraste 4.5:1 (texto) / 3:1 (UI)
- Soportar navegación por teclado completa


---

## 📦 Tokens Utilizados

### Colores

| Token | Uso |
|-------|-----|
| --color-success | Uso en alert |
| --color-error | Uso en alert |
| --color-warning | Uso en alert |
| --color-info | Uso en alert |

### Espaciado

| Token | Uso |
|-------|-----|
| --space-3 | Espaciado interno/externo |
| --space-4 | Espaciado interno/externo |
| --space-5 | Espaciado interno/externo |

### Tipografía

| Token | Uso |
|-------|-----|
| --typography-body-base | Texto del componente |

### Otras Propiedades

- Border radius: `--radius-md`
- Shadow: `--shadow-sm` (on hover)

---

## 💻 Código

### HTML

```html
<!-- Ejemplo: alert -->
<div class='alert alert--success'>
  <i class='icon icon-check'></i>
  <p class='alert__message'>Operación completada</p>
  <button class='alert__close' aria-label='Cerrar'>&times;</button>
</div>

```

### CSS (Tokens Semánticos)

```css
.alert {
  padding: var(--space-4);
  background: var(--color-neutral-50);
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-md);
  font-family: var(--typography-base);
}

.alert:hover {
  box-shadow: var(--shadow-sm);
}

.alert:focus {
  outline: 2px solid var(--color-action);
  outline-offset: 2px;
}

```

### JavaScript

```javascript
// Inicializar alert
const alertElements = document.querySelectorAll('.alert');

alertElements.forEach(element => {
  // Agregar event listeners
  element.addEventListener('click', handleClick);
  element.addEventListener('keydown', handleKeydown);
});

function handleClick(event) {
  // Lógica de interacción
}

function handleKeydown(event) {
  // Soporte para teclado (Enter, Space, Escape)
}

```

---

## 📱 Responsive

### Mobile (xs: 320px)


- Stack vertical
- Touch target: `var(--layout-touch-target-min)`
- Font size aumentado
- Espaciado adaptado


### Desktop (lg: 1024px+)


- Layout horizontal
- Touch target: `var(--layout-touch-target-desktop)`
- Font size normal
- Espaciado normal


---

## ✅ Do's & Don'ts

### Do's

- ✅ Usar tokens semánticos para colores y espaciado
- ✅ Incluir estados hover, focus, active, disabled
- ✅ Validar accesibilidad con teclado y screen reader
- ✅ Respetar prefers-reduced-motion
- ✅ Usar `var(--layout-touch-target-min)` en móvil

### Don'ts

- ❌ No usar colores hardcodeados
- ❌ No omitir estados visuales
- ❌ No usar solo color para comunicar estado (agregar icono)
- ❌ No ignorar contraste WCAG AA
- ❌ No hacer componentes más pequeños que `var(--layout-touch-target-desktop)` en escritorio

---

## 🔗 Relaciones

### Componentes Relacionados

- [Card (container hermano)](#)
- [Button (acción relacionada)](#)

### Patrones que Lo Utilizan

- [Formularios](#)
- [Navegación](#)

---

## 📚 Referencias

- [AGENT-CONTRACT.md](../05-agentes/AGENT-CONTRACT.md)
- [component-manifest.json](../05-agentes/component-manifest.json)
- [Foundations](../00-fundamentos/FOUNDATIONS.md)
- [WCAG 2.2 AA Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)

---

**Versión:** 2.2.0 | **Última actualización:** 2026-07-09
