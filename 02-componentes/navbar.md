# Barra de navegación

Navegación principal del producto. Permanente (sticky) o flotante en header.

## Cuándo usarlo
- Navegación principal de la aplicación.
- Logo + enlaces a secciones principales.
- Usuario + acciones rápidas (notificaciones, perfil).

## Cuándo NO usarlo
- Navegación local de sección → usa tabs.
- Acciones contextuales de página → usa botones en main.
- Menú de dropdown simple → usa un botón con popover.

## Anatomía
```
<nav aria-label="Principal" class="navbar">
  <a href="/" class="logo">Logo</a>
  <ul class="navbar-menu">
    <li><a href="/inicio" aria-current="page">Inicio</a></li>
    <li><a href="/docs">Documentación</a></li>
  </ul>
  <div class="navbar-actions">
    <button class="btn ghost">Perfil</button>
  </div>
</nav>
```

## Variantes
| Variante | Uso |
| --- | --- |
| Default | Logo + menú + acciones |
| With Actions | Incluye botones de CTA (login, signup) |

## Estados
- [x] Default · Scrolled (sticky, cambio de sombra)

## Accesibilidad
- **Landmark:** `<nav>` con `aria-label="Navegación principal"`.
- **Página actual:** `aria-current="page"` en el link activo.
- **Orden lógico:** logo → menú → acciones, siguiendo tabulación visual.
- **Foco visible:** outline en todos los links.
- **Responsive:** en móvil, menú en hamburguesa (detalle de implementación).

## Comportamiento e interacción
- Sticky top (posición fija).
- Click en link → navega a destino.
- Scroll → sombra leve (`box-shadow` con `color.border`).
- Menú activo → subrayado o fondo claro.

## Tokens
`color.bg` · `color.border` · `space.4` · `space.5` · `motion.base`

## Do's & Don'ts
- ✅ Logo siempre clickeable (vuelve a inicio).
- ❌ Logo solo decorativo.
- ✅ Menú con máx. 5-6 items principales.
- ❌ Todos los items ahí; algunos en dropdown es OK.
- ✅ Contraste botones ≥ 4.5:1.

## Código

```html
<nav aria-label="Navegación principal" class="navbar">
  <a href="/" class="navbar-logo">
    <img src="/logo.svg" alt="Design.MD" width="24" height="24" />
    Design.MD
  </a>

  <ul class="navbar-menu">
    <li><a href="/" aria-current="page">Inicio</a></li>
    <li><a href="/componentes">Componentes</a></li>
    <li><a href="/docs">Documentación</a></li>
    <li><a href="/github" rel="external">GitHub</a></li>
  </ul>

  <div class="navbar-actions">
    <button class="btn ghost sm">Cambiar marca</button>
    <button class="btn primary sm">Comenzar</button>
  </div>
</nav>
```

## Props
- `aria-label` en `<nav>` (string): descriptivo.
- `aria-current="page"` en link activo (boolean).
- Items de menú: `<li><a>` o `<a>` directo.
- Acciones: flex layout con buttons o links.
