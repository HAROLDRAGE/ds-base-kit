# Tabs — Pestañas

## Cuándo usarlo

Para cambiar entre diferentes vistas o contenidos relacionados.
NO usar para navegación principal (usar navbar).

## Anatomía

```
[Tab 1] [Tab 2] [Tab 3]
┌─────────────────────────┐
│ Contenido Tab 1         │
└─────────────────────────┘
```

- **Tabs:** Botones con rol="tab"
- **Panel:** Contenido con rol="tabpanel"
- **Active tab:** Tiene aria-selected="true"
- **Asociación:** aria-controls y id para vincular

## Variantes

- **Default:** Tabs arriba, contenido abajo
- **Vertical:** Tabs a la izquierda
- **Iconos:** Cada tab con icono + texto

## Estados

- Default (pasivo)
- Active (seleccionado)
- Hover
- Focus
- Disabled (tab deshabilitado)

## Accesibilidad

✅ **Do:**
- `role="tablist"` en contenedor de tabs
- `role="tab"` + `aria-controls="panel-id"`
- `aria-selected="true"` en tab activo
- `role="tabpanel"` con `aria-labelledby="tab-id"`
- Arrow keys navegan entre tabs (Left/Right)
- Home/End van al primer/último tab

❌ **Don't:**
- Tabs sin roles ARIA
- Cambio de contenido sin aria-controls
- Tab activo sin aria-selected

## Tokens

- `color.action` — Tab activo
- `color.border` — Línea inferior
- `color.text` — Texto de tab
- `space.3` — Padding en tabs
- `motion.fast` — Transición de contenido

## Contrato WCAG 2.2 AA

- **2.1.1 Keyboard:** Arrow keys navegan tabs
- **2.4.3 Focus Order:** Tab order lógico
- **1.3.1 Info and Relationships:** Roles ARIA comunican estructura

## Código

```html
<div role="tablist" aria-label="Secciones">
  <button 
    role="tab" 
    aria-selected="true" 
    aria-controls="panel1"
    id="tab1"
  >
    General
  </button>
  <button 
    role="tab" 
    aria-selected="false" 
    aria-controls="panel2"
    id="tab2"
  >
    Seguridad
  </button>
</div>

<div role="tabpanel" id="panel1" aria-labelledby="tab1">
  Contenido General
</div>
<div role="tabpanel" id="panel2" aria-labelledby="tab2" hidden>
  Contenido Seguridad
</div>
```
