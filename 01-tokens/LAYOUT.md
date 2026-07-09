# Sistema de Layout · Responsive Design y Multi-Dispositivo

**Versión:** 2.1.0  
**Última actualización:** 2026-07-09

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Breakpoints Estándar](#breakpoints-estándar)
3. [Grid System](#grid-system)
4. [Safe Areas (iOS/Android)](#safe-areas-iosandroid)
5. [Touch Targets](#touch-targets)
6. [Densidades de UI](#densidades-de-ui)
7. [Android · Material Design 3](#android--material-design-3)
8. [iOS · Human Interface Guidelines](#ios--human-interface-guidelines)
9. [Web · HTML/CSS/JS](#web--htmlcssjs)
10. [Tokens de Layout](#tokens-de-layout)

---

## Introducción

El sistema de layout de **ds-base-kit** es agnóstico de plataforma. Define un conjunto unificado de **breakpoints, tokens de espaciado y safe areas** que funcionan idénticamente en Android (Material Design 3), iOS (HIG) y Web (responsive).

**Principios clave:**
- **Mobile-first:** Estilos base para 320px, luego media queries para más grande
- **Fluido:** Usa `rem`, no `px` → escalable con font-size
- **Accesible:** Touch targets mínimos (44px iOS, 48dp Android)
- **Agnóstico:** Mismo token en web, app, documento

---

## Breakpoints Estándar

Nuestro sistema define **6 puntos de ruptura** alineados con dispositivos reales:

| Breakpoint | Desde | Hasta  | Dispositivos | Columnas | Padding |
|:-----------|:-----:|:------:|:-------------|:--------:|:-------:|
| **xs**     | 320px | 479px  | Móvil pequeño | 1 | 16px |
| **sm**     | 480px | 767px  | Móvil estándar | 1 | 20px |
| **md**     | 768px | 1023px | Tablet | 2 | 24px |
| **lg**     | 1024px| 1279px | Desktop pequeño | 3–4 | 32px |
| **xl**     | 1280px| 1535px | Desktop full | 4–6 | 40px |
| **2xl**    | 1536px| ∞      | Desktop ultra-wide | 6+ | 48px |

### Tokens CSS

```css
/* :root */
--breakpoint-xs: 320px;
--breakpoint-sm: 480px;
--breakpoint-md: 768px;
--breakpoint-lg: 1024px;
--breakpoint-xl: 1280px;
--breakpoint-2xl: 1536px;
```

### Uso en Media Queries

```css
/* Mobile-first: estilos base para xs */
.card { 
  display: grid;
  grid-template-columns: 1fr; /* 1 columna */
}

/* Tablet: 768px+ */
@media (min-width: 768px) {
  .card { grid-template-columns: repeat(2, 1fr); }
}

/* Desktop: 1024px+ */
@media (min-width: 1024px) {
  .card { grid-template-columns: repeat(3, 1fr); }
}
```

---

## Grid System

### Columnas por Breakpoint

```css
/* Tokens en :root */
--grid-cols-mobile: 1;       /* xs, sm */
--grid-cols-tablet: 2;       /* md */
--grid-cols-desktop: 3;      /* lg, xl */
```

### Espaciado (Gap)

Todos los grids usan el token de espaciado correspondiente:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4); /* 16px en mobile, 24px en tablet, etc. */
}
```

### Contendor Max-Width

```css
/* Token */
--container-max-width: 1280px;
--container-padding: var(--space-4);

/* Uso */
.wrap, main {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: 0 var(--container-padding);
}
```

---

## Safe Areas (iOS/Android)

Los dispositivos modernos tienen **notches, Dynamic Islands (iOS 15+) y curved edges (Android)**. El token `env(safe-area-inset-*)` respeta estos espacios.

### iOS: Dynamic Island & Notch

```html
<meta name="viewport" content="viewport-fit=cover">
```

```css
/* Tokens */
--safe-area-inset-top: env(safe-area-inset-top, 0px);
--safe-area-inset-bottom: env(safe-area-inset-bottom, 0px);
--safe-area-inset-left: env(safe-area-inset-left, 0px);
--safe-area-inset-right: env(safe-area-inset-right, 0px);

/* Uso */
.header { padding-top: max(var(--space-4), var(--safe-area-inset-top)); }
```

### Android: DisplayCutout & Rounded Corners

Android 9+ soporta `WindowInsets.getDisplayCutout()`. En web, usa los mismos tokens `env()`.

---

## Touch Targets

Las especificaciones de accesibilidad (WCAG 2.5.5) y plataformas requieren **touch targets mínimos**:

| Plataforma | Mínimo | Token | Notas |
|:-----------|:------:|:-----:|:------|
| **iOS** | 44×44 pt | `--touch-target-min` | Apple HIG estándar |
| **Android** | 48×48 dp | `--touch-target-min` | Material Design 3 |
| **Web (mouse)** | 32×32 px | `--touch-target-desktop` | Más compacto con ratón |

### Tokens CSS

```css
--touch-target-min: 44px;        /* iOS + Android */
--touch-target-desktop: 32px;    /* Web desktop */
```

### Clase Utilitaria

```css
.touch-target {
  min-width: var(--touch-target-min);
  min-height: var(--touch-target-min);
}
```

### Ejemplo

```html
<!-- Botón accesible en móvil y desktop -->
<button class="touch-target">
  Acción
</button>
```

---

## Densidades de UI

Tres niveles de densidad para acomodar diferentes contextos de uso:

| Densidad | Factor | Uso | Ejemplo |
|:---------|:------:|:----|:--------|
| **Compact** | 1.0× | Máxima información | Datatable en desktop |
| **Normal** | 1.25× | Equilibrado (default) | Aplicaciones generales |
| **Comfortable** | 1.5× | Máximo espacio | Interfaces táctiles, accesibilidad |

```css
/* Tokens */
--density-compact: 1.0;
--density-normal: 1.25;
--density-comfortable: 1.5;

/* Uso */
.card {
  padding: calc(var(--space-4) * var(--density-normal));
}

/* En contexto táctil */
.touch .card {
  padding: calc(var(--space-4) * var(--density-comfortable));
}
```

---

## Android · Material Design 3

### Diferencias Clave

#### 1. **Unidades: Density-Independent Pixels (dp)**
- Android usa **dp**, no px
- 160 dpi = 1 dp = 1 px (baseline)
- En dispositivos de alta densidad (3x), 1 dp = 3 px
- **Nuestro mapeo:** 1 rem (16px) = 16 dp (exacto)

#### 2. **Grid Base: 4 dp**
Material Design usa grid de **4 dp**. Nuestros espacios (4, 8, 12, 16, 20...) alinean perfectamente.

```
Nuestros valores (rem): 0.25, 0.5, 0.75, 1, 1.25...
En dp: 4, 8, 12, 16, 20...
```

#### 3. **Colores: Material You (Dinámicos)**
Android 12+ extrae colores del wallpaper. Nuestros tokens semánticos facilitan esta integración:

```kotlin
// Kotlin (Jetpack Compose)
Button(
  colors = ButtonColors(
    containerColor = Color.fromToken("--color-action"), // Dynamic
    contentColor = Color.fromToken("--color-on-action")
  )
) {
  Text("Guardar")
}
```

#### 4. **Navegación: Back Button + Gestures**
- Android **siempre tiene** botón "Atrás" (físico o software)
- Modales se cierren con back (Contrato 07)
- No uses "swipe from left" (eso es iOS)

```kotlin
// Monitorear back press
BackHandler(enabled = isModalOpen) {
  closeModal() // Mapea a Contrato 07
}
```

#### 5. **Safe Areas: DisplayCutout & Insets (API 28+)**
```kotlin
val windowInsets = WindowCompat.getInsetsController(window)
val cutout = window?.decorView?.rootWindowInsets?.displayCutout

// Aplicar padding dinámicamente
contentView.setPadding(
  cutout?.safeInsetLeft ?: 0,
  cutout?.safeInsetTop ?: 0,
  cutout?.safeInsetRight ?: 0,
  cutout?.safeInsetBottom ?: 0
)
```

#### 6. **Motion: Durations & Easing**
Material Design 3 especifica duraciones:
- **Short:** 150ms (hover, focus)
- **Medium:** 250ms (entrada, expansión)
- **Long:** 500ms (transiciones complejas)

Nuestros tokens:
```css
--motion-fast: 120ms;   /* Sync con haptic feedback */
--motion-base: 240ms;   /* Estándar Material 3 ~250ms */
--motion-slow: 400ms;   /* Complejo */
```

---

## iOS · Human Interface Guidelines (HIG)

### Diferencias Clave

#### 1. **Unidades: Puntos (pt)**
- iOS usa **puntos (pt)**, no pixeles
- 1 pt = 1 px en iPhone 6/7/8/SE (1x)
- 1 pt = 2 px en iPhone 6s Plus, X, 11 (2x)
- 1 pt = 3 px en iPhone 12 Pro Max, 13 Pro Max (3x)
- **Nuestro mapeo:** 1 rem (16px) = 16 pt (exacto)

#### 2. **Dynamic Island & Notch (iPhone 15+, X–14)**
```swift
// SwiftUI (iOS 15+)
var body: some View {
  VStack {
    Text("Contenido")
      .safeAreaInset(edge: .top) {
        Rectangle()
          .frame(height: 20) // Espacio bajo Dynamic Island
      }
  }
}
```

#### 3. **Vibrancy & Blur (UIKit + SwiftUI)**
iOS favorece efectos de vidrio sobre sombras flat:

```swift
// UIBlurEffect (iOS 8+)
let blur = UIBlurEffect(style: .systemMaterial)
let blurView = UIVisualEffectView(effect: blur)

// SwiftUI (iOS 15+)
ZStack {
  Image("background")
  Text("Content")
    .font(.system(.title, design: .rounded))
}
.modifier(VisualEffectBlur())
```

#### 4. **Navegación: Gestos + Swipe-back**
- iOS **no tiene botón "Atrás" de sistema**
- Los usuarios esperan "swipe from left" para retroceder
- Modales se cierran con "swipe down" o botón
- **Contrato 05 (Navegación):** No uses patrón Android

```swift
// SwiftUI (iOS 13+)
NavigationStack(path: $navPath) {
  List {
    NavigationLink(value: "detail") {
      Text("Ir a detalle")
    }
  }
  .navigationDestination(for: String.self) { _ in
    DetailView()
  }
}
```

#### 5. **Haptic Feedback**
iOS enfatiza retroalimentación táctil (vibración):

```swift
// Crear diferentes tipos de haptic
let impact = UIImpactFeedbackGenerator(style: .medium)
impact.impactOccurred()

let selection = UISelectionFeedbackGenerator()
selection.selectionChanged()

let notification = UINotificationFeedbackGenerator()
notification.notificationOccurred(.success)
```

Sincroniza con nuestros `--motion-*` para timing coincidente.

#### 6. **Colores: Light/Dark Adaptive**
iOS adapta automáticamente colores según el tema:

```swift
// UIKit
let color = UIColor { traitCollection in
  if traitCollection.userInterfaceStyle == .dark {
    return .systemBlue  // Dark theme
  } else {
    return .blue        // Light theme
  }
}

// SwiftUI (iOS 14+)
Color.adaptive(light: .blue, dark: .cyan)
```

Nuestros tokens semánticos (`--color-action`, `--color-surface`) manejan esto automáticamente.

---

## Web · HTML/CSS/JS

### Meta Viewport (Obligatorio)

```html
<meta 
  name="viewport" 
  content="width=device-width, initial-scale=1, viewport-fit=cover"
>
<!-- viewport-fit=cover: permite contenido bajo safe areas en iOS -->
```

### Mobile-First Responsive

**Orden:** Mobile (base) → Tablet → Desktop

```css
/* 1. Estilos base para móvil (320px+) */
.card {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-4);
}

/* 2. Tablet: 768px+ */
@media (min-width: 768px) {
  .card {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-6);
  }
}

/* 3. Desktop: 1024px+ */
@media (min-width: 1024px) {
  .card {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-8);
  }
}
```

### Grid & Flexbox

Evita floats. Usa CSS Grid y Flexbox:

```css
/* Grid automático (recomendado) */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
}

/* Flexbox (para contenido lineal) */
.flex-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.flex-row > * {
  flex: 1 1 auto;
  min-width: 200px;
}
```

### Imágenes Responsivas

```html
<!-- Usando srcset -->
<img 
  src="image-320w.jpg"
  srcset="image-320w.jpg 320w, image-640w.jpg 640w, image-1280w.jpg 1280w"
  sizes="(max-width: 640px) 100vw, (max-width: 1280px) 50vw, 33vw"
  alt="Descripción"
>

<!-- Usando <picture> para formatos diferentes -->
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="Descripción">
</picture>
```

### Performance: Core Web Vitals

| Métrica | Meta | Cómo mejorar |
|:--------|:----:|:------------|
| **LCP** | < 2.5s | Optimiza hero image, CSS crítico, fonts preload |
| **INP** | < 100ms | Evita JS bloqueante, Web Workers para cálculo |
| **CLS** | < 0.1 | Asigna dimensions a imágenes, evita inserciones dinámicas |

```html
<!-- Preload critical resources -->
<link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="hero.jpg" as="image">

<!-- Lazy-load imágenes -->
<img src="image.jpg" loading="lazy" alt="...">

<!-- Lazy-load iframes -->
<iframe src="..." loading="lazy"></iframe>
```

### Accesibilidad (WCAG 2.2 AA)

Siempre requerido:
- ✅ Keyboard navigation (Tab, Enter, Escape)
- ✅ ARIA roles & attributes (`aria-label`, `aria-expanded`, `aria-describedby`)
- ✅ Contrast 4.5:1 para texto
- ✅ Focus visible (ring, outline)
- ✅ Skip links (`<a class="skip-link" href="#main">`)
- ✅ Labels explícitos (`<label for="input-id">`)

---

## Tokens de Layout

Aquí están todos los tokens de layout en `component-manifest.json`:

```json
{
  "layout.breakpoint-xs": { "value": "320px", "use": "Móviles pequeños" },
  "layout.breakpoint-sm": { "value": "480px", "use": "Móviles medianos" },
  "layout.breakpoint-md": { "value": "768px", "use": "Tablets" },
  "layout.breakpoint-lg": { "value": "1024px", "use": "Desktop pequeño" },
  "layout.breakpoint-xl": { "value": "1280px", "use": "Desktop full" },
  "layout.breakpoint-2xl": { "value": "1536px", "use": "Desktop ultra-wide" },
  
  "layout.grid-cols-mobile": { "value": "1", "use": "Columnas en móvil" },
  "layout.grid-cols-tablet": { "value": "2", "use": "Columnas en tablet" },
  "layout.grid-cols-desktop": { "value": "3", "use": "Columnas en desktop" },
  
  "layout.touch-target-min": { "value": "44px", "use": "iOS 44×44, Android 48×48 dp" },
  "layout.touch-target-desktop": { "value": "32px", "use": "Desktop (mouse)" },
  
  "layout.container-max-width": { "value": "1280px", "use": "Ancho máximo" },
  "layout.container-padding": { "value": "16px", "use": "Padding del contenedor" },
  
  "layout.density-compact": { "value": "1.0", "use": "Máxima información" },
  "layout.density-normal": { "value": "1.25", "use": "Equilibrado (default)" },
  "layout.density-comfortable": { "value": "1.5", "use": "Máximo espacio (táctil)" },
  
  "layout.safe-area-inset-top": { "value": "env(...)", "use": "Notch/Dynamic Island (top)" },
  "layout.safe-area-inset-bottom": { "value": "env(...)", "use": "Home indicator (bottom)" }
}
```

---

## Resumen Rápido

| Plataforma | Breakpoints | Grid | Touch Target | Navegación |
|:-----------|:-----------:|:----:|:------------:|:-----------|
| **Android** | 4 (xs, md, lg, 2xl) | 1→2→3 col | 48×48 dp | Back button |
| **iOS** | 4 (xs, md, lg, 2xl) | 1→2→3 col | 44×44 pt | Swipe-back |
| **Web** | 6 (xs–2xl) | 1→2→3 col | 44×44 px | Keyboard |

**Siempre:** Usa tokens, nunca valores raw. Respeta safe areas. Implementa WCAG 2.2 AA.

---

**Documento generado:** 2026-07-09 · **Versión:** 2.1.0
