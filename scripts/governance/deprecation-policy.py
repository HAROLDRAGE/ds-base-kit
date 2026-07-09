#!/usr/bin/env python3
"""
PHASE 4: Deprecation Lifecycle Policy Agent
Enforces 3-phase deprecation (mark → alias → remove) with timeline validation
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class DeprecationPolicyAgent:
    """
    Manages token deprecation lifecycle with 3 phases:
    
    PHASE 1 (Mark): Mark token as deprecated + add migration path (0 days)
    PHASE 2 (Alias): Create alias for backward compat (7 days minimum)
    PHASE 3 (Remove): Remove old token from build (30 days minimum)
    
    Total lifecycle: 37 days minimum before removal
    """
    
    DEPRECATION_CONFIG = {
        "phase_1_mark": {"delay_days": 0, "action": "Add deprecation metadata"},
        "phase_2_alias": {"delay_days": 7, "action": "Create alias for backward compat"},
        "phase_3_remove": {"delay_days": 30, "action": "Remove from build"},
    }
    
    def __init__(self, tokens_file: str = "01-tokens/tokens.dtcg.json"):
        self.tokens_file = Path(tokens_file)
        self.tokens = self._load_tokens()
        self.report = {
            "timestamp": datetime.now().isoformat(),
            "total_tokens": 0,
            "active_tokens": 0,
            "deprecated_tokens": [],
            "candidates_for_phase_2": [],
            "candidates_for_phase_3": [],
            "breaking_changes": [],
            "warnings": [],
            "recommendations": [],
        }
    
    def _load_tokens(self) -> Dict:
        """Load token definitions from DTCG file"""
        try:
            with open(self.tokens_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading tokens: {e}", file=sys.stderr)
            sys.exit(1)
    
    def analyze_deprecation_lifecycle(self) -> Dict:
        """Analyze all tokens for deprecation status"""
        
        self.report["total_tokens"] = len(self._flatten_tokens(self.tokens))
        
        for token_path, token in self._iter_tokens(self.tokens):
            if not token.get("$extensions"):
                continue
            
            metadata = token["$extensions"].get("metadata", {})
            deprecation = metadata.get("deprecation", {})
            
            if not deprecation or deprecation.get("status") == "active":
                self.report["active_tokens"] += 1
                continue
            
            # Token is deprecated - check lifecycle phase
            self._process_deprecated_token(token_path, token, deprecation)
        
        return self.report
    
    def _process_deprecated_token(self, token_path: str, token: Dict, deprecation: Dict):
        """Process deprecated token through lifecycle phases"""
        
        deprecated_date = deprecation.get("date", "")
        migration_path = deprecation.get("migration_path", "")
        reason = deprecation.get("reason", "Unknown")
        
        # Parse deprecation date
        try:
            dep_date = datetime.fromisoformat(deprecated_date)
        except ValueError:
            self.report["warnings"].append(
                f"⚠️  Invalid deprecation date for {token_path}: {deprecated_date}"
            )
            return
        
        # Calculate days since deprecation
        days_since = (datetime.now() - dep_date).days
        
        # Determine current phase
        self.report["deprecated_tokens"].append({
            "token": token_path,
            "reason": reason,
            "deprecated_date": deprecated_date,
            "days_since_deprecation": days_since,
            "migration_path": migration_path,
            "current_phase": self._determine_phase(days_since),
            "next_phase": self._get_next_phase(days_since),
            "removal_date": (dep_date + timedelta(days=37)).isoformat()[:10],
        })
        
        # Check readiness for phase transitions
        if days_since >= 7 and days_since < 30:
            self.report["candidates_for_phase_2"].append({
                "token": token_path,
                "reason": reason,
                "migration_path": migration_path,
                "action": "Create alias for backward compatibility",
            })
        
        if days_since >= 30:
            self.report["candidates_for_phase_3"].append({
                "token": token_path,
                "reason": reason,
                "migration_path": migration_path,
                "action": "Remove from build (migration period complete)",
            })
            
            # Flag breaking change
            self.report["breaking_changes"].append({
                "token": token_path,
                "type": "token_removal",
                "migration_required": True,
                "migration_path": migration_path,
            })
    
    def _determine_phase(self, days_since: int) -> str:
        """Determine deprecation phase based on time elapsed"""
        if days_since < 7:
            return "PHASE 1 (Mark)"
        elif days_since < 30:
            return "PHASE 2 (Alias)"
        else:
            return "PHASE 3 (Ready for Removal)"
    
    def _get_next_phase(self, days_since: int) -> str:
        """Get next phase and timeline"""
        if days_since < 7:
            days_left = 7 - days_since
            return f"PHASE 2 in {days_left} day(s)"
        elif days_since < 30:
            days_left = 30 - days_since
            return f"PHASE 3 in {days_left} day(s)"
        else:
            return "Ready for removal"
    
    def _flatten_tokens(self, tokens: Dict, prefix: str = "") -> List[Tuple[str, Dict]]:
        """Flatten nested token structure"""
        result = []
        for key, value in tokens.items():
            if key.startswith("$"):
                continue
            
            path = f"{prefix}{key}" if prefix else key
            
            if isinstance(value, dict) and "$value" not in value:
                result.extend(self._flatten_tokens(value, f"{path}."))
            else:
                result.append((path, value))
        
        return result
    
    def _iter_tokens(self, tokens: Dict, prefix: str = ""):
        """Iterate through all tokens with their paths"""
        for key, value in tokens.items():
            if key.startswith("$"):
                continue
            
            path = f"{prefix}{key}" if prefix else key
            
            if isinstance(value, dict) and "$value" not in value:
                yield from self._iter_tokens(value, f"{path}.")
            else:
                yield (path, value)
    
    def validate_deprecation_compliance(self) -> bool:
        """Validate that deprecations follow policy"""
        valid = True
        
        for token_info in self.report["deprecated_tokens"]:
            token = token_info["token"]
            migration_path = token_info["migration_path"]
            
            # Warn if no migration path provided
            if not migration_path:
                self.report["warnings"].append(
                    f"⚠️  Token {token} deprecated but no migration_path specified"
                )
                valid = False
        
        return valid
    
    def generate_removal_checklist(self) -> List[Dict]:
        """Generate checklist for PHASE 3 (removal) tokens"""
        checklist = []
        
        for token_info in self.report["candidates_for_phase_3"]:
            token = token_info["token"]
            migration_path = token_info["migration_path"]
            
            checklist.append({
                "token": token,
                "migration_path": migration_path,
                "steps": [
                    f"1. Verify all consumidores migrated to {migration_path}",
                    f"2. Remove {token} from 01-tokens/tokens.dtcg.json",
                    f"3. Remove alias from tokens.aliases.json",
                    f"4. Update TOKENS-CHANGELOG.md (version bump)",
                    f"5. Run npm run tokens:build to verify no breakage",
                    f"6. Commit: 'chore: remove deprecated token {token} (v2.3.x)'",
                    f"7. Announce removal in release notes",
                ],
                "team_responsible": ["Engineering Owner", "Design Lead"],
            })
        
        return checklist
    
    def generate_markdown_report(self) -> str:
        """Generate human-readable Markdown report"""
        lines = [
            "# Token Deprecation Lifecycle Report",
            f"Generated: {self.report['timestamp'][:10]}",
            "",
            "## Summary",
            f"- Total Tokens: {self.report['total_tokens']}",
            f"- Active: {self.report['active_tokens']}",
            f"- Deprecated: {len(self.report['deprecated_tokens'])}",
            f"- Ready for Phase 2 (Alias): {len(self.report['candidates_for_phase_2'])}",
            f"- Ready for Phase 3 (Removal): {len(self.report['candidates_for_phase_3'])}",
            f"- Breaking Changes Pending: {len(self.report['breaking_changes'])}",
            "",
        ]
        
        if self.report["deprecated_tokens"]:
            lines.extend([
                "## Deprecated Tokens",
                "",
                "| Token | Reason | Days | Phase | Removal Date |",
                "|-------|--------|------|-------|--------------|",
            ])
            
            for token_info in self.report["deprecated_tokens"]:
                lines.append(
                    f"| {token_info['token']} | {token_info['reason'][:30]}... "
                    f"| {token_info['days_since_deprecation']} "
                    f"| {token_info['current_phase']} "
                    f"| {token_info['removal_date']} |"
                )
            
            lines.append("")
        
        if self.report["candidates_for_phase_2"]:
            lines.extend([
                "## Phase 2 Ready (Create Aliases)",
                "",
            ])
            for item in self.report["candidates_for_phase_2"]:
                lines.append(f"- **{item['token']}** → {item['migration_path']}")
            lines.append("")
        
        if self.report["candidates_for_phase_3"]:
            lines.extend([
                "## Phase 3 Ready (Remove from Build)",
                "",
            ])
            for item in self.report["candidates_for_phase_3"]:
                lines.append(f"- **{item['token']}** → {item['migration_path']}")
            lines.append("")
        
        if self.report["breaking_changes"]:
            lines.extend([
                "## ⚠️  Breaking Changes",
                "",
                "These tokens will be removed and require consumer migration:",
                "",
            ])
            for change in self.report["breaking_changes"]:
                lines.append(f"- {change['token']} → {change['migration_path']}")
            lines.append("")
        
        if self.report["warnings"]:
            lines.extend([
                "## ⚠️  Warnings",
                "",
            ])
            for warning in self.report["warnings"]:
                lines.append(f"- {warning}")
            lines.append("")
        
        return "\n".join(lines)
    
    def print_report(self):
        """Print human-readable report to stdout"""
        print(self.generate_markdown_report())
    
    def save_report(self, output_file: str = "logs/deprecation-lifecycle.json"):
        """Save JSON report to file"""
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"✅ Report saved to {output_file}")


if __name__ == "__main__":
    agent = DeprecationPolicyAgent()
    agent.analyze_deprecation_lifecycle()
    agent.validate_deprecation_compliance()
    agent.print_report()
    agent.save_report()
