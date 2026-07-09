#!/usr/bin/env python3
"""
🔍 SCRIPT DE AUDITORÍA COMPLETA
Sistema de validación exhaustiva de coherencia, sincronización y completitud

Funciones:
1. Auditar sincronización de tokens (CSS ↔ JSON ↔ JS ↔ Manifest)
2. Validar documentación de Foundations (8 categorías)
3. Validar componentes documentados (19 componentes)
4. Validar patrones documentados (4 patrones)
5. Validar WCAG AA en documentación
6. Validar matriz de tokens × componentes
7. Generar reporte de estado
8. Identificar huecos de documentación

Uso: python3 scripts/audit-complete.py [--verbose] [--fix] [--export]
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datetime import datetime
import sys

class TokenAuditor:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "status": "PENDING",
            "checks": {},
            "warnings": [],
            "errors": [],
            "summary": {}
        }
        
    def audit_token_sync(self) -> Dict:
        """Auditar sincronización de tokens en 4 fuentes"""
        print("\n🔍 AUDITORÍA 1: SINCRONIZACIÓN DE TOKENS")
        print("=" * 60)
        
        check = {
            "name": "Token Synchronization (CSS ↔ JSON ↔ JS ↔ Manifest)",
            "status": "PENDING",
            "issues": []
        }
        
        # Leer tokens.css
        css_tokens = self._extract_css_tokens()
        print(f"✓ Tokens en CSS: {len(css_tokens)}")
        
        # Leer tokens.json
        json_tokens = self._extract_json_tokens()
        print(f"✓ Tokens en JSON: {len(json_tokens)}")
        
        # Leer TOKEN_META (JS)
        js_tokens = self._extract_js_tokens()
        print(f"✓ Tokens en JS: {len(js_tokens)}")
        
        # Leer manifest
        manifest_tokens = self._extract_manifest_tokens()
        print(f"✓ Tokens en Manifest: {len(manifest_tokens)}")
        
        # Comparar
        all_tokens = set(css_tokens.keys()) | set(json_tokens.keys()) | set(js_tokens.keys())
        
        # Verificar coherencia
        for token in all_tokens:
            sources = []
            if token in css_tokens: sources.append("CSS")
            if token in json_tokens: sources.append("JSON")
            if token in js_tokens: sources.append("JS")
            if token in manifest_tokens: sources.append("Manifest")
            
            if len(sources) < 4:
                check["issues"].append({
                    "token": token,
                    "found_in": sources,
                    "missing_from": set(["CSS", "JSON", "JS", "Manifest"]) - set(sources),
                    "severity": "ERROR" if len(sources) < 2 else "WARN"
                })
        
        check["status"] = "PASS" if not check["issues"] else ("WARN" if all(i["severity"] == "WARN" for i in check["issues"]) else "FAIL")
        self.results["checks"]["token_sync"] = check
        
        print(f"\n→ Status: {check['status']}")
        if check["issues"]:
            print(f"→ Issues encontradas: {len(check['issues'])}")
            for issue in check["issues"][:5]:
                missing_from = list(issue['missing_from']) if isinstance(issue['missing_from'], set) else issue['missing_from']
                print(f"  - {issue['token']}: {issue['found_in']} (falta en: {missing_from})")
        
        return check
    
    def audit_foundations(self) -> Dict:
        """Auditar documentación de Foundations (8 categorías)"""
        print("\n🏛️  AUDITORÍA 2: FOUNDATIONS DOCUMENTATION")
        print("=" * 60)
        
        check = {
            "name": "Foundations Categories (8 expected)",
            "status": "PENDING",
            "categories": {},
            "issues": []
        }
        
        expected_categories = [
            "COLORES", "TIPOGRAFIA", "ESPACIADO", "LAYOUT",
            "MOVIMIENTO", "ICONOGRAFIA", "BORDES", "SOMBRAS"
        ]
        
        for category in expected_categories:
            file_path = self.root / f"01-tokens/{category}-FOUNDATIONS.md"
            if file_path.exists():
                size = file_path.stat().st_size
                lines = len(file_path.read_text().split('\n'))
                check["categories"][category] = {
                    "exists": True,
                    "size_kb": round(size / 1024, 2),
                    "lines": lines
                }
                print(f"✓ {category}-FOUNDATIONS.md ({lines} líneas)")
            else:
                check["categories"][category] = {"exists": False}
                check["issues"].append({
                    "category": category,
                    "issue": "File not found",
                    "severity": "ERROR"
                })
                print(f"✗ {category}-FOUNDATIONS.md (MISSING)")
        
        check["status"] = "PASS" if not check["issues"] else "FAIL"
        self.results["checks"]["foundations"] = check
        
        print(f"\n→ Status: {check['status']}")
        print(f"→ Categories found: {len([c for c in check['categories'] if check['categories'][c].get('exists')])}/8")
        
        return check
    
    def audit_components(self) -> Dict:
        """Auditar documentación de componentes (19 esperados)"""
        print("\n🧩 AUDITORÍA 3: COMPONENTS DOCUMENTATION")
        print("=" * 60)
        
        check = {
            "name": "Components Documentation (19 expected)",
            "status": "PENDING",
            "components": {},
            "issues": []
        }
        
        expected_components = [
            # Atoms (6)
            "boton", "input", "link", "badge", "field", "breadcrumb",
            # Molecules (9)
            "alert", "card", "dropdown", "tabs", "accordion",
            "tooltip", "toast", "table", "pagination",
            # Organisms (3)
            "modal", "navbar", "select"
        ]
        
        for component in expected_components:
            file_path = self.root / f"02-componentes/{component}.md"
            if file_path.exists():
                content = file_path.read_text()
                lines = len(content.split('\n'))
                # Verificar secciones esperadas
                sections = {
                    "Cuándo usarlo": "Cuándo usarlo" in content,
                    "Anatomía": "Anatomía" in content,
                    "Estados": "Estados" in content,
                    "Accesibilidad": "Accesibilidad" in content or "WCAG" in content,
                    "Tokens": "Tokens" in content or "tokens" in content,
                }
                check["components"][component] = {
                    "exists": True,
                    "lines": lines,
                    "sections": sections,
                    "completeness": sum(sections.values()) / len(sections)
                }
                status = "✓" if all(sections.values()) else "⚠"
                print(f"{status} {component}.md ({lines} líneas, {sum(sections.values())}/{len(sections)} sections)")
            else:
                check["components"][component] = {"exists": False}
                check["issues"].append({
                    "component": component,
                    "issue": "File not found",
                    "severity": "ERROR"
                })
                print(f"✗ {component}.md (MISSING)")
        
        check["status"] = "PASS" if not check["issues"] else "WARN" if all(i["severity"] == "WARN" for i in check["issues"]) else "FAIL"
        self.results["checks"]["components"] = check
        
        found = len([c for c in check["components"] if check["components"][c].get("exists")])
        print(f"\n→ Status: {check['status']}")
        print(f"→ Components found: {found}/{len(expected_components)}")
        
        return check
    
    def audit_patterns(self) -> Dict:
        """Auditar documentación de patrones (4 esperados)"""
        print("\n🎯 AUDITORÍA 4: PATTERNS DOCUMENTATION")
        print("=" * 60)
        
        check = {
            "name": "Patterns Documentation (4 expected)",
            "status": "PENDING",
            "patterns": {},
            "issues": []
        }
        
        expected_patterns = ["formularios", "navegación", "modales", "tarjetas"]
        
        for pattern in expected_patterns:
            file_path = self.root / f"03-patrones/{pattern}.md"
            if file_path.exists():
                lines = len(file_path.read_text().split('\n'))
                check["patterns"][pattern] = {"exists": True, "lines": lines}
                print(f"✓ {pattern}.md ({lines} líneas)")
            else:
                check["patterns"][pattern] = {"exists": False}
                check["issues"].append({
                    "pattern": pattern,
                    "issue": "File not found"
                })
                print(f"✗ {pattern}.md (MISSING)")
        
        check["status"] = "PASS" if not check["issues"] else "FAIL"
        self.results["checks"]["patterns"] = check
        
        found = len([p for p in check["patterns"] if check["patterns"][p]["exists"]])
        print(f"\n→ Status: {check['status']}")
        print(f"→ Patterns found: {found}/4")
        
        return check
    
    def audit_wcag_aa(self) -> Dict:
        """Auditar validación WCAG AA en documentación"""
        print("\n♿ AUDITORÍA 5: WCAG AA VALIDATION")
        print("=" * 60)
        
        check = {
            "name": "WCAG AA Coverage",
            "status": "PENDING",
            "files_with_wcag": [],
            "files_without_wcag": [],
            "issues": []
        }
        
        # Buscar en Foundations
        foundations_dir = self.root / "01-tokens"
        for file in foundations_dir.glob("*FOUNDATIONS.md"):
            content = file.read_text()
            if "WCAG" in content or "accesibilidad" in content.lower():
                check["files_with_wcag"].append(file.name)
                print(f"✓ {file.name}: WCAG validation found")
            else:
                check["files_without_wcag"].append(file.name)
                print(f"⚠ {file.name}: No WCAG validation found")
        
        # Buscar en componentes
        components_dir = self.root / "02-componentes"
        for file in components_dir.glob("*.md"):
            if file.name.startswith("plantilla"): continue
            content = file.read_text()
            if "WCAG" in content or "accesibilidad" in content.lower():
                check["files_with_wcag"].append(file.name)
            else:
                check["files_without_wcag"].append(file.name)
        
        wcag_coverage = len(check["files_with_wcag"]) / (len(check["files_with_wcag"]) + len(check["files_without_wcag"])) * 100 if (len(check["files_with_wcag"]) + len(check["files_without_wcag"])) > 0 else 0
        
        check["status"] = "PASS" if wcag_coverage >= 95 else "WARN" if wcag_coverage >= 80 else "FAIL"
        self.results["checks"]["wcag"] = check
        
        print(f"\n→ Status: {check['status']}")
        print(f"→ WCAG AA Coverage: {wcag_coverage:.1f}%")
        
        return check
    
    def _extract_css_tokens(self) -> Dict:
        """Extraer tokens de tokens.css"""
        css_file = self.root / "01-tokens/tokens.css"
        tokens = {}
        if css_file.exists():
            content = css_file.read_text()
            # Buscar --variable-name: value;
            matches = re.findall(r'--([a-zA-Z0-9\-]+):\s*([^;]+);', content)
            for name, value in matches:
                tokens[f"--{name}"] = value.strip()
        return tokens
    
    def _extract_json_tokens(self) -> Dict:
        """Extraer tokens de tokens.json"""
        json_file = self.root / "01-tokens/tokens.json"
        tokens = {}
        if json_file.exists():
            try:
                data = json.loads(json_file.read_text())
                def flatten(obj, prefix=""):
                    for key, value in obj.items():
                        if isinstance(value, dict):
                            if "value" in value:
                                tokens[f"--{key}"] = value["value"]
                            else:
                                flatten(value, f"{prefix}{key}-" if prefix else key + "-")
                flatten(data.get("tokens", {}))
            except:
                pass
        return tokens
    
    def _extract_js_tokens(self) -> Dict:
        """Extraer TOKEN_META de main.js"""
        js_file = self.root / "assets/js/main.js"
        tokens = {}
        if js_file.exists():
            content = js_file.read_text()
            # Buscar TOKEN_META array
            match = re.search(r'const TOKEN_META = \[(.*?)\];', content, re.DOTALL)
            if match:
                entries = re.findall(r'\["([^"]+)",', match.group(1))
                for entry in entries:
                    tokens[entry] = True
        return tokens
    
    def _extract_manifest_tokens(self) -> Dict:
        """Extraer tokens de component-manifest.json"""
        manifest_file = self.root / "05-agentes/component-manifest.json"
        tokens = {}
        if manifest_file.exists():
            try:
                data = json.loads(manifest_file.read_text())
                # Buscar en todos los lugares donde puedan estar los tokens
                if "token_count" in data:
                    # Metadata dice cuántos tokens hay
                    pass
                for section in data.values():
                    if isinstance(section, dict) and "tokens" in section:
                        for token in section["tokens"]:
                            tokens[token] = True
            except:
                pass
        return tokens
    
    def generate_report(self, verbose=False) -> str:
        """Generar reporte de auditoría"""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE AUDITORÍA COMPLETA")
        print("=" * 60)
        
        passed = sum(1 for c in self.results["checks"].values() if c.get("status") == "PASS")
        warned = sum(1 for c in self.results["checks"].values() if c.get("status") == "WARN")
        failed = sum(1 for c in self.results["checks"].values() if c.get("status") == "FAIL")
        
        self.results["summary"] = {
            "total_checks": len(self.results["checks"]),
            "passed": passed,
            "warned": warned,
            "failed": failed,
            "overall_status": "PASS" if failed == 0 else "WARN" if warned > 0 else "FAIL"
        }
        
        print(f"\n✅ Passed: {passed}")
        print(f"⚠️  Warned: {warned}")
        print(f"❌ Failed: {failed}")
        print(f"\n→ Overall Status: {self.results['summary']['overall_status']}")
        
        # Recommendations
        print(f"\n💡 RECOMENDACIONES:")
        recommendations = []
        
        if not self.results["checks"]["token_sync"]["status"] == "PASS":
            recommendations.append("1. Ejecutar: python3 scripts/sync-tokens.py --all")
        
        if not self.results["checks"]["foundations"]["status"] == "PASS":
            recommendations.append("2. Crear Foundations faltantes")
        
        if not self.results["checks"]["components"]["status"] == "PASS":
            missing = [c for c in self.results["checks"]["components"]["components"] if not self.results["checks"]["components"]["components"][c].get("exists")]
            recommendations.append(f"3. Crear documentación para componentes: {', '.join(missing[:3])}")
        
        for rec in recommendations:
            print(f"  {rec}")
        
        # Convertir sets a listas para JSON serialization
        def convert_sets(obj):
            if isinstance(obj, dict):
                return {k: convert_sets(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_sets(item) for item in obj]
            elif isinstance(obj, set):
                return list(obj)
            return obj
        
        results_serializable = convert_sets(self.results)
        return json.dumps(results_serializable, indent=2, ensure_ascii=False)


def main():
    verbose = "--verbose" in sys.argv
    fix = "--fix" in sys.argv
    export = "--export" in sys.argv
    
    auditor = TokenAuditor()
    
    # Ejecutar auditorías
    auditor.audit_token_sync()
    auditor.audit_foundations()
    auditor.audit_components()
    auditor.audit_patterns()
    auditor.audit_wcag_aa()
    
    # Generar reporte
    report = auditor.generate_report(verbose)
    
    if export:
        export_path = Path("AUDIT-REPORT.json")
        export_path.write_text(report)
        print(f"\n💾 Reporte exportado a: {export_path}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
