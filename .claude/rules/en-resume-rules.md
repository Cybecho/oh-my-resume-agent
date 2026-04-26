# EN Resume Pipeline Rules

This rule file applies to EN resume workflow and must be used with existing common rules.

## Output and State

- EN artifacts must be stored under `output/{YYYYMMDD}_{company}/en_resume/`.
- EN state must be stored in `output/{YYYYMMDD}_{company}/state_en.json`.
- Do not modify KOR state file (`state.json`) for EN workflow.
- `state_en.json` uses `state_version: 2` and includes optional `steps.8` publish state.
- If legacy `state_version: 1` is found, augment `steps.8` in-memory and persist as `state_version: 2` on next write.

## Data Integrity Priority

1. `workspace/experience_cards/*.md` (fact SSOT)
2. `workspace/claims/claim_registry.yaml` (numeric truth)
3. `workspace/profile/*.md` (identity/profile SSOT)
4. `workspace/writing_samples/*.md` (tone/style reference when needed)
5. Legacy fallback for private seed only: `data/experience_cards/`, `data/experience_bullets/`, `data/RESUME/snapshots/en/`, `data/profile.md`

## Claim Rules

- Only `approved` claims are allowed in generated resume bullets.
- No new numeric statement is allowed without claim evidence.
- Every numeric bullet should be traceable via `claim_id`.

## ATS Hard-Fail Rules

- No image/table/multi-column dependencies.
- No header/footer-only contact info.
- No disallowed PII (age, marital status, religion, etc.).
- Required contact fields must exist.
- ATS pass is mandatory for optional publish step.

## Writing Rules

- Output language for resume artifacts is English.
- Use Action Verb + Context + Result bullet pattern.
- Avoid weak starters (`responsible for`, `duties included`).
- Default output is 3 variants (`A`, `B`, `C`).
- One-page is a guideline; do not hardcode line count constraints.

## Optional Step 8 Publish Rules

- Step 8 is manual-only and must run via `/resume-publish`.
- Step 8 source must be Step 7 `top_pick` variant only.
- Allowed step 8 targets: `docx`, `figma`.
- Publish gate requires:
  - ATS overall pass
  - `top_pick` exists
  - no effective `Mandatory Fixes`
- On gate failure, external artifacts must not be generated and step 8 status must be `blocked`.
- Step 8 outputs must be written under `en_resume/08_publish/`.
- DOCX must be generated locally from `docxtpl` template.
- Figma must use remote MCP endpoint (`https://mcp.figma.com/mcp`).
- `current_step` update rule:
  - Step 7 completed -> `current_step: 8`
  - Step 8 completed -> `current_step: 9`

## Company Research Fallback

- If web research is not available, generate a reduced company context from JD only.
- Mark fallback explicitly (`fallback_mode: true`) with reason.
