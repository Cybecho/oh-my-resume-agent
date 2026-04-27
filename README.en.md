<div align="center">
  <img src="image/Oh-My-Resume-Agent.png" alt="Oh My Resume-Agent" width="100%" />

  <p><a href="README.en.md">English</a> | <a href="README.md">한국어</a></p>
</div>

# oh-my-resume-agent

This is a local-first application-document agent harness for Codex and Claude Code. It prepares user data, checks readiness, documents fallbacks, and then lets the existing agent/skill pipelines generate Korean self-introductions and English resume drafts from grounded evidence.

## v0 scope

v0 is a public template release, not a full document parser or standalone AI writer.

- `omr` / `resume`: setup, status, paths, doctor, and release-gate checks.
- `userinfo/`: private raw source documents from each user.
- `workspace/`: normalized local knowledge base generated from user sources.
- Codex + Claude Code: actual KOR/EN drafting pipelines.
- Explicit fallback: if a job-post URL cannot be crawled, paste the JD or save it as PDF into `userinfo/job_posts/`.

Not supported in v0: complete PDF/DOCX/HWP/PPTX/Excel/Notion ingestion, OCR for image-only job posts, guaranteed crawling for every recruiting site, direct LLM generation inside the `resume` CLI, and DOCX/Figma publish completion.

## Quickstart

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
curl -L https://raw.githubusercontent.com/Cybecho/oh-my-resume-agent/main/README.en.md
```

For a global shell command on macOS/Linux, either use `npm link` from the clone or ensure your npm global bin directory is on `PATH`:

```bash
npm bin -g
```

Place your private resume, prior self-introductions, career documents, awards, and certificates in `userinfo/raw/`. Because job-post crawling can fail, keep the full JD text, PDFs, or screenshots in `userinfo/job_posts/`. Run `omr doctor` to check readiness, then run Codex or Claude Code from the repository root and call the relevant pipeline.

Codex:

- KOR: `self-intro-pipeline`
- EN: `en-resume-pipeline`

Claude Code:

- KOR: `/자소서`
- EN: `/resume`

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

## Current agent architecture and behavior

Oh My Resume-Agent is not a standalone AI app that generates application documents from a single `resume` command. It is an agent harness that safely connects **local user data → normalized evidence → agent pipelines → output review**. The core v0 design separates responsibilities: the CLI handles preparation and validation, while Codex/Claude Code skills and agents handle the actual writing.

### Design layers

```text
User input layer
  └─ userinfo/                 # raw resumes, self-introductions, career materials, job-post fallbacks

Normalized evidence layer
  └─ workspace/                # structured profile, experience cards, claims, writing samples

Control/validation layer
  └─ bin/omr, bin/resume       # folder setup, status checks, privacy gates, skill surface checks

Agent execution layer
  ├─ .agents/skills/           # Codex skill surface
  ├─ .claude/skills/           # Claude Code slash-command surface
  ├─ .github/skills/           # KOR mirror for GitHub/Copilot; EN unsupported in v0
  └─ agents/                   # step-specific specialist agent instructions

Output/state layer
  └─ output/                   # company-specific outputs and state.json/state_en.json
```

Each layer has a separate role. `userinfo/` is the raw input boundary, and `workspace/` is the normalized evidence store used for writing. `bin/omr` and `bin/resume` check whether these folders are ready, but they do not call an LLM directly. Actual generation runs through `.agents/skills/` or `.claude/skills/`, which read the step-specific instructions in `agents/` and operate on `workspace/` evidence.

### Detailed folder structure

```text
oh-my-resume-agent/
├── bin/
│   ├── omr                    # canonical CLI for setup/status/doctor/eval
│   └── resume                 # omr alias and easier entrypoint
├── userinfo/
│   ├── README.md              # raw source placement guide
│   ├── raw/                   # raw resumes, prior self-introductions, career docs, etc.
│   └── job_posts/             # pasted JD, PDF, screenshot fallback when crawling fails
├── workspace/
│   ├── README.md              # normalized data authoring guide
│   ├── profile/               # base profile and career timeline
│   ├── experience_cards/      # reusable experience cards; primary evidence for KOR/EN
│   ├── claims/                # claim_registry.yaml; only approved metrics/outcomes are final
│   ├── writing_samples/       # user writing samples
│   ├── job_posts/             # normalized job posts/JDs
│   └── feedback/              # post-submission feedback and future matching hints
├── agents/
│   ├── 조사선생.md             # company/job research
│   ├── JD분석선생.md           # JD requirement analysis
│   ├── 인사관선생.md           # hiring intent and prompt intent interpretation
│   ├── 기억선생.md             # experience candidate pooling and matching
│   ├── 기획선생.md             # answer concept and storyline planning
│   ├── 필체선생.md             # self-introduction draft writing
│   ├── 검수선생.md             # factuality, prompt-fit, and length review
│   └── en/                    # 8 EN Resume agents
├── .agents/skills/            # Codex execution skills such as self-intro-pipeline and en-resume-pipeline
├── .claude/
│   ├── rules/                 # shared KOR/EN pipeline rules
│   └── skills/                # Claude Code commands such as /자소서, /resume, /검수
├── .github/skills/            # KOR skill mirror for GitHub/Copilot; EN intentionally excluded in v0
├── templates/
│   ├── samples/               # public synthetic samples only; no real personal data
│   └── schemas/               # output schemas and review criteria for each step
├── docs/                      # fallback policy and release gate docs
├── plan/                      # Objective/Model/Evaluation/roadmap design docs
├── output/                    # company-specific generated outputs; only README is tracked
├── data/                      # legacy seed compatibility boundary; only README is kept in public repo
└── .omr/                      # local runtime state and logs; state/logs/plans are gitignored
```

### Runtime flow

1. **Initialize**: `resume setup` or `resume init` creates local folders such as `userinfo/`, `workspace/`, `output/`, and `.omr/state/`.
2. **Collect raw sources**: Users place resumes, prior self-introductions, and career materials in `userinfo/raw/`. Because job-post URLs can fail, full JD text, PDFs, or screenshots are kept in `userinfo/job_posts/`.
3. **Normalize evidence**: Raw sources are not used directly as final writing evidence. They are organized into structured files such as `workspace/profile/`, `workspace/experience_cards/`, `workspace/claims/`, and `workspace/writing_samples/`.
4. **Validate readiness**: `resume doctor` checks required folders/files and whether user data exists. `resume eval privacy` checks that private data or generated real outputs are not tracked in the public repo, and `resume eval skills` checks the Codex/Claude skill surfaces.
5. **Run pipelines**: Codex uses `self-intro-pipeline` or `en-resume-pipeline`; Claude Code uses `/자소서` or `/resume`. Skills read step instructions in `agents/` and shared rules in `.claude/rules/`.
6. **Record state**: The KOR self-introduction flow writes `output/{YYYYMMDD}_{company}/state.json`, and the EN Resume flow writes `output/{YYYYMMDD}_{company}/state_en.json`.
7. **Review and feedback**: Drafts are checked for factuality, claim approval, prompt fit, and length/ATS criteria. Post-submission feedback is stored in `workspace/feedback/` as hints for later matching and planning.

### KOR pipeline structure

```text
조사선생
  → JD분석선생
  → 인사관선생
  → 기억선생(경험풀/경험매칭)
  → 기획선생
  → 필체선생
  → 검수선생
```

The KOR pipeline starts with company/job research and JD analysis, then selects evidence from the user's experience cards for each prompt. It plans answer concepts, writes self-introduction drafts, and has the review agent check for unsupported claims or unapproved metrics.

### EN Resume pipeline structure

```text
CompanyResearcher
  → JDAnalyst
  → EvidenceMatcher
  → ResumeArchitect
  → ResumeWriter
  → ATSLinter
  → ResumeReviewer
  → ResumePublisher(optional)
```

The EN flow keeps its state separate from the KOR self-introduction flow. Core steps 1-7 cover company/JD analysis, evidence selection, resume architecture, variant writing, ATS linting, and final review. Step 8 publish is optional and runs separately through `/resume-publish`.

### Data and safety principles

- **No unsupported generation**: experiences, metrics, and outcomes absent from `workspace/experience_cards/` or approved `workspace/claims/claim_registry.yaml` are not written.
- **Workspace first**: active pipelines use `workspace/` as the primary evidence source. `data/` remains only as a legacy fallback boundary for older private seeds.
- **Public repository hygiene**: real contents under `userinfo/raw/`, `userinfo/job_posts/`, `workspace/`, `output/`, and `.omr/state/` are gitignored. The public repo contains only READMEs, `.gitkeep` files, schemas, and synthetic samples.
- **Explicit fallback**: if job-post crawling or document parsing fails, the system does not guess. It asks the user to add JD text, a PDF, or screenshots to `userinfo/job_posts/`.
- **CLI/writing separation**: the `resume` CLI only handles setup/status/doctor/eval. Actual LLM-based writing runs in the Codex or Claude Code agent runtime.

## License

MIT
