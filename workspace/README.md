# workspace/ — normalized local knowledge base

The agent should transform raw `userinfo/` documents into structured local
working artifacts here.

Recommended public-safe structure:

- `profile/`: normalized user profile and career timeline.
- `experience_cards/`: reusable evidence cards grouped by real events.
- `claims/`: claim registry, metrics, and evidence provenance.
- `writing_samples/`: reusable tone/style examples extracted from prior essays.
- `feedback/`: post-submission outcomes and reusable weighting signals.
- `job_posts/`: normalized job descriptions and crawl/OCR results.

The contents are ignored by git because they are private to each user. Commit
only schema/templates or sanitized examples outside this directory.
