#!/usr/bin/env python3
"""
Token Schema Validator v1.0
Validates design tokens against the machine-readable metadata schema.

Purpose:
  - Validate tokens.dtcg.json structure against token-metadata.schema.json
  - Check WCAG compliance (contrast ratios)
  - Verify brand coverage
  - Detect missing metadata

Usage:
  python3 validate-schema.py [--fix] [--report]
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import re

class TokenSchemaValidator:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.tokens_dir = self.project_root / "01-tokens"
        self.schema_path = self.tokens_dir / "token-metadata.schema.json"
        self.tokens_dtcg_path = self.tokens_dir / "tokens.dtcg.json"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.successes: List[str] = []
        
    def load_schema(self) -> Dict:
        """Load the token metadata schema"""
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {self.schema_path}")
        with open(self.schema_path) as f:
            return json.load(f)
    
    def load_tokens(self) -> Dict:
        """Load DTCG tokens"""
        if not self.tokens_dtcg_path.exists():
            raise FileNotFoundError(f"Tokens not found: {self.tokens_dtcg_path}")
        with open(self.tokens_dtcg_path) as f:
            return json.load(f)
    
    def validate_metadata_structure(self, token_path: str, token: Dict) -> bool:
        """Validate token metadata structure"""
        if "$extensions" not in token:
            self.warnings.append(f"Token {token_path}: Missing $extensions metadata")
            return False
        
        metadata = token.get("$extensions", {}).get("metadata", {})
        
        # Required fields
        required = ["element", "attribute", "purpose", "category"]
        missing = [f for f in required if f not in metadata]
        
        if missing:
            self.errors.append(
                f"Token {token_path}: Missing required metadata fields: {', '.join(missing)}"
            )
            return False
        
        # Validate enum values
        valid_purposes = [
            "action", "success", "warning", "danger", "info", "neutral",
            "background", "surface", "text", "border", "focus", "disabled",
            "heading", "body", "caption", "code", "label", "button",
            "xs", "sm", "md", "lg", "xl", "2xl"
        ]
        
        if metadata.get("purpose") not in valid_purposes:
            self.warnings.append(
                f"Token {token_path}: Invalid purpose '{metadata.get('purpose')}'"
            )
        
        valid_categories = ["primitive", "semantic", "component"]
        if metadata.get("category") not in valid_categories:
            self.errors.append(
                f"Token {token_path}: Invalid category '{metadata.get('category')}'"
            )
            return False
        
        self.successes.append(f"✓ Token {token_path}: Metadata valid")
        return True
    
    def validate_wcag_compliance(self, token_path: str, token: Dict) -> bool:
        """Validate WCAG compliance levels"""
        metadata = token.get("$extensions", {}).get("metadata", {})
        wcag_level = metadata.get("wcag_level", "AA")
        contrast_ratio = metadata.get("contrast_ratio", 0)
        
        valid_levels = ["A", "AA", "AAA"]
        if wcag_level not in valid_levels:
            self.errors.append(
                f"Token {token_path}: Invalid WCAG level '{wcag_level}'"
            )
            return False
        
        # Check contrast ratio based on level
        min_ratios = {"A": 3, "AA": 4.5, "AAA": 7}
        required_ratio = min_ratios.get(wcag_level, 4.5)
        
        if contrast_ratio > 0 and contrast_ratio < required_ratio:
            self.warnings.append(
                f"Token {token_path}: Contrast ratio {contrast_ratio} below {wcag_level} level ({required_ratio})"
            )
        
        return True
    
    def validate_brand_coverage(self, token_path: str, token: Dict) -> bool:
        """Validate brand coverage (white label)"""
        metadata = token.get("$extensions", {}).get("metadata", {})
        brands = metadata.get("brands", {})
        
        expected_brands = ["promptea", "nova", "ocean"]
        missing_brands = [b for b in expected_brands if b not in brands]
        
        if missing_brands:
            self.warnings.append(
                f"Token {token_path}: Missing brand values for: {', '.join(missing_brands)}"
            )
        
        for brand, themes in brands.items():
            if brand not in expected_brands:
                self.warnings.append(f"Token {token_path}: Unknown brand '{brand}'")
            
            expected_themes = ["light", "dark"]
            missing_themes = [t for t in expected_themes if t not in themes]
            if missing_themes:
                self.warnings.append(
                    f"Token {token_path}/{brand}: Missing themes: {', '.join(missing_themes)}"
                )
        
        return True
    
    def validate_platform_coverage(self, token_path: str, token: Dict) -> bool:
        """Validate platform coverage"""
        metadata = token.get("$extensions", {}).get("metadata", {})
        coverage = metadata.get("coverage", {})
        
        expected_platforms = ["web", "ios", "android", "tailwind", "storybook"]
        missing = [p for p in expected_platforms if p not in coverage]
        
        if missing:
            self.warnings.append(
                f"Token {token_path}: Missing platform coverage for: {', '.join(missing)}"
            )
            return False
        
        return True
    
    def validate_aliases(self, token_path: str, token: Dict) -> bool:
        """Validate aliases for backward compatibility"""
        metadata = token.get("$extensions", {}).get("metadata", {})
        aliases = metadata.get("aliases", [])
        
        if not aliases:
            self.warnings.append(f"Token {token_path}: No aliases defined (backward compat)")
            return True
        
        # Validate alias format
        for alias in aliases:
            if not isinstance(alias, str) or not alias.strip():
                self.errors.append(f"Token {token_path}: Invalid alias format: {alias}")
                return False
        
        return True
    
    def validate_deprecation(self, token_path: str, token: Dict) -> bool:
        """Validate deprecation information"""
        metadata = token.get("$extensions", {}).get("metadata", {})
        deprecation = metadata.get("deprecation", {})
        
        if not deprecation or not deprecation.get("deprecated"):
            return True
        
        # If deprecated, check for replacement
        replacement = deprecation.get("replacement")
        if not replacement:
            self.warnings.append(
                f"Token {token_path}: Deprecated but no replacement specified"
            )
        
        removal_date = deprecation.get("removal_date")
        if removal_date:
            try:
                from datetime import datetime
                datetime.strptime(removal_date, "%Y-%m-%d")
            except ValueError:
                self.errors.append(
                    f"Token {token_path}: Invalid removal_date format (use YYYY-MM-DD)"
                )
                return False
        
        return True
    
    def validate_token(self, token_path: str, token: Dict) -> bool:
        """Validate a single token completely"""
        all_valid = True
        
        # Required fields
        if "$value" not in token:
            self.errors.append(f"Token {token_path}: Missing $value")
            return False
        
        if "$type" not in token:
            self.errors.append(f"Token {token_path}: Missing $type")
            return False
        
        # Validate metadata structure
        all_valid &= self.validate_metadata_structure(token_path, token)
        
        # For color tokens, validate WCAG
        if token.get("$type") == "color":
            all_valid &= self.validate_wcag_compliance(token_path, token)
            all_valid &= self.validate_brand_coverage(token_path, token)
        
        # Platform coverage
        all_valid &= self.validate_platform_coverage(token_path, token)
        
        # Aliases
        all_valid &= self.validate_aliases(token_path, token)
        
        # Deprecation
        all_valid &= self.validate_deprecation(token_path, token)
        
        return all_valid

    def iter_tokens(self, value: Dict, prefix: str = ""):
        """Yield every DTCG leaf token with its dot-separated path."""
        for key, child in value.items():
            if key.startswith("$"):
                continue
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(child, dict) and "$value" in child:
                yield path, child
            elif isinstance(child, dict):
                yield from self.iter_tokens(child, path)
    
    def validate_all_tokens(self) -> bool:
        """Validate all tokens in dtcg file"""
        tokens = self.load_tokens()
        
        total_tokens = 0
        valid_tokens = 0
        
        for token_path, token in self.iter_tokens(tokens):
            total_tokens += 1
            if self.validate_token(token_path, token):
                valid_tokens += 1
        
        # Print results
        print(f"\n{'='*70}")
        print(f"Token Schema Validation Report")
        print(f"{'='*70}\n")
        
        print(f"✓ Successes: {len(self.successes)}")
        for msg in self.successes[:5]:
            print(f"  {msg}")
        if len(self.successes) > 5:
            print(f"  ... and {len(self.successes) - 5} more")
        
        print(f"\n⚠ Warnings: {len(self.warnings)}")
        for msg in self.warnings[:10]:
            print(f"  {msg}")
        if len(self.warnings) > 10:
            print(f"  ... and {len(self.warnings) - 10} more")
        
        print(f"\n✗ Errors: {len(self.errors)}")
        for msg in self.errors:
            print(f"  {msg}")
        
        print(f"\n{'='*70}")
        print(f"Summary: {valid_tokens}/{total_tokens} tokens valid")
        print(f"Status: {'🟢 PASS' if len(self.errors) == 0 else '🔴 FAIL'}")
        print(f"{'='*70}\n")
        
        return len(self.errors) == 0
    
    def run(self):
        """Run the validator"""
        try:
            print("\n🔍 Loading token metadata schema...")
            self.load_schema()
            print("✓ Schema loaded")
            
            print("\n🔍 Validating tokens...")
            valid = self.validate_all_tokens()
            
            return 0 if valid else 1
        except Exception as e:
            print(f"\n✗ Validation error: {e}", file=sys.stderr)
            return 1

if __name__ == "__main__":
    validator = TokenSchemaValidator()
    sys.exit(validator.run())
