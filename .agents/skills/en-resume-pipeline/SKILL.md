---
name: en-resume-pipeline
description: "Run EN resume core pipeline (step 1~7) and prepare optional step 8 publish via /resume-publish."
---

# EN Resume Full Pipeline

Use this skill for full end-to-end EN resume generation.

## Inputs

- Company name
- Target role
- JD text
- Region (default: US)

## Initialize

1. Ensure `output/{YYYYMMDD}_{company}/en_resume/05_resume/` exists.
2. Create or refresh `output/{YYYYMMDD}_{company}/state_en.json`.
3. Set `state_version=2`, `variant_count=3`, `include_cover_letter=false`, `pipeline=en_resume`.
4. Ensure `steps.8` exists with:
   - `status: not_requested`
   - `optional: true`
   - `file: en_resume/08_publish/08_publish_report.md`
   - `targets: []`

## Execute

1. Read `agents/en/CompanyResearcher.md` and produce `01_company_research.md`.
2. Read `agents/en/JDAnalyst.md` and produce `02_jd_analysis.md`.
3. Read `agents/en/EvidenceMatcher.md` and produce `03_evidence_selection.md`.
4. Read `agents/en/ResumeArchitect.md` and produce `04_resume_plan.md`.
5. Read `agents/en/ResumeWriter.md` and produce variants A/B/C.
6. Read `agents/en/ATSLinter.md` and produce `06_ats_report.md`.
7. Read `agents/en/ResumeReviewer.md` and produce `07_review_report.md`.
8. Update state transitions in `state_en.json` per step.
9. Do not auto-run publish. Step 8 must be invoked manually via `/resume-publish` (`en-resume-publish` skill).
10. On step 7 completion, set `current_step=8`.

## Guardrails

- Do not update KOR `state.json`.
- Resolve EN evidence in this order: `workspace/experience_cards/*.md` -> `workspace/claims/claim_registry.yaml` -> `workspace/profile/*.md`; use `data/*` only as legacy private-seed fallback.
- Use approved claims only for numeric statements.
- Step 8 publish is optional/manual and must enforce ATS + review gate checks.
