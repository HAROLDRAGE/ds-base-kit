#!/usr/bin/env python3
"""
🏗️  SCRIPT MAESTRO DE MANTENIMIENTO INTEGRAL
Orquesta auditoría, sincronización, generación y validación del sistema

Funciones:
1. Ejecutar auditoría completa
2. Sincronizar tokens en 4 fuentes
3. Generar componentes faltantes
4. Validar integridad completa
5. Generar reporte de estado
6. Limpiar y organizar sistema

Uso: python3 scripts/maintain.py [--full] [--audit] [--sync] [--generate] [--validate] [--report] [--dry-run]
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
import sys

class SystemMaintenance:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "operations": [],
            "status": "PENDING"
        }
        
    def run_audit(self, verbose=False) -> bool:
        """Ejecutar auditoría completa"""
        print("\n" + "=" * 60)
        print("🔍 PASO 1: AUDITORÍA COMPLETA")
        print("=" * 60)
        
        cmd = ["python3", "scripts/audit-complete.py"]
        if verbose:
            cmd.append("--verbose")
        cmd.append("--export")
        
        try:
            result = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, timeout=30)
            print(result.stdout)
            if result.returncode == 0:
                self.results["operations"].append({
                    "operation": "audit",
                    "status": "SUCCESS",
                    "timestamp": datetime.now().isoformat()
                })
                return True
            else:
                print(result.stderr)
                self.results["operations"].append({
                    "operation": "audit",
                    "status": "FAILED",
                    "error": result.stderr
                })
                return False
        except Exception as e:
            print(f"✗ Error en auditoría: {e}")
            return False
    
    def run_sync(self, dry_run=False) -> bool:
        """Ejecutar sincronización de tokens"""
        print("\n" + "=" * 60)
        print("🔄 PASO 2: SINCRONIZACIÓN DE TOKENS")
        print("=" * 60)
        
        cmd = ["python3", "scripts/sync-tokens.py", "--all", "--verbose"]
        if dry_run:
            cmd.append("--dry-run")
        
        try:
            result = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, timeout=30)
            print(result.stdout)
            if result.returncode == 0:
                self.results["operations"].append({
                    "operation": "sync_tokens",
                    "status": "SUCCESS",
                    "timestamp": datetime.now().isoformat()
                })
                return True
            else:
                print(result.stderr)
                return False
        except Exception as e:
            print(f"✗ Error en sincronización: {e}")
            return False
    
    def run_generate(self, dry_run=False) -> bool:
        """Ejecutar generación de componentes faltantes"""
        print("\n" + "=" * 60)
        print("🧩 PASO 3: GENERACIÓN DE COMPONENTES FALTANTES")
        print("=" * 60)
        
        cmd = ["python3", "scripts/generate-components.py", "--all"]
        if dry_run:
            cmd.append("--dry-run")
        
        try:
            result = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, timeout=30)
            print(result.stdout)
            if result.returncode == 0:
                self.results["operations"].append({
                    "operation": "generate_components",
                    "status": "SUCCESS",
                    "timestamp": datetime.now().isoformat()
                })
                return True
            else:
                print(result.stderr)
                return False
        except Exception as e:
            print(f"✗ Error en generación: {e}")
            return False
    
    def run_validate(self) -> bool:
        """Ejecutar validación de coherencia"""
        print("\n" + "=" * 60)
        print("✅ PASO 4: VALIDACIÓN DE COHERENCIA")
        print("=" * 60)
        
        cmd = ["python3", "scripts/validate-coherence.py"]
        
        try:
            result = subprocess.run(cmd, cwd=self.root, capture_output=True, text=True, timeout=30)
            # Mostrar últimas líneas
            lines = result.stdout.split('\n')
            for line in lines[-30:]:
                if line.strip():
                    print(line)
            
            if result.returncode == 0:
                self.results["operations"].append({
                    "operation": "validate",
                    "status": "SUCCESS",
                    "timestamp": datetime.now().isoformat()
                })
                return True
            else:
                return False
        except Exception as e:
            print(f"✗ Error en validación: {e}")
            return False
    
    def cleanup_and_organize(self) -> bool:
        """Limpiar y organizar el sistema"""
        print("\n" + "=" * 60)
        print("🧹 PASO 5: LIMPIEZA Y ORGANIZACIÓN")
        print("=" * 60)
        
        try:
            # Verificar que todos los directorios existan
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
                "scripts"
            ]
            
            for dir_path in required_dirs:
                full_path = self.root / dir_path
                if not full_path.exists():
                    full_path.mkdir(parents=True, exist_ok=True)
                    print(f"✓ Directorio creado: {dir_path}")
                else:
                    print(f"✓ Directorio verificado: {dir_path}")
            
            # Verificar archivos críticos
            critical_files = [
                "01-tokens/tokens.css",
                "01-tokens/tokens.json",
                "05-agentes/component-manifest.json",
                "assets/js/main.js",
                "index.html"
            ]
            
            for file_path in critical_files:
                full_path = self.root / file_path
                if full_path.exists():
                    print(f"✓ Archivo verificado: {file_path}")
                else:
                    print(f"⚠️  Archivo faltante: {file_path}")
            
            self.results["operations"].append({
                "operation": "cleanup",
                "status": "SUCCESS",
                "timestamp": datetime.now().isoformat()
            })
            
            return True
        except Exception as e:
            print(f"✗ Error en limpieza: {e}")
            return False
    
    def generate_maintenance_report(self) -> dict:
        """Generar reporte de mantenimiento"""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE MANTENIMIENTO")
        print("=" * 60)
        
        successful = sum(1 for op in self.results["operations"] if op.get("status") == "SUCCESS")
        failed = sum(1 for op in self.results["operations"] if op.get("status") == "FAILED")
        
        self.results["status"] = "SUCCESS" if failed == 0 else "PARTIAL" if successful > 0 else "FAILED"
        
        print(f"\n✅ Operaciones exitosas: {successful}")
        print(f"❌ Operaciones fallidas: {failed}")
        print(f"\n→ Status general: {self.results['status']}")
        
        print(f"\nOperaciones realizadas:")
        for op in self.results["operations"]:
            status = "✓" if op.get("status") == "SUCCESS" else "✗"
            print(f"  {status} {op['operation']}: {op['status']}")
        
        # Guardar reporte
        report_file = self.root / "MAINTENANCE-REPORT.json"
        report_file.write_text(json.dumps(self.results, indent=2, ensure_ascii=False))
        print(f"\n💾 Reporte guardado en: {report_file}")
        
        return self.results
    
    def run_full_maintenance(self, dry_run=False):
        """Ejecutar mantenimiento completo"""
        print("\n" + "╔" + "=" * 58 + "╗")
        print("║" + " 🏗️  MANTENIMIENTO INTEGRAL DEL SISTEMA v2.2.1 ".center(58) + "║")
        print("╚" + "=" * 58 + "╝")
        
        if dry_run:
            print("\n🔍 MODO DRY-RUN: Se simularán cambios sin guardar\n")
        
        # Ejecutar operaciones
        steps = [
            ("Auditoría", self.run_audit),
            ("Sincronización", lambda: self.run_sync(dry_run=dry_run)),
            ("Generación", lambda: self.run_generate(dry_run=dry_run)),
            ("Validación", self.run_validate),
            ("Limpieza", self.cleanup_and_organize)
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n⚠️  {step_name} completada con advertencias")
                else:
                    print(f"\n✓ {step_name} completada")
            except Exception as e:
                print(f"\n✗ Error en {step_name}: {e}")
        
        # Generar reporte
        self.generate_maintenance_report()
        
        print("\n" + "=" * 60)
        if self.results["status"] == "SUCCESS":
            print("🎉 ¡MANTENIMIENTO COMPLETO Y EXITOSO!")
        elif self.results["status"] == "PARTIAL":
            print("⚠️  Mantenimiento completado con algunas advertencias")
        else:
            print("❌ Mantenimiento fallido - revisar errores arriba")
        print("=" * 60 + "\n")


def main():
    full = "--full" in sys.argv or (len(sys.argv) == 1)  # Por defecto, full
    audit = "--audit" in sys.argv
    sync = "--sync" in sys.argv
    generate = "--generate" in sys.argv
    validate = "--validate" in sys.argv
    report = "--report" in sys.argv
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    
    maintainer = SystemMaintenance()
    
    if full:
        maintainer.run_full_maintenance(dry_run=dry_run)
    else:
        if audit:
            maintainer.run_audit(verbose=verbose)
        if sync:
            maintainer.run_sync(dry_run=dry_run)
        if generate:
            maintainer.run_generate(dry_run=dry_run)
        if validate:
            maintainer.run_validate()
        if report:
            maintainer.generate_maintenance_report()
        
        if not any([audit, sync, generate, validate, report]):
            print("Uso: python3 scripts/maintain.py [options]")
            print("  --full          Ejecutar mantenimiento completo (default)")
            print("  --audit         Solo auditoría")
            print("  --sync          Solo sincronización")
            print("  --generate      Solo generación")
            print("  --validate      Solo validación")
            print("  --report        Solo generar reporte")
            print("  --dry-run       Simular sin guardar cambios")
            print("  --verbose       Salida detallada")


if __name__ == "__main__":
    main()
