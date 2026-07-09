# ds-base-kit

Sistema de diseño white label para equipos de producto. Reúne componentes accesibles, tokens DTCG, documentación navegable y entregables para Web, Tailwind, iOS, Android y Storybook.

**Versión:** 2.3.0 · **Marcas:** Promptea, Nova y Ocean · **Temas:** claro y oscuro · **Accesibilidad:** WCAG 2.2 AA

## Qué está listo

- **72 tokens DTCG** con metadata de uso, cobertura de cinco plataformas y variantes de marca/tema.
- **95 tokens semánticos declarados, 160 tokens estructurados heredados y 240 variables CSS** para la biblioteca documental; no se deben confundir con el catálogo DTCG exportable.
- **9 componentes declarados** en el manifiesto, con contratos de uso, estados y accesibilidad.
- **Exportaciones verificadas** para Web (CSS, JS, TypeScript y JSON), Tailwind, iOS (Swift), Android (Kotlin y XML) y Storybook.
- **Gobernanza automatizada:** validación de esquema, ciclo de desuso, matriz de cobertura e informe de salud.
- **Explorador de tokens** en la portada: filtra las 240 variables CSS genéricas (incluidas las variantes activas de marca y tema) y el catálogo DTCG de 72 tokens; ambas vistas se generan desde sus fuentes.
- **Importador de fuentes** en la portada: analiza HTML/CSS compatible con CORS o JSON de Figma para producir una propuesta DTCG descargable que se revisa antes de incorporarse al sistema.

## Inicio rápido

```bash
git clone https://github.com/HAROLDRAGE/ds-base-kit.git
cd ds-base-kit
npm run tokens:build
npm run tokens:validate
npm run tokens:govern
npm run validate
open index.html
```

`npm run tokens:build` no requiere paquetes de npm: usa el exportador local y genera los artefactos bajo [build](build). Para ejecutar `npm run validate` se necesita Python 3.11+ y las dependencias de [requirements-dev.txt](requirements-dev.txt).

## Flujo de trabajo

1. Editar la fuente de verdad DTCG: [01-tokens/tokens.dtcg.json](01-tokens/tokens.dtcg.json).
2. Regenerar metadata determinista: `npm run tokens:metadata`.
3. Crear exportaciones: `npm run tokens:build`.
4. Ejecutar controles: `npm run tokens:validate`, `npm run tokens:govern`, `npm run tokens:lint` y `npm test`.
5. Revisar [TOKENS-HEALTH.md](TOKENS-HEALTH.md) y [01-tokens/tokens-coverage-matrix.json](01-tokens/tokens-coverage-matrix.json).

## Importar una fuente externa

La sección **Importar valores de una fuente** de la portada crea una propuesta DTCG con los valores brutos detectados. Para una web, proporciona una URL que permita CORS o pega su HTML/CSS; el análisis incluye HTML, estilos embebidos, atributos `style` y hojas CSS accesibles por CORS. Para Figma, carga un documento JSON de su API, pégalo o usa una URL de archivo con un token de acceso introducido directamente en el formulario; no se persiste ni se incluye en la propuesta. Los archivos `.fig` binarios deben exportarse como JSON mediante la API de Figma antes de cargarse.

El importador organiza los valores como tokens brutos y añade un primer mapeo semántico para fondo, superficie, texto, acción, borde, tipografía y espaciado. También genera CSS y una vista previa local. El resultado es una base técnica, no un sistema publicado: se debe revisar su intención semántica, cobertura white label, contrastes WCAG y componentes afectados antes de incorporarlo a [01-tokens/tokens.dtcg.json](01-tokens/tokens.dtcg.json) o al [05-agentes/component-manifest.json](05-agentes/component-manifest.json).

Los cambios de tokens se documentan en [CHANGELOG.md](CHANGELOG.md). Un token nuevo debe incluir metadata, cobertura, variantes white label y evidencia WCAG cuando se aplique sobre una superficie conocida.

## Fuentes de verdad

| Artefacto | Propósito |
| --- | --- |
| [01-tokens/tokens.dtcg.json](01-tokens/tokens.dtcg.json) | Catálogo DTCG exportable y metadata de 72 tokens hoja. |
| [05-agentes/component-manifest.json](05-agentes/component-manifest.json) | Componentes, reglas y tokens semánticos que consumen agentes. |
| [05-agentes/AGENT-CONTRACT.md](05-agentes/AGENT-CONTRACT.md) | Contratos obligatorios de tokens, accesibilidad, white label y entrega. |
| [01-tokens/tokens.css](01-tokens/tokens.css) | Variables CSS de la biblioteca documental existente. |

## Entregables de plataforma

Después de ejecutar `npm run tokens:build` se actualizan:

- [build/web](build/web): CSS, JavaScript, TypeScript y JSON.
- [build/tailwind/preset.js](build/tailwind/preset.js): preset de Tailwind.
- [build/ios/Tokens.swift](build/ios/Tokens.swift): constantes Swift.
- [build/android](build/android): constantes Kotlin y recursos XML.
- [build/storybook/tokens.js](build/storybook/tokens.js): objeto de tokens para Storybook.
- [assets/js/dtcg-tokens.js](assets/js/dtcg-tokens.js): catálogo que alimenta el explorador de la portada.
- [assets/js/generic-tokens.js](assets/js/generic-tokens.js): catálogo generado de las 240 variables CSS de la biblioteca documental.

## Salud y calidad

El estado actual se publica en [TOKENS-HEALTH.md](TOKENS-HEALTH.md): 72/72 tokens con metadata, cobertura declarada del 100% en cinco plataformas y 42/42 colores evaluables que superan WCAG AA. Los fondos, superficies y bordes no se califican de forma aislada.

La automatización de GitHub Actions en [.github/workflows/validate-tokens.yml](.github/workflows/validate-tokens.yml) reconstruye los entregables y ejecuta los controles obligatorios en cada cambio relevante.

## Estructura

```text
00-fundamentos/   Principios, voz y fundamentos
01-tokens/        Tokens DTCG, CSS y documentación de tokens
02-componentes/   Documentación de componentes
03-patrones/      Patrones reutilizables
04-plantillas/    Plantilla canónica de componente
05-agentes/       Manifiesto, contratos y roles para agentes
06-skills/        Skill ds-guardian
assets/           Aplicación documental estática
build/            Entregables generados y versionados
scripts/          Exportación, validación y gobernanza
```

## Para agentes de IA

Antes de proponer o modificar interfaz, leer [05-agentes/component-manifest.json](05-agentes/component-manifest.json) y cumplir [05-agentes/AGENT-CONTRACT.md](05-agentes/AGENT-CONTRACT.md). Usar tokens semánticos, mantener `data-brand` y `data-theme`, y no crear componentes o tokens fuera del manifiesto sin un cambio versionado.

## Licencia

MIT. Material derivado de Design.MD · Edición 2026.
