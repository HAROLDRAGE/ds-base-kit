# Patrón · Tarjetas

Composición de múltiples tarjetas en grilla, lista o carrusel.

## Variantes de layout

### Grilla (Grid)
- Responsive: 1 columna (móvil) → 2 (tablet) → 3+ (desktop).
- Espaciado consistente: `space.5` o `space.6` entre tarjetas.
- Cada card igual altura o flexible.

### Lista (Flex)
- Stack vertical.
- Cards anchas (100% - padding).
- Mejor para detalles dentro de tarjeta.

### Carrusel (Scroll horizontal)
- Muchas tarjetas en poco espacio.
- Scroll nativo o con botones prev/next.

## Composición de una tarjeta

```
card
├── Imagen (opcional, siempre alt)
├── Contenido
│  ├── Título (H3 o H4)
│  ├── Descripción (párrafo)
│  └── Metadata (badge + fecha)
└── Acción
   └── Link o botón al pie
```

## Accesibilidad
- **Imagen en card:** alt descriptivo o `alt=""` si es decorativa.
- **Título único por card:** no repetir ID o estructura.
- **Si card es enlace:** todo el contenido es clickeable, foco en la tarjeta.
- **Foco visible:** outline en card interactiva.
- **Orden de lectura:** lógico (arriba-abajo, izq-der).

## Comportamiento e interacción
- Hover en card interactiva → elevación (sombra + escala leve).
- Focus → borde de `color.focus`.
- Click → navega a destino.

## Tokens
`color.surface` · `color.border` · `space.4` · `space.5` · `space.6` · `radius.lg` · `motion.fast`

## Ejemplo de implementación

```html
<!-- Grilla de tarjetas -->
<section class="cards-grid">
  <article class="card">
    <img src="/producto-1.jpg" alt="Auriculares inalámbricos" />
    <div class="card-content">
      <h3>Auriculares</h3>
      <p>Calidad de audio premium...</p>
      <span class="badge brand">$99</span>
    </div>
  </article>

  <a href="/producto-2" class="card">
    <img src="/producto-2.jpg" alt="Altavoz inteligente" />
    <div class="card-content">
      <h3>Altavoz</h3>
      <p>Control por voz, diseño moderno...</p>
      <span class="badge brand">$149</span>
    </div>
  </a>
  <!-- más tarjetas... -->
</section>
```

```css
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--space-5);
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: box-shadow var(--motion-fast);
}

.card:hover, .card:focus-visible {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}
```

## Do's & Don'ts
- ✅ Contenido consistente en cards.
- ❌ Tarjetas de altura variable sin razón.
- ✅ Imagen siempre con alt.
- ❌ Imagen decorativa sin alt.
- ✅ Espaciado responsive.
- ❌ Tarjetas pegadas sin espacio en móvil.
