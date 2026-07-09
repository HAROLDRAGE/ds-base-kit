# Progress — Indicador de progreso

## Cuándo usarlo

Para mostrar el avance de una operación (carga, descarga, procesamiento).
USO: Operaciones de **duración conocida** (progress bar) o **desconocida** (spinner).

## Anatomía

### Progress Bar
```
[████████░░░░░░░] 60%
```

### Spinner
```
⟳ (circulo rotativo)
```

## Variantes

- **Determinado (progress bar):** Con % conocido
- **Indeterminado (spinner):** Sin % específico
- **Con etiqueta:** Texto describiendo la operación

## Estados

- En progreso (animación activa)
- Completado (100% o desaparece)
- Error (color rojo)

## Accesibilidad

✅ **Do:**
- `role="progressbar"` con `aria-valuenow`, `aria-valuemin`, `aria-valuemax`
- `aria-label` o `aria-labelledby` describiendo la operación
- Para spinner: `role="status"` + `aria-live="polite"`
- Texto alternativo: "Cargando... 60% completado"

❌ **Don't:**
- Progress sin aria-valuenow/aria-valuemax
- No comunicar que es progreso sin aria-label
- Spinner sin indicación verbal de que es una carga

## Tokens

- `color.action` — Color de progreso
- `color.action-soft` — Background
- `color.danger` — Estado error
- `radius.full` — Forma redondeada
- `motion.base` — Animación de rotación

## Contrato WCAG 2.2 AA

- **1.1.1 Non-text Content:** Progreso comunicado en texto + visual
- **4.1.1 Parsing:** Atributos aria correctos
- **4.1.3 Status Messages:** aria-live para actualizaciones

## Código

```html
<!-- Progress bar -->
<div 
  role="progressbar" 
  aria-valuenow="60" 
  aria-valuemin="0" 
  aria-valuemax="100"
  aria-label="Cargando archivo..."
>
  <div style="width: 60%"></div>
</div>
<span>60%</span>

<!-- Spinner -->
<div role="status" aria-label="Cargando..." aria-live="polite">
  <span class="spinner">⟳</span>
  Procesando...
</div>
```
