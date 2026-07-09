#!/usr/bin/env python3
"""
🚀 ORQUESTADOR ROBUSTO MEJORADO v2
Integra auditoría, sincronización, validación, tests, recovery y versionado

Funciones:
1. Ejecución robusta de todos los sistemas
2. Logging centralizado
3. Recuperación automática ante errores
4. Reportes completos
5. Automatización completa

Uso: python3 scripts/robust-maintain.py [--full] [--pre-release] [--recovery] [--test] [--verbose]
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime
import logging

class RobustMaintainer:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.logs_dir = self.root / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Setup logging
        log_file = self.logs_dir / f"robust-maintain-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("RobustMaintainer")
        
        self.operations = []
        self.failures = []
        
    def run_full_maintenance(self, recovery=False, test=False):
        """Ejecutar mantenimiento completo y robusto"""
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║         🚀 MANTENIMIENTO ROBUSTO v2.2.1+                  ║")
        print("║    Auditoría + Sincronización + Validación + Testing      ║")
        print("╚════════════════════════════════════════════════════════════╝")
        
        self.logger.info("Iniciando mantenimiento robusto completo")
        
        steps = [
            ("Backup Pre-Mantenimiento", self._step_backup),
            ("Validación Robusta", self._step_validate),
            ("Auditoría Completa", self._step_audit),
            ("Sincronización de Tokens", self._step_sync),
            ("Generación de Componentes", self._step_generate),
            ("Testing de Integridad", self._step_test if test else None),
            ("Generación de Reportes", self._step_reports),
            ("Snapshot Post-Mantenimiento", self._step_snapshot),
        ]
        
        for step_name, step_func in steps:
            if step_func is None:
                continue
            
            print(f"\n▶️  {step_name}...")
            try:
                success = step_func()
                if success:
                    self.operations.append({
                        "step": step_name,
                        "status": "SUCCESS",
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"✅ {step_name} completado")
                else:
                    self.failures.append(step_name)
                    print(f"⚠️  {step_name} completado con advertencias")
            except Exception as e:
                self.logger.error(f"Error en {step_name}: {e}")
                self.failures.append(step_name)
                print(f"❌ Error en {step_name}: {e}")
                
                if recovery and "recovery" not in step_name.lower():
                    self.logger.warning(f"Intentando recuperación...")
                    self._attempt_recovery()
        
        self._print_final_report()
    
    def _step_backup(self) -> bool:
        """Crear backup antes del mantenimiento"""
        result = subprocess.run(
            ["python3", "scripts/recovery.py", "--backup"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def _step_validate(self) -> bool:
        """Ejecutar validación robusta"""
        result = subprocess.run(
            ["python3", "scripts/validate-robust.py"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        self.logger.info(f"Validación: {result.stdout[:500]}")
        return result.returncode == 0
    
    def _step_audit(self) -> bool:
        """Ejecutar auditoría completa"""
        result = subprocess.run(
            ["python3", "scripts/audit-complete.py", "--export"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def _step_sync(self) -> bool:
        """Sincronizar tokens"""
        result = subprocess.run(
            ["python3", "scripts/sync-tokens.py", "--all"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def _step_generate(self) -> bool:
        """Generar componentes faltantes"""
        result = subprocess.run(
            ["python3", "scripts/generate-components.py", "--all"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def _step_test(self) -> bool:
        """Ejecutar tests"""
        result = subprocess.run(
            ["python3", "scripts/test.py", "--all"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def _step_reports(self) -> bool:
        """Generar reportes"""
        result = subprocess.run(
            ["python3", "scripts/report.py", "--executive", "--health"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def _step_snapshot(self) -> bool:
        """Crear snapshot post-mantenimiento"""
        result = subprocess.run(
            ["python3", "scripts/recovery.py", "--snapshot", "post-maintenance"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def _attempt_recovery(self):
        """Intentar recuperación automática"""
        self.logger.info("Ejecutando procedimiento de recuperación...")
        
        result = subprocess.run(
            ["python3", "scripts/recovery.py", "--restore"],
            cwd=self.root,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            self.logger.info("✅ Recuperación exitosa")
        else:
            self.logger.error("❌ Fallo en recuperación")
    
    def _print_final_report(self):
        """Imprimir reporte final"""
        print("\n" + "=" * 60)
        print("📊 REPORTE FINAL DE MANTENIMIENTO")
        print("=" * 60)
        
        successful = len(self.operations)
        failed = len(self.failures)
        total = successful + failed
        
        print(f"\n✅ Operaciones exitosas: {successful}/{total}")
        if self.failures:
            print(f"❌ Operaciones fallidas: {failed}")
            for failure in self.failures:
                print(f"  - {failure}")
        
        # Guardar reporte JSON
        report = {
            "timestamp": datetime.now().isoformat(),
            "status": "SUCCESS" if not self.failures else "PARTIAL",
            "operations": self.operations,
            "failures": self.failures,
            "duration": len(self.operations) * 10  # Estimado
        }
        
        report_file = self.root / "ROBUST-MAINTAIN-REPORT.json"
        report_file.write_text(json.dumps(report, indent=2))
        
        print(f"\n💾 Reporte guardado: {report_file}")
        print("=" * 60 + "\n")


def main():
    full = "--full" in sys.argv or len(sys.argv) == 1
    pre_release = "--pre-release" in sys.argv
    recovery = "--recovery" in sys.argv
    test = "--test" in sys.argv
    verbose = "--verbose" in sys.argv
    
    maintainer = RobustMaintainer()
    
    if pre_release:
        # Pre-release: más exhaustivo
        print("🚀 MODO PRE-RELEASE: Validación y testing exhaustivo")
        maintainer.run_full_maintenance(recovery=True, test=True)
    elif full:
        maintainer.run_full_maintenance(recovery=recovery, test=test)
    
    print("✅ Mantenimiento completado")


if __name__ == "__main__":
    main()
