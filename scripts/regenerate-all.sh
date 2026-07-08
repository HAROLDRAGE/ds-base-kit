#!/bin/bash
# scripts/regenerate-all.sh
# Regenera todos los artefactos desde el manifiesto

set -e

echo "🔄 Regenerando todos los artefactos desde component-manifest.json..."

# Validar
echo "✓ Validando schema + contraste..."
python3 scripts/validate.py

# Exportar tokens
echo "✓ Exportando CSS..."
python3 scripts/export-tokens.py --format css

echo "✓ Exportando JavaScript..."
python3 scripts/export-tokens.py --format js

echo "✓ Exportando JSON..."
python3 scripts/export-tokens.py --format json

echo "✓ Exportando SCSS..."
python3 scripts/export-tokens.py --format scss

echo ""
echo "✅ Todos los artefactos regenerados:"
echo "   - 01-tokens/tokens.css"
echo "   - 01-tokens/tokens.js"
echo "   - 01-tokens/tokens.json"
echo "   - 01-tokens/tokens.scss"
echo ""
echo "Próximo: git add 01-tokens/* && git commit -m 'chore: regenerate tokens'"
