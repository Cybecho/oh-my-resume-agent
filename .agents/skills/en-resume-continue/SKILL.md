---
name: en-resume-continue
description: "Resume EN workflow by scanning output/*/state_en.json and continuing only unfinished core steps (1~7) or recover step 8 in-progress."
---

# EN Resume Continue

Resume interrupted EN resume workflow.

## Execute

1. Scan `output/*/state_en.json`.
   - If `state_version=1` or `steps.8` is missing, treat step 8 as `not_requested`.
2. Identify latest incomplete workflow.
3. Continue from the first incomplete EN core step:
   - 1: company research
   - 2: jd analysis
   - 3: evidence matching
   - 4: planning
   - 5: writing
   - 6: ats lint
   - 7: review
4. If step 1~7 are completed and step 8 is `in_progress`, resume step 8 publish recovery.
5. If step 1~7 are completed and step 8 is `not_requested|completed|blocked`, mark workflow as complete and suggest `/resume-publish` for optional document generation.
6. If no incomplete EN workflow exists, return summary and suggest new `/resume`.
