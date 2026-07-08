# Patrón · Formularios

## Composición
- Cada campo es una molécula `field`: label visible + input + ayuda/error (`aria-describedby`).
- Un solo botón primario (enviar); acciones secundarias como `secondary` o `ghost`.

## Errores
- Icono + palabra + mensaje específico, nunca solo color.
- Foco al primer campo con error tras el envío fallido.

## Tokens
`color.surface` · `color.danger` · `space.2` · `space.4` · `radius.md`
