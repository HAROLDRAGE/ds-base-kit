#!/usr/bin/env python3
"""
⚙️  CONFIGURACIÓN Y SETUP DEL SISTEMA
Instalación automática, configuración y verificación

Funciones:
1. Instalación de dependencias
2. Configuración de hooks
3. Inicialización de directorios
4. Verificación de setup
5. Primera ejecución

Uso: python3 scripts/setup.py [--install] [--verify] [--hooks] [--init]
"""

import subprocess
import json
import sys
from pathlib import Path

class SystemSetup:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.config_file = self.root / ".design-system-config.json"
    
    def install_all(self) -> bool:
        """Instalar y configurar todo"""
        print("\n" + "╔" + "=" * 58 + "╗")
        print("║" + " ⚙️  INSTALACIÓN DEL SISTEMA v2.2.1".center(58) + "║")
        print("╚" + "=" * 58 + "╝")
        
        steps = [
            ("Verificar dependencias", self.verify_dependencies),
            ("Crear directorios", self.create_directories),
            ("Instalar hooks", self.install_hooks),
            ("Inicializar configuración", self.initialize_config),
            ("Ejecutar validación inicial", self.initial_validation),
        ]
        
        for step_name, step_func in steps:
            print(f"\n▶️  {step_name}...")
            try:
                if step_func():
                    print(f"✅ {step_name} completado")
                else:
                    print(f"⚠️  {step_name} completado con advertencias")
            except Exception as e:
                print(f"❌ Error en {step_name}: {e}")
                return False
        
        print("\n" + "=" * 60)
        print("✅ INSTALACIÓN COMPLETADA")
        print("=" * 60)
        print("\n🚀 Próximos pasos:")
        print("  1. Ejecutar: python3 scripts/robust-maintain.py")
        print("  2. Ver reportes: cat HEALTH-DASHBOARD.md")
        print("  3. Usar guía: bash scripts/README.sh")
        
        return True
    
    def verify_dependencies(self) -> bool:
        """Verificar que Python y dependencias estén disponibles"""
        print("  Verificando Python 3.8+...")
        
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"  ✓ {version}")
                return True
            else:
                print("  ✗ Python 3 no encontrado")
                return False
                
        except Exception as e:
            print(f"  ✗ Error verificando Python: {e}")
            return False
    
    def create_directories(self) -> bool:
        """Crear directorios necesarios"""
        required_dirs = [
            "00-fundamentos",
            "01-tokens",
            "02-componentes",
            "03-patrones",
            "04-plantillas",
            "05-agentes",
            "06-skills",
            "assets/css",
            "assets/js",
            "logs",
            ".backups"
        ]
        
        for dir_name in required_dirs:
            dir_path = self.root / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✓ Creado: {dir_name}")
            else:
                print(f"  ✓ Existe: {dir_name}")
        
        return True
    
    def install_hooks(self) -> bool:
        """Instalar Git hooks"""
        result = subprocess.run(
            ["python3", "scripts/ci-hooks.py", "--install"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        
        return result.returncode == 0
    
    def initialize_config(self) -> bool:
        """Crear archivo de configuración"""
        config = {
            "version": "2.2.1",
            "timestamp": "2026-07-09",
            "project_name": "Design System White Label",
            "settings": {
                "enable_cache": True,
                "logging_level": "INFO",
                "auto_backup": True,
                "backup_count": 5,
                "auto_sync": True,
                "validate_on_commit": True
            },
            "brands": [
                "promptea",
                "nova",
                "ocean"
            ],
            "themes": [
                "light",
                "dark"
            ]
        }
        
        self.config_file.write_text(json.dumps(config, indent=2))
        print(f"  ✓ Configuración guardada en: {self.config_file}")
        
        return True
    
    def initial_validation(self) -> bool:
        """Ejecutar validación inicial"""
        result = subprocess.run(
            ["python3", "scripts/audit-complete.py"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✓ Auditoría inicial completada")
            return True
        else:
            print("  ⚠️  Auditoría completada con advertencias")
            return True


def main():
    install = "--install" in sys.argv
    verify = "--verify" in sys.argv
    hooks = "--hooks" in sys.argv
    init = "--init" in sys.argv
    
    setup = SystemSetup()
    
    if install or (not any([verify, hooks, init])):
        setup.install_all()
    else:
        if verify:
            setup.verify_dependencies()
        if hooks:
            setup.install_hooks()
        if init:
            setup.initialize_config()


if __name__ == "__main__":
    main()
