# Accordion (Acordeón)

Secciones colapsables que revelan contenido bajo demanda mediante **progressive disclosure**. Ideal para FAQs, términos y condiciones, desgloses complejos.

## Cuándo usarlo
- Preguntas frecuentes (FAQs).
- Términos y condiciones legales.
- Detalles desglozables sin necesidad de nueva página.
- Reducir scroll en móviles manteniendo contexto.

## Cuándo NO usarlo
- Contenido que siempre debe ser visible (usa secciones en su lugar).
- Pasos secuenciales (usa stepper/wizard).
- Navegación principal (usa navbar).

## Variantes
| Variante | Uso |
| --- | --- |
| Mono | Una sección abierta a la vez |
| Multi | Múltiples abiertas simultáneamente |
| Nested | Acordeones dentro de acordeones |

## Estados
- [x] Default (cerrado) · Hover · Focus · Expanded (abierto) · Disabled

## Accesibilidad (WCAG 2.2 AA)
- Encabezado semántico real (`<h4>`, `<h5>`) envolviendo un `<button>`.
- `aria-expanded` refleja estado (true/false).
- `aria-controls` vincula botón con panel.
- Panel con `role="region"` + `aria-labelledby` (opcional).
- Ícono de chevron/flecha no es único indicador de estado (acompañado de texto).

## Comportamiento e interacción
- Click en botón alterna sección.
- Enter / Espacio también alternan.
- Tab navega entre botones.
- Flechas ↑↓ pueden navegar entre botones (opcional, pero recomendado).
- Chevron gira cuando se expande (visual feedback).

## Tokens utilizados
`color.on-surface` · `color.border` · `radius.md` · `space.3` · `space.4` · `motion.base`

## Do's & Don'ts

**✔ Do**
- Encabezado real (`<h4>`) envolviendo el botón.
- `aria-expanded="true|false"` refleja estado real.
- Chevron rotado como indicador visual (acompañado de semántica).
- Foco visible ≥ 3:1.

**❌ Don't**
- Divs clicables sin rol de botón.
- Ícono como único indicador (usuarios sin visión no ven cambio).
- Paneles siempre en el DOM si son muy pesados (cargar bajo demanda).
- Texto del botón que no describe su propósito.

## Código HTML
```html
<div class="accordion">
  <h4>
    <button 
      class="acc-btn" 
      aria-expanded="false" 
      aria-controls="acc-panel-1"
      onclick="accToggle(this)">
      ¿Qué incluye el kit? 
      <span aria-hidden="true">▾</span>
    </button>
  </h4>
  <div id="acc-panel-1" role="region" aria-labelledby="acc-btn-1" hidden>
    <p>Contenido de la respuesta aquí.</p>
  </div>

  <h4>
    <button 
      class="acc-btn" 
      aria-expanded="false" 
      aria-controls="acc-panel-2"
      onclick="accToggle(this)">
      ¿Es gratuito? 
      <span aria-hidden="true">▾</span>
    </button>
  </h4>
  <div id="acc-panel-2" role="region" aria-labelledby="acc-btn-2" hidden>
    <p>Sí, de uso libre para la comunidad.</p>
  </div>
</div>
```

## JavaScript de control
```javascript
function accToggle(btn) {
  const open = btn.getAttribute('aria-expanded') === 'true';
  btn.setAttribute('aria-expanded', String(!open));
  document.getElementById(btn.getAttribute('aria-controls')).hidden = open;
}
```

## Contrato ARIA
- Encabezado semántico (`<h4>`, `<h5>`) **envolviendo** un `<button>`.
- `aria-expanded="true|false"` en el botón indica estado.
- `aria-controls="id-del-panel"` vincula botón con panel.
- Panel con `role="region"` + `aria-labelledby` (opcional pero mejor).
- Chevron con `aria-hidden="true"` si es puramente visual.

## Contrato de teclado
- **Tab**: Navega entre botones.
- **Enter / Espacio**: Alterna el estado del botón.
- **↑↓** (Opcional): Navega entre botones si hay varias secciones.
- **Foco visible**: ≥ 3:1 contraste con fondo.

## WCAG 2.2 AA
- **1.3.1 Información y relaciones**: Estructura semántica con `h4/button`.
- **2.1.1 Teclado**: Completamente operable por teclado.
- **2.4.7 Foco visible**: Indicador visual claro en focus.
- **3.2.1 Al recibir el foco**: Cambio de estado obvio cuando se expande.
- **4.1.2 Nombre, rol, valor**: `aria-expanded` comunica estado a tecnología asistiva.
