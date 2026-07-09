#!/usr/bin/env python3
"""
PHASE 4: Token Coverage Matrix Agent
Tracks token coverage across 5 platforms × 3 brands × 2 themes
Generates coverage dashboard with health metrics
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict

class CoverageMatrixAgent:
    """
    Generates coverage matrix tracking which tokens are available on which platforms.
    
    Platforms: Web, Tailwind, iOS, Android, Storybook
    Coverage tracking: Semantic tokens only (foundations are implicit)
    """
    
    PLATFORMS = ["web", "tailwind", "ios", "android", "storybook"]
    BRANDS = ["promptea", "nova", "ocean"]
    THEMES = ["light", "dark"]
    
    def __init__(self, tokens_file: str = "01-tokens/tokens.dtcg.json"):
        self.tokens_file = Path(tokens_file)
        self.tokens = self._load_tokens()
        self.coverage_matrix = defaultdict(lambda: defaultdict(bool))
        self.metrics = {
            "total_tokens": 0,
            "platform_coverage": {},
            "brand_coverage": {},
            "theme_coverage": {},
            "gaps": [],
            "recommendations": [],
        }
    
    def _load_tokens(self) -> Dict:
        """Load token definitions"""
        try:
            with open(self.tokens_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading tokens: {e}", file=sys.stderr)
            sys.exit(1)
    
    def analyze_coverage(self) -> Dict:
        """Analyze token coverage across all dimensions"""
        
        semantic_tokens = self._extract_semantic_tokens()
        self.metrics["total_tokens"] = len(semantic_tokens)
        
        for token_path, token in semantic_tokens.items():
            metadata = token.get("$extensions", {}).get("metadata", {})
            coverage = metadata.get("coverage", {})
            brands = metadata.get("brands", {})
            token_coverage = self.coverage_matrix[token_path]
            
            # Track platform coverage
            for platform in self.PLATFORMS:
                if coverage.get(platform, False):
                    token_coverage[platform] = True
            
            # Track brand coverage
            for brand in self.BRANDS:
                if brands.get(brand, False) or token_path.startswith(f"color.{brand}.") or not token_path.startswith("color."):
                    token_coverage[f"brand_{brand}"] = True
            
            # Track theme coverage
            for theme in self.THEMES:
                if (
                    brands.get(theme, False)
                    or all(isinstance(variant, dict) and theme in variant for variant in brands.values())
                    or f".{theme}." in token_path
                    or not token_path.startswith("color.")
                ):
                    token_coverage[f"theme_{theme}"] = True
        
        # Calculate platform metrics
        self._calculate_platform_metrics()
        self._calculate_brand_metrics()
        self._identify_gaps()
        
        return self.metrics
    
    def _extract_semantic_tokens(self) -> Dict:
        """Extract DTCG leaf tokens, including ones pending metadata migration."""
        return {
            token_path: token
            for token_path, token in self._iter_tokens(self.tokens)
            if isinstance(token, dict) and "$value" in token
        }
    
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
    
    def _calculate_platform_metrics(self):
        """Calculate coverage % for each platform"""
        total = self.metrics["total_tokens"]
        
        for platform in self.PLATFORMS:
            covered = sum(
                1 for token in self.coverage_matrix.values()
                if token.get(platform, False)
            )
            
            percentage = (covered / total * 100) if total > 0 else 0
            self.metrics["platform_coverage"][platform] = {
                "covered": covered,
                "total": total,
                "percentage": round(percentage, 2),
            }
            
            # Flag low coverage
            if percentage < 95:
                self.metrics["gaps"].append({
                    "type": "platform_coverage",
                    "platform": platform,
                    "percentage": percentage,
                    "missing_count": total - covered,
                })
    
    def _calculate_brand_metrics(self):
        """Calculate coverage % for each brand and theme"""
        total = self.metrics["total_tokens"]
        
        for brand in self.BRANDS:
            covered = sum(
                1 for token in self.coverage_matrix.values()
                if token.get(f"brand_{brand}", False)
            )
            
            percentage = (covered / total * 100) if total > 0 else 0
            self.metrics["brand_coverage"][brand] = {
                "covered": covered,
                "total": total,
                "percentage": round(percentage, 2),
            }
        
        for theme in self.THEMES:
            covered = sum(
                1 for token in self.coverage_matrix.values()
                if token.get(f"theme_{theme}", False)
            )
            
            percentage = (covered / total * 100) if total > 0 else 0
            self.metrics["theme_coverage"][theme] = {
                "covered": covered,
                "total": total,
                "percentage": round(percentage, 2),
            }
    
    def _identify_gaps(self):
        """Identify tokens with incomplete coverage"""
        for token_path, platforms in self.coverage_matrix.items():
            covered_platforms = [p for p in self.PLATFORMS if platforms.get(p, False)]
            
            if len(covered_platforms) < len(self.PLATFORMS):
                missing = set(self.PLATFORMS) - set(covered_platforms)
                self.metrics["gaps"].append({
                    "type": "token_incomplete",
                    "token": token_path,
                    "covered_platforms": covered_platforms,
                    "missing_platforms": list(missing),
                })
    
    def generate_coverage_json(self) -> Dict:
        """Generate coverage matrix in JSON format"""
        return {
            "generated": datetime.now().isoformat(),
            "total_semantic_tokens": self.metrics["total_tokens"],
            "platform_coverage": self.metrics["platform_coverage"],
            "brand_coverage": self.metrics["brand_coverage"],
            "theme_coverage": self.metrics["theme_coverage"],
            "gaps": self.metrics["gaps"],
            "recommendations": self._generate_recommendations(),
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on coverage analysis"""
        recommendations = []
        
        # Check platform coverage
        for platform, coverage in self.metrics["platform_coverage"].items():
            if coverage["percentage"] < 100:
                recommendations.append(
                    f"📌 Platform '{platform}' has {coverage['total'] - coverage['covered']} "
                    f"missing tokens ({coverage['percentage']}% coverage)"
                )
        
        # Check brand coverage
        for brand, coverage in self.metrics["brand_coverage"].items():
            if coverage["percentage"] < 100:
                recommendations.append(
                    f"📌 Brand '{brand}' has {coverage['total'] - coverage['covered']} "
                    f"missing token variants ({coverage['percentage']}% coverage)"
                )
        
        return recommendations
    
    def generate_markdown_report(self) -> str:
        """Generate human-readable coverage report"""
        lines = [
            "# Token Coverage Matrix Dashboard",
            f"Generated: {datetime.now().isoformat()[:10]}",
            "",
            "## Overall Metrics",
            f"- **Total Semantic Tokens:** {self.metrics['total_tokens']}",
            f"- **Platforms:** {len(self.PLATFORMS)} (Web, Tailwind, iOS, Android, Storybook)",
            f"- **Brands:** {len(self.BRANDS)} (Promptea, Nova, Ocean)",
            f"- **Themes:** {len(self.THEMES)} (Light, Dark)",
            "",
            "## Platform Coverage",
            "",
            "| Platform | Covered | Total | % | Status |",
            "|----------|---------|-------|---|--------|",
        ]
        
        for platform, coverage in self.metrics["platform_coverage"].items():
            status = "✅" if coverage["percentage"] == 100 else "⚠️ "
            lines.append(
                f"| {platform.upper()} | {coverage['covered']} | {coverage['total']} "
                f"| {coverage['percentage']}% | {status} |"
            )
        
        lines.extend([
            "",
            "## Brand Coverage",
            "",
            "| Brand | Covered | Total | % | Status |",
            "|-------|---------|-------|---|--------|",
        ])
        
        for brand, coverage in self.metrics["brand_coverage"].items():
            status = "✅" if coverage["percentage"] == 100 else "⚠️ "
            lines.append(
                f"| {brand.capitalize()} | {coverage['covered']} | {coverage['total']} "
                f"| {coverage['percentage']}% | {status} |"
            )
        
        lines.extend([
            "",
            "## Theme Coverage",
            "",
            "| Theme | Covered | Total | % | Status |",
            "|-------|---------|-------|---|--------|",
        ])
        
        for theme, coverage in self.metrics["theme_coverage"].items():
            status = "✅" if coverage["percentage"] == 100 else "⚠️ "
            lines.append(
                f"| {theme.capitalize()} | {coverage['covered']} | {coverage['total']} "
                f"| {coverage['percentage']}% | {status} |"
            )
        
        if self.metrics["gaps"]:
            lines.extend([
                "",
                "## ⚠️  Coverage Gaps",
                "",
            ])
            
            for gap in self.metrics["gaps"]:
                if gap["type"] == "token_incomplete":
                    lines.append(
                        f"- **{gap['token']}** "
                        f"(Missing: {', '.join(gap['missing_platforms'])})"
                    )
        
        return "\n".join(lines)
    
    def print_report(self):
        """Print coverage report"""
        print(self.generate_markdown_report())
    
    def save_reports(self):
        """Save coverage matrix and reports"""
        from datetime import datetime
        
        # Save JSON matrix
        matrix_file = "01-tokens/tokens-coverage-matrix.json"
        Path(matrix_file).parent.mkdir(parents=True, exist_ok=True)
        with open(matrix_file, 'w') as f:
            json.dump(self.generate_coverage_json(), f, indent=2)
        print(f"✅ Coverage matrix saved to {matrix_file}")
        
        # Save markdown report
        report_file = "logs/coverage-matrix-report.md"
        Path(report_file).parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w') as f:
            f.write(self.generate_markdown_report())
        print(f"✅ Coverage report saved to {report_file}")


# Import datetime for save_reports
from datetime import datetime

if __name__ == "__main__":
    agent = CoverageMatrixAgent()
    agent.analyze_coverage()
    agent.print_report()
    agent.save_reports()
