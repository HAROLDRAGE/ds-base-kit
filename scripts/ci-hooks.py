#!/usr/bin/env python3
"""
🔗 HOOKS DE PRE-COMMIT Y CI/CD
Validación automática antes de commit y en CI/CD

Funciones:
1. Pre-commit hooks (ejecuta validaciones)
2. GitHub Actions setup
3. Pre-push checks
4. Auto-fix en pre-commit
5. Bloquear cambios incoherentes

Uso: 
  python3 scripts/ci-hooks.py --install
  python3 scripts/ci-hooks.py --test
"""

import subprocess
import json
from pathlib import Path
from typing import List, Tuple
import sys
import os

class CIHookManager:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.git_dir = self.root / ".git"
        self.hooks_dir = self.git_dir / "hooks"
        
    def install_hooks(self) -> bool:
        """Instalar pre-commit hooks"""
        print("\n🔗 INSTALANDO HOOKS DE PRE-COMMIT")
        print("=" * 60)
        
        if not self.git_dir.exists():
            print("✗ No es un repositorio Git")
            return False
        
        # Crear directorio de hooks si no existe
        self.hooks_dir.mkdir(exist_ok=True)
        
        # Pre-commit hook
        pre_commit_hook = self.hooks_dir / "pre-commit"
        pre_commit_content = '''#!/bin/bash
# Pre-commit hook: Validación automática

echo "🔍 Ejecutando validaciones pre-commit..."

cd "$(git rev-parse --show-toplevel)" || exit 1

# 1. Validar sintaxis
echo "  ✓ Validando sintaxis..."
python3 scripts/validate-robust.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "  ✗ Errores de sintaxis encontrados"
  exit 1
fi

# 2. Sincronizar tokens
echo "  ✓ Sincronizando tokens..."
python3 scripts/sync-tokens.py --all > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "  ✗ Fallo en sincronización de tokens"
  exit 1
fi

# 3. Auditar coherencia
echo "  ✓ Auditando coherencia..."
python3 scripts/audit-complete.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "  ✗ Problemas de coherencia detectados"
  exit 1
fi

echo "✅ Pre-commit checks pasaron"
exit 0
'''
        
        pre_commit_hook.write_text(pre_commit_content)
        os.chmod(pre_commit_hook, 0o755)
        print("✅ Pre-commit hook instalado")
        
        # Pre-push hook
        pre_push_hook = self.hooks_dir / "pre-push"
        pre_push_content = '''#!/bin/bash
# Pre-push hook: Validación completa antes de push

echo "🚀 Ejecutando validaciones pre-push..."

cd "$(git rev-parse --show-toplevel)" || exit 1

# Ejecutar suite completa de validación
python3 scripts/maintain.py --validate > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "✗ Validación fallida. No se puede hacer push."
  exit 1
fi

echo "✅ Pre-push checks pasaron"
exit 0
'''
        
        pre_push_hook.write_text(pre_push_content)
        os.chmod(pre_push_hook, 0o755)
        print("✅ Pre-push hook instalado")
        
        # Commit-msg hook (opcional)
        commit_msg_hook = self.hooks_dir / "commit-msg"
        commit_msg_content = '''#!/bin/bash
# Commit-msg hook: Validar mensaje de commit

COMMIT_MSG_FILE=$1
COMMIT_SOURCE=$2

# Leer mensaje
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Validar formato
if ! echo "$COMMIT_MSG" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore|ci):"; then
  echo "✗ Formato de commit inválido."
  echo "Usar: <type>: <mensaje>"
  echo "Types: feat|fix|docs|style|refactor|perf|test|chore|ci"
  exit 1
fi

exit 0
'''
        
        commit_msg_hook.write_text(commit_msg_content)
        os.chmod(commit_msg_hook, 0o755)
        print("✅ Commit-msg hook instalado")
        
        return True
    
    def create_github_actions(self) -> bool:
        """Crear GitHub Actions workflows"""
        print("\n🔗 CREANDO GITHUB ACTIONS")
        print("=" * 60)
        
        workflows_dir = self.root / ".github" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Workflow: Validación en cada push/PR
        validate_workflow = '''name: Validación Robusta

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Auditoría Completa
      run: python3 scripts/audit-complete.py --export
    
    - name: Sincronización de Tokens
      run: python3 scripts/sync-tokens.py --all
    
    - name: Validación Robusta
      run: python3 scripts/validate-robust.py
    
    - name: Upload Reportes
      uses: actions/upload-artifact@v2
      with:
        name: validation-reports
        path: |
          AUDIT-REPORT.json
          VALIDATION-REPORT.json
          logs/
'''
        
        (workflows_dir / "validate.yml").write_text(validate_workflow)
        print("✅ Workflow de validación creado")
        
        # Workflow: Release
        release_workflow = '''name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Mantenimiento Pre-Release
      run: python3 scripts/maintain.py --full
    
    - name: Generar Reportes
      run: python3 scripts/report.py --executive --health
    
    - name: Crear Release
      uses: actions/create-release@v1
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body_path: EXECUTIVE-REPORT.md
'''
        
        (workflows_dir / "release.yml").write_text(release_workflow)
        print("✅ Workflow de release creado")
        
        return True
    
    def test_hooks(self) -> bool:
        """Probar que los hooks estén funcionando"""
        print("\n🧪 PROBANDO HOOKS")
        print("=" * 60)
        
        hooks = ["pre-commit", "pre-push", "commit-msg"]
        
        for hook_name in hooks:
            hook_path = self.hooks_dir / hook_name
            
            if not hook_path.exists():
                print(f"✗ Hook {hook_name} no encontrado")
                continue
            
            # Verificar que sea ejecutable
            if os.access(hook_path, os.X_OK):
                print(f"✓ Hook {hook_name} está instalado y es ejecutable")
            else:
                print(f"⚠️  Hook {hook_name} no es ejecutable")
                os.chmod(hook_path, 0o755)
        
        return True


def main():
    install = "--install" in sys.argv
    test = "--test" in sys.argv
    github = "--github" in sys.argv
    
    manager = CIHookManager()
    
    if install:
        manager.install_hooks()
    
    if github:
        manager.create_github_actions()
    
    if test or not any([install, github, test]):
        manager.test_hooks()


if __name__ == "__main__":
    main()
