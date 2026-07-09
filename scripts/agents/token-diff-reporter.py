#!/usr/bin/env python3
"""
Agent 4: Token Diff Reporter
Generates comprehensive changelog and breaking change detection
Compares token versions and generates release notes
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class TokenDiffReporter:
    """Generate diff reports between token versions"""
    
    def __init__(self, new_tokens_path="01-tokens/tokens.dtcg.json",
                 old_tokens_path="01-tokens/tokens.dtcg.json.backup"):
        self.new_tokens_path = Path(new_tokens_path)
        self.old_tokens_path = Path(old_tokens_path)
        
        self.new_tokens = self._load_json(new_tokens_path)
        self.old_tokens = self._load_json(old_tokens_path)
        
        self.old_index = self._index_tokens(self.old_tokens)
        self.new_index = self._index_tokens(self.new_tokens)
        
        self.diff = self._calculate_diff()
        self.logger = self._setup_logger()
    
    def _load_json(self, path):
        """Load JSON file safely"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            # If old tokens don't exist, return empty
            if "backup" in str(path):
                return {}
            print(f"❌ Error loading {path}: {e}", file=sys.stderr)
            return {}
    
    def _setup_logger(self):
        """Setup logging infrastructure"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"token-diff-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        return {"file": log_file, "entries": []}
    
    def _index_tokens(self, tokens_dict, parent_key=""):
        """Index tokens with full metadata"""
        items = {}
        for k, v in tokens_dict.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            
            if isinstance(v, dict):
                if "$value" in v:
                    items[new_key] = {
                        "value": v.get("$value"),
                        "type": v.get("$type", "unknown"),
                        "extensions": v.get("$extensions", {}),
                        "metadata": v.get("$extensions", {}).get("metadata", {})
                    }
                else:
                    items.update(self._index_tokens(v, new_key))
        
        return items
    
    def _calculate_diff(self):
        """Calculate differences between token versions"""
        old_keys = set(self.old_index.keys())
        new_keys = set(self.new_index.keys())
        
        added = new_keys - old_keys
        removed = old_keys - new_keys
        common = old_keys & new_keys
        
        # Find modified tokens
        modified = {}
        for token_name in common:
            old_token = self.old_index[token_name]
            new_token = self.new_index[token_name]
            
            # Check if value changed
            if old_token["value"] != new_token["value"]:
                modified[token_name] = {
                    "old": old_token,
                    "new": new_token,
                    "reason": "value_change"
                }
            # Check if metadata changed
            elif old_token["metadata"] != new_token["metadata"]:
                modified[token_name] = {
                    "old": old_token,
                    "new": new_token,
                    "reason": "metadata_change"
                }
        
        # Find deprecated tokens
        deprecated = {}
        for token_name in new_keys:
            metadata = self.new_index[token_name].get("metadata", {})
            if metadata.get("deprecated", False):
                deprecated[token_name] = {
                    "deprecation_reason": metadata.get("deprecation_reason", "Unknown"),
                    "replacement": metadata.get("replacement"),
                    "removal_version": metadata.get("removal_version")
                }
        
        return {
            "added": sorted(added),
            "removed": sorted(removed),
            "modified": modified,
            "deprecated": deprecated,
            "summary": self._generate_summary(added, removed, modified, deprecated)
        }
    
    def _generate_summary(self, added, removed, modified, deprecated):
        """Generate summary statistics"""
        return {
            "total_tokens": len(self.new_index),
            "added_count": len(added),
            "removed_count": len(removed),
            "modified_count": len(modified),
            "deprecated_count": len(deprecated),
            "has_breaking_changes": len(removed) > 0 or any(
                r.get("metadata", {}).get("removal_version") for r in self.new_index.values()
            ),
            "change_summary": f"↑ {len(added)} → {len(removed)} ≈ {len(modified)} ⚠️ {len(deprecated)}"
        }
    
    def generate_markdown_report(self, title="Token Changes"):
        """Generate markdown changelog"""
        md = f"# {title}\n\n"
        md += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Summary
        summary = self.diff["summary"]
        md += "## Summary\n\n"
        md += f"- **Total Tokens:** {summary['total_tokens']}\n"
        md += f"- **Added:** {summary['added_count']}\n"
        md += f"- **Removed:** {summary['removed_count']}\n"
        md += f"- **Modified:** {summary['modified_count']}\n"
        md += f"- **Deprecated:** {summary['deprecated_count']}\n"
        
        if summary["has_breaking_changes"]:
            md += "\n⚠️ **BREAKING CHANGES DETECTED** — See deprecation section below\n"
        
        md += "\n---\n\n"
        
        # Added
        if self.diff["added"]:
            md += f"## ✅ Added Tokens ({len(self.diff['added'])})\n\n"
            md += "```\n"
            for token_name in self.diff["added"]:
                token_data = self.new_index[token_name]
                md += f"{token_name} = {token_data['value']}\n"
            md += "```\n\n"
        
        # Modified
        if self.diff["modified"]:
            md += f"## 🔄 Modified Tokens ({len(self.diff['modified'])})\n\n"
            for token_name, change in self.diff["modified"].items():
                old_val = change["old"]["value"]
                new_val = change["new"]["value"]
                reason = change["reason"]
                md += f"- `{token_name}`: `{old_val}` → `{new_val}` ({reason})\n"
            md += "\n"
        
        # Deprecated
        if self.diff["deprecated"]:
            md += f"## ⚠️ Deprecated Tokens ({len(self.diff['deprecated'])})\n\n"
            md += "The following tokens are deprecated and will be removed in future versions:\n\n"
            for token_name, deprecation in self.diff["deprecated"].items():
                replacement = deprecation.get("replacement", "N/A")
                removal_version = deprecation.get("removal_version", "Next major")
                reason = deprecation.get("deprecation_reason", "No reason provided")
                md += f"- **`{token_name}`**\n"
                md += f"  - Reason: {reason}\n"
                md += f"  - Replacement: `{replacement}`\n"
                md += f"  - Removal: {removal_version}\n"
                md += f"  - **Action:** Migrate to `{replacement}` before upgrade\n\n"
        
        # Removed
        if self.diff["removed"]:
            md += f"## ❌ Removed Tokens ({len(self.diff['removed'])})\n\n"
            md += "```\n"
            for token_name in self.diff["removed"]:
                md += f"{token_name}\n"
            md += "```\n\n"
        
        md += "---\n\n"
        md += "## Migration Guide\n\n"
        
        if self.diff["deprecated"]:
            md += "### Deprecated Tokens\n\n"
            md += "Update your code to use the recommended replacements:\n\n"
            for token_name, deprecation in self.diff["deprecated"].items():
                replacement = deprecation.get("replacement", "N/A")
                md += f"- `{token_name}` → `{replacement}`\n"
            md += "\n"
        
        if self.diff["removed"] and not self.diff["deprecated"]:
            md += "### Removed Tokens\n\n"
            md += "These tokens have been permanently removed. Update your code accordingly:\n\n"
            for token_name in self.diff["removed"]:
                md += f"- ❌ `{token_name}`\n"
            md += "\n"
        
        md += "**Note:** All changes respect semantic versioning. Major version bumps indicate breaking changes.\n"
        
        return md
    
    def generate_json_report(self):
        """Generate JSON report"""
        return {
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "diff": self.diff,
            "summary": self.diff["summary"]
        }
    
    def save_json_report(self, output_file=None):
        """Save JSON report to file"""
        if output_file is None:
            output_file = self.logger["file"]
        
        report = self.generate_json_report()
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return output_file
    
    def save_markdown_report(self, output_file="TOKENS-CHANGELOG.md"):
        """Save markdown report to file"""
        output_file = Path(output_file)
        
        markdown = self.generate_markdown_report("Token Platform Changelog")
        
        with open(output_file, 'w') as f:
            f.write(markdown)
        
        return output_file
    
    def print_report(self):
        """Print human-readable report"""
        summary = self.diff["summary"]
        
        print("\n" + "="*80)
        print("🤖 TOKEN DIFF REPORTER AGENT — CHANGE REPORT")
        print("="*80)
        print(f"\n📊 Summary:")
        print(f"  • Total Tokens: {summary['total_tokens']}")
        print(f"  • Added: {summary['added_count']}")
        print(f"  • Removed: {summary['removed_count']}")
        print(f"  • Modified: {summary['modified_count']}")
        print(f"  • Deprecated: {summary['deprecated_count']}")
        
        if summary["has_breaking_changes"]:
            print(f"\n⚠️  BREAKING CHANGES DETECTED")
        
        if self.diff["added"]:
            print(f"\n✅ Added ({len(self.diff['added'])}):")
            for token_name in self.diff["added"][:5]:
                token_data = self.new_index[token_name]
                print(f"  + {token_name} = {token_data['value']}")
            if len(self.diff["added"]) > 5:
                print(f"  ... and {len(self.diff['added']) - 5} more")
        
        if self.diff["modified"]:
            print(f"\n🔄 Modified ({len(self.diff['modified'])}):")
            for token_name, change in list(self.diff["modified"].items())[:5]:
                old_val = change["old"]["value"]
                new_val = change["new"]["value"]
                print(f"  ~ {token_name}: {old_val} → {new_val}")
            if len(self.diff["modified"]) > 5:
                print(f"  ... and {len(self.diff['modified']) - 5} more")
        
        if self.diff["deprecated"]:
            print(f"\n⚠️  Deprecated ({len(self.diff['deprecated'])}):")
            for token_name, deprecation in list(self.diff["deprecated"].items())[:5]:
                replacement = deprecation.get("replacement", "N/A")
                print(f"  ⚠️  {token_name} → {replacement}")
            if len(self.diff["deprecated"]) > 5:
                print(f"  ... and {len(self.diff['deprecated']) - 5} more")
        
        if self.diff["removed"]:
            print(f"\n❌ Removed ({len(self.diff['removed'])}):")
            for token_name in self.diff["removed"][:5]:
                print(f"  - {token_name}")
            if len(self.diff["removed"]) > 5:
                print(f"  ... and {len(self.diff['removed']) - 5} more")
        
        print("\n" + "="*80 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Token Diff Reporter Agent")
    parser.add_argument("--json", help="Output JSON file for report")
    parser.add_argument("--markdown", help="Output markdown file for changelog")
    parser.add_argument("--full", action="store_true", help="Full analysis")
    
    args = parser.parse_args()
    
    reporter = TokenDiffReporter()
    reporter.print_report()
    
    if args.json:
        json_file = reporter.save_json_report(args.json)
        print(f"📁 JSON report saved to: {json_file}")
    else:
        json_file = reporter.save_json_report()
        print(f"📁 JSON report saved to: {json_file}")
    
    if args.markdown:
        md_file = reporter.save_markdown_report(args.markdown)
        print(f"📋 Changelog saved to: {md_file}")
    else:
        md_file = reporter.save_markdown_report()
        print(f"📋 Changelog saved to: {md_file}")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
