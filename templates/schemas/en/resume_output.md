# EN Resume Output Schema

`en_resume/05_resume/variant_{A|B|C}.md` uses the following structure.

```markdown
# {Name}
{Location} | {Phone} | {Email} | {LinkedIn}

## Professional Summary
{2-4 lines tailored to target role}

## Technical Skills
- Category: skills...

## Experience
### {Title}
{Company} | {Location} | {Start} - {End}
- {Action + Context + Result} <!-- experience_id:EXP-XX claim_ids:CLM-001,CLM-002 -->

## Projects
### {Project}
- {Action + Context + Result} <!-- experience_id:EXP-XX claim_ids:... -->

## Education
- {Degree, University, Date, GPA(optional)}

## Certifications / Community (Optional)
- ...

## Provenance Notes
- variant: A|B|C
- role_lens:
- used_experience_ids: []
- used_claim_ids: []
```
