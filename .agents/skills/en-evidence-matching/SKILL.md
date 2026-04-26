---
name: en-evidence-matching
description: "Run EN step 3 evidence matching using workspace cards -> workspace claim registry -> workspace profile priority."
---

# EN Evidence Matching

Run EN step 3 only.

## Execute

1. Read `en_resume/02_jd_analysis.md`.
2. Read `agents/en/EvidenceMatcher.md`.
3. Use sources in order:
   - `workspace/experience_cards/*.md`
   - `workspace/claims/claim_registry.yaml`
   - `workspace/profile/*.md`
   - legacy private seed fallback only: `data/experience_cards/*.md`, `data/experience_bullets/*.md`, `data/experience_bullets/claim_registry.yaml`
4. Write `en_resume/03_evidence_selection.md`.
5. Update step 3 status.
