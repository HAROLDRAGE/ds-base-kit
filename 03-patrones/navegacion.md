# Patrón · Navegación

Estructura de navegación primaria y secundaria en el producto.

## Niveles de navegación

### Primaria (navbar)
- Barra fija en header.
- Logo + secciones principales (5-6 máximo).
- Acciones rápidas: búsqueda, notificaciones, usuario.

### Secundaria (sidebar o tabs)
- Dentro de una sección: categorías, filtros.
- Tabs: subsecciones de una vista.

### Breadcrumbs
- Ruta desde inicio hasta página actual.
- Opcional, refuerza contexto.

## Composición
```
navbar
└── logo (clickeable a inicio)
└── menú principal (links activos con aria-current="page")
└── acciones (buscar, notificaciones, perfil)

[contenido principal]
└── sidebar (links a subsecciones) O tabs (vista alternativa)
└── breadcrumbs (opcional)
```

## Accesibilidad
- **Landmark `<nav>`:** con `aria-label="Principal"` o `aria-label="Secundaria"`.
- **Página actual:** `aria-current="page"` en el link.
- **Orden visual:** tabulación respeta orden izq-der, superior-inferior.
- **Contraste:** links ≥ 4.5:1 sobre fondo.
- **Foco visible:** outline claro en cada elemento.
- **Sin trampa de teclado:** Tab recorre navbar, puede salir.

## Tokens
`color.action` · `color.bg` · `space.4` · `space.5` · `radius.md` · `motion.fast`

## Ejemplo de implementación

```html
<!-- Navbar primaria -->
<nav aria-label="Principal" class="navbar">
  <a href="/">Logo</a>
  <ul>
    <li><a href="/inicio" aria-current="page">Inicio</a></li>
    <li><a href="/componentes">Componentes</a></li>
    <li><a href="/patrones">Patrones</a></li>
  </ul>
</nav>

<!-- Sidebar secundaria (dentro de sección) -->
<div class="main">
  <nav aria-label="Secundaria" class="sidebar">
    <a href="/componentes/botones" aria-current="page">Botones</a>
    <a href="/componentes/inputs">Inputs</a>
    <a href="/componentes/campos">Campos</a>
  </nav>
  <main>
    <!-- contenido de página -->
  </main>
</div>
```

## Do's & Don'ts
- ✅ Un `<nav>` por nivel.
- ❌ Múltiples navs sin `aria-label`.
- ✅ `aria-current="page"` en el item activo.
- ❌ Cambiar estilo sin comunicar estado.
- ✅ Links pequeños pero clickeables (≥44px de altura).
- ❌ Espaciado comprimido, difícil de tocar en móvil.
