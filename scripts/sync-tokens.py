#!/usr/bin/env python3
"""
🔄 SCRIPT DE SINCRONIZACIÓN DE TOKENS
Mantiene coherencia entre CSS, JSON, JavaScript y Manifest

Funciones:
1. Sincronizar tokens.css → tokens.json
2. Sincronizar tokens.json → TOKEN_META (main.js)
3. Sincronizar tokens → component-manifest.json
4. Validar sincronización
5. Generar reportes de cambios

Uso: python3 scripts/sync-tokens.py [--css-to-json] [--json-to-js] [--all] [--dry-run] [--verbose]
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set
from datetime import datetime
import sys

class TokenSynchronizer:
    def __init__(self, workspace_root="."):
        self.root = Path(workspace_root)
        self.changes = []
        self.errors = []
        
    def sync_css_to_json(self, dry_run=False):
        """Sincronizar tokens.css → tokens.json"""
        print("\n🔄 SINCRONIZACIÓN: CSS → JSON")
        print("=" * 60)
        
        css_file = self.root / "01-tokens/tokens.css"
        json_file = self.root / "01-tokens/tokens.json"
        
        if not css_file.exists():
            self.errors.append("tokens.css no encontrado")
            print("✗ tokens.css no encontrado")
            return False
        
        # Extraer todos los tokens de CSS
        css_content = css_file.read_text()
        tokens_dict = self._parse_css_to_dict(css_content)
        
        print(f"✓ Extrayendo {len(tokens_dict)} tokens de CSS")
        
        # Agrupar por categoría
        categorized = self._categorize_tokens(tokens_dict)
        
        # Crear estructura JSON
        json_data = {
            "version": "2.2.0",
            "timestamp": datetime.now().isoformat(),
            "tokens": categorized
        }
        
        if not dry_run:
            json_file.write_text(json.dumps(json_data, indent=2, ensure_ascii=False))
            print(f"✓ Archivo {json_file} actualizado con {len(tokens_dict)} tokens")
            self.changes.append({
                "type": "css_to_json",
                "file": str(json_file),
                "tokens_count": len(tokens_dict),
                "status": "SUCCESS"
            })
        else:
            print(f"[DRY RUN] Se escribirían {len(tokens_dict)} tokens en {json_file}")
        
        return True
    
    def sync_json_to_js(self, dry_run=False):
        """Sincronizar tokens.json → TOKEN_META (main.js)"""
        print("\n🔄 SINCRONIZACIÓN: JSON → JAVASCRIPT")
        print("=" * 60)
        
        json_file = self.root / "01-tokens/tokens.json"
        js_file = self.root / "assets/js/main.js"
        
        if not json_file.exists():
            self.errors.append("tokens.json no encontrado")
            print("✗ tokens.json no encontrado")
            return False
        
        if not js_file.exists():
            self.errors.append("main.js no encontrado")
            print("✗ main.js no encontrado")
            return False
        
        # Leer JSON
        json_data = json.loads(json_file.read_text())
        tokens_list = self._flatten_tokens(json_data.get("tokens", {}))
        
        print(f"✓ Leyendo {len(tokens_list)} tokens de JSON")
        
        # Generar TOKEN_META array
        token_meta = []
        for token_name, token_info in tokens_list.items():
            if isinstance(token_info, dict) and "value" in token_info:
                description = self._generate_token_description(token_name)
                token_meta.append([token_name, description])
            else:
                token_meta.append([token_name, token_name])
        
        # Leer main.js y reemplazar TOKEN_META
        js_content = js_file.read_text()
        
        # Generar nuevo TOKEN_META
        new_token_meta = "var TOKEN_META = [\n"
        for token_name, description in token_meta:
            new_token_meta += f'  ["{token_name}", "{description}"],\n'
        new_token_meta += "];"
        
        # Reemplazar en JS (buscar tanto var como const)
        old_token_meta = re.search(r'(?:var|const) TOKEN_META = \[.*?\];', js_content, re.DOTALL)
        
        if old_token_meta:
            old_count = len(re.findall(r'\[', old_token_meta.group()))
            print(f"✓ Reemplazando {old_count} tokens anteriores con {len(token_meta)} nuevos")
            
            if not dry_run:
                new_js_content = js_content[:old_token_meta.start()] + new_token_meta + js_content[old_token_meta.end():]
                js_file.write_text(new_js_content)
                print(f"✓ Archivo {js_file} actualizado")
                self.changes.append({
                    "type": "json_to_js",
                    "file": str(js_file),
                    "tokens_count": len(token_meta),
                    "status": "SUCCESS"
                })
            else:
                print(f"[DRY RUN] Se escribirían {len(token_meta)} tokens en {js_file}")
        else:
            self.errors.append("TOKEN_META no encontrado en main.js")
            print("✗ TOKEN_META no encontrado en main.js")
            return False
        
        return True
    
    def sync_to_manifest(self, dry_run=False):
        """Sincronizar tokens → component-manifest.json"""
        print("\n🔄 SINCRONIZACIÓN: TOKENS → MANIFEST")
        print("=" * 60)
        
        json_file = self.root / "01-tokens/tokens.json"
        manifest_file = self.root / "05-agentes/component-manifest.json"
        
        if not json_file.exists():
            self.errors.append("tokens.json no encontrado")
            return False
        
        if not manifest_file.exists():
            self.errors.append("component-manifest.json no encontrado")
            return False
        
        # Leer tokens
        tokens_data = json.loads(json_file.read_text())
        tokens_list = self._flatten_tokens(tokens_data.get("tokens", {}))
        
        # Leer manifest
        manifest = json.loads(manifest_file.read_text())
        
        # Actualizar metadata
        old_count = manifest.get("token_count", 0)
        manifest["token_count"] = len(tokens_list)
        manifest["last_sync"] = datetime.now().isoformat()
        
        print(f"✓ Actualizando conteo de tokens: {old_count} → {len(tokens_list)}")
        
        if not dry_run:
            manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
            print(f"✓ Manifest actualizado")
            self.changes.append({
                "type": "tokens_to_manifest",
                "file": str(manifest_file),
                "tokens_count": len(tokens_list),
                "status": "SUCCESS"
            })
        else:
            print(f"[DRY RUN] Se escribiría manifest con {len(tokens_list)} tokens")
        
        return True
    
    def verify_sync(self) -> bool:
        """Verificar sincronización entre todas las fuentes"""
        print("\n✅ VERIFICACIÓN DE SINCRONIZACIÓN")
        print("=" * 60)
        
        # Extraer de cada fuente
        css_tokens = self._extract_from_css()
        json_tokens = self._extract_from_json()
        js_tokens = self._extract_from_js()
        manifest_tokens = self._extract_from_manifest()
        
        print(f"CSS:      {len(css_tokens)} tokens")
        print(f"JSON:     {len(json_tokens)} tokens")
        print(f"JS:       {len(js_tokens)} tokens")
        print(f"Manifest: {len(manifest_tokens)} tokens")
        
        # Verificar convergencia
        all_tokens = css_tokens | json_tokens | js_tokens | manifest_tokens
        css_only = all_tokens - json_tokens - js_tokens - manifest_tokens
        json_only = all_tokens - css_tokens - js_tokens - manifest_tokens
        js_only = all_tokens - css_tokens - json_tokens - manifest_tokens
        manifest_only = all_tokens - css_tokens - json_tokens - js_tokens
        
        issues = []
        if css_only:
            issues.append(f"Solo en CSS: {len(css_only)} tokens")
        if json_only:
            issues.append(f"Solo en JSON: {len(json_only)} tokens")
        if js_only:
            issues.append(f"Solo en JS: {len(js_only)} tokens")
        if manifest_only:
            issues.append(f"Solo en Manifest: {len(manifest_only)} tokens")
        
        if issues:
            print("\n⚠️  Issues encontradas:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("\n✓ Todas las fuentes están sincronizadas")
            return True
    
    def _parse_css_to_dict(self, css_content: str) -> Dict:
        """Parsear CSS a diccionario de tokens"""
        tokens = {}
        # Buscar --variable-name: value;
        matches = re.findall(r'--([a-zA-Z0-9\-]+):\s*([^;]+);', css_content)
        for name, value in matches:
            tokens[f"--{name}"] = value.strip()
        return tokens
    
    def _categorize_tokens(self, tokens: Dict) -> Dict:
        """Categorizar tokens por prefijo"""
        categorized = {}
        for token_name, value in tokens.items():
            # Extraer categoría del nombre (--color-* → color)
            match = re.match(r'--([a-z]+)', token_name)
            if match:
                category = match.group(1)
                if category not in categorized:
                    categorized[category] = {}
                categorized[category][token_name.replace(f"--{category}-", "")] = {
                    "value": value,
                    "type": self._infer_token_type(category)
                }
        return categorized
    
    def _infer_token_type(self, category: str) -> str:
        """Inferir tipo de token según categoría"""
        type_map = {
            "color": "color",
            "space": "dimension",
            "typography": "typography",
            "border": "dimension",
            "shadow": "shadow",
            "motion": "duration",
            "radius": "dimension",
            "breakpoint": "breakpoint"
        }
        return type_map.get(category, "other")
    
    def _flatten_tokens(self, tokens_dict: Dict) -> Dict:
        """Aplanar estructura de tokens anidada"""
        flat = {}
        def flatten(obj, prefix=""):
            for key, value in obj.items():
                if isinstance(value, dict):
                    if "value" in value:
                        full_key = f"{prefix}{key}" if prefix else key
                        flat[full_key] = value
                    else:
                        new_prefix = f"{prefix}{key}-" if prefix else f"{key}-"
                        flatten(value, new_prefix)
        flatten(tokens_dict)
        return flat
    
    def _generate_token_description(self, token_name: str) -> str:
        """Generar descripción automática para token"""
        # Mapeo de ejemplos para descripciones
        examples = {
            "color-action": "Color para acciones principales",
            "color-error": "Color para estados de error",
            "color-success": "Color para estados de éxito",
            "color-warning": "Color para estados de advertencia",
            "space-": "Espaciado",
            "typography-": "Tipografía",
            "border-": "Borde",
            "shadow-": "Sombra",
            "motion-": "Movimiento",
            "radius-": "Radio de borde"
        }
        
        for key, desc in examples.items():
            if key in token_name:
                return desc
        
        return token_name
    
    def _extract_from_css(self) -> Set:
        """Extraer nombres de tokens de CSS"""
        css_file = self.root / "01-tokens/tokens.css"
        tokens = set()
        if css_file.exists():
            matches = re.findall(r'--([a-zA-Z0-9\-]+):', css_file.read_text())
            tokens = set([f"--{name}" for name in matches])
        return tokens
    
    def _extract_from_json(self) -> Set:
        """Extraer nombres de tokens de JSON"""
        json_file = self.root / "01-tokens/tokens.json"
        tokens = set()
        if json_file.exists():
            try:
                data = json.loads(json_file.read_text())
                flat = self._flatten_tokens(data.get("tokens", {}))
                tokens = set(flat.keys())
            except:
                pass
        return tokens
    
    def _extract_from_js(self) -> Set:
        """Extraer TOKEN_META de JavaScript"""
        js_file = self.root / "assets/js/main.js"
        tokens = set()
        if js_file.exists():
            content = js_file.read_text()
            match = re.search(r'const TOKEN_META = \[(.*?)\];', content, re.DOTALL)
            if match:
                entries = re.findall(r'\["([^"]+)",', match.group(1))
                tokens = set(entries)
        return tokens
    
    def _extract_from_manifest(self) -> Set:
        """Extraer tokens de manifest"""
        manifest_file = self.root / "05-agentes/component-manifest.json"
        tokens = set()
        if manifest_file.exists():
            try:
                data = json.loads(manifest_file.read_text())
                # Buscar en metadata de tokens
                if "token_count" in data:
                    # Extraer conteo
                    pass
            except:
                pass
        return tokens
    
    def generate_sync_report(self) -> str:
        """Generar reporte de sincronización"""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE SINCRONIZACIÓN")
        print("=" * 60)
        
        if not self.changes:
            print("\nℹ️  No se realizaron cambios")
        else:
            print(f"\n✅ Cambios realizados: {len(self.changes)}")
            for change in self.changes:
                print(f"  - {change['type']}: {change['tokens_count']} tokens")
        
        if self.errors:
            print(f"\n❌ Errores: {len(self.errors)}")
            for error in self.errors:
                print(f"  - {error}")
        
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "changes": self.changes,
            "errors": self.errors,
            "status": "SUCCESS" if not self.errors else "FAILED"
        }, indent=2)


def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv
    all_sync = "--all" in sys.argv
    
    if dry_run:
        print("🔍 MODO DRY-RUN: No se realizarán cambios")
    
    sync = TokenSynchronizer()
    
    if all_sync or "--css-to-json" in sys.argv:
        sync.sync_css_to_json(dry_run=dry_run)
    
    if all_sync or "--json-to-js" in sys.argv:
        sync.sync_json_to_js(dry_run=dry_run)
    
    if all_sync:
        sync.sync_to_manifest(dry_run=dry_run)
        sync.verify_sync()
    
    report = sync.generate_sync_report()
    
    if verbose:
        print(report)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
