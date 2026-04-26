# EN ATS Report Schema

`en_resume/06_ats_report.md` uses the following structure.

```markdown
# ATS Report: {Company} - {Role}

## Target
- variants_checked: [A, B, C]
- hard_fail_gate: all variants must pass

## Hard Fail Checks
| Check | Variant A | Variant B | Variant C | Notes |
|-------|-----------|-----------|-----------|-------|
| No image/table/multi-column layout dependency | pass/fail | pass/fail | pass/fail | |
| No header/footer-only contact info | pass/fail | pass/fail | pass/fail | |
| No disallowed PII | pass/fail | pass/fail | pass/fail | |
| No unsupported numeric claim | pass/fail | pass/fail | pass/fail | |
| Required contact fields present | pass/fail | pass/fail | pass/fail | |

## Score Checks
| Metric | A | B | C | Target |
|--------|---|---|---|--------|
| Must keyword coverage | | | | >= 70% |
| Action-verb opening ratio | | | | >= 80% |
| Weak phrase frequency | | | | as low as possible |
| Bullet length fitness | | | | in range |
| Date/format consistency | | | | consistent |
| Variant differentiation | | | | meaningful |

## Result
- overall_status: pass|fail
- failed_variants: []
- required_fixes:
  1. ...
```
