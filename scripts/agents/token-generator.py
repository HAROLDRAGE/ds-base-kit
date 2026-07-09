#!/usr/bin/env python3
"""
Agent 2: Token Generator
Proposes new semantic tokens from component requirements
Integrates with component manifest to infer missing tokens
"""

import json
import sys
from pathlib import Path
from datetime import datetime


class TokenGenerator:
    """Generate proposals for missing semantic tokens"""
    
    def __init__(self, manifest_path="05-agentes/component-manifest.json",
                 tokens_path="01-tokens/tokens.dtcg.json",
                 schema_path="01-tokens/token-metadata.schema.json"):
        self.manifest_path = Path(manifest_path)
        self.tokens_path = Path(tokens_path)
        self.schema_path = Path(schema_path)
        
        self.manifest = self._load_json(manifest_path)
        self.tokens = self._load_json(tokens_path)
        self.schema = self._load_json(schema_path)
        
        self.existing_tokens = set(self._flatten_tokens(self.tokens).keys())
        self.proposals = []
        self.logger = self._setup_logger()
    
    def _load_json(self, path):
        """Load JSON file safely"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {path}: {e}", file=sys.stderr)
            return {}
    
    def _setup_logger(self):
        """Setup logging infrastructure"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"token-generator-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        return {"file": log_file, "entries": []}
    
    def analyze_components(self, component_names=None):
        """Analyze components and identify missing tokens"""
        components = self.manifest.get("components", [])
        
        if component_names:
            components = [component for component in components if component.get("name") in component_names]
        
        for component in components:
            self._analyze_component(component.get("name", "unknown"), component)
        
        return self.proposals
    
    def _analyze_component(self, component_name, component_spec):
        """Analyze single component for missing tokens"""
        tokens_required = component_spec.get("tokens_used", [])
        
        missing = []
        for token_path in tokens_required:
            if not self._token_exists(token_path):
                missing.append(token_path)
        
        if missing:
            self.logger["entries"].append({
                "component": component_name,
                "missing_count": len(missing),
                "tokens": missing,
                "timestamp": datetime.now().isoformat()
            })
            
            for token_path in missing:
                proposal = self._generate_proposal(token_path, component_name)
                self.proposals.append(proposal)

    def _token_exists(self, token_path):
        """Resolve manifest semantic names against the DTCG catalog."""
        if token_path in self.existing_tokens:
            return True
        if token_path.startswith("color."):
            role = token_path.split(".", 1)[1]
            return any(path.endswith(f".{role}") for path in self.existing_tokens)
        aliases = {
            "space.": "dimension.space.",
            "radius.": "dimension.radius.",
            "motion.": "duration.",
        }
        for source, target in aliases.items():
            if token_path.startswith(source):
                return target + token_path[len(source):] in self.existing_tokens
        return False
    
    def _generate_proposal(self, token_path, component_name):
        """Generate proposal for a missing token"""
        metadata = self._infer_metadata(token_path, component_name)
        
        return {
            "path": token_path,
            "metadata": metadata,
            "component": component_name,
            "type": self._classify_token_type(token_path),
            "requires_design_lead_approval": self._needs_approval(token_path),
            "reason": f"Required by component '{component_name}'"
        }
    
    def _infer_metadata(self, token_path, component_name):
        """Infer metadata from token path and context"""
        parts = token_path.split('.')
        
        return {
            "category": "semantic",
            "element": [component_name],
            "attribute": self._parse_attribute(token_path),
            "purpose": self._parse_purpose(token_path),
            "prominence": "medium",
            "state": ["default"],
            "wcag_level": "AA",
            "brands": ["promptea", "nova", "ocean"],
            "coverage": ["web", "tailwind", "ios", "android", "storybook"],
            "tags": ["generated", "semantic", component_name],
            "design_decision": f"Inferred from component '{component_name}' requirements"
        }
    
    def _parse_attribute(self, token_path):
        """Parse attribute from token path"""
        path_lower = token_path.lower()
        
        if "color" in path_lower:
            return "color"
        elif "space" in path_lower or "padding" in path_lower or "margin" in path_lower:
            return "padding"
        elif "radius" in path_lower or "border-radius" in path_lower:
            return "radius"
        elif "motion" in path_lower or "transition" in path_lower or "duration" in path_lower:
            return "transition"
        elif "font-size" in path_lower or "size" in path_lower:
            return "font-size"
        elif "weight" in path_lower or "bold" in path_lower:
            return "font-weight"
        elif "opacity" in path_lower or "alpha" in path_lower:
            return "opacity"
        else:
            return "custom"
    
    def _parse_purpose(self, token_path):
        """Parse purpose from token path"""
        path_lower = token_path.lower()
        
        if "action" in path_lower or "primary" in path_lower:
            return "action"
        elif "danger" in path_lower or "error" in path_lower or "destructive" in path_lower:
            return "danger"
        elif "success" in path_lower or "positive" in path_lower:
            return "success"
        elif "warning" in path_lower or "caution" in path_lower:
            return "warning"
        elif "info" in path_lower or "information" in path_lower:
            return "info"
        elif "muted" in path_lower or "subtle" in path_lower or "secondary" in path_lower:
            return "muted"
        elif "interactive" in path_lower or "interactive" in path_lower:
            return "interactive"
        else:
            return "neutral"
    
    def _classify_token_type(self, token_path):
        """Classify token as primitive or semantic"""
        if "semantic" in token_path.lower():
            return "semantic"
        elif "foundation" in token_path.lower():
            return "foundation"
        else:
            return "semantic"  # default: inferred tokens are semantic
    
    def _needs_approval(self, token_path):
        """Check if token needs design lead approval"""
        path_lower = token_path.lower()
        
        # Primitives always need approval
        if "foundation" in path_lower or "primitive" in path_lower:
            return True
        
        # Scale changes need approval
        if "scale" in path_lower or "step" in path_lower:
            return True
        
        # New color palettes need approval
        if "color" in path_lower and "palette" in path_lower:
            return True
        
        return False
    
    def _flatten_tokens(self, tokens_dict, parent_key=""):
        """Flatten nested token dict"""
        items = {}
        for k, v in tokens_dict.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            
            if isinstance(v, dict):
                if "$value" in v:
                    # This is a token
                    items[new_key] = v
                else:
                    # Recurse into nested structure
                    items.update(self._flatten_tokens(v, new_key))
        
        return items
    
    def generate_report(self):
        """Generate comprehensive report"""
        return {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "proposals_count": len(self.proposals),
            "proposals": self.proposals,
            "summary": {
                "total_proposals": len(self.proposals),
                "require_approval": sum(1 for p in self.proposals if p["requires_design_lead_approval"]),
                "semantic_only": sum(1 for p in self.proposals if p["type"] == "semantic"),
                "by_component": self._group_by_component()
            }
        }
    
    def _group_by_component(self):
        """Group proposals by component"""
        grouped = {}
        for proposal in self.proposals:
            comp = proposal["component"]
            if comp not in grouped:
                grouped[comp] = []
            grouped[comp].append(proposal["path"])
        return grouped
    
    def save_report(self, output_file=None):
        """Save report to file"""
        if output_file is None:
            output_file = self.logger["file"]
        
        report = self.generate_report()
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return output_file
    
    def print_report(self):
        """Print human-readable report"""
        report = self.generate_report()
        
        print("\n" + "="*80)
        print("🤖 TOKEN GENERATOR AGENT — ANALYSIS REPORT")
        print("="*80)
        print(f"\n📊 Summary:")
        print(f"  • Total Proposals: {report['summary']['total_proposals']}")
        print(f"  • Require Approval: {report['summary']['require_approval']}")
        print(f"  • Semantic Only: {report['summary']['semantic_only']}")
        
        if report['proposals']:
            print(f"\n📝 Proposals by Component:")
            for comp, tokens in report['summary']['by_component'].items():
                print(f"\n  {comp}:")
                for token in tokens:
                    proposal = next(p for p in report['proposals'] if p['path'] == token)
                    approval_badge = "⚠️ " if proposal['requires_design_lead_approval'] else "✓ "
                    print(f"    {approval_badge} {token}")
        else:
            print("\n✅ No missing tokens detected!")
        
        print("\n" + "="*80 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Token Generator Agent")
    parser.add_argument("--components", nargs="+", help="Specific components to analyze")
    parser.add_argument("--full", action="store_true", help="Analyze all components")
    parser.add_argument("--output", help="Output file for report")
    
    args = parser.parse_args()
    
    generator = TokenGenerator()
    proposals = generator.analyze_components(args.components)
    
    generator.print_report()
    
    if args.output:
        output_file = generator.save_report(args.output)
        print(f"📁 Report saved to: {output_file}")
    else:
        output_file = generator.save_report()
        print(f"📁 Report saved to: {output_file}")
    
    # Exit with appropriate code
    approval_needed = sum(1 for p in proposals if p["requires_design_lead_approval"])
    if approval_needed > 0:
        print(f"\n⚠️  {approval_needed} proposal(s) require Design Lead approval")
        sys.exit(1)
    else:
        sys.exit(0 if proposals else 0)


if __name__ == "__main__":
    main()
