# EN Evidence Selection Schema

`en_resume/03_evidence_selection.md` uses the following structure.

```markdown
# Evidence Selection: {Company} - {Role}

## Data Priority Confirmation
1. `workspace/experience_cards/*.md`
2. `workspace/claims/claim_registry.yaml`
3. `workspace/profile/*.md`
4. Optional local tone/reference context: `workspace/writing_samples/*.md`
5. Legacy private seed fallback only: `data/experience_cards/*.md`, `data/experience_bullets/*.md`, `data/experience_bullets/claim_registry.yaml`, `data/RESUME/snapshots/en/*.md`, `data/profile.md`

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
