#!/usr/bin/env python3
"""
PHASE 4: Token Health Monitor Agent
Tracks system health metrics: WCAG compliance, deprecation status, coverage trends
Generates health dashboard with actionable metrics
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class TokenHealthMonitor:
    """
    Monitors token system health across multiple dimensions:
    - WCAG AA compliance (contrast ratios)
    - Deprecation lifecycle status
    - Platform coverage completeness
    - Schema metadata completeness
    - Build system stability
    """
    
    def __init__(self, tokens_file: str = "01-tokens/tokens.dtcg.json"):
        self.tokens_file = Path(tokens_file)
        self.tokens = self._load_tokens()
        self.health = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "HEALTHY",  # HEALTHY, WARNING, CRITICAL
            "metrics": {
                "wcag_compliance": {"status": "UNKNOWN", "percentage": 0, "issues": []},
                "metadata_completeness": {"status": "UNKNOWN", "percentage": 0, "issues": []},
                "deprecation_status": {"status": "UNKNOWN", "healthy_tokens": 0, "deprecated_tokens": 0},
                "platform_coverage": {"status": "UNKNOWN", "percentage": 0, "gaps": []},
                "schema_validation": {"status": "UNKNOWN", "valid": 0, "invalid": 0},
            },
            "alerts": [],
            "recommendations": [],
            "next_review": "",
        }
    
    def _load_tokens(self) -> Dict:
        """Load token definitions"""
        try:
            with open(self.tokens_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading tokens: {e}", file=sys.stderr)
            sys.exit(1)
    
    def analyze_health(self) -> Dict:
        """Run all health checks"""
        self._check_wcag_compliance()
        self._check_metadata_completeness()
        self._check_deprecation_status()
        self._check_platform_coverage()
        self._check_schema_validation()
        self._determine_overall_status()
        self._generate_recommendations()
        
        return self.health
    
    def _check_wcag_compliance(self):
        """Check WCAG AA compliance for all color tokens"""
        tokens = self._iter_semantic_tokens()
        wcag_checked = 0
        wcag_assessed = 0
        wcag_compliant = 0
        wcag_violations = []
        wcag_pending = []
        
        for token_path, token in tokens:
            if "color" not in token_path:
                continue
            
            metadata = token.get("$extensions", {}).get("metadata", {})
            if not metadata.get("contrast_assessable", False):
                continue

            wcag_checked += 1
            wcag_level = metadata.get("wcag_level", "UNKNOWN")
            contrast_ratio = metadata.get("contrast_ratio", 0)
            
            if wcag_level == "UNKNOWN" or not contrast_ratio:
                wcag_pending.append(token_path)
                continue

            wcag_assessed += 1
            if wcag_level == "AA" and contrast_ratio >= 4.5:
                wcag_compliant += 1
            else:
                wcag_violations.append({
                    "token": token_path,
                    "wcag_level": wcag_level,
                    "contrast_ratio": contrast_ratio,
                })
        
        percentage = (wcag_compliant / wcag_assessed * 100) if wcag_assessed > 0 else 0
        status = "⚠️ NOT ASSESSED" if wcag_assessed == 0 else (
            "✅ PASS" if percentage >= 95 else "⚠️ WARNING"
        )
        
        self.health["metrics"]["wcag_compliance"] = {
            "status": status,
            "percentage": round(percentage, 2),
            "compliant": wcag_compliant,
            "assessed": wcag_assessed,
            "total": wcag_checked,
            "violations": wcag_violations,
            "pending_evidence": wcag_pending,
        }
        
        if wcag_pending:
            self.health["alerts"].append(
                f"⚠️  WCAG Evidence: {len(wcag_pending)} color tokens lack declared level or contrast ratio"
            )
        elif percentage < 95:
            self.health["alerts"].append(
                f"⚠️  WCAG Compliance: {100 - percentage:.1f}% of assessed color tokens non-compliant"
            )
    
    def _check_metadata_completeness(self):
        """Check that all tokens have required metadata fields"""
        BASE_REQUIRED_FIELDS = ["element", "attribute", "purpose", "category", "brands", "coverage"]
        
        tokens = self._iter_semantic_tokens()
        total = 0
        complete = 0
        incomplete_tokens = []
        
        for token_path, token in tokens:
            total += 1
            metadata = token.get("$extensions", {}).get("metadata", {})
            required_fields = list(BASE_REQUIRED_FIELDS)
            if token.get("$type") == "color":
                required_fields.append("wcag_level")
            
            missing_fields = [f for f in required_fields if f not in metadata]
            
            if len(missing_fields) == 0:
                complete += 1
            else:
                incomplete_tokens.append({
                    "token": token_path,
                    "missing_fields": missing_fields,
                })
        
        percentage = (complete / total * 100) if total > 0 else 0
        
        self.health["metrics"]["metadata_completeness"] = {
            "status": "✅ PASS" if percentage >= 100 else "⚠️ WARNING",
            "percentage": round(percentage, 2),
            "complete": complete,
            "total": total,
            "incomplete": incomplete_tokens[:5],  # Show first 5
        }
        
        if percentage < 100:
            self.health["alerts"].append(
                f"⚠️  Metadata: {total - complete} tokens missing required fields"
            )
    
    def _check_deprecation_status(self):
        """Check deprecation lifecycle status"""
        tokens = self._iter_semantic_tokens()
        healthy = 0
        deprecated = 0
        at_risk = 0  # Deprecated for >37 days
        
        for token_path, token in tokens:
            metadata = token.get("$extensions", {}).get("metadata", {})
            deprecation = metadata.get("deprecation", {})
            
            if not deprecation or deprecation.get("status") == "active":
                healthy += 1
            else:
                deprecated += 1
                
                # Check if past removal threshold
                dep_date = deprecation.get("date", "")
                try:
                    from datetime import datetime
                    dep_dt = datetime.fromisoformat(dep_date)
                    days_since = (datetime.now() - dep_dt).days
                    if days_since > 37:
                        at_risk += 1
                except:
                    pass
        
        self.health["metrics"]["deprecation_status"] = {
            "status": "⚠️ WARNING" if at_risk > 0 else "✅ PASS",
            "active_tokens": healthy,
            "deprecated_tokens": deprecated,
            "overdue_for_removal": at_risk,
        }
        
        if at_risk > 0:
            self.health["alerts"].append(
                f"🚨 Deprecation: {at_risk} token(s) overdue for removal (>37 days)"
            )
    
    def _check_platform_coverage(self):
        """Check that tokens are available on all 5 platforms"""
        PLATFORMS = ["web", "tailwind", "ios", "android", "storybook"]
        tokens = list(self._iter_semantic_tokens())
        covered_by_platform = {p: 0 for p in PLATFORMS}
        coverage_gaps = []
        
        for token_path, token in tokens:
            metadata = token.get("$extensions", {}).get("metadata", {})
            coverage = metadata.get("coverage", {})
            
            for platform in PLATFORMS:
                if coverage.get(platform, False):
                    covered_by_platform[platform] += 1
                else:
                    coverage_gaps.append({
                        "token": token_path,
                        "missing_platform": platform,
                    })
        
        total_tokens = len(tokens)
        avg_coverage = sum(covered_by_platform.values()) / (len(PLATFORMS) * total_tokens * 100) if total_tokens > 0 else 0
        
        self.health["metrics"]["platform_coverage"] = {
            "status": "✅ PASS" if all(c == total_tokens for c in covered_by_platform.values()) else "⚠️ WARNING",
            "percentage": round(min(covered_by_platform.values()) / total_tokens * 100, 2) if total_tokens > 0 else 0,
            "coverage_by_platform": covered_by_platform,
            "gaps_count": len(coverage_gaps),
        }
        
        if self.health["metrics"]["platform_coverage"]["percentage"] < 100:
            self.health["alerts"].append(
                f"⚠️  Platform Coverage: Some tokens missing on certain platforms"
            )
    
    def _check_schema_validation(self):
        """Check that all tokens pass schema validation"""
        # This would normally run the validate-schema.py
        # For now, we'll do a basic check
        
        tokens = list(self._iter_tokens(self.tokens))
        valid = 0
        invalid = 0
        
        for token_path, token in tokens:
            if isinstance(token, dict) and "$value" in token:
                # Basic schema check: has $value
                if token.get("$value") is not None:
                    valid += 1
                else:
                    invalid += 1
        
        self.health["metrics"]["schema_validation"] = {
            "status": "✅ PASS" if invalid == 0 else "⚠️ WARNING",
            "valid": valid,
            "invalid": invalid,
        }
        
        if invalid > 0:
            self.health["alerts"].append(
                f"⚠️  Schema: {invalid} token(s) fail validation"
            )
    
    def _iter_semantic_tokens(self):
        """Iterate DTCG leaf tokens, including tokens pending metadata migration."""
        for token_path, token in self._iter_tokens(self.tokens):
            if isinstance(token, dict) and "$value" in token:
                yield (token_path, token)
    
    def _iter_tokens(self, tokens: Dict, prefix: str = ""):
        """Iterate through all tokens"""
        for key, value in tokens.items():
            if key.startswith("$"):
                continue
            
            path = f"{prefix}{key}" if prefix else key
            
            if isinstance(value, dict) and "$value" not in value:
                yield from self._iter_tokens(value, f"{path}.")
            else:
                yield (path, value)
    
    def _determine_overall_status(self):
        """Determine overall system health"""
        if self.health["alerts"]:
            # Count critical vs warning alerts
            critical_count = sum(1 for a in self.health["alerts"] if a.startswith("🚨"))
            
            if critical_count > 0:
                self.health["overall_status"] = "🚨 CRITICAL"
            else:
                self.health["overall_status"] = "⚠️ WARNING"
        else:
            self.health["overall_status"] = "✅ HEALTHY"
    
    def _generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = self.health["recommendations"]
        
        if self.health["metrics"]["wcag_compliance"]["violations"]:
            recommendations.append(
                "📌 Review WCAG violations in color tokens and adjust contrast ratios"
            )
        
        if self.health["metrics"]["metadata_completeness"]["incomplete"]:
            recommendations.append(
                "📌 Complete metadata for incomplete tokens (element, attribute, purpose, etc.)"
            )
        
        if self.health["metrics"]["deprecation_status"]["overdue_for_removal"] > 0:
            recommendations.append(
                "🚨 URGENT: Remove overdue deprecated tokens (>37 days old)"
            )
        
        if self.health["metrics"]["platform_coverage"]["gaps_count"] > 0:
            recommendations.append(
                "📌 Fill platform coverage gaps: ensure all tokens exported to all 5 platforms"
            )
        
        if not recommendations:
            recommendations.append("✅ All systems nominal. Continue monitoring.")
        
        self.health["next_review"] = (
            datetime.now() + timedelta(days=7)
        ).isoformat()[:10]
    
    def generate_markdown_report(self) -> str:
        """Generate human-readable health report"""
        lines = [
            "# Token System Health Dashboard",
            f"Generated: {self.health['timestamp'][:10]}",
            f"**Status: {self.health['overall_status']}**",
            "",
        ]
        
        if self.health["alerts"]:
            lines.extend([
                "## ⚠️  Alerts",
                "",
            ])
            for alert in self.health["alerts"]:
                lines.append(f"- {alert}")
            lines.append("")
        
        # WCAG Compliance
        wcag = self.health["metrics"]["wcag_compliance"]
        lines.extend([
            "## WCAG AA Compliance",
            f"- **Status:** {wcag['status']}",
            f"- **Assessed coverage:** {wcag['percentage']}% ({wcag['compliant']}/{wcag['assessed']} assessed; {wcag['total']} color tokens total)",
        ])
        
        if wcag["violations"]:
            lines.append("- **Violations:**")
            for v in wcag["violations"][:3]:
                lines.append(f"  - {v['token']} (ratio: {v['contrast_ratio']})")
        if wcag["pending_evidence"]:
            lines.append(f"- **Pending evidence:** {len(wcag['pending_evidence'])} color tokens lack declared WCAG metadata.")
        lines.append("")
        
        # Metadata Completeness
        meta = self.health["metrics"]["metadata_completeness"]
        lines.extend([
            "## Metadata Completeness",
            f"- **Status:** {meta['status']}",
            f"- **Coverage:** {meta['percentage']}% ({meta['complete']}/{meta['total']})",
        ])
        
        if meta["incomplete"]:
            lines.append("- **Incomplete tokens:**")
            for t in meta["incomplete"][:3]:
                lines.append(f"  - {t['token']}")
        lines.append("")
        
        # Deprecation Status
        dep = self.health["metrics"]["deprecation_status"]
        lines.extend([
            "## Deprecation Lifecycle",
            f"- **Status:** {dep['status']}",
            f"- **Active tokens:** {dep['active_tokens']}",
            f"- **Deprecated:** {dep['deprecated_tokens']}",
            f"- **Overdue for removal:** {dep['overdue_for_removal']}",
            "",
        ])
        
        # Platform Coverage
        plat = self.health["metrics"]["platform_coverage"]
        lines.extend([
            "## Platform Coverage",
            f"- **Status:** {plat['status']}",
            f"- **Minimum coverage:** {plat['percentage']}%",
            f"- **Coverage gaps:** {plat['gaps_count']}",
            "",
        ])
        
        # Schema Validation
        schema = self.health["metrics"]["schema_validation"]
        lines.extend([
            "## Schema Validation",
            f"- **Status:** {schema['status']}",
            f"- **Valid tokens:** {schema['valid']}",
            f"- **Invalid tokens:** {schema['invalid']}",
            "",
        ])
        
        return "\n".join(lines)
    
    def print_report(self):
        """Print health report"""
        print(self.generate_markdown_report())
    
    def save_report(self, output_file: str = "TOKENS-HEALTH.md"):
        """Save health report to file"""
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(self.generate_markdown_report())
        print(f"✅ Health report saved to {output_file}")
        
        # Also save JSON for programmatic access
        json_file = "logs/tokens-health.json"
        Path(json_file).parent.mkdir(parents=True, exist_ok=True)
        with open(json_file, 'w') as f:
            json.dump(self.health, f, indent=2)
        print(f"✅ Health metrics saved to {json_file}")


from datetime import timedelta

if __name__ == "__main__":
    monitor = TokenHealthMonitor()
    monitor.analyze_health()
    monitor.print_report()
    monitor.save_report()
