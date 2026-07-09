# ⚡ QUICK START — 5 Minutos para Empezar (v2.2.1+)

## 🚀 Instalación (Primera vez — 5 min)

```bash
cd /Users/haroldrage/Desktop/ds-base-kit
python3 scripts/setup.py --install
```

**Qué hace:**
- ✅ Verifica Python 3.8+
- ✅ Crea directorios
- ✅ Instala Git hooks
- ✅ Genera configuración
- ✅ Primera auditoría

**Resultado esperado:**
```
✅ INSTALACIÓN COMPLETADA
```

---

## 📅 Operación Diaria (2-3 min)

### Validación rápida
```bash
python3 scripts/robust-maintain.py --validate
```

**Qué hace:** Verifica coherencia sin cambios
**Tiempo:** 2-3 minutos

---

## 📋 Mantenimiento Semanal (10-15 min)

```bash
python3 scripts/robust-maintain.py
```

**Qué hace:**
1. Backup automático
2. Validación completa
3. Auditoría
4. Sincronización de tokens
5. Generación de componentes
6. Reportes

**Resultado:** `ROBUST-MAINTAIN-REPORT.json`

---

## 🧪 Antes de Release (20-30 min)

```bash
# 1. Backup y validación exhaustiva
python3 scripts/robust-maintain.py --pre-release

# 2. Tests
python3 scripts/test.py --all

# 3. Bump de versión
python3 scripts/version.py --minor --tag

# 4. Ver reportes
cat HEALTH-DASHBOARD.md
```

---

## 🔄 Si Algo Falla

### Ver qué pasó
```bash
python3 scripts/validate-robust.py --verbose
```

### Restaurar última versión
```bash
python3 scripts/recovery.py --restore
```

### Ver backups disponibles
```bash
python3 scripts/recovery.py --list-backups
```

---

## 📊 Ver Reportes

```bash
# Dashboard de salud
cat HEALTH-DASHBOARD.md

# Reporte ejecutivo
cat EXECUTIVE-REPORT.md

# Detalles de validación
cat VALIDATION-REPORT.json
```

---

## 🎯 Comandos Útiles

| Comando | Tiempo | Propósito |
|---------|--------|----------|
| `python3 scripts/robust-maintain.py --validate` | 2 min | Verificación rápida |
| `python3 scripts/robust-maintain.py` | 15 min | Mantenimiento semanal |
| `python3 scripts/test.py --all` | 3 min | Testing |
| `python3 scripts/recovery.py --status` | 1 seg | Ver backups |
| `python3 scripts/sync-tokens.py --all` | 2 min | Sincronizar |
| `python3 scripts/audit-complete.py` | 5 min | Auditoría |

---

## 🚨 Troubleshooting

### Python 3 no encontrado
```bash
brew install python@3.12
```

### Permission denied en scripts
```bash
chmod +x scripts/*.py
chmod +x .git/hooks/*
```

### Pre-commit hook bloquea cambios
```bash
# Ver qué falla
python3 scripts/validate-robust.py --verbose

# Arreglar manualmente
# Luego reintentar commit
```

---

## 📞 Más Información

- **Guía Completa:** [GUÍA-SCRIPTS-v2.2.1+.md](GUÍA-SCRIPTS-v2.2.1+.md)
- **Estado:** [ESTADO-v2.2.1+.md](ESTADO-v2.2.1+.md)
- **Entrega Final:** [ENTREGA-FINAL-v2.2.1+.md](ENTREGA-FINAL-v2.2.1+.md)

---

**Tiempo estimado:** 5 minutos  
**Complejidad:** ⚡ Muy fácil  
**Status:** 🟢 Production Ready

```bash
# 1. Editar component-manifest.json (fuente única de verdad)
nano 05-agentes/component-manifest.json

# 2. Regenerar artefactos
bash scripts/regenerate-all.sh

# 3. Validar cambios
python3 scripts/validate.py

# 4. Commit
git add .
git commit -m "feat: agregar componente XXX"
git push
```

## 🤖 Para Agentes IA

```bash
# Leer en este orden:
1. cat llms.txt  # descubrimiento
2. cat 05-agentes/component-manifest.json  # qué existe
3. cat 05-agentes/AGENT-CONTRACT.md  # cómo actuar

# Instalar skill
cp -r 06-skills/ds-guardian ~/.claude/skills/

# Operar bajo Contratos 00-08
# Si algo no existe en el manifiesto → escalar (Contrato 07)
```

## 📊 Archivos Clave

| Archivo | Propósito |
|---|---|
| `05-agentes/component-manifest.json` | Fuente única de verdad (SSOT) |
| `05-agentes/AGENT-CONTRACT.md` | Contratos 00-08 (RFC 2119) |
| `05-agentes/manifest.schema.json` | Validación JSON Schema |
| `scripts/validate.py` | Linting de diseño (CI) |
| `scripts/export-tokens.py` | Exportador multiformat |
| `scripts/regenerate-all.sh` | Regenerar todos los artefactos |
| `CHANGELOG.md` | Keep a Changelog + SemVer |
| `index.html` | Documentación navegable |

## 🎯 Flujo de Desarrollo

```
component-manifest.json (editar aquí)
          ↓
    validate.py (schema + contraste)
          ↓
    export-tokens.py (CSS, JS, JSON, SCSS)
          ↓
   01-tokens/*.{css,js,json,scss} (generados)
          ↓
    git add . && git commit
          ↓
    CI: .github/workflows/validate.yml
```

## 🔗 Enlaces Útiles

- **GitHub:** https://github.com/haroldrage/ds-base-kit
- **Documentación completa:** Abre `index.html` en tu navegador (o `python3 -m http.server 8000` para servir localmente)
- **Mejoras v1.3.0:** `docs/v1.3.0-improvements.md`

## ❓ FAQ

**P: ¿Cómo agrego un componente nuevo?**
R: Edita `component-manifest.json` (estructura + tokens), luego documenta en `02-componentes/nombre.md`, luego `bash scripts/regenerate-all.sh` y `python3 scripts/validate.py`.

**P: ¿Puedo editar `tokens.css` directamente?**
R: No. Edita el manifiesto y ejecuta `export-tokens.py`. Los archivos generados llevan comentario "NO editar a mano".

**P: ¿Cómo integro con Figma?**
R: Exporta `tokens.json` y usa Token Studio plugin o Figma Dev Mode + MCP.

**P: ¿Es posible agregar una 4ª marca?**
R: Sí. Agrega a `component-manifest.json` > `brands` array y en `tokens.values`. Luego regenera con `scripts/regenerate-all.sh`.

---

**Última actualización:** 2026-07-08 · v1.3.0
