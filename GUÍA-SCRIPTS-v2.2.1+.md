# 🚀 GUÍA COMPLETA v2.2.1+ — Sistema Robusto

## 📦 Suite de Scripts Disponibles

### 1️⃣ **INSTALACIÓN Y SETUP** (Primera vez)
```bash
# Instalación completa del sistema
python3 scripts/setup.py --install

# Verificar setup
python3 scripts/setup.py --verify

# Solo instalar hooks
python3 scripts/setup.py --hooks
```

**Qué hace:**
- ✅ Verifica Python 3.8+
- ✅ Crea directorios necesarios
- ✅ Instala Git hooks (pre-commit, pre-push)
- ✅ Inicializa configuración
- ✅ Ejecuta validación inicial

---

### 2️⃣ **MANTENIMIENTO ROBUSTO** (Operación diaria)
```bash
# Mantenimiento completo (recomendado)
python3 scripts/robust-maintain.py

# Solo validación (5 min)
python3 scripts/robust-maintain.py --validate

# Pre-release exhaustivo (15 min)
python3 scripts/robust-maintain.py --pre-release

# Con recuperación automática en caso de error
python3 scripts/robust-maintain.py --recovery

# Con testing completo
python3 scripts/robust-maintain.py --test
```

**Pasos ejecutados:**
1. Backup automático pre-mantenimiento
2. Validación robusta con logging
3. Auditoría exhaustiva
4. Sincronización de tokens
5. Generación de componentes faltantes
6. Testing de integridad (opcional)
7. Generación de reportes
8. Snapshot post-mantenimiento

---

### 3️⃣ **VALIDACIÓN ROBUSTA** (Verificación exhaustiva)
```bash
# Validación completa con logging
python3 scripts/validate-robust.py

# Validación verbose (salida detallada)
python3 scripts/validate-robust.py --verbose

# Con auto-fix de problemas simples
python3 scripts/validate-robust.py --fix

# Exportar logs
python3 scripts/validate-robust.py --export-logs
```

**Qué valida:**
- ✅ Integridad de archivos críticos (checksums)
- ✅ Coherencia de tokens (CSS ↔ JSON ↔ JS ↔ Manifest)
- ✅ Documentación completa (mínimo 50 líneas)
- ✅ Estructura de componentes
- ✅ Referencias cruzadas (links)
- ✅ Encoding UTF-8 correcto
- ✅ Sintaxis de JSON

---

### 4️⃣ **TESTING** (Garantía de calidad)
```bash
# Todos los tests
python3 scripts/test.py

# Solo tests de componentes
python3 scripts/test.py --components

# Solo tests de tokens
python3 scripts/test.py --tokens

# Solo tests de documentación
python3 scripts/test.py --docs

# Solo tests de WCAG AA
python3 scripts/test.py --wcag

# Con reporte de cobertura
python3 scripts/test.py --coverage
```

**Qué testa:**
- ✅ Estructura de componentes (50+ líneas, secciones requeridas)
- ✅ Validez de JSON
- ✅ Coherencia CSS-JSON
- ✅ Existencia de Foundations
- ✅ Accesibilidad WCAG AA (menciones)
- ✅ Integridad de archivos críticos
- ✅ Existencia de directorios críticos

---

### 5️⃣ **AUDITORÍA COMPLETA** (Diagnóstico profundo)
```bash
# Auditoría estándar
python3 scripts/audit-complete.py

# Verbose (salida detallada)
python3 scripts/audit-complete.py --verbose

# Exportar reporte JSON
python3 scripts/audit-complete.py --export
```

**Qué audita:**
- ✅ Sincronización de 4 fuentes (CSS, JSON, JS, Manifest)
- ✅ Cobertura de Foundations (8/8)
- ✅ Documentación de componentes
- ✅ Patrones
- ✅ WCAG AA compliance
- ✅ Genera: AUDIT-REPORT.json

---

### 6️⃣ **SINCRONIZACIÓN DE TOKENS** (Coherencia garantizada)
```bash
# Sincronizar todo
python3 scripts/sync-tokens.py --all

# Solo CSS → JSON
python3 scripts/sync-tokens.py --css-to-json

# Solo JSON → JavaScript
python3 scripts/sync-tokens.py --json-to-js

# Preview sin cambios (dry-run)
python3 scripts/sync-tokens.py --dry-run

# Verbose
python3 scripts/sync-tokens.py --verbose
```

**Flujo:**
```
tokens.css (240)
    ↓
tokens.json (160)
    ↓
TOKEN_META en main.js
    ↓
component-manifest.json
```

---

### 7️⃣ **RECOVERY Y ROLLBACK** (Recuperación ante errores)
```bash
# Crear backup completo
python3 scripts/recovery.py --backup

# Restaurar desde backup más reciente
python3 scripts/recovery.py --restore

# Restaurar desde backup específico
python3 scripts/recovery.py --restore [backup-name]

# Crear snapshot actual
python3 scripts/recovery.py --snapshot [name]

# Ver estado de recovery
python3 scripts/recovery.py --status

# Listar todos los backups
python3 scripts/recovery.py --list-backups

# Limpiar backups antiguos (mantener 5)
python3 scripts/recovery.py --cleanup
```

**Características:**
- ✅ Backups automáticos con timestamp
- ✅ Snapshots para comparación
- ✅ Checksums SHA256
- ✅ Metadata de cada backup
- ✅ Recuperación automática en pre-commit hooks

---

### 8️⃣ **VERSIONADO AUTOMÁTICO** (Release management)
```bash
# Bump patch (2.2.0 → 2.2.1)
python3 scripts/version.py --patch

# Bump minor (2.2.0 → 2.3.0)
python3 scripts/version.py --minor

# Bump major (2.2.0 → 3.0.0)
python3 scripts/version.py --major

# Generar changelog
python3 scripts/version.py --patch --changelog

# Crear Git tag
python3 scripts/version.py --patch --tag

# Ver release notes
python3 scripts/version.py --release-notes
```

**Genera:**
- ✅ VERSION actualizado
- ✅ CHANGELOG.md
- ✅ Git tags (v2.2.1, etc.)
- ✅ Release notes automáticas

---

### 9️⃣ **CI/CD HOOKS** (Automatización)
```bash
# Instalar pre-commit hooks
python3 scripts/ci-hooks.py --install

# Crear GitHub Actions workflows
python3 scripts/ci-hooks.py --github

# Verificar que hooks están instalados
python3 scripts/ci-hooks.py --test
```

**Pre-commit hook ejecuta:**
- ✅ Validación de sintaxis
- ✅ Sincronización de tokens
- ✅ Auditoría de coherencia
- Bloquea commit si hay problemas

**Pre-push hook ejecuta:**
- ✅ Suite completa de validación
- Bloquea push si hay problemas

---

### 🔟 **REPORTES Y DASHBOARDS** (Visibilidad)
```bash
# Reporte ejecutivo
python3 scripts/report.py --executive

# Dashboard de salud del sistema
python3 scripts/report.py --health

# Reporte de cobertura
python3 scripts/report.py --coverage

# Exportar como JSON
python3 scripts/report.py --json

# Todos los reportes
python3 scripts/report.py --executive --health --coverage
```

**Métricas:**
- 📊 Documentación (líneas totales)
- 📊 Tokens (sincronizados, coherencia)
- 📊 Componentes (documentados, cobertura)
- 📊 Accesibilidad (WCAG AA %)
- 📊 Salud general del sistema

---

## 🎯 FLUJOS RECOMENDADOS

### ⚡ DIARIO (5 minutos)
```bash
python3 scripts/robust-maintain.py --validate
```

### 📅 SEMANAL (15 minutos)
```bash
python3 scripts/robust-maintain.py
```

### 🚀 ANTES DE RELEASE (30 minutos)
```bash
# 1. Backup
python3 scripts/recovery.py --backup

# 2. Tests exhaustivos
python3 scripts/test.py --all

# 3. Auditoría
python3 scripts/audit-complete.py --export

# 4. Sincronización
python3 scripts/sync-tokens.py --all

# 5. Bump de versión
python3 scripts/version.py --minor --changelog --tag

# 6. Reportes
python3 scripts/report.py --executive --health

# 7. Mantenimiento completo
python3 scripts/robust-maintain.py --pre-release
```

### 🔍 DEBUGGING
```bash
# Validación verbose con logging
python3 scripts/validate-robust.py --verbose

# Sincronización con dry-run
python3 scripts/sync-tokens.py --dry-run

# Dashboard de salud
python3 scripts/report.py --health

# Ver backups disponibles
python3 scripts/recovery.py --list-backups

# Estado de recovery
python3 scripts/recovery.py --status
```

---

## 🛠️ INSTALACIÓN INICIAL

### Opción 1: Automática (Recomendado)
```bash
cd /Users/haroldrage/Desktop/ds-base-kit
python3 scripts/setup.py --install
```

### Opción 2: Manual
```bash
# 1. Instalar hooks
python3 scripts/ci-hooks.py --install

# 2. Crear GitHub Actions
python3 scripts/ci-hooks.py --github

# 3. Auditoría inicial
python3 scripts/audit-complete.py

# 4. Sincronizar
python3 scripts/sync-tokens.py --all

# 5. Tests
python3 scripts/test.py --all
```

---

## 📊 ARCHIVOS GENERADOS

### Reportes
- `AUDIT-REPORT.json` — Auditoría exhaustiva
- `ROBUST-MAINTAIN-REPORT.json` — Mantenimiento completo
- `VALIDATION-REPORT.json` — Validación
- `EXECUTIVE-REPORT.md` — Ejecutivo
- `COVERAGE-REPORT.md` — Cobertura
- `HEALTH-DASHBOARD.md` — Salud del sistema

### Logs
- `logs/validation-*.log` — Logs de validación
- `logs/robust-maintain-*.log` — Logs de mantenimiento
- `.validation-cache/` — Cache de checksums

### Backups
- `.backups/backup-*-*/` — Backups automáticos
- `.snapshots` — Snapshots de estado

### Configuración
- `.design-system-config.json` — Configuración global
- `VERSION` — Versión actual
- `CHANGELOG.md` — Historial de cambios

---

## 🚨 TROUBLESHOOTING

### ❌ "Permission denied" en hooks
```bash
chmod +x scripts/*.py
chmod +x .git/hooks/*
```

### ❌ "No module named" en scripts
```bash
# Python 3 viene con módulos necesarios
python3 --version  # Debe ser 3.8+
```

### ❌ Pre-commit hook bloquea cambios
```bash
# Ver qué falla
python3 scripts/validate-robust.py --verbose

# Arreglar manualmente o saltarse
git commit --no-verify  # No recomendado
```

### ❌ Tokens no sincronizados
```bash
python3 scripts/sync-tokens.py --all --verbose
```

### ❌ Recovery fallida
```bash
# Ver backups disponibles
python3 scripts/recovery.py --list-backups

# Restaurar específico
python3 scripts/recovery.py --restore [backup-name]
```

---

## 📞 REFERENCIAS

- [ESTADO-v2.2.1.md](../ESTADO-v2.2.1.md) — Estado completo del sistema
- [CLAUDE.md](../CLAUDE.md) — Instrucciones para agentes IA
- [05-agentes/AGENT-CONTRACT.md](../05-agentes/AGENT-CONTRACT.md) — Contratos
- [00-fundamentos/FOUNDATIONS.md](../00-fundamentos/FOUNDATIONS.md) — Arquitectura

---

**Version:** 2.2.1+  
**Status:** 🟢 Production Ready  
**Last Updated:** 2026-07-09
