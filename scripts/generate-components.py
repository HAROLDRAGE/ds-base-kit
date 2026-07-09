#!/usr/bin/env python3
"""
🧩 SCRIPT DE GENERACIÓN DE COMPONENTES
Genera documentación faltante basada en plantillas y contratos

Funciones:
1. Detectar componentes faltantes
2. Generar plantilla de documentación
3. Completar con ejemplos
4. Validar contra AGENT-CONTRACT

Uso: python3 scripts/generate-components.py [--component NAME] [--all] [--preview]
"""

import json
from pathlib import Path
from datetime import datetime
import sys

COMPONENT_TEMPLATE = """# {component_title}

**Categoría:** {category} | **Estado:** v2.2.0 | **Última actualización:** {date}

---

## 🎯 Cuándo Usarlo

### Casos de Uso

{use_cases}

### No Usarlo Para

{dont_use}

---

## 📐 Anatomía

### Estructura

```html
{anatomy_example}
```

### Partes Principales

{anatomy_parts}

---

## 🎭 Estados

### Estados del Componente

| Estado | Descripción | Interacción |
|--------|-------------|------------|
{states_table}

### Ejemplos Visuales

{states_examples}

---

## 🎨 Variaciones

### Por Tamaño

{size_variations}

### Por Tipo/Intención

{type_variations}

---

## ♿ Accesibilidad (WCAG 2.2 AA)

### Requisitos

- ✅ Contraste mínimo: 4.5:1 para texto, 3:1 para componentes
- ✅ Touch target: 44px en mobile, 32px en desktop
- ✅ Teclado: Tab, Enter/Space, Escape accesibles
- ✅ Screen reader: aria-label, aria-describedby, role descriptivos
- ✅ Motion: Respeta prefers-reduced-motion

### Implementación

{wcag_implementation}

---

## 📦 Tokens Utilizados

### Colores

| Token | Uso |
|-------|-----|
{color_tokens}

### Espaciado

| Token | Uso |
|-------|-----|
{spacing_tokens}

### Tipografía

| Token | Uso |
|-------|-----|
{typography_tokens}

### Otras Propiedades

{other_tokens}

---

## 💻 Código

### HTML

```html
{html_code}
```

### CSS (Tokens Semánticos)

```css
{css_code}
```

### JavaScript

```javascript
{js_code}
```

---

## 📱 Responsive

### Mobile (xs: 320px)

{mobile_responsive}

### Desktop (lg: 1024px+)

{desktop_responsive}

---

## ✅ Do's & Don'ts

### Do's

- ✅ Usar tokens semánticos para colores y espaciado
- ✅ Incluir estados hover, focus, active, disabled
- ✅ Validar accesibilidad con teclado y screen reader
- ✅ Respetar prefers-reduced-motion
- ✅ Usar touch targets de 44px en mobile

### Don'ts

- ❌ No usar colores hardcodeados
- ❌ No omitir estados visuales
- ❌ No usar solo color para comunicar estado (agregar icono)
- ❌ No ignorar contraste WCAG AA
- ❌ No hacer componentes más pequeños que 32px en desktop

---

## 🔗 Relaciones

### Componentes Relacionados

- [{related_component_1}](#)
- [{related_component_2}](#)

### Patrones que Lo Utilizan

- [{pattern_1}](#)
- [{pattern_2}](#)

---

## 📚 Referencias

- [AGENT-CONTRACT.md](../05-agentes/AGENT-CONTRACT.md)
- [component-manifest.json](../05-agentes/component-manifest.json)
- [Foundations](../00-fundamentos/FOUNDATIONS.md)
- [WCAG 2.2 AA Guidelines](https://www.w3.org/WAI/WCAG22/quickref/)

---

**Versión:** 2.2.0 | **Última actualización:** {date}
"""

COMPONENT_CONFIGS = {
    "alert": {
        "category": "Molecule",
        "title": "Alert",
        "use_cases": "- Mensajes informativos que requieren atención\n- Notificaciones de error, warning, success\n- Feedback del sistema al usuario",
        "dont_use": "- Para confirmaciones destructivas (usar Modal)\n- Para notificaciones transitorias (usar Toast)\n- Para contenido principal (usar Card)",
        "anatomy": "<div class='alert alert--success'>\n  <i class='icon icon-check'></i>\n  <p class='alert__message'>Operación completada</p>\n  <button class='alert__close' aria-label='Cerrar'>&times;</button>\n</div>",
        "states": ["default", "with-icon", "dismissible", "with-title"],
        "tokens_color": ["--color-success", "--color-error", "--color-warning", "--color-info"],
        "tokens_spacing": ["--space-3", "--space-4", "--space-5"],
        "tokens_typography": ["--typography-body-base"],
    },
    "accordion": {
        "category": "Molecule",
        "title": "Accordion",
        "use_cases": "- FAQs y preguntas frecuentes\n- Contenido colapsable y expandible\n- Navegación por secciones de documentación",
        "dont_use": "- Para contenido que debe verse siempre\n- Para navegación principal (usar Navbar)\n- Para formularios complejos (usar Tabs)",
        "anatomy": "<div class='accordion'>\n  <button class='accordion__trigger' aria-expanded='false'>Sección</button>\n  <div class='accordion__panel' hidden>\n    Contenido\n  </div>\n</div>",
        "states": ["default", "expanded", "disabled"],
        "tokens_color": ["--color-action"],
        "tokens_spacing": ["--space-4", "--space-5"],
        "tokens_typography": ["--typography-body-base"],
    },
    "tooltip": {
        "category": "Molecule",
        "title": "Tooltip",
        "use_cases": "- Explicaciones adicionales breves\n- Información contextual al pasar mouse\n- Ayuda sobre acciones o campos",
        "dont_use": "- Para información crítica (usar Help Text)\n- Para contenido largo (usar Popover)\n- Para acciones destructivas (usar Confirmation)",
        "anatomy": "<div class='tooltip-wrapper'>\n  <button aria-describedby='tooltip-1'>?</button>\n  <div class='tooltip' id='tooltip-1' role='tooltip'>Texto de ayuda</div>\n</div>",
        "states": ["default", "visible", "with-arrow", "dark"],
        "tokens_color": ["--color-neutral-900", "--color-neutral-50"],
        "tokens_spacing": ["--space-2", "--space-3"],
        "tokens_typography": ["--typography-body-small"],
    },
    "toast": {
        "category": "Molecule",
        "title": "Toast",
        "use_cases": "- Notificaciones transitorias y no-bloqueantes\n- Confirmaciones de acciones\n- Mensajes temporales del sistema",
        "dont_use": "- Para confirmaciones destructivas (usar Modal)\n- Para información crítica permanente (usar Alert)\n- Para contenido largo (usar Notification Panel)",
        "anatomy": "<div class='toast toast--success' role='status'>\n  <i class='icon icon-success'></i>\n  <p>Guardado exitosamente</p>\n</div>",
        "states": ["success", "error", "warning", "info"],
        "tokens_color": ["--color-success", "--color-error", "--color-warning", "--color-info"],
        "tokens_spacing": ["--space-4", "--space-5"],
        "tokens_typography": ["--typography-body-base"],
    },
    "table": {
        "category": "Molecule",
        "title": "Table",
        "use_cases": "- Mostrar datos estructurados\n- Comparación de información\n- Listas complejas con múltiples columnas",
        "dont_use": "- Para layouts visuales (usar Grid)\n- Para contenido que debe ser responsive (considerar Cards)\n- Para datos simples (considerar List)",
        "anatomy": "<table>\n  <thead>\n    <tr>\n      <th>Encabezado</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>Celda</td>\n    </tr>\n  </tbody>\n</table>",
        "states": ["default", "sortable", "selectable", "striped"],
        "tokens_color": ["--color-neutral-100", "--color-neutral-900"],
        "tokens_spacing": ["--space-3", "--space-4"],
        "tokens_typography": ["--typography-body-base", "--typography-body-small"],
    },
    "pagination": {
        "category": "Molecule",
        "title": "Pagination",
        "use_cases": "- Navegación entre páginas de resultados\n- División de contenido extenso\n- Experiencia en listas largas",
        "dont_use": "- Para navegación principal (usar Navbar)\n- Para contenido que cabe en una página\n- Para infinite scroll (considerar alternativa)",
        "anatomy": "<nav aria-label='Paginación'>\n  <button aria-label='Página anterior'>&laquo;</button>\n  <button aria-current='page'>1</button>\n  <button>2</button>\n  <button aria-label='Página siguiente'>&raquo;</button>\n</nav>",
        "states": ["default", "active", "disabled"],
        "tokens_color": ["--color-action", "--color-neutral-400"],
        "tokens_spacing": ["--space-2", "--space-3"],
        "tokens_typography": ["--typography-body-base"],
    },
    "progress": {
        "category": "Molecule",
        "title": "Progress",
        "use_cases": "- Indicar progreso de tareas\n- Barras de carga y completitud\n- Feedback visual de procesos",
        "dont_use": "- Para valores que no son porcentaje (usar Rating)\n- Para estado binario (usar Checkbox)\n- Para tiempo restante exacto (usar Timer)",
        "anatomy": "<div class='progress' role='progressbar' aria-valuenow='65' aria-valuemin='0' aria-valuemax='100'>\n  <div class='progress__bar'></div>\n</div>",
        "states": ["default", "determinate", "indeterminate", "success", "error"],
        "tokens_color": ["--color-action", "--color-success", "--color-error"],
        "tokens_spacing": ["--space-4"],
        "tokens_typography": ["--typography-body-small"],
    }
}


class ComponentGenerator:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.components_dir = self.root / "02-componentes"
        
    def generate_component(self, component_name: str, preview=False) -> str:
        """Generar documentación para un componente"""
        config = COMPONENT_CONFIGS.get(component_name)
        
        if not config:
            return f"Error: Componente '{component_name}' no configurado"
        
        # Rellenar template
        content = COMPONENT_TEMPLATE.format(
            component_title=config["title"],
            category=config["category"],
            date=datetime.now().strftime("%Y-%m-%d"),
            use_cases=config.get("use_cases", ""),
            dont_use=config.get("dont_use", ""),
            anatomy_example=config.get("anatomy", ""),
            anatomy_parts="- Trigger/Control\n- Container\n- Content",
            states_table="\n".join([
                f"| {state} | Descripción | Interacción |" 
                for state in config.get("states", [])
            ]),
            states_examples="Ver ejemplos en sección de código",
            size_variations="- Small (24px)\n- Medium (32px)\n- Large (40px)",
            type_variations=f"- Variantes según tipo: {', '.join(config.get('states', []))[:3]}",
            wcag_implementation="""
- Usar `role` descriptivo (button, alert, etc.)
- Incluir `aria-label` o `aria-describedby`
- Cumplir contraste 4.5:1 (texto) / 3:1 (UI)
- Soportar navegación por teclado completa
""",
            color_tokens="\n".join([
                f"| {token} | Uso en {component_name} |"
                for token in config.get("tokens_color", [])
            ]),
            spacing_tokens="\n".join([
                f"| {token} | Espaciado interno/externo |"
                for token in config.get("tokens_spacing", [])
            ]),
            typography_tokens="\n".join([
                f"| {token} | Texto del componente |"
                for token in config.get("tokens_typography", [])
            ]),
            other_tokens="- Border radius: `--radius-md`\n- Shadow: `--shadow-sm` (on hover)",
            html_code=f"""<!-- Ejemplo: {component_name} -->
{config.get('anatomy', '<div class="component"></div>')}
""",
            css_code=f""".{component_name} {{
  padding: var(--space-4);
  background: var(--color-neutral-50);
  border: 1px solid var(--color-neutral-200);
  border-radius: var(--radius-md);
  font-family: var(--typography-base);
}}

.{component_name}:hover {{
  box-shadow: var(--shadow-sm);
}}

.{component_name}:focus {{
  outline: 2px solid var(--color-action);
  outline-offset: 2px;
}}
""",
            js_code=f"""// Inicializar {component_name}
const {component_name}Elements = document.querySelectorAll('.{component_name}');

{component_name}Elements.forEach(element => {{
  // Agregar event listeners
  element.addEventListener('click', handleClick);
  element.addEventListener('keydown', handleKeydown);
}});

function handleClick(event) {{
  // Lógica de interacción
}}

function handleKeydown(event) {{
  // Soporte para teclado (Enter, Space, Escape)
}}
""",
            mobile_responsive="""
- Stack vertical
- Touch target: 44px
- Font size aumentado
- Espaciado adaptado
""",
            desktop_responsive="""
- Layout horizontal
- Touch target: 32px
- Font size normal
- Espaciado normal
""",
            related_component_1="Card (container hermano)",
            related_component_2="Button (acción relacionada)",
            pattern_1="Formularios",
            pattern_2="Navegación"
        )
        
        return content
    
    def list_missing_components(self) -> list:
        """Listar componentes sin documentación"""
        expected = list(COMPONENT_CONFIGS.keys())
        existing = [f.stem for f in self.components_dir.glob("*.md") if f.stem != "plantilla-componente"]
        
        missing = [c for c in expected if c not in existing]
        return missing
    
    def create_component_file(self, component_name: str, dry_run=False) -> bool:
        """Crear archivo de componente"""
        if component_name not in COMPONENT_CONFIGS:
            print(f"✗ Componente '{component_name}' no configurado")
            return False
        
        file_path = self.components_dir / f"{component_name}.md"
        
        if file_path.exists():
            print(f"⚠️  {component_name}.md ya existe")
            return False
        
        content = self.generate_component(component_name)
        
        if not dry_run:
            file_path.write_text(content)
            print(f"✓ Creado: {file_path}")
            return True
        else:
            print(f"[DRY RUN] Creería: {file_path}")
            return True
    
    def create_all_missing(self, dry_run=False):
        """Crear todos los componentes faltantes"""
        missing = self.list_missing_components()
        
        if not missing:
            print("✓ Todos los componentes están documentados")
            return True
        
        print(f"\n🧩 GENERANDO {len(missing)} COMPONENTES FALTANTES")
        print("=" * 60)
        
        for component in missing:
            self.create_component_file(component, dry_run=dry_run)
        
        return True


def main():
    component = None
    all_components = "--all" in sys.argv
    preview = "--preview" in sys.argv
    dry_run = "--dry-run" in sys.argv
    
    # Buscar --component NAME
    for i, arg in enumerate(sys.argv):
        if arg == "--component" and i + 1 < len(sys.argv):
            component = sys.argv[i + 1]
    
    if dry_run:
        print("🔍 MODO DRY-RUN: No se crearán archivos\n")
    
    gen = ComponentGenerator()
    
    if all_components:
        gen.create_all_missing(dry_run=dry_run)
    elif component:
        if preview:
            content = gen.generate_component(component)
            print(content[:1000])
            print(f"\n... (vista previa de {component}.md)\n")
        else:
            gen.create_component_file(component, dry_run=dry_run)
    else:
        missing = gen.list_missing_components()
        print("🧩 COMPONENTES FALTANTES:")
        for comp in missing:
            print(f"  - {comp}")
        print(f"\nPara generar todos: python3 scripts/generate-components.py --all")
        print(f"Para generar uno: python3 scripts/generate-components.py --component {missing[0] if missing else 'alert'}")


if __name__ == "__main__":
    main()
