---
name: en-resume-publish
description: "Run EN optional step 8 publish: convert top-picked markdown resume into local DOCX + Figma (remote MCP)."
---

# EN Resume Publish (Optional Step 8)

Run optional EN step 8 only.

## Inputs

- `targets` (optional): `docx`, `figma` (default: `docx,figma`)
- `session` (optional): specific `output/{YYYYMMDD}_{company}` path
- `force` (optional, default false): gate override is not recommended

## Prerequisites

- Python dependency: `docxtpl` installed (see `requirements/en_resume_publish.txt`).
- Figma must be connected via remote MCP (`https://mcp.figma.com/mcp`).

## Execute

1. Run prepare phase (shared script):
   - `python3 scripts/en_resume_publish.py prepare --targets <docx,figma> [--session <path>] [--force]`
2. Prepare phase responsibilities:
   - Resolve session (explicit `--session` or latest step-7-completed run).
   - Upgrade legacy state (`state_version:1` -> `2`) and ensure `steps.8`.
   - Validate gate: ATS pass, `top_pick` exists, mandatory fixes clear.
   - Generate local DOCX via `docxtpl` using `config/en_resume_publish.json`.
   - Write `08_publish_report.md` + `publish_manifest.json`.
3. If `figma` target requested and prepare status is `in_progress`, run Figma MCP action.
4. Finalize phase:
   - `python3 scripts/en_resume_publish.py finalize [--session <path>] --figma-status <success|failed|skipped> [--figma-node-id <id>] [--figma-url <url>] [--figma-error <error>]`
5. Finalize updates:
   - Persist figma result in manifest/report.
   - all requested targets success -> step 8 `completed` and `current_step=9`
   - partial/any failure -> step 8 `blocked`

## Rules

- Step 8 is manual-only; do not auto-run from `/resume`.
- Source resume must be `top_pick` variant only.
- Keep KOR state untouched.
