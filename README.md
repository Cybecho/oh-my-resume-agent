# oh-my-resume-agent (자소서 선생)

지원서 작성도 혼자 하지 않는다. Oh My Resume-Agent는 Codex와 Claude Code 위에서 한국어 자기소개서와 영문 Resume 생성을 더 안전하게 수행하도록 돕는 local-first agent harness입니다.

This is a local-first application-document agent harness for Codex and Claude Code. It prepares user data, checks readiness, documents fallbacks, and then lets the existing agent/skill pipelines generate Korean self-introductions and English resume drafts from grounded evidence.

## v0 scope

v0 is a public template release, not a full document parser or standalone AI writer.

- `omr` / `resume`: setup, status, paths, doctor, and release-gate checks.
- `userinfo/`: private raw source documents from each user.
- `workspace/`: normalized local knowledge base generated from user sources.
- Codex + Claude Code: actual KOR/EN drafting pipelines.
- Explicit fallback: if a job-post URL cannot be crawled, paste the JD or save it as PDF into `userinfo/job_posts/`.

Not supported in v0: complete PDF/DOCX/HWP/PPTX/Excel/Notion ingestion, OCR for image-only job posts, guaranteed crawling for every recruiting site, direct LLM generation inside the `resume` CLI, and DOCX/Figma publish completion.

## Quickstart — Korean

```bash
git clone https://github.com/Cybecho/oh-my-resume-agent.git
cd oh-my-resume-agent
npm install
npm link
resume setup
resume doctor
```

Alternative install checks:

```bash
npx --yes --package github:Cybecho/oh-my-resume-agent resume doctor
curl -L https://raw.githubusercontent.com/Cybecho/oh-my-resume-agent/main/README.md
```

For a global shell command on macOS/Linux, either use `npm link` from the clone or ensure your npm global bin directory is on `PATH`:

```bash
npm bin -g
```

1. `userinfo/raw/`에 본인의 이력서, 기존 자기소개서, 경력기술서, 수상/자격 자료를 넣습니다.
2. 채용공고 크롤링이 실패할 수 있으므로 공고 전문, PDF, 스크린샷은 `userinfo/job_posts/`에 보관합니다.
3. `resume doctor`로 준비 상태를 확인합니다.
4. 실제 생성은 저장소 루트에서 Codex 또는 Claude Code를 실행한 뒤 아래 파이프라인을 호출합니다.

Codex:

- KOR: `self-intro-pipeline`
- EN: `en-resume-pipeline`

Claude Code:

- KOR: `/자소서`
- EN: `/resume`

## Quickstart — English

```bash
git clone https://github.com/Cybecho/oh-my-resume-agent.git
cd oh-my-resume-agent
npm install
npm link
omr setup
omr status
omr doctor
```

You can also run a one-off doctor check without installing globally:

```bash
npx --yes --package github:Cybecho/oh-my-resume-agent resume doctor
```

Place your private source files in `userinfo/raw/`. Place copied job descriptions, saved PDFs, or screenshots in `userinfo/job_posts/` when a URL cannot be accessed. The CLI does not generate resumes itself; it prepares and validates the local workspace so Codex or Claude Code can run the agent pipelines with evidence.

## CLI commands

`omr` is the canonical command and `resume` is an alias.

| Command | Purpose |
| --- | --- |
| `resume setup` | Text UI setup wizard for local folders, private source readiness, and job-post fallback readiness. |
| `resume init` | Create local user/workspace/state folders and placeholders. |
| `resume status` | Print private source counts, job-post fallback counts, workspace counts, and local state. |
| `resume doctor` | Check required folders/files and explain missing user data without pretending setup is complete. |
| `resume config` | Show what this CLI does and which KOR/EN agent pipelines to run. |
| `resume paths` | Print absolute paths for `userinfo`, `workspace`, `output`, and `.omr/state`. |
| `resume eval privacy` | Fail if tracked private paths or obvious PII patterns are found. |
| `resume eval skills` | Check Codex and Claude skill surfaces and document GitHub EN v0 unsupported status. |

## Directory model

```text
oh-my-resume-agent/
├── AGENTS.md                  # Codex rules
├── CLAUDE.md                  # Claude Code rules
├── bin/                       # omr/resume CLI entrypoints
├── docs/                      # release gates and fallback policy
├── userinfo/                  # private raw user inputs; gitignored below placeholders
│   ├── raw/
│   └── job_posts/
├── workspace/                 # normalized private working set; gitignored below placeholders
│   ├── profile/
│   ├── experience_cards/
│   ├── claims/
│   ├── writing_samples/
│   ├── feedback/
│   └── job_posts/
├── agents/                    # KOR/EN specialist agent instructions
├── .agents/skills/            # Codex skill surface
├── .claude/skills/            # Claude Code slash-command surface
├── templates/samples/         # synthetic public samples only
├── templates/schemas/         # pipeline output schemas
├── output/                    # generated outputs; gitignored below README
└── .omr/                      # local runtime state/logs; private state is gitignored
```

`data/` is kept only as a legacy compatibility boundary in the public template. Do not commit personal profiles, real experience cards, real claim registries, writing samples, or generated company outputs.

## Agent pipelines

KOR self-introduction pipeline:

```text
조사 → JD분석 → 의도분석 → 경험풀 → 경험매칭 → 기획 → 작성 → 검수
```

EN resume pipeline:

```text
company research → jd analysis → evidence matching → resume plan → resume write → ATS lint → review → optional publish
```

Core rules:

- Never invent experiences, metrics, awards, or outcomes not present in user evidence.
- Numeric claims must be traceable to approved evidence or an approved claim registry entry.
- Candidate claims are review candidates only and must not be used as final resume metrics.
- KOR and EN state files stay separate under `output/{YYYYMMDD}_{company}/`.
- If job-post collection fails, stop and request paste/PDF/screenshot fallback instead of guessing the JD.

## Public release gates

Before creating a public repository or publishing a package, run:

```bash
resume init
resume setup
resume doctor
resume eval privacy
resume eval skills
```

The full release policy is in `docs/release-gates.md` and `plan/03_evaluation_metrics.md`. v0 release requires all hard gates to pass and a weighted score of at least 85/100.

## Reference docs

- `plan/README.md`: deployment plan overview
- `plan/01_objective.md`: Objective
- `plan/02_model.md`: Model
- `plan/03_evaluation_metrics.md`: Evaluation metric
- `docs/job-intake-fallback.md`: URL/JD fallback policy
- `docs/release-gates.md`: v0 release hard gates

## GitHub/Copilot surface

The v0 GitHub surface mirrors the KOR pipeline only. EN Resume GitHub skills are explicitly unsupported in v0; use Codex (`en-resume-pipeline`) or Claude Code (`/resume`) for EN generation until the GitHub surface is deliberately mirrored.

## License

MIT
