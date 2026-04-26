# Job intake fallback policy

Oh My Resume-Agent must never pretend a job posting was collected when crawling
failed.

## v0 behavior

1. Try the URL or user-provided JD text in Codex/Claude Code.
2. If URL access fails, stop and mark the job-intake step as blocked.
3. Ask the user to provide one of these fallbacks:
   - paste the full JD text into the chat,
   - save the posting with `Ctrl+P` as a PDF and place it in `userinfo/job_posts/`,
   - save screenshots or images in `userinfo/job_posts/` for later OCR-supported versions.

## Not supported in v0

- guaranteed crawling for every Korean recruiting site,
- OCR for image-only postings,
- HWP/PPTX/Excel/Notion ingestion automation,
- guessing JD requirements from company name alone.
