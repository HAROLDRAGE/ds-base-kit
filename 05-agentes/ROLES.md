# ROLES.md — Matriz de roles de agentes

| Rol | Puede | No puede | Contratos |
| --- | --- | --- | --- |
| Generador | Componer UI con componentes y tokens existentes | Crear tokens o componentes nuevos | 00-05, 08 |
| Supervisor | Validar schema, contraste, estados, checklist | Modificar artefactos | 02-04 |
| Documentador | Generar/actualizar .md desde código y manifiesto | Cambiar valores | 06, 08 |
| Curador | Proponer extensiones (PR versionado) | Aprobar sus propias propuestas | 07 |

Flujo: Generador entrega → Supervisor valida → Documentador registra. Toda propuesta del Curador la aprueba un humano.
