# 🚀 Instrucciones para Publicar en GitHub

Después de actualizar el proyecto a tu perfil, sigue estos pasos para publicar correctamente.

## 1. Crear el repositorio en GitHub

1. Abre https://github.com/new
2. **Repository name:** `ds-base-kit`
3. **Description:** 
   ```
   Sistema de diseño white label (3 marcas × 2 temas) operable por humanos y agentes IA. 
   Componentes, patrones, tokens (CSS/JS/JSON/SCSS), contratos, skill ds-guardian.
   ```
4. **Public:** ✅ (así agentes LLM pueden consultarlo)
5. **Initialize:** No (vamos a hacer push de un repo existente)
6. **Click:** "Create repository"

---

## 2. Configurar el repositorio local

```bash
cd /Users/haroldrage/Desktop/ds-base-kit

# Inicializar git si no está ya
git init

# Agregar tu repositorio de GitHub
git remote add origin https://github.com/haroldrage/ds-base-kit.git

# Configurar rama main
git branch -M main

# Agregar todo
git add .

# Commit inicial
git commit -m "init: Design.MD White Label v1.3.0

- 6/6 componentes documentados (100%)
- 4/4 patrones documentados (100%)
- Exportadores de tokens: CSS, JS, JSON, SCSS
- Tests visuales: VRT ready (Playwright + Percy)
- Validación WCAG 2.2 AA: 48/48 pasan
- Contratos 00-08 para agentes IA
- White label: 3 marcas × 2 temas
"

# Push a GitHub
git push -u origin main
```

---

## 3. Configurar GitHub (Settings)

### 🏷️ Topics (tags)
Agrega en Settings → General → Topics:
- `design-system`
- `white-label`
- `components`
- `design-tokens`
- `ai-ready`
- `agents`
- `markdown`

### 📋 Descripción corta (en profile del repo)
```
White label design system + component library for humans and AI agents
```

### 📌 GitHub Pages (opcional, para demo)
Si quieres servir `index.html` vía GitHub Pages:

1. Settings → Pages
2. **Source:** Deploy from branch
3. **Branch:** main
4. **Folder:** / (root)
5. **Save**

Luego tu demo estará en: `https://haroldrage.github.io/ds-base-kit/`

Actualiza entonces:
```bash
# En QUICK-START.md y otros:
sed -i '' 's|Abre `index.html`|Demo: https://haroldrage.github.io/ds-base-kit/|g' *.md
```

### 📚 README en perfil
En tu profile README (github.com/haroldrage?tab=repositories), agregar:
```markdown
### 🎨 [ds-base-kit](https://github.com/haroldrage/ds-base-kit)
White label design system con componentes, patrones, tokens y gobernanza para agentes IA.
- 6 componentes + 4 patrones (100% documentados)
- Exportadores: CSS, JS, JSON, SCSS
- WCAG 2.2 AA validado en CI
- Operado por contratos (RFC 2119)
```

---

## 4. Configurar CI/CD (GitHub Actions)

Ya está `.github/workflows/validate.yml`. Para que funcione:

1. En tu repo de GitHub, ve a **Settings → Secrets and variables**
2. Agregar secretos si necesitas (ej: `PERCY_TOKEN` para tests visuales)
3. El flujo ejecutará automáticamente en cada push

### Para tests visuales (opcional)
```bash
# Si quieres integrar Percy.io:
# 1. Crea cuenta en https://percy.io
# 2. Conecta tu repo
# 3. Agrega PERCY_TOKEN en GitHub Secrets
# 4. El workflow .github/workflows/vrt.yml tomará snapshots en cada PR
```

---

## 5. Versioning y releases

Después del primer push, crear una release:

```bash
# Crear un tag
git tag -a v1.3.0 -m "v1.3.0: 100% cobertura + exportadores"

# Push del tag
git push origin v1.3.0

# O ir a GitHub → Releases → Draft a new release
# Tag: v1.3.0
# Title: Design.MD v1.3.0 — 100% Cobertura
# Description: (copiar del CHANGELOG.md sección v1.3.0)
```

---

## 6. Documentación en GitHub

### Wiki (opcional)
En Settings → Features, habilitar Wiki si quieres agregar guides.

### Discussions (opcional)
Para que agentes puedan hacer preguntas:
Settings → Features → Discussions → Enable

---

## 7. Integración con agentes LLM

Una vez publicado, agentes pueden acceder:

```bash
# Agentes externos descubren:
GET https://github.com/haroldrage/ds-base-kit/raw/main/llms.txt

# O leer directamente:
cat https://github.com/haroldrage/ds-base-kit/raw/main/05-agentes/component-manifest.json
```

---

## ✅ Checklist final

- [ ] Repositorio creado en GitHub
- [ ] Push inicial con `git push -u origin main`
- [ ] Settings completados (descripciones, topics)
- [ ] GitHub Pages habilitado (si quieres demo en vivo)
- [ ] CI/CD verificado (Actions ejecutándose)
- [ ] Release v1.3.0 creada
- [ ] Links actualizados si usas GitHub Pages
- [ ] README del perfil actualizado

---

## 🎯 Comandos rápidos

```bash
# Ver estado del repo
git remote -v
git status
git log --oneline -5

# Hacer cambios y push
git add .
git commit -m "fix: descripción del cambio"
git push

# Ver en GitHub
open https://github.com/haroldrage/ds-base-kit
```

---

**Después de publicar, comparte el link:**
https://github.com/haroldrage/ds-base-kit

¡Listo para que agentes IA descubran y operen sobre tu sistema de diseño! 🚀
