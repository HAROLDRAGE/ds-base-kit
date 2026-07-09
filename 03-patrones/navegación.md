# Patrón: Navegación

**Última actualización:** 2026-07-09 | **Version:** 2.2.0

---

## 🎯 Cuándo Usarlo

La navegación es el mapa que guía a los usuarios por la experiencia. Usa este patrón cuando necesites:

- ✅ Permitir acceso a todas las secciones principales
- ✅ Mostrar dónde está el usuario en la estructura
- ✅ Mantener consistencia entre páginas
- ✅ Facilitar búsqueda de contenido

### No Usarlo Para

- ❌ Compartir contenido en redes (usar share buttons)
- ❌ Filtros secundarios (usar dropdowns o panels)
- ❌ Historial de pasos completados (usar breadcrumbs)

---

## 📐 Estructura

```
┌─ Header ─────────────────────────────────┐
│ Logo  [Nav items]  [Theme] [User menu]   │
└──────────────────────────────────────────┘
│ Navbar                                   │
│  [Home] [Docs] [About] [Contact]        │
└──────────────────────────────────────────┘
│ Sidebar (optional)                       │
│ • Sección 1                              │
│   └─ Subsección 1.1                      │
│   └─ Subsección 1.2                      │
│ • Sección 2                              │
└──────────────────────────────────────────┘
```

---

## 🏗️ Componentes que Lo Componen

| Componente | Rol | Cantidad |
|-----------|-----|----------|
| **Navbar** | Navegación principal horizontal | 1 |
| **Link** | Elementos individuales de navegación | N |
| **Badge** | Indicadores (notificaciones, count) | 0+ |
| **Dropdown** | Menús desplegables (user, language) | 0+ |
| **Breadcrumb** | Ruta actual | 0-1 |
| **Icon** | Iconos de sección | 0+ |
| **Button** | Cerrar sidebar, toggle | 0+ |

---

## 🎭 Variaciones

### Desktop (lg+)

```
┌─────────────────────────────────────┐
│ Logo | Home Docs About Contact      │  ← Navbar horizontal
└─────────────────────────────────────┘
│ Breadcrumb > Current > Page         │  ← Ubicación actual
├──────────────────────────────────────┤
│ Sidebar    │  Main Content          │
│ • Docs     │                        │
│   ├─ Intro│  ...                   │
│   └─ API  │                        │
│ • Blog     │                        │
└──────────────────────────────────────┘
```

### Mobile (xs-md)

```
┌────────────────────────────────┐
│ [☰] Logo        [Theme] [User] │  ← Hamburger menu
└────────────────────────────────┘
│ Breadcrumb > Current > Page    │
├────────────────────────────────┤
│ Sidebar Overlay (cuando abierto):
│ • Docs
│   ├─ Intro
│   └─ API
│ • Blog
│ • Contact
│
│ Main Content (debajo)
└────────────────────────────────┘
```

---

## ♿ Accesibilidad (WCAG 2.2 AA)

### Requisitos Críticos

- ✅ `<nav>` con `aria-label` descriptivo ("Main navigation", "Sidebar navigation")
- ✅ `<a>` o `<button>` con estado `aria-current="page"` en página actual
- ✅ Teclado: Tab para navegar, Enter para activar links
- ✅ Contraste 4.5:1 en texto, 3:1 en iconos
- ✅ Touch target: 44px en mobile, 32px en desktop
- ✅ Sidebar overlay: Escape para cerrar, trap foco

### Implementación

```html
<!-- Navbar principal -->
<nav aria-label="Main navigation" class="navbar">
  <a href="/" class="navbar__logo" aria-label="Home">Logo</a>
  <ul class="navbar__menu" role="menubar">
    <li role="none">
      <a href="/docs" role="menuitem" aria-current="page">Docs</a>
    </li>
    <li role="none">
      <a href="/blog" role="menuitem">Blog</a>
    </li>
  </ul>
</nav>

<!-- Sidebar navigation -->
<aside aria-label="Sidebar navigation" class="sidebar">
  <nav>
    <ul>
      <li>
        <a href="/docs/intro" aria-current="page">Intro</a>
      </li>
      <li>
        <a href="/docs/api">API</a>
      </li>
    </ul>
  </nav>
</aside>

<!-- Breadcrumb -->
<nav aria-label="Breadcrumb" class="breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/docs">Docs</a></li>
    <li aria-current="page">Getting Started</li>
  </ol>
</nav>
```

---

## 📦 Tokens Utilizados

### Colores
| Token | Uso |
|-------|-----|
| `--color-action` | Links activos, hover |
| `--color-text` | Texto de navegación |
| `--color-muted` | Links no activos |
| `--color-border` | Divisores, líneas |
| `--color-surface` | Fondo de navbar/sidebar |

### Espaciado
| Token | Uso |
|-------|-----|
| `--space-4` | Padding interno de items |
| `--space-5` | Gap entre items |
| `--space-6` | Padding de navbar/sidebar |

### Tipografía
| Token | Uso |
|-------|-----|
| `--typography-body-base` | Texto de items |
| `--typography-body-small` | Labels secundarios |

### Otras
| Token | Uso |
|-------|-----|
| `--radius-md` | Radius en hover |
| `--shadow-sm` | Dropdown shadow |

---

## 💻 Código Ejemplo

### HTML

```html
<header class="header">
  <nav aria-label="Primary navigation" class="navbar">
    <a href="/" class="navbar__logo">
      <img src="logo.svg" alt="Design System" />
    </a>
    
    <button class="navbar__toggle" id="sidebarToggle" aria-label="Toggle menu">
      <span class="icon">☰</span>
    </button>

    <ul class="navbar__menu" role="menubar">
      <li><a href="/docs" role="menuitem">Docs</a></li>
      <li><a href="/components" role="menuitem">Components</a></li>
      <li><a href="/about" role="menuitem">About</a></li>
    </ul>

    <div class="navbar__actions">
      <button id="themeBtn" class="navbar__theme">🌙</button>
      <button class="navbar__user" aria-label="User menu">👤</button>
    </div>
  </nav>
</header>

<aside class="sidebar" id="sidebar" aria-label="Sidebar">
  <nav class="sidebar__nav">
    <ul>
      <li>
        <a href="/docs/intro" aria-current="page" class="sidebar__link--active">
          Introducción
        </a>
      </li>
      <li>
        <a href="/docs/components">Componentes</a>
        <ul class="sidebar__submenu">
          <li><a href="/docs/components/button">Button</a></li>
          <li><a href="/docs/components/input">Input</a></li>
        </ul>
      </li>
    </ul>
  </nav>
</aside>

<nav aria-label="Breadcrumb" class="breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/docs">Docs</a></li>
    <li aria-current="page">Getting Started</li>
  </ol>
</nav>

<main class="main-content">
  <!-- Contenido principal -->
</main>
```

### CSS

```css
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-6);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

.navbar__menu {
  display: flex;
  list-style: none;
  gap: var(--space-5);
  margin: 0;
  padding: 0;
}

.navbar__menu a {
  color: var(--color-text);
  text-decoration: none;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  transition: all 240ms ease;
}

.navbar__menu a:hover {
  background: var(--color-action-soft);
  color: var(--color-action);
}

.navbar__menu a[aria-current="page"] {
  color: var(--color-action);
  font-weight: 600;
  border-bottom: 2px solid var(--color-action);
}

.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  width: 260px;
  height: 100vh;
  padding: var(--space-6);
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  overflow-y: auto;
  z-index: 1000;
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform 240ms ease;
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
}

.breadcrumb {
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--color-border);
}

.breadcrumb ol {
  display: flex;
  list-style: none;
  gap: var(--space-2);
  margin: 0;
  padding: 0;
}

.breadcrumb li::after {
  content: " / ";
  margin-left: var(--space-2);
  color: var(--color-muted);
}

.breadcrumb li:last-child::after {
  display: none;
}
```

### JavaScript

```javascript
// Toggle sidebar en mobile
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');

if (sidebarToggle) {
  sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    sidebarToggle.setAttribute('aria-expanded', 
      sidebar.classList.contains('open'));
  });
  
  // Cerrar con Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebar.classList.contains('open')) {
      sidebar.classList.remove('open');
    }
  });
}

// Trap focus en sidebar cuando está abierto
function trapFocus(element) {
  const focusable = element.querySelectorAll(
    'a, button, input, select, textarea, [tabindex]'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === first) {
          last.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === last) {
          first.focus();
          e.preventDefault();
        }
      }
    }
  });
}
```

---

## 📱 Responsive

### Breakpoints

| Breakpoint | Cambios |
|-----------|---------|
| **xs-sm (320-480px)** | Hamburger menu, sidebar overlay, breadcrumb simplificado |
| **md (768px)** | Navbar con algunos items, sidebar lateral |
| **lg+ (1024px+)** | Navbar completa, sidebar siempre visible |

### Comportamiento

- **Mobile**: Hamburger → Sidebar overlay con trap focus
- **Tablet**: Navbar compacto + Sidebar lateral (flexible)
- **Desktop**: Navbar horizontal + Sidebar lateral permanente

---

## ✅ Do's & Don'ts

### Do's

- ✅ Mantener navegación consistente en todas las páginas
- ✅ Indicar página actual claramente (`aria-current="page"`)
- ✅ Usar breadcrumbs para jerarquía profunda
- ✅ Agrupar items relacionados lógicamente
- ✅ Hacer teclado navegable completamente
- ✅ Usar iconos + etiquetas (no solo iconos)

### Don'ts

- ❌ Esconder navegación principal en submenú
- ❌ Usar solo color para indicar estado (agregar icono/underline)
- ❌ Navs con más de 7-8 items sin agrupar
- ❌ Olvidar Escape para cerrar sidebars en mobile
- ❌ Usar texto muy pequeño en navegación
- ❌ Hacer items de nav más pequeños que 44px en mobile

---

## 🔗 Componentes Relacionados

- [Navbar](../02-componentes/navbar.md)
- [Breadcrumb](../02-componentes/breadcrumb.md)
- [Dropdown](../02-componentes/dropdown.md)
- [Link](../02-componentes/link.md)

---

## 📚 Referencias

- [Web Content Accessibility Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)
- [ARIA: navigation role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/navigation_role)
- [Foundations](../00-fundamentos/FOUNDATIONS.md)

---

**Versión:** 2.2.0 | **Última actualización:** 2026-07-09
