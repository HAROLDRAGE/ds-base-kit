#!/usr/bin/env python3
"""
Agent 3: Migration Assistant
Detects hardcoded values in codebase and suggests token replacements
Generates migration codemods and reports
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class MigrationAssistant:
    """Detect hardcoded values and suggest migrations to tokens"""
    
    def __init__(self, tokens_path="01-tokens/tokens.dtcg.json",
                 components_dir="02-componentes"):
        self.tokens_path = Path(tokens_path)
        self.components_dir = Path(components_dir)
        
        self.tokens = self._load_json(tokens_path)
        self.value_index = self._build_value_index()
        
        self.issues = []
        self.logger = self._setup_logger()
        
        # Patterns to detect
        self.patterns = {
            'hex_color': r'#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?',
            'rgb_color': r'rgb\([^)]+\)',
            'px_value': r'(\d+)px',
            'ms_value': r'(\d+)ms',
            'percentage': r'(\d+)%',
        }
    
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
        log_file = log_dir / f"token-migrate-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        return {"file": log_file, "entries": []}
    
    def _build_value_index(self):
        """Index tokens by their values for quick lookup"""
        index = defaultdict(list)
        
        for token_name, token_data in self._flatten_tokens(self.tokens).items():
            value = token_data.get("$value")
            if value:
                # Normalize value for comparison
                normalized = self._normalize_value(value)
                index[normalized].append({
                    "name": token_name,
                    "value": value,
                    "category": token_data.get("$extensions", {}).get("metadata", {}).get("category", "unknown")
                })
        
        return index
    
    def _normalize_value(self, value):
        """Normalize value for comparison"""
        if isinstance(value, str):
            value = value.lower().strip()
            # Normalize hex colors
            if value.startswith("#"):
                value = value.upper()
        return value
    
    def scan_components(self):
        """Scan all component files for hardcoded values"""
        for component_file in self.components_dir.glob("*.md"):
            self._scan_file(component_file)
        
        return self.issues
    
    def _scan_file(self, file_path):
        """Scan single file for hardcoded values"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Skip comments and documentation
                if line.strip().startswith('#') or line.strip().startswith('//'):
                    continue
                
                # Check for CSS/HTML/JavaScript content
                if any(marker in line for marker in ['<', '>', '{', '}', 'color', 'padding', 'margin', 'px', 'ms']):
                    self._scan_line(file_path, line_num, line)
        
        except Exception as e:
            print(f"⚠️  Error scanning {file_path}: {e}", file=sys.stderr)
    
    def _scan_line(self, file_path, line_num, line):
        """Scan single line for hardcoded values"""
        
        # Detect hex colors
        for match in re.finditer(self.patterns['hex_color'], line):
            hex_val = match.group(0).upper()
            tokens = self.value_index.get(self._normalize_value(hex_val), [])
            
            if tokens:
                self._add_issue(
                    file_path=file_path,
                    line_num=line_num,
                    match_text=hex_val,
                    match_type="color",
                    suggestions=tokens,
                    context=line.strip()
                )
        
        # Detect px values
        for match in re.finditer(self.patterns['px_value'], line):
            px_val = int(match.group(1))
            px_str = f"{px_val}px"
            
            # Look for spacing/dimension tokens
            tokens = self._find_spacing_tokens(px_val)
            
            if tokens:
                self._add_issue(
                    file_path=file_path,
                    line_num=line_num,
                    match_text=px_str,
                    match_type="spacing",
                    suggestions=tokens,
                    context=line.strip()
                )
        
        # Detect ms values
        for match in re.finditer(self.patterns['ms_value'], line):
            ms_val = int(match.group(1))
            ms_str = f"{ms_val}ms"
            
            # Look for duration tokens
            tokens = self._find_duration_tokens(ms_val)
            
            if tokens:
                self._add_issue(
                    file_path=file_path,
                    line_num=line_num,
                    match_text=ms_str,
                    match_type="duration",
                    suggestions=tokens,
                    context=line.strip()
                )
    
    def _find_spacing_tokens(self, px_val):
        """Find spacing tokens matching pixel value"""
        matches = []
        
        # Check standard token naming patterns
        for token_name, token_data in self._flatten_tokens(self.tokens).items():
            value = token_data.get("$value")
            
            # Match px values
            if isinstance(value, str) and value.endswith("px"):
                try:
                    token_px = int(value[:-2])
                    if token_px == px_val:
                        matches.append({
                            "name": token_name,
                            "value": value,
                            "category": token_data.get("$extensions", {}).get("metadata", {}).get("category", "spacing")
                        })
                except (ValueError, IndexError):
                    pass
        
        return matches
    
    def _find_duration_tokens(self, ms_val):
        """Find duration tokens matching millisecond value"""
        matches = []
        
        for token_name, token_data in self._flatten_tokens(self.tokens).items():
            value = token_data.get("$value")
            
            # Match ms values
            if isinstance(value, str) and value.endswith("ms"):
                try:
                    token_ms = int(value[:-2])
                    if token_ms == ms_val:
                        matches.append({
                            "name": token_name,
                            "value": value,
                            "category": token_data.get("$extensions", {}).get("metadata", {}).get("category", "motion")
                        })
                except (ValueError, IndexError):
                    pass
        
        return matches
    
    def _add_issue(self, file_path, line_num, match_text, match_type, suggestions, context):
        """Add issue to issues list"""
        issue = {
            "file": str(file_path),
            "line": line_num,
            "match": match_text,
            "type": match_type,
            "context": context,
            "suggestions": suggestions,
            "codemod": self._generate_codemod(match_text, suggestions[0] if suggestions else None)
        }
        
        self.issues.append(issue)
        self.logger["entries"].append(issue)
    
    def _generate_codemod(self, original_value, suggested_token=None):
        """Generate codemod to replace hardcoded value"""
        if not suggested_token:
            return None
        
        token_name = suggested_token["name"]
        token_var = self._to_css_var_format(token_name)
        
        return {
            "from": original_value,
            "to": token_var,
            "type": "codemod"
        }
    
    def _to_css_var_format(self, token_name):
        """Convert token name to CSS variable format"""
        # Convert semantic.color.action.primary → --color-action-primary
        parts = token_name.split('.')
        var_name = "--" + "-".join(parts[1:]) if len(parts) > 1 else "--" + token_name
        return f"var({var_name})"
    
    def _flatten_tokens(self, tokens_dict, parent_key=""):
        """Flatten nested token dict"""
        items = {}
        for k, v in tokens_dict.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            
            if isinstance(v, dict):
                if "$value" in v:
                    items[new_key] = v
                else:
                    items.update(self._flatten_tokens(v, new_key))
        
        return items
    
    def generate_report(self):
        """Generate comprehensive migration report"""
        return {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "issues_count": len(self.issues),
            "issues": self.issues,
            "summary": {
                "total_hardcoded": len(self.issues),
                "by_type": self._group_by_type(),
                "by_file": self._group_by_file(),
                "migration_effort": self._estimate_effort()
            }
        }
    
    def _group_by_type(self):
        """Group issues by type"""
        grouped = defaultdict(int)
        for issue in self.issues:
            grouped[issue["type"]] += 1
        return dict(grouped)
    
    def _group_by_file(self):
        """Group issues by file"""
        grouped = defaultdict(int)
        for issue in self.issues:
            grouped[issue["file"]] += 1
        return dict(grouped)
    
    def _estimate_effort(self):
        """Estimate migration effort"""
        return {
            "issues": len(self.issues),
            "files_affected": len(self._group_by_file()),
            "estimated_hours": max(0.5, len(self.issues) * 0.05),
            "codemods_available": sum(1 for i in self.issues if i.get("codemod"))
        }
    
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
        print("🤖 MIGRATION ASSISTANT AGENT — ANALYSIS REPORT")
        print("="*80)
        print(f"\n📊 Summary:")
        print(f"  • Total Hardcoded Values: {report['summary']['total_hardcoded']}")
        print(f"  • Files Affected: {report['summary']['by_file'] | len}")
        print(f"  • Estimated Effort: {report['summary']['migration_effort']['estimated_hours']:.1f} hours")
        print(f"  • Codemods Available: {report['summary']['migration_effort']['codemods_available']}")
        
        if report['summary']['by_type']:
            print(f"\n📈 Issues by Type:")
            for issue_type, count in report['summary']['by_type'].items():
                print(f"  • {issue_type}: {count}")
        
        if self.issues:
            print(f"\n⚠️  Issues by File:")
            for file_name, count in report['summary']['by_file'].items():
                print(f"  • {file_name}: {count}")
            
            print(f"\n📝 Top 10 Issues:")
            for i, issue in enumerate(self.issues[:10], 1):
                print(f"\n  {i}. {issue['file']}:{issue['line']}")
                print(f"     Found: {issue['match']}")
                if issue.get('suggestions'):
                    print(f"     → Suggest: {issue['suggestions'][0]['name']}")
        else:
            print("\n✅ No hardcoded values detected!")
        
        print("\n" + "="*80 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration Assistant Agent")
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument("--full", action="store_true", help="Full analysis")
    
    args = parser.parse_args()
    
    assistant = MigrationAssistant()
    issues = assistant.scan_components()
    
    assistant.print_report()
    
    if args.output:
        output_file = assistant.save_report(args.output)
        print(f"📁 Report saved to: {output_file}")
    else:
        output_file = assistant.save_report()
        print(f"📁 Report saved to: {output_file}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
