# EN Publish Report Schema

`en_resume/08_publish/08_publish_report.md` uses the following structure.

```markdown
# Resume Publish Report: {Company} - {Role}

## Request
- session: output/{YYYYMMDD}_{company}
- requested_targets: [docx|figma...]
- source_variant: A|B|C
- force: false

## Gate Check
- ats_pass: true|false
- has_top_pick: true|false
- mandatory_fixes_clear: true|false
- gate_passed: true|false
- gate_blocking_reasons:
  1. ...

## Target Results
| Target | Status | Artifact | Identifier | Link | Error |
|--------|--------|----------|------------|------|-------|
| docx | success\|failed\|skipped | file | filename | - | - |
| figma | success\|failed\|pending\|skipped | frame | frame_id | https://... | - |

## Manifest
- path: en_resume/08_publish/publish_manifest.json

## State Update
- step_8_status: completed|blocked
- blocked_reason: null|...
- completed_at: ISO8601|null
```
