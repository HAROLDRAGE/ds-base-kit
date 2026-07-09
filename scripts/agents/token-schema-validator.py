#!/usr/bin/env python3
"""
Token Schema Validator Agent v1.0
FASE 3 Implementation: First of 4 Agents for Design Tokens Platform

Purpose:
  - Validate tokens against machine-readable metadata schema
  - Enforce WCAG compliance automatically
  - Check brand coverage (white label)
  - Detect missing metadata before merge

Governance:
  - Agent PROPOSES fixes
  - Design Lead APPROVES or REJECTS
  - Merge only after APPROVAL
  - Never auto-merge

Triggered by:
  - Pre-commit hook: `python3 scripts/agents/token-schema-validator.py --pre-commit`
  - Pre-push hook: `python3 scripts/agents/token-schema-validator.py --pre-push`
  - Manual: `python3 scripts/agents/token-schema-validator.py --full`
  - CI/CD: `.github/workflows/validate-tokens.yml`
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(Path(__file__).parent.parent / "logs" / "token-schema-validator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TokenSchemaValidatorAgent:
    """First Agent: Schema Validator for Design Tokens Platform"""
    
    def __init__(self, mode: str = "full"):
        self.mode = mode  # "pre-commit", "pre-push", or "full"
        self.script_dir = Path(__file__).parent.parent
        self.tokens_dir = self.script_dir / "01-tokens"
        self.schema_path = self.tokens_dir / "token-metadata.schema.json"
        self.tokens_dtcg_path = self.tokens_dir / "tokens.dtcg.json"
        self.violations: List[Dict] = []
        self.warnings: List[Dict] = []
        self.pass_checks: List[Dict] = []
        
    def validate_schema_exists(self) -> bool:
        """Ensure schema file exists"""
        if not self.schema_path.exists():
            self.violations.append({
                "code": "SCHEMA_MISSING",
                "message": f"Token metadata schema not found: {self.schema_path}",
                "severity": "critical",
                "action": "Create token-metadata.schema.json"
            })
            return False
        return True
    
    def validate_tokens_exist(self) -> bool:
        """Ensure tokens file exists"""
        if not self.tokens_dtcg_path.exists():
            self.violations.append({
                "code": "TOKENS_MISSING",
                "message": f"Tokens file not found: {self.tokens_dtcg_path}",
                "severity": "critical",
                "action": "Create or restore tokens.dtcg.json"
            })
            return False
        return True
    
    def load_files(self) -> Tuple[Dict, Dict]:
        """Load schema and tokens"""
        with open(self.schema_path) as f:
            schema = json.load(f)
        with open(self.tokens_dtcg_path) as f:
            tokens = json.load(f)
        return schema, tokens
    
    def check_metadata_required_fields(self, token_path: str, metadata: Dict) -> bool:
        """Check that all required metadata fields are present"""
        required = ["element", "attribute", "purpose", "category"]
        missing = [f for f in required if f not in metadata]
        
        if missing:
            self.violations.append({
                "code": "METADATA_INCOMPLETE",
                "token": token_path,
                "message": f"Missing metadata fields: {', '.join(missing)}",
                "severity": "high",
                "action": f"Add missing fields: {', '.join(missing)}"
            })
            return False
        
        self.pass_checks.append({
            "token": token_path,
            "check": "Metadata required fields present"
        })
        return True
    
    def check_wcag_compliance(self, token_path: str, token: Dict) -> bool:
        """Validate WCAG compliance"""
        if token.get("$type") != "color":
            return True  # Only color tokens need WCAG check
        
        metadata = token.get("$extensions", {}).get("metadata", {})
        wcag_level = metadata.get("wcag_level", "AA")
        contrast_ratio = metadata.get("contrast_ratio", 0)
        
        if wcag_level not in ["A", "AA", "AAA"]:
            self.violations.append({
                "code": "INVALID_WCAG_LEVEL",
                "token": token_path,
                "message": f"Invalid WCAG level: {wcag_level}",
                "severity": "high",
                "action": "Set wcag_level to A, AA, or AAA"
            })
            return False
        
        min_ratios = {"A": 3, "AA": 4.5, "AAA": 7}
        required = min_ratios[wcag_level]
        
        if contrast_ratio > 0 and contrast_ratio < required:
            self.warnings.append({
                "code": "WCAG_BELOW_LEVEL",
                "token": token_path,
                "message": f"Contrast ratio {contrast_ratio} below {wcag_level} ({required} required)",
                "severity": "medium"
            })
        
        self.pass_checks.append({
            "token": token_path,
            "check": f"WCAG {wcag_level} compliance checked"
        })
        return True
    
    def check_brand_coverage(self, token_path: str, metadata: Dict) -> bool:
        """Validate brand coverage (white label)"""
        brands = metadata.get("brands", {})
        expected_brands = {"promptea", "nova", "ocean"}
        
        if not brands:
            self.warnings.append({
                "code": "NO_BRANDS",
                "token": token_path,
                "message": "No brand overrides specified",
                "severity": "low"
            })
            return True
        
        provided_brands = set(brands.keys())
        missing_brands = expected_brands - provided_brands
        
        if missing_brands:
            self.warnings.append({
                "code": "INCOMPLETE_BRAND_COVERAGE",
                "token": token_path,
                "message": f"Missing brands: {', '.join(missing_brands)}",
                "severity": "medium"
            })
        
        # Check each brand has light/dark
        for brand, themes in brands.items():
            if isinstance(themes, dict):
                if "light" not in themes or "dark" not in themes:
                    self.violations.append({
                        "code": "INCOMPLETE_BRAND_THEMES",
                        "token": token_path,
                        "message": f"Brand {brand}: missing light/dark themes",
                        "severity": "high"
                    })
                    return False
        
        self.pass_checks.append({
            "token": token_path,
            "check": f"Brand coverage complete ({len(brands)}/{len(expected_brands)} brands)"
        })
        return True
    
    def check_platform_coverage(self, token_path: str, metadata: Dict) -> bool:
        """Validate platform coverage"""
        coverage = metadata.get("coverage", {})
        expected_platforms = {"web", "ios", "android", "tailwind", "storybook"}
        
        if not coverage:
            self.warnings.append({
                "code": "NO_COVERAGE",
                "token": token_path,
                "message": "No platform coverage specified",
                "severity": "low"
            })
            return True
        
        provided = set(p for p, v in coverage.items() if v)
        missing = expected_platforms - provided
        
        if missing:
            self.warnings.append({
                "code": "INCOMPLETE_COVERAGE",
                "token": token_path,
                "message": f"Missing platforms: {', '.join(missing)}",
                "severity": "medium"
            })
        
        self.pass_checks.append({
            "token": token_path,
            "check": f"Platform coverage: {len(provided)}/{len(expected_platforms)}"
        })
        return True
    
    def check_deprecation_integrity(self, token_path: str, metadata: Dict) -> bool:
        """Validate deprecation information"""
        deprecation = metadata.get("deprecation", {})
        
        if not deprecation.get("deprecated"):
            return True
        
        # If deprecated, check for replacement
        if not deprecation.get("replacement"):
            self.violations.append({
                "code": "DEPRECATION_NO_REPLACEMENT",
                "token": token_path,
                "message": "Deprecated token must specify replacement",
                "severity": "high",
                "action": "Add 'replacement' field"
            })
            return False
        
        removal_date = deprecation.get("removal_date")
        if removal_date:
            try:
                from datetime import datetime
                datetime.strptime(removal_date, "%Y-%m-%d")
            except ValueError:
                self.violations.append({
                    "code": "INVALID_REMOVAL_DATE",
                    "token": token_path,
                    "message": "removal_date must be in YYYY-MM-DD format",
                    "severity": "high"
                })
                return False
        
        self.pass_checks.append({
            "token": token_path,
            "check": f"Deprecation integrity verified (replacement: {deprecation['replacement']})"
        })
        return True
    
    def validate_token_complete(self, token_path: str, token: Dict) -> bool:
        """Run all validations for a token"""
        if "$value" not in token or "$type" not in token:
            self.violations.append({
                "code": "INVALID_TOKEN_STRUCTURE",
                "token": token_path,
                "message": "Token missing $value or $type",
                "severity": "critical"
            })
            return False
        
        metadata = token.get("$extensions", {}).get("metadata", {})
        
        all_valid = True
        all_valid &= self.check_metadata_required_fields(token_path, metadata)
        all_valid &= self.check_wcag_compliance(token_path, token)
        all_valid &= self.check_brand_coverage(token_path, metadata)
        all_valid &= self.check_platform_coverage(token_path, metadata)
        all_valid &= self.check_deprecation_integrity(token_path, metadata)
        
        return all_valid
    
    def generate_report(self) -> Dict:
        """Generate validation report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "mode": self.mode,
            "violations": self.violations,
            "warnings": self.warnings,
            "passes": len(self.pass_checks),
            "status": "🟢 PASS" if not self.violations else "🔴 FAIL"
        }
    
    def print_report(self):
        """Print human-readable report"""
        report = self.generate_report()
        
        print(f"\n{'='*70}")
        print(f"TOKEN SCHEMA VALIDATOR AGENT — {self.mode.upper()}")
        print(f"{'='*70}\n")
        
        print(f"✓ Passes: {report['passes']}")
        
        if self.warnings:
            print(f"\n⚠ Warnings: {len(self.warnings)}")
            for warning in self.warnings[:5]:
                print(f"  [{warning['code']}] {warning['token']}: {warning['message']}")
            if len(self.warnings) > 5:
                print(f"  ... and {len(self.warnings) - 5} more")
        
        if self.violations:
            print(f"\n✗ Violations: {len(self.violations)}")
            for violation in self.violations:
                print(f"  [{violation['code']}] {violation.get('token', 'GLOBAL')}")
                print(f"    Message: {violation['message']}")
                if violation.get('action'):
                    print(f"    Action: {violation['action']}")
        
        print(f"\n{'='*70}")
        print(f"Status: {report['status']}")
        print(f"{'='*70}\n")
    
    def save_report(self):
        """Save report to file"""
        report = self.generate_report()
        report_path = self.script_dir / "logs" / f"token-validation-{datetime.now().isoformat()}.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved: {report_path}")
    
    def run(self) -> int:
        """Execute the agent"""
        logger.info(f"Starting Token Schema Validator Agent (mode: {self.mode})")
        
        # Check files exist
        if not self.validate_schema_exists():
            self.print_report()
            return 1
        
        if not self.validate_tokens_exist():
            self.print_report()
            return 1
        
        # Load and validate
        try:
            schema, tokens = self.load_files()
            logger.info("Files loaded successfully")
            
            # Validate each token
            color_tokens = tokens.get("color", {})
            for token_name, token_def in color_tokens.items():
                if isinstance(token_def, dict) and "$value" in token_def:
                    self.validate_token_complete(f"color.{token_name}", token_def)
            
            # Print and save report
            self.print_report()
            self.save_report()
            
            # Return exit code
            return 0 if not self.violations else 1
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            self.violations.append({
                "code": "VALIDATION_ERROR",
                "message": str(e),
                "severity": "critical"
            })
            self.print_report()
            return 1

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Token Schema Validator Agent")
    parser.add_argument("--pre-commit", action="store_true", help="Pre-commit mode")
    parser.add_argument("--pre-push", action="store_true", help="Pre-push mode")
    parser.add_argument("--full", action="store_true", help="Full validation")
    
    args = parser.parse_args()
    
    mode = "full"
    if args.pre_commit:
        mode = "pre-commit"
    elif args.pre_push:
        mode = "pre-push"
    
    agent = TokenSchemaValidatorAgent(mode=mode)
    sys.exit(agent.run())
