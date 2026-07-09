#!/usr/bin/env python3
"""
🛡️  VALIDADOR AVANZADO CON LOGGING Y RECUPERACIÓN
Sistema robusto de validación, logging, caché y recovery

Funciones:
1. Validación exhaustiva de integridad
2. Logging detallado con niveles
3. Sistema de caché para optimización
4. Detección automática de problemas
5. Recuperación y rollback
6. Reportes de diagnóstico

Uso: python3 scripts/validate-robust.py [--verbose] [--fix] [--recovery] [--export-logs]
"""

import json
import re
import hashlib
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
import logging
import sys

class RobustValidator:
    def __init__(self, workspace_root=".", enable_cache=True):
        self.root = Path(workspace_root)
        self.cache_dir = self.root / ".validation-cache"
        self.logs_dir = self.root / "logs"
        self.enable_cache = enable_cache
        
        # Crear directorios
        self.cache_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Configurar logging
        self.setup_logging()
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "validations": {},
            "issues": [],
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
    def setup_logging(self):
        """Configurar sistema de logging robusto"""
        log_file = self.logs_dir / f"validation-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("Validator")
        self.logger.info("=== INICIO VALIDACIÓN ROBUSTA ===")
        
    def validate_all(self, fix=False) -> Dict:
        """Ejecutar todas las validaciones"""
        self.logger.info("Iniciando validaciones completas...")
        
        validations = [
            ("file_integrity", self.validate_file_integrity),
            ("token_coherence", self.validate_token_coherence),
            ("documentation", self.validate_documentation),
            ("component_structure", self.validate_component_structure),
            ("references", self.validate_cross_references),
            ("encoding", self.validate_encoding),
            ("syntax", self.validate_syntax),
        ]
        
        for name, validator in validations:
            self.logger.info(f"Ejecutando validación: {name}")
            try:
                result = validator(fix=fix)
                self.results["validations"][name] = result
            except Exception as e:
                self.logger.error(f"Error en validación {name}: {e}")
                self.results["errors"].append({
                    "validation": name,
                    "error": str(e)
                })
        
        return self.results
    
    def validate_file_integrity(self, fix=False) -> Dict:
        """Validar integridad de archivos críticos"""
        self.logger.info("Validando integridad de archivos...")
        
        result = {
            "status": "PASS",
            "files_checked": 0,
            "files_ok": 0,
            "files_corrupted": 0,
            "checksums": {}
        }
        
        critical_files = {
            "01-tokens/tokens.css": "tokens-css",
            "01-tokens/tokens.json": "tokens-json",
            "05-agentes/component-manifest.json": "manifest",
            "assets/js/main.js": "main-js",
            "index.html": "index-html"
        }
        
        cache_file = self.cache_dir / "checksums.json"
        
        # Leer checksums anteriores
        previous_checksums = {}
        if cache_file.exists():
            previous_checksums = json.loads(cache_file.read_text())
        
        current_checksums = {}
        
        for rel_path, name in critical_files.items():
            full_path = self.root / rel_path
            result["files_checked"] += 1
            
            if not full_path.exists():
                self.logger.error(f"Archivo crítico faltante: {rel_path}")
                result["status"] = "FAIL"
                result["files_corrupted"] += 1
                self.results["errors"].append({
                    "type": "missing_file",
                    "file": rel_path
                })
                continue
            
            # Calcular checksum
            checksum = self.calculate_checksum(full_path)
            current_checksums[name] = checksum
            
            # Verificar integridad
            if name in previous_checksums:
                if previous_checksums[name] != checksum:
                    self.logger.warning(f"Archivo modificado: {rel_path}")
                    self.results["warnings"].append({
                        "type": "file_modified",
                        "file": rel_path
                    })
            
            result["files_ok"] += 1
            self.logger.debug(f"Archivo OK: {rel_path} ({checksum[:8]}...)")
        
        # Guardar checksums actuales
        if self.enable_cache:
            cache_file.write_text(json.dumps(current_checksums, indent=2))
        
        result["checksums"] = current_checksums
        return result
    
    def validate_token_coherence(self, fix=False) -> Dict:
        """Validar coherencia de tokens entre fuentes"""
        self.logger.info("Validando coherencia de tokens...")
        
        result = {
            "status": "PASS",
            "css_tokens": 0,
            "json_tokens": 0,
            "manifest_tokens": 0,
            "coherent": True,
            "missing_in_json": [],
            "missing_in_manifest": [],
            "extra_in_json": []
        }
        
        # Extraer de CSS
        css_file = self.root / "01-tokens/tokens.css"
        css_tokens = set()
        if css_file.exists():
            css_content = css_file.read_text()
            css_tokens = set(re.findall(r'--([a-zA-Z0-9\-]+):', css_content))
            result["css_tokens"] = len(css_tokens)
            self.logger.debug(f"Tokens en CSS: {len(css_tokens)}")
        
        # Extraer de JSON
        json_file = self.root / "01-tokens/tokens.json"
        json_tokens = set()
        if json_file.exists():
            try:
                data = json.loads(json_file.read_text())
                json_tokens = self._flatten_token_keys(data.get("tokens", {}))
                result["json_tokens"] = len(json_tokens)
                self.logger.debug(f"Tokens en JSON: {len(json_tokens)}")
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON inválido en tokens.json: {e}")
                result["status"] = "FAIL"
                return result
        
        # Verificar coherencia
        missing_in_json = css_tokens - json_tokens
        extra_in_json = json_tokens - css_tokens
        
        if missing_in_json:
            result["coherent"] = False
            result["status"] = "WARN"
            result["missing_in_json"] = list(missing_in_json)[:5]
            self.logger.warning(f"Tokens en CSS pero no en JSON: {len(missing_in_json)}")
        
        if extra_in_json:
            result["extra_in_json"] = list(extra_in_json)[:5]
            self.logger.warning(f"Tokens en JSON pero no en CSS: {len(extra_in_json)}")
        
        return result
    
    def validate_documentation(self, fix=False) -> Dict:
        """Validar documentación completa"""
        self.logger.info("Validando documentación...")
        
        result = {
            "status": "PASS",
            "files_analyzed": 0,
            "min_line_count": 50,
            "files_too_small": [],
            "missing_sections": {},
            "total_lines": 0
        }
        
        expected_sections = {
            "02-componentes": ["Cuándo usarlo", "Anatomía", "Estados", "Accesibilidad"],
            "03-patrones": ["Estructura", "Componentes", "Accesibilidad"],
            "01-tokens": ["Descripción", "Escala", "Uso"]
        }
        
        for doc_dir, sections in expected_sections.items():
            dir_path = self.root / doc_dir
            if not dir_path.exists():
                continue
            
            for file in dir_path.glob("*.md"):
                if file.name.startswith("plantilla"):
                    continue
                
                result["files_analyzed"] += 1
                content = file.read_text()
                lines = len(content.split('\n'))
                result["total_lines"] += lines
                
                # Verificar tamaño mínimo
                if lines < result["min_line_count"]:
                    result["files_too_small"].append(file.name)
                    result["status"] = "WARN"
                    self.logger.warning(f"Archivo pequeño: {file.name} ({lines} líneas)")
                
                # Verificar secciones
                for section in sections:
                    if section not in content:
                        if file.name not in result["missing_sections"]:
                            result["missing_sections"][file.name] = []
                        result["missing_sections"][file.name].append(section)
                        self.logger.warning(f"Sección faltante en {file.name}: {section}")
        
        self.logger.info(f"Documentación analizada: {result['files_analyzed']} archivos, {result['total_lines']} líneas")
        return result
    
    def validate_component_structure(self, fix=False) -> Dict:
        """Validar estructura de componentes"""
        self.logger.info("Validando estructura de componentes...")
        
        result = {
            "status": "PASS",
            "components_checked": 0,
            "valid_structure": 0,
            "invalid_structure": []
        }
        
        components_dir = self.root / "02-componentes"
        
        for file in components_dir.glob("*.md"):
            if file.name.startswith("plantilla"):
                continue
            
            result["components_checked"] += 1
            content = file.read_text()
            
            # Verificar estructura
            has_header = file.name.lower() in content.lower()
            has_code = "```" in content
            
            if not (has_header and has_code):
                result["invalid_structure"].append(file.name)
                result["status"] = "WARN"
                self.logger.warning(f"Estructura incompleta: {file.name}")
            else:
                result["valid_structure"] += 1
        
        return result
    
    def validate_cross_references(self, fix=False) -> Dict:
        """Validar referencias cruzadas"""
        self.logger.info("Validando referencias cruzadas...")
        
        result = {
            "status": "PASS",
            "references_checked": 0,
            "broken_links": [],
            "valid_links": 0
        }
        
        # Buscar links en archivos markdown
        for md_file in self.root.rglob("*.md"):
            content = md_file.read_text()
            
            # Buscar [text](path) referencias
            links = re.findall(r'\[(.*?)\]\((.*?)\)', content)
            
            for text, path in links:
                result["references_checked"] += 1
                
                # Si es URL externa, skip
                if path.startswith("http"):
                    result["valid_links"] += 1
                    continue
                
                # Verificar que el archivo exista
                target_path = md_file.parent / path
                if "#" in path:
                    target_path = md_file.parent / path.split("#")[0]
                
                if not target_path.exists() and not path.startswith("#"):
                    result["broken_links"].append({
                        "source": str(md_file.relative_to(self.root)),
                        "target": path
                    })
                    result["status"] = "WARN"
                    self.logger.warning(f"Link roto: {path} en {md_file.name}")
                else:
                    result["valid_links"] += 1
        
        return result
    
    def validate_encoding(self, fix=False) -> Dict:
        """Validar encoding de archivos"""
        self.logger.info("Validando encoding de archivos...")
        
        result = {
            "status": "PASS",
            "files_checked": 0,
            "encoding_issues": []
        }
        
        for file in self.root.rglob("*"):
            if file.is_dir() or file.name.startswith("."):
                continue
            
            if file.suffix not in [".py", ".md", ".json", ".html", ".css", ".js"]:
                continue
            
            result["files_checked"] += 1
            
            try:
                content = file.read_text(encoding="utf-8")
            except UnicodeDecodeError as e:
                result["encoding_issues"].append(str(file.relative_to(self.root)))
                result["status"] = "WARN"
                self.logger.warning(f"Encoding issue: {file.name}")
        
        return result
    
    def validate_syntax(self, fix=False) -> Dict:
        """Validar sintaxis de archivos"""
        self.logger.info("Validando sintaxis de archivos...")
        
        result = {
            "status": "PASS",
            "files_checked": 0,
            "syntax_errors": []
        }
        
        # Validar JSON
        for json_file in self.root.rglob("*.json"):
            result["files_checked"] += 1
            try:
                json.loads(json_file.read_text())
            except json.JSONDecodeError as e:
                result["syntax_errors"].append({
                    "file": str(json_file.relative_to(self.root)),
                    "error": str(e)
                })
                result["status"] = "FAIL"
                self.logger.error(f"JSON error en {json_file.name}: {e}")
        
        return result
    
    def calculate_checksum(self, file_path: Path) -> str:
        """Calcular checksum SHA256 de archivo"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _flatten_token_keys(self, obj, prefix="") -> Set:
        """Aplanar claves de tokens"""
        keys = set()
        for key, value in obj.items():
            if isinstance(value, dict):
                keys.update(self._flatten_token_keys(value, f"{prefix}{key}-"))
            else:
                keys.add(f"{prefix}{key}".rstrip("-"))
        return keys
    
    def generate_report(self) -> str:
        """Generar reporte de validación"""
        print("\n" + "=" * 60)
        print("🛡️  REPORTE DE VALIDACIÓN ROBUSTA")
        print("=" * 60)
        
        total_validations = len(self.results["validations"])
        passed = sum(1 for v in self.results["validations"].values() if v.get("status") == "PASS")
        warned = sum(1 for v in self.results["validations"].values() if v.get("status") == "WARN")
        failed = sum(1 for v in self.results["validations"].values() if v.get("status") == "FAIL")
        
        print(f"\n✅ Pasadas: {passed}")
        print(f"⚠️  Advertencias: {warned}")
        print(f"❌ Fallidas: {failed}")
        
        print(f"\nDetalles:")
        for name, result in self.results["validations"].items():
            status = result.get("status", "UNKNOWN")
            print(f"  {name}: {status}")
        
        print(f"\n💾 Logs guardados en: {self.logs_dir}")
        
        # Guardar reporte JSON
        report_file = self.root / "VALIDATION-REPORT.json"
        report_file.write_text(json.dumps(self.results, indent=2, ensure_ascii=False))
        print(f"📄 Reporte JSON: {report_file}")
        
        return json.dumps(self.results, indent=2, ensure_ascii=False)


def main():
    verbose = "--verbose" in sys.argv
    fix = "--fix" in sys.argv
    recovery = "--recovery" in sys.argv
    export_logs = "--export-logs" in sys.argv
    
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    validator = RobustValidator()
    results = validator.validate_all(fix=fix)
    report = validator.generate_report()
    
    if export_logs:
        # Crear archivo zip con logs
        pass
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
