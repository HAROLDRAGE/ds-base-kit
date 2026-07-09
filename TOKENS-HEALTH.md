# Token System Health Dashboard

**Generated:** [AUTO-GENERATED - Run `python scripts/governance/health-monitor.py`]  
**Status:** [HEALTHY | WARNING | CRITICAL]  
**Next Review:** [Date from script]

---

## Overall Status

**System Health:** [ICON] [STATUS]

This dashboard monitors the health of the Design Tokens Platform across multiple dimensions:
- **WCAG AA Compliance** — Contrast ratio validation
- **Metadata Completeness** — Required field coverage
- **Deprecation Lifecycle** — Policy compliance
- **Platform Coverage** — Multi-platform export status
- **Schema Validation** — Token definition integrity

---

## Key Metrics

### WCAG AA Compliance
- **Status:** [✅ PASS | ⚠️ WARNING | 🚨 CRITICAL]
- **Coverage:** [X]% ([X] compliant / [X] total)
- **Target:** 100%

**Details:**
- Color tokens with valid contrast ratios: [X]/[X]
- Tokens meeting WCAG AA minimum (4.5:1): [X]
- Violations found: [X]

**Action Items (if any):**
- [ ] Review color tokens with contrast <4.5:1
- [ ] Update contrast ratios in token metadata
- [ ] Re-validate after changes

---

### Metadata Completeness
- **Status:** [✅ PASS | ⚠️ WARNING | 🚨 CRITICAL]
- **Coverage:** [X]% ([X] complete / [X] total)
- **Target:** 100%

**Required Fields:**
- element, attribute, purpose, category
- wcag_level, brands, coverage

**Details:**
- Tokens with complete metadata: [X]/[X]
- Tokens with missing fields: [X]
- Most common missing field: [X]

**Action Items (if any):**
- [ ] Add missing metadata fields
- [ ] Update element/attribute mappings
- [ ] Document token purposes
- [ ] Verify brand coverage

---

### Deprecation Lifecycle
- **Status:** [✅ PASS | ⚠️ WARNING | 🚨 CRITICAL]
- **Deprecated Tokens:** [X]
- **Target:** No tokens overdue (>37 days)

**Details:**
- Active tokens: [X]
- Deprecated tokens: [X]
  - In PHASE 1 (Mark): [X]
  - In PHASE 2 (Alias): [X]
  - Overdue for PHASE 3 (Remove): [X]

**Timeline:**
| Token | Deprecated | Days | Phase | Removal Date |
|-------|-----------|------|-------|--------------|
| [Token] | [Date] | [N] | [Phase 1/2/3] | [Date] |

**Action Items (if any):**
- [ ] Review PHASE 2 candidates and create aliases
- [ ] Remove PHASE 3 overdue tokens
- [ ] Update consumidores for breaking changes
- [ ] Document migration path in release notes

---

### Platform Coverage
- **Status:** [✅ PASS | ⚠️ WARNING | 🚨 CRITICAL]
- **Minimum Coverage:** [X]%
- **Target:** 100%

**Coverage by Platform:**
| Platform | Covered | Total | % | Status |
|----------|---------|-------|---|--------|
| Web | [X] | [X] | [X]% | [✅/⚠️] |
| Tailwind | [X] | [X] | [X]% | [✅/⚠️] |
| iOS | [X] | [X] | [X]% | [✅/⚠️] |
| Android | [X] | [X] | [X]% | [✅/⚠️] |
| Storybook | [X] | [X] | [X]% | [✅/⚠️] |

**Coverage Gaps (if any):**
- Token: [Token Name]
  - Missing platforms: [List]
  - Impact: [High/Medium/Low]

**Action Items (if any):**
- [ ] Export missing tokens to all platforms
- [ ] Run Style Dictionary build for all platforms
- [ ] Validate exports in each platform's build directory
- [ ] Update test coverage

---

### Schema Validation
- **Status:** [✅ PASS | ⚠️ WARNING | 🚨 CRITICAL]
- **Valid Tokens:** [X]
- **Invalid Tokens:** [X]
- **Target:** 0 invalid

**Details:**
- Tokens passing schema validation: [X]/[X]
- Schema version: [X]
- Last validation: [Auto]

**Action Items (if any):**
- [ ] Fix invalid token definitions
- [ ] Run `npm run tokens:validate` to identify issues
- [ ] Update token structure to match schema
- [ ] Re-validate after fixes

---

## Recommendations

### Priority Actions
1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

### Sprint Planning
- **Immediate:** [Critical issues to fix this sprint]
- **High:** [Important improvements for next sprint]
- **Medium:** [Enhancements for planning ahead]
- **Low:** [Nice-to-have improvements]

### Trend Analysis
- WCAG compliance: [Improving ↗ | Stable → | Declining ↘]
- Metadata completeness: [Improving ↗ | Stable → | Declining ↘]
- Deprecation backlog: [Improving ↗ | Stable → | Declining ↘]
- Platform coverage: [Improving ↗ | Stable → | Declining ↘]

---

## How to Use This Report

### For Design Leads
- Check WCAG compliance and metadata completeness
- Review deprecation timeline
- Plan token updates based on recommendations

### For Engineers
- Check platform coverage and schema validation
- Plan build system updates
- Fix any validation errors

### For Project Managers
- Track project health trends
- Plan sprints based on action items
- Monitor deprecation timeline

### For QA
- Use recommendations to guide testing focus
- Validate platform-specific exports
- Check brand and theme coverage

---

## Next Steps

**Last Review:** [Auto]  
**Next Scheduled Review:** [Date - typically 7 days]  
**Review Frequency:** Weekly (or on-demand)

To manually generate this report:
```bash
python scripts/governance/health-monitor.py
```

To integrate into CI/CD:
```bash
npm run tokens:health
```

---

## Support & Questions

- **Design System:** #design-tokens Slack
- **GitHub Issues:** [link to issues]
- **Documentation:** [01-tokens/TOKENS-METADATA.md](../../01-tokens/TOKENS-METADATA.md)
- **Contact:** @design-team

---

*This report is auto-generated by TokenHealthMonitor. Last generated: [Auto]*
