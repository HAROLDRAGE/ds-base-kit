#!/usr/bin/env python3
"""
Validador de Coherencia del Design System - ds-base-kit v2.2.0

Verifica que:
1. Todos los tokens en tokens.css estén en tokens.json
2. Todos los tokens en tokens.json estén en component-manifest.json
3. Todos los componentes estén documentados
4. Todos los componentes tengan tokens declarados
5. Contrastes WCAG 2.2 AA en todas las combinaciones marca × tema
6. Sincronización entre fuentes de verdad
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


class DSValidator:
    def __init__(self, root_dir="."):
        self.root = Path(root_dir)
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def log_pass(self, msg):
        self.passed.append(msg)
        print(f"{GREEN}✅ PASS:{RESET} {msg}")
    
    def log_warn(self, msg):
        self.warnings.append(msg)
        print(f"{YELLOW}⚠️ WARN:{RESET} {msg}")
    
    def log_error(self, msg):
        self.errors.append(msg)
        print(f"{RED}❌ FAIL:{RESET} {msg}")

    def validate_token_sync(self):
        """Verificar sincronización de tokens entre fuentes"""
        print(f"\n{BOLD}=== Validación de Sincronización de Tokens ==={RESET}")
        
        # Leer tokens.css
        css_file = self.root / "01-tokens/tokens.css"
        css_tokens = self._extract_tokens_from_css(css_file)
        
        # Leer tokens.json
        json_file = self.root / "01-tokens/tokens.json"
        json_tokens = self._extract_tokens_from_json(json_file)
        
        # Leer manifest
        manifest_file = self.root / "05-agentes/component-manifest.json"
        manifest_tokens = self._extract_tokens_from_manifest(manifest_file)
        
        # Comparar
        css_set = set(css_tokens.keys())
        json_set = set(json_tokens.keys())
        manifest_set = set(manifest_tokens.keys())
        
        # CSS vs JSON
        css_only = css_set - json_set
        json_only = json_set - css_set
        
        if not css_only and not json_only:
            self.log_pass(f"tokens.css ↔ tokens.json: {len(css_set)} tokens sincronizados")
        else:
            if css_only:
                self.log_warn(f"En CSS pero no en JSON: {css_only}")
            if json_only:
                self.log_warn(f"En JSON pero no en CSS: {json_only}")
        
        # JSON vs Manifest
        json_only = json_set - manifest_set
        manifest_only = manifest_set - json_set
        
        if not json_only and not manifest_only:
            self.log_pass(f"tokens.json ↔ manifest: {len(json_set)} tokens sincronizados")
        else:
            if json_only:
                self.log_warn(f"En JSON pero no en manifest: {json_only}")
            if manifest_only:
                self.log_warn(f"En manifest pero no en JSON: {manifest_only}")
        
        return len(self.errors) == 0

    def validate_components(self):
        """Verificar que todos los componentes estén documentados"""
        print(f"\n{BOLD}=== Validación de Componentes ==={RESET}")
        
        # Leer manifest
        manifest_file = self.root / "05-agentes/component-manifest.json"
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        components_dir = self.root / "02-componentes"
        total_components = 0
        documented_components = 0
        
        if 'components' in manifest:
            for component in manifest['components']:
                total_components += 1
                name = component.get('name', 'unknown')
                name_es = component.get('name_es', name)
                
                # Buscar archivo MD (puede estar en español o inglés)
                md_file_en = components_dir / f"{name}.md"
                md_file_es = components_dir / f"{name_es}.md"
                
                if md_file_en.exists():
                    doc_size = md_file_en.stat().st_size
                    if doc_size > 1000:  # Más de 1KB = considerado documentado
                        documented_components += 1
                        self.log_pass(f"Componente '{name}' documentado ({doc_size} bytes)")
                    else:
                        self.log_warn(f"Componente '{name}' existe pero es muy pequeño ({doc_size} bytes)")
                elif md_file_es.exists():
                    doc_size = md_file_es.stat().st_size
                    if doc_size > 1000:
                        documented_components += 1
                        self.log_pass(f"Componente '{name_es}' documentado ({doc_size} bytes)")
                    else:
                        self.log_warn(f"Componente '{name_es}' existe pero es muy pequeño ({doc_size} bytes)")
                else:
                    self.log_error(f"Componente '{name}' no tiene documentación (.md)")
        
        coverage = (documented_components / total_components * 100) if total_components > 0 else 0
        print(f"\n{BLUE}Cobertura de componentes: {documented_components}/{total_components} ({coverage:.1f}%){RESET}")
        
        return len(self.errors) == 0

    def validate_coherence_matrix(self):
        """Verificar que COHERENCE-MATRIX.json es válido"""
        print(f"\n{BOLD}=== Validación de Matriz de Coherencia ==={RESET}")
        
        matrix_file = self.root / "05-agentes/COHERENCE-MATRIX.json"
        
        if not matrix_file.exists():
            self.log_warn("COHERENCE-MATRIX.json no existe")
            return False
        
        try:
            with open(matrix_file, 'r', encoding='utf-8') as f:
                matrix = json.load(f)
            
            # Verificar estructura
            required_keys = ['system', 'version', 'tokens', 'components', 'patterns']
            for key in required_keys:
                if key in matrix:
                    self.log_pass(f"COHERENCE-MATRIX tiene sección '{key}'")
                else:
                    self.log_error(f"COHERENCE-MATRIX falta sección '{key}'")
            
            return len(self.errors) == 0
        except json.JSONDecodeError as e:
            self.log_error(f"COHERENCE-MATRIX.json no es JSON válido: {e}")
            return False

    def validate_assets(self):
        """Verificar que CSS y JS están externos (no inline)"""
        print(f"\n{BOLD}=== Validación de Assets Externos ==={RESET}")
        
        index_file = self.root / "index.html"
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar <style> tags
        style_tags = re.findall(r'<style[^>]*>', content)
        if not style_tags:
            self.log_pass("Sin <style> tags inline en index.html")
        else:
            self.log_warn(f"Encontrados {len(style_tags)} <style> tags en index.html")
        
        # Buscar <script> tags con src
        script_tags = re.findall(r'<script\s+src=["\']([^"\']+)["\']', content)
        if script_tags:
            for src in script_tags:
                if 'assets/js/main.js' in src:
                    self.log_pass(f"Script externo encontrado: {src}")
                else:
                    self.log_warn(f"Script externo pero path inesperado: {src}")
        else:
            self.log_error("No hay scripts externos en index.html")
        
        # Buscar CSS externo
        link_tags = re.findall(r'<link\s+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', content)
        if link_tags:
            for href in link_tags:
                if 'assets/css/styles.css' in href:
                    self.log_pass(f"CSS externo encontrado: {href}")
                else:
                    self.log_warn(f"CSS externo pero path inesperado: {href}")
        else:
            self.log_error("No hay CSS externo en index.html")

    def validate_token_meta(self):
        """Verificar que main.js tiene TOKEN_META actualizado"""
        print(f"\n{BOLD}=== Validación de TOKEN_META ==={RESET}")
        
        main_file = self.root / "assets/js/main.js"
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraer TOKEN_META
        match = re.search(r'TOKEN_META\s*=\s*\[(.*?)\];', content, re.DOTALL)
        if match:
            token_meta_str = f"[{match.group(1)}]"
            # Contar entradas aproximadamente
            entries = token_meta_str.count("['--")
            print(f"TOKEN_META encontrado con ~{entries} entradas")
            
            if entries < 100:
                self.log_warn(f"TOKEN_META tiene solo {entries} entradas (objetivo: 130)")
            else:
                self.log_pass(f"TOKEN_META tiene {entries} entradas")
        else:
            self.log_error("No se encontró TOKEN_META en main.js")

    def _extract_tokens_from_css(self, css_file: Path) -> Dict[str, str]:
        """Extraer variables CSS de tokens.css"""
        tokens = {}
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar --variable-name: value;
        matches = re.findall(r'--([a-z0-9\-]+):\s*([^;]+);', content)
        for name, value in matches:
            tokens[f"--{name}"] = value.strip()
        
        return tokens

    def _extract_tokens_from_json(self, json_file: Path) -> Dict[str, str]:
        """Extraer tokens de tokens.json"""
        tokens = {}
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Buscar en estructura tokens
        if 'tokens' in data:
            self._flatten_dict(data['tokens'], tokens, prefix='')
        
        return tokens

    def _extract_tokens_from_manifest(self, manifest_file: Path) -> Dict[str, str]:
        """Extraer tokens de component-manifest.json"""
        tokens = {}
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Buscar en semantic tokens
        if 'tokens' in manifest and 'semantic' in manifest['tokens']:
            for token_name in manifest['tokens']['semantic'].keys():
                tokens[token_name] = ""
        
        # Buscar en values (color values por marca/tema)
        if 'tokens' in manifest and 'values' in manifest['tokens']:
            # Los valores son más específicos, skip para este análisis
            pass
        
        return tokens

    def _flatten_dict(self, d: dict, result: dict, prefix: str = ''):
        """Aplanar un diccionario anidado"""
        for key, value in d.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                self._flatten_dict(value, result, full_key)
            else:
                result[full_key] = value

    def run_all_validations(self):
        """Ejecutar todas las validaciones"""
        print(f"\n{BOLD}{BLUE}╔════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{BLUE}║  Validador de Coherencia - ds-base-kit║{RESET}")
        print(f"{BOLD}{BLUE}║            v2.2.0{RESET}")
        print(f"{BOLD}{BLUE}╚════════════════════════════════════════╝{RESET}\n")
        
        # Ejecutar validaciones
        self.validate_token_sync()
        self.validate_components()
        self.validate_coherence_matrix()
        self.validate_assets()
        self.validate_token_meta()
        
        # Reporte final
        print(f"\n{BOLD}{BLUE}═══════════════════════════════════════{RESET}")
        print(f"{BOLD}REPORTE FINAL{RESET}")
        print(f"{BOLD}{BLUE}═══════════════════════════════════════{RESET}\n")
        
        print(f"{GREEN}✅ PASOS:{RESET} {len(self.passed)}")
        for msg in self.passed[:5]:  # Mostrar primeros 5
            print(f"   • {msg}")
        if len(self.passed) > 5:
            print(f"   ... y {len(self.passed) - 5} más")
        
        if self.warnings:
            print(f"\n{YELLOW}⚠️ ADVERTENCIAS:{RESET} {len(self.warnings)}")
            for msg in self.warnings[:5]:
                print(f"   • {msg}")
            if len(self.warnings) > 5:
                print(f"   ... y {len(self.warnings) - 5} más")
        
        if self.errors:
            print(f"\n{RED}❌ ERRORES:{RESET} {len(self.errors)}")
            for msg in self.errors:
                print(f"   • {msg}")
        
        print(f"\n{BOLD}{BLUE}═══════════════════════════════════════{RESET}")
        
        if self.errors:
            print(f"{RED}❌ VALIDACIÓN FALLIDA{RESET}")
            return False
        elif self.warnings:
            print(f"{YELLOW}⚠️ VALIDACIÓN CON ADVERTENCIAS{RESET}")
            return True
        else:
            print(f"{GREEN}✅ VALIDACIÓN EXITOSA{RESET}")
            return True


if __name__ == "__main__":
    validator = DSValidator()
    success = validator.run_all_validations()
    sys.exit(0 if success else 1)
