# EN Evidence Selection Schema

`en_resume/03_evidence_selection.md` uses the following structure.

```markdown
# Evidence Selection: {Company} - {Role}

## Data Priority Confirmation
1. `data/experience_cards/*.md`
2. `data/experience_bullets/*.md`
3. `data/experience_bullets/claim_registry.yaml`
4. `data/RESUME/snapshots/en/*.md`
5. `data/profile.md`

## Candidate Evidence Pool
| Experience ID | Card Path | Bullet Path | Role Fit | Claim IDs | Notes |
|---------------|-----------|-------------|----------|-----------|-------|

## Claim Integrity Check
| Claim ID | Status (approved/candidate) | Used? | Evidence Paths |
|----------|-------------------------------|-------|----------------|

## Match Scoring
`match_score = 0.40*must_coverage + 0.20*nice_coverage + 0.15*claim_strength + 0.15*role_fit + 0.10*recency`

| Experience ID | must_coverage | nice_coverage | claim_strength | role_fit | recency | score |
|---------------|---------------|---------------|----------------|----------|---------|-------|

## Variant Evidence Selection

### Variant A (JD-dense)
- Primary experiences:
- Backup experiences:

### Variant B (impact-dense)
- Primary experiences:
- Backup experiences:

### Variant C (balanced)
- Primary experiences:
- Backup experiences:

## Gaps and Mitigation
- Gap:
- Mitigation (without fabrication):
```
