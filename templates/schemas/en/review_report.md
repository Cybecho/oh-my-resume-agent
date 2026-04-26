# EN Review Report Schema

`en_resume/07_review_report.md` uses the following structure.

```markdown
# Resume Review Report: {Company} - {Role}

## 10-Criteria Evaluation
| # | Criterion | Variant A | Variant B | Variant C | Notes |
|---|-----------|-----------|-----------|-----------|-------|
| 1 | JD keyword coverage | 1-5 | 1-5 | 1-5 | |
| 2 | Claim integrity | 1-5 | 1-5 | 1-5 | |
| 3 | Bullet quality | 1-5 | 1-5 | 1-5 | |
| 4 | Page density/readability | 1-5 | 1-5 | 1-5 | |
| 5 | Section strategy fit | 1-5 | 1-5 | 1-5 | |
| 6 | Summary effectiveness | 1-5 | 1-5 | 1-5 | |
| 7 | ATS format compliance | 1-5 | 1-5 | 1-5 | |
| 8 | Variant differentiation | 1-5 | 1-5 | 1-5 | |
| 9 | Profile SSOT consistency | 1-5 | 1-5 | 1-5 | |
| 10 | Role-fit credibility | 1-5 | 1-5 | 1-5 | |

## Recommendation
- top_pick: A|B|C
- rationale:
  1. ...
  2. ...
  3. ...

## Mandatory Fixes
1. ...

## Suggested Improvements
1. ...

## Publish Gate Summary
- ats_pass: true|false
- has_top_pick: true|false
- mandatory_fixes_clear: true|false
- ready_to_publish: true|false
- selected_variant: A|B|C|null
- blocking_reasons:
  1. ...
```
