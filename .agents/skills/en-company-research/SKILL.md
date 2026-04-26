---
name: en-company-research
description: "Run EN step 1 only for company research and ATS keyword extraction with JD-only fallback."
---

# EN Company Research

Run EN step 1 only.

## Execute

1. Open `output/{YYYYMMDD}_{company}/state_en.json`.
2. Read `agents/en/CompanyResearcher.md`.
3. Produce `output/{YYYYMMDD}_{company}/en_resume/01_company_research.md`.
4. Update step 1 status in `state_en.json`.

## Rule

- If web research is unavailable, fallback to JD-only context and record `fallback_mode: true`.
