# Breadcrumb — Rastro de navegación

## Cuándo usarlo

Para mostrar la ubicación del usuario dentro de la jerarquía de la aplicación.
Especialmente útil en aplicaciones con múltiples niveles.

## Anatomía

```
[Inicio] › [Sección] › [Subsección] › [Página actual]
```

- **Enlaces:** Todas las ubicaciones previas
- **Página actual:** Texto sin enlace con `aria-current="page"`
- **Separadores:** Generados por CSS, no marcado HTML

## Variantes

- **Estándar:** Con enlaces hasta la página actual
- **Compacta:** Solo últimos 2-3 niveles en mobile

## Estados

- Default
- Hover (enlaces)
- Active (página actual)

## Accesibilidad

✅ **Do:**
- `<nav aria-label="Ruta de navegación">`
- Lista ordenada `<ol>`
- Página actual con `aria-current="page"` sin enlace
- Separadores por CSS (::before)

❌ **Don't:**
- Separadores como contenido HTML
- Enlazar la página actual
- Usar divs en lugar de nav/ol

## Tokens

- `color.action-hover` — Color de enlaces
- `color.muted` — Color de separadores
- `space.2` — Gap entre items
- `motion.fast` — Hover transitions

## Contrato WCAG 2.2 AA

- **2.4.8 Location:** El usuario conoce su ubicación
- **1.3.1 Info and Relationships:** Estructura semántica clara (nav, ol, aria-current)

## Código

```html
<nav aria-label="Ruta de navegación">
  <ol class="breadcrumb">
    <li><a href="/">Inicio</a></li>
    <li><a href="/componentes">Componentes</a></li>
    <li aria-current="page">Breadcrumb</li>
  </ol>
</nav>
```
