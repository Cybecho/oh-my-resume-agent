# v0 release gates

Public release requires all hard gates to pass before any weighted score is
considered.

## Hard gates

- `omr eval privacy` passes with no tracked private paths or obvious PII.
- `omr doctor` can run from a clean clone and explain missing user data.
- `omr init`, `omr status`, and `omr paths` work without network access.
- Codex and Claude Code execution paths are documented.
- Unsupported v0 features are explicitly listed.
- Job-post URL failure fallback is documented.

## Weighted score

Use `plan/03_evaluation_metrics.md` as the source of truth. v0 release requires:

```text
All hard gates pass
AND weighted score >= 85 / 100
```
