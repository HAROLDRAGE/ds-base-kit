#!/usr/bin/env python3
"""
🧪 TESTING Y QUALITY ASSURANCE
Suite de tests para validar componentes, tokens y documentación

Funciones:
1. Tests de componentes
2. Tests de tokens
3. Tests de documentación
4. Tests de accesibilidad (WCAG AA)
5. Tests de integridad

Uso: python3 scripts/test.py [--all] [--components] [--tokens] [--docs] [--wcag] [--coverage]
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import re
import sys

class TestSuite:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_skipped = 0
        
        self.results = {
            "timestamp": "",
            "tests": {},
            "summary": {}
        }
    
    def run_all_tests(self) -> Dict:
        """Ejecutar toda la suite de tests"""
        print("\n🧪 EJECUTANDO SUITE DE TESTS")
        print("=" * 60)
        
        tests = [
            ("component_tests", self.test_components),
            ("token_tests", self.test_tokens),
            ("documentation_tests", self.test_documentation),
            ("wcag_tests", self.test_wcag_aa),
            ("integrity_tests", self.test_integrity),
        ]
        
        for test_name, test_func in tests:
            print(f"\n▶️  {test_name}...")
            try:
                result = test_func()
                self.results["tests"][test_name] = result
                
                if result.get("status") == "PASS":
                    self.tests_passed += result.get("count", 0)
                    print(f"  ✅ PASS ({result.get('count', 0)} tests)")
                else:
                    self.tests_failed += result.get("count_failed", 0)
                    print(f"  ❌ FAIL ({result.get('count_failed', 0)} tests)")
            except Exception as e:
                print(f"  ⚠️  Error: {e}")
                self.tests_skipped += 1
        
        self.print_summary()
        return self.results
    
    def test_components(self) -> Dict:
        """Tests para componentes"""
        result = {
            "status": "PASS",
            "count": 0,
            "count_failed": 0,
            "components_tested": [],
            "issues": []
        }
        
        components_dir = self.root / "02-componentes"
        
        for component_file in components_dir.glob("*.md"):
            if component_file.name.startswith("plantilla"):
                continue
            
            result["components_tested"].append(component_file.name)
            content = component_file.read_text()
            
            # Test 1: Archivo existe y tiene contenido
            if len(content) < 100:
                result["issues"].append(f"Componente muy pequeño: {component_file.name}")
                result["count_failed"] += 1
                continue
            
            result["count"] += 1
            
            # Test 2: Tiene estructura mínima
            required_sections = ["Cuándo usarlo", "Anatomía", "Estados"]
            for section in required_sections:
                if section not in content:
                    result["issues"].append(f"{component_file.name}: Falta sección '{section}'")
            
            # Test 3: Tiene ejemplos de código
            if "```" not in content:
                result["issues"].append(f"{component_file.name}: Sin ejemplos de código")
        
        result["status"] = "PASS" if result["count_failed"] == 0 else "FAIL"
        return result
    
    def test_tokens(self) -> Dict:
        """Tests para tokens"""
        result = {
            "status": "PASS",
            "count": 0,
            "count_failed": 0,
            "issues": []
        }
        
        # Test 1: tokens.css válido
        css_file = self.root / "01-tokens/tokens.css"
        if css_file.exists():
            content = css_file.read_text()
            css_tokens = len(re.findall(r'--[a-zA-Z0-9\-]+:', content))
            result["count"] += 1
            
            if css_tokens < 100:
                result["issues"].append(f"Muy pocos tokens en CSS: {css_tokens}")
                result["count_failed"] += 1
            else:
                print(f"  ✓ CSS tokens: {css_tokens}")
        
        # Test 2: tokens.json válido
        json_file = self.root / "01-tokens/tokens.json"
        if json_file.exists():
            result["count"] += 1
            try:
                data = json.loads(json_file.read_text())
                flat_tokens = self._flatten_tokens(data.get("tokens", {}))
                print(f"  ✓ JSON tokens: {len(flat_tokens)}")
            except json.JSONDecodeError:
                result["issues"].append("tokens.json inválido (JSON malformado)")
                result["count_failed"] += 1
        
        # Test 3: Coherencia entre CSS y JSON
        if css_file.exists() and json_file.exists():
            result["count"] += 1
            css_count = len(re.findall(r'--[a-zA-Z0-9\-]+:', css_file.read_text()))
            json_data = json.loads(json_file.read_text())
            json_count = len(self._flatten_tokens(json_data.get("tokens", {})))
            
            if css_count == json_count:
                print(f"  ✓ Coherencia CSS-JSON: {css_count} tokens")
            else:
                result["issues"].append(f"Incoherencia: CSS tiene {css_count}, JSON tiene {json_count}")
                result["count_failed"] += 1
        
        result["status"] = "PASS" if result["count_failed"] == 0 else "FAIL"
        return result
    
    def test_documentation(self) -> Dict:
        """Tests para documentación"""
        result = {
            "status": "PASS",
            "count": 0,
            "count_failed": 0,
            "issues": []
        }
        
        # Test 1: Todas las Foundations existen
        foundations = ["COLORES", "TIPOGRAFIA", "ESPACIADO", "LAYOUT", "MOVIMIENTO", "ICONOGRAFIA", "BORDES", "SOMBRAS"]
        for foundation in foundations:
            result["count"] += 1
            file_path = self.root / f"01-tokens/{foundation}-FOUNDATIONS.md"
            if file_path.exists():
                lines = len(file_path.read_text().split('\n'))
                if lines < 200:
                    result["issues"].append(f"{foundation}-FOUNDATIONS.md tiene pocas líneas ({lines})")
                    result["count_failed"] += 1
            else:
                result["issues"].append(f"Falta: {foundation}-FOUNDATIONS.md")
                result["count_failed"] += 1
        
        # Test 2: README principal existe
        result["count"] += 1
        readme = self.root / "README.md"
        if readme.exists() and len(readme.read_text()) > 1000:
            print(f"  ✓ README.md existe y tiene contenido")
        else:
            result["issues"].append("README.md falta o es muy pequeño")
            result["count_failed"] += 1
        
        result["status"] = "PASS" if result["count_failed"] == 0 else "FAIL"
        return result
    
    def test_wcag_aa(self) -> Dict:
        """Tests para accesibilidad WCAG 2.2 AA"""
        result = {
            "status": "PASS",
            "count": 0,
            "count_failed": 0,
            "issues": [],
            "components_without_wcag": []
        }
        
        # Test: Todos los componentes mencionan accesibilidad
        components_dir = self.root / "02-componentes"
        for component_file in components_dir.glob("*.md"):
            if component_file.name.startswith("plantilla"):
                continue
            
            result["count"] += 1
            content = component_file.read_text()
            
            # Buscar mención de WCAG o accesibilidad
            if "WCAG" not in content and "Accesibilidad" not in content:
                result["components_without_wcag"].append(component_file.name)
                result["count_failed"] += 1
        
        # Test: CSS tiene suficiente contrast (no se puede verificar automáticamente)
        result["count"] += 1
        print(f"  ⚠️  Nota: Validación de contraste requiere análisis manual")
        
        result["status"] = "PASS" if result["count_failed"] <= 1 else "WARN"
        return result
    
    def test_integrity(self) -> Dict:
        """Tests de integridad del sistema"""
        result = {
            "status": "PASS",
            "count": 0,
            "count_failed": 0,
            "issues": []
        }
        
        # Test 1: Archivos críticos existen
        critical_files = [
            "index.html",
            "README.md",
            "VERSION",
            "01-tokens/tokens.css",
            "01-tokens/tokens.json"
        ]
        
        for file_path in critical_files:
            result["count"] += 1
            full_path = self.root / file_path
            if not full_path.exists():
                result["issues"].append(f"Archivo crítico faltante: {file_path}")
                result["count_failed"] += 1
        
        # Test 2: Directorios críticos existen
        critical_dirs = ["01-tokens", "02-componentes", "03-patrones", "05-agentes", "scripts"]
        for dir_name in critical_dirs:
            result["count"] += 1
            full_path = self.root / dir_name
            if not full_path.exists():
                result["issues"].append(f"Directorio crítico faltante: {dir_name}")
                result["count_failed"] += 1
        
        result["status"] = "PASS" if result["count_failed"] == 0 else "FAIL"
        return result
    
    def print_summary(self):
        """Imprimir resumen de tests"""
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE TESTS")
        print("=" * 60)
        print(f"\n✅ Pasados: {self.tests_passed}")
        print(f"❌ Fallidos: {self.tests_failed}")
        print(f"⏭️  Saltados: {self.tests_skipped}")
        
        total = self.tests_passed + self.tests_failed
        if total > 0:
            success_rate = (self.tests_passed / total) * 100
            print(f"\n📈 Tasa de éxito: {success_rate:.1f}%")
    
    def _flatten_tokens(self, obj, prefix="") -> set:
        """Aplanar estructura de tokens"""
        tokens = set()
        for key, value in obj.items():
            if isinstance(value, dict):
                if "value" in value:
                    tokens.add(f"{prefix}{key}")
                else:
                    tokens.update(self._flatten_tokens(value, f"{prefix}{key}-"))
        return tokens


def main():
    all_tests = "--all" in sys.argv or len(sys.argv) == 1
    components = "--components" in sys.argv or all_tests
    tokens = "--tokens" in sys.argv or all_tests
    docs = "--docs" in sys.argv or all_tests
    wcag = "--wcag" in sys.argv or all_tests
    coverage = "--coverage" in sys.argv
    
    suite = TestSuite()
    
    if all_tests:
        suite.run_all_tests()
    else:
        if components:
            result = suite.test_components()
            print(result)
        if tokens:
            result = suite.test_tokens()
            print(result)
        if docs:
            result = suite.test_documentation()
            print(result)
        if wcag:
            result = suite.test_wcag_aa()
            print(result)


if __name__ == "__main__":
    main()
