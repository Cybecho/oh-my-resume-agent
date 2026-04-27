![Oh-My-Resume-Agent](image/Oh-My-Resume-Agent.png)

# oh-my-resume-agent (자소서 선생)

[English README](README.en.md)

지원서 작성도 혼자 하지 않는다. Oh My Resume-Agent는 Codex와 Claude Code 위에서 한국어 자기소개서와 영문 Resume 생성을 더 안전하게 수행하도록 돕는 local-first agent harness입니다.

## v0 범위

v0는 공개 템플릿 릴리스이며, 완전한 문서 파서나 독립형 AI 작성 앱이 아닙니다.

- `omr`: setup, status, paths, doctor, release-gate 점검을 담당합니다. `resume`은 같은 CLI의 alias입니다.
- `userinfo/`: 사용자별 비공개 원본 문서가 들어가는 경계입니다.
- `workspace/`: 사용자 원천에서 정규화한 로컬 지식 베이스입니다.
- Codex + Claude Code: 실제 KOR/EN 작성 파이프라인을 실행합니다.
- 명시적 fallback: 채용공고 URL을 크롤링할 수 없으면 JD를 붙여넣거나 PDF로 저장해 `userinfo/job_posts/`에 둡니다.

v0에서 지원하지 않는 것: 완전한 PDF/DOCX/HWP/PPTX/Excel/Notion ingestion, 이미지 전용 채용공고 OCR, 모든 채용 사이트 크롤링 보장, `omr` CLI 내부의 직접 LLM 생성, DOCX/Figma publish 완료.

## 빠른 시작

```bash
git clone https://github.com/Cybecho/oh-my-resume-agent.git
cd oh-my-resume-agent
npm install
npm link
omr setup
omr doctor
```

대체 설치 점검:

```bash
npx --yes --package github:Cybecho/oh-my-resume-agent omr doctor
curl -L https://raw.githubusercontent.com/Cybecho/oh-my-resume-agent/main/README.md
```

macOS/Linux에서 전역 shell command로 쓰려면 clone한 저장소에서 `npm link`를 사용하거나 npm global bin 경로가 `PATH`에 잡혀 있는지 확인합니다.

```bash
npm bin -g
```

1. `userinfo/raw/`에 본인의 이력서, 기존 자기소개서, 경력기술서, 수상/자격 자료를 넣습니다.
2. 채용공고 크롤링이 실패할 수 있으므로 공고 전문, PDF, 스크린샷은 `userinfo/job_posts/`에 보관합니다.
3. `omr doctor`로 준비 상태를 확인합니다.
4. 실제 생성은 저장소 루트에서 Codex 또는 Claude Code를 실행한 뒤 아래 파이프라인을 호출합니다.

Codex:

- KOR: `self-intro-pipeline`
- EN: `en-resume-pipeline`

Claude Code:

- KOR: `/자소서`
- EN: `/resume`

## CLI 명령

`omr`이 canonical command이고, `resume`은 alias입니다.

| 명령 | 설명 |
| --- | --- |
| `omr setup` | 로컬 폴더, 비공개 원천 자료 준비, 채용공고 fallback 준비를 확인하는 텍스트 UI setup wizard입니다. |
| `omr init` | 로컬 user/workspace/state 폴더와 placeholder를 생성합니다. |
| `omr status` | 비공개 원천 수, 채용공고 fallback 수, workspace 수, 로컬 상태를 출력합니다. |
| `omr doctor` | 필수 폴더/파일을 점검하고, 누락된 사용자 데이터를 setup 완료로 가장하지 않고 설명합니다. |
| `omr config` | 이 CLI가 하는 일과 실행할 KOR/EN agent pipeline을 보여줍니다. |
| `omr paths` | `userinfo`, `workspace`, `output`, `.omr/state`의 절대 경로를 출력합니다. |
| `omr eval privacy` | 추적 중인 private path나 명백한 PII 패턴이 있으면 실패합니다. |
| `omr eval skills` | Codex/Claude skill surface를 점검하고 GitHub EN v0 미지원 상태를 문서화합니다. |

## 디렉터리 모델

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

`data/`는 공개 템플릿에서 legacy compatibility boundary로만 유지합니다. 개인 프로필, 실제 경험카드, 실제 claim registry, 문체 샘플, 회사별 생성 산출물은 commit하지 마세요.

## 에이전트 파이프라인

KOR 자기소개서 파이프라인:

```text
조사 → JD분석 → 의도분석 → 경험풀 → 경험매칭 → 기획 → 작성 → 검수
```

EN resume 파이프라인:

```text
company research → jd analysis → evidence matching → resume plan → resume write → ATS lint → review → optional publish
```

핵심 규칙:

- 사용자 근거에 없는 경험, 수치, 수상, 성과는 만들지 않습니다.
- 수치 claim은 승인된 근거 또는 승인된 claim registry entry로 추적 가능해야 합니다.
- candidate claim은 검토 후보일 뿐이며 최종 resume metric으로 쓰면 안 됩니다.
- KOR/EN state file은 `output/{YYYYMMDD}_{company}/` 아래에 분리해 둡니다.
- 채용공고 수집이 실패하면 JD를 추측하지 않고 paste/PDF/screenshot fallback을 요청합니다.

## 공개 릴리스 게이트

공개 저장소를 만들거나 package를 publish하기 전 아래를 실행합니다.

```bash
omr init
omr setup
omr doctor
omr eval privacy
omr eval skills
```

전체 release policy는 `docs/release-gates.md`와 `plan/03_evaluation_metrics.md`에 있습니다. v0 release는 모든 hard gate 통과와 85/100 이상의 weighted score를 요구합니다.

## 참고 문서

- `plan/README.md`: deployment plan overview
- `plan/01_objective.md`: Objective
- `plan/02_model.md`: Model
- `plan/03_evaluation_metrics.md`: Evaluation metric
- `docs/job-intake-fallback.md`: URL/JD fallback policy
- `docs/release-gates.md`: v0 release hard gates

## GitHub/Copilot 표면

v0 GitHub surface는 KOR pipeline만 mirror합니다. EN Resume GitHub skills는 v0에서 명시적으로 미지원입니다. GitHub surface가 의도적으로 mirror되기 전까지 EN 생성은 Codex(`en-resume-pipeline`) 또는 Claude Code(`/resume`)를 사용하세요.

## 현재 에이전트 설계 구조와 동작 방식

Oh My Resume-Agent는 `omr` 명령 하나로 자기소개서를 바로 생성하는 단일 AI 앱이 아니라, **사용자 로컬 데이터 → 정규화된 근거 → 에이전트 파이프라인 → 산출물 검수**를 안전하게 연결하는 agent harness입니다. v0의 핵심 설계는 “CLI는 준비와 검증만 담당하고, 실제 작성은 Codex/Claude Code의 스킬과 에이전트가 수행한다”는 분리입니다.

### 설계 레이어

```text
사용자 입력 레이어
  └─ userinfo/                 # 사용자의 원본 이력서, 자기소개서, 경력자료, 채용공고 fallback

정규화 근거 레이어
  └─ workspace/                # 에이전트가 참조하는 구조화된 프로필, 경험카드, claim, 문체 샘플

제어/검증 레이어
  └─ bin/omr, bin/resume       # 폴더 생성, 상태 확인, privacy gate, skill surface 점검

에이전트 실행 레이어
  ├─ .agents/skills/           # Codex에서 호출하는 스킬 표면
  ├─ .claude/skills/           # Claude Code slash command 표면
  ├─ .github/skills/           # GitHub/Copilot용 KOR mirror 표면(v0에서는 EN 미지원)
  └─ agents/                   # 실제 단계별 전문 에이전트 지침

산출/상태 레이어
  └─ output/                   # 회사별 결과물과 state.json/state_en.json
```

각 레이어는 서로 역할이 다릅니다. `userinfo/`는 원본 입력 경계이고, `workspace/`는 작성에 사용할 수 있는 정규화된 근거 저장소입니다. `bin/omr`과 `bin/resume`은 이 폴더들이 준비됐는지 확인하지만 직접 LLM을 호출하지 않습니다. 실제 생성은 `.agents/skills/` 또는 `.claude/skills/`가 `agents/`의 단계별 지침을 읽고, `workspace/` 근거를 기반으로 진행합니다.

### 폴더 구조 상세

```text
oh-my-resume-agent/
├── bin/
│   ├── omr                    # canonical CLI. setup/status/doctor/eval 담당
│   └── resume                 # omr alias. 사용자가 기억하기 쉬운 진입점
├── userinfo/
│   ├── README.md              # 원본 자료 배치 안내
│   ├── raw/                   # 개인 이력서, 기존 자소서, 경력기술서 등 원본 자료
│   └── job_posts/             # 크롤링 실패 시 붙여넣은 JD, PDF, 스크린샷 fallback
├── workspace/
│   ├── README.md              # 정규화 데이터 작성 기준
│   ├── profile/               # 기본 프로필, 커리어 타임라인
│   ├── experience_cards/      # 재사용 가능한 경험 카드. KOR/EN 모두의 1차 근거
│   ├── claims/                # claim_registry.yaml. 승인된 수치/성과만 최종 사용
│   ├── writing_samples/       # 사용자 문체 샘플
│   ├── job_posts/             # 정규화된 채용공고/JD
│   └── feedback/              # 제출 후 피드백과 다음 매칭 가중치 힌트
├── agents/
│   ├── 조사선생.md             # 기업/직무 조사
│   ├── JD분석선생.md           # JD 요구사항 분석
│   ├── 인사관선생.md           # 채용 의도와 문항 의도 해석
│   ├── 기억선생.md             # 경험 후보군 구성과 매칭
│   ├── 기획선생.md             # 답변 컨셉과 스토리라인 설계
│   ├── 필체선생.md             # 자기소개서 초안 작성
│   ├── 검수선생.md             # 사실성/문항적합성/글자수 검수
│   └── en/                    # EN Resume 전용 에이전트 8종
├── .agents/skills/            # Codex용 실행 스킬. self-intro-pipeline, en-resume-pipeline 등
├── .claude/
│   ├── rules/                 # KOR/EN 공통 파이프라인 규칙
│   └── skills/                # Claude Code 명령. /자소서, /resume, /검수 등
├── .github/skills/            # GitHub/Copilot용 KOR skill mirror. v0 EN은 의도적으로 제외
├── templates/
│   ├── samples/               # 공개용 synthetic 샘플. 실제 개인정보 금지
│   └── schemas/               # 각 단계 산출물 형식과 검수 기준
├── docs/                      # fallback 정책, release gate 문서
├── plan/                      # Objective/Model/Evaluation/roadmap 설계 문서
├── output/                    # 회사별 생성 결과. README 외 내용은 gitignore
├── data/                      # legacy seed 호환 경계. public repo에서는 README만 유지
└── .omr/                      # 로컬 실행 상태와 로그. state/logs/plans는 gitignore
```

### 동작 흐름

1. **초기화**: 사용자가 `omr setup` 또는 `omr init`을 실행하면 `userinfo/`, `workspace/`, `output/`, `.omr/state/` 등 필요한 로컬 폴더가 만들어집니다.
2. **원본 수집**: 사용자는 이력서, 기존 자기소개서, 경력자료를 `userinfo/raw/`에 넣습니다. 채용공고 URL 접근이 실패할 수 있으므로 JD 전문, PDF, 스크린샷은 `userinfo/job_posts/`에 보관합니다.
3. **정규화**: 원본 자료는 바로 최종 작성 근거로 쓰지 않고 `workspace/profile/`, `workspace/experience_cards/`, `workspace/claims/`, `workspace/writing_samples/` 같은 구조화된 자료로 정리합니다.
4. **준비 검증**: `omr doctor`가 필수 폴더/파일과 사용자 자료 존재 여부를 확인합니다. `omr eval privacy`는 공개 repo에 개인정보나 실제 산출물이 추적되는지 검사하고, `omr eval skills`는 Codex/Claude skill surface가 살아 있는지 확인합니다.
5. **파이프라인 실행**: Codex에서는 `self-intro-pipeline` 또는 `en-resume-pipeline`, Claude Code에서는 `/자소서` 또는 `/resume`을 호출합니다. 이때 스킬은 `agents/`의 단계별 지침과 `.claude/rules/`의 공통 규칙을 읽습니다.
6. **상태 기록**: KOR 자기소개서 흐름은 `output/{YYYYMMDD}_{회사명}/state.json`, EN Resume 흐름은 `output/{YYYYMMDD}_{회사명}/state_en.json`에 진행 상태를 분리해 기록합니다.
7. **검수와 피드백**: 초안은 검수 단계에서 사실성, claim 승인 여부, 문항 적합성, 글자수/ATS 기준을 확인합니다. 제출 후 결과나 피드백은 `workspace/feedback/`에 축적해 다음 매칭과 기획의 힌트로 사용합니다.

### KOR 파이프라인 구조

```text
조사선생
  → JD분석선생
  → 인사관선생
  → 기억선생(경험풀/경험매칭)
  → 기획선생
  → 필체선생
  → 검수선생
```

KOR 파이프라인은 회사/직무 조사와 JD 분석을 먼저 수행한 뒤, 사용자의 경험카드에서 해당 문항에 맞는 근거를 고릅니다. 이후 컨셉을 나누고 자기소개서 초안을 작성한 뒤, 검수선생이 원천 데이터에 없는 주장이나 승인되지 않은 수치가 들어갔는지 확인합니다.

### EN Resume 파이프라인 구조

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

EN 흐름은 KOR 자기소개서와 상태 파일을 분리합니다. 핵심 1~7단계는 회사/JD 분석, 근거 선택, 이력서 설계, 변형안 작성, ATS lint, 최종 리뷰까지이며, Step 8 publish는 `/resume-publish`로 별도 실행하는 optional 단계입니다.

### 데이터와 안전성 원칙

- **원천 없는 생성 금지**: `workspace/experience_cards/`나 승인된 `workspace/claims/claim_registry.yaml`에 없는 경험·수치·성과는 작성하지 않습니다.
- **workspace 우선**: active pipeline은 `workspace/`를 1차 근거로 사용하고, `data/`는 기존 개인용 seed 호환을 위한 legacy fallback 경계로만 남깁니다.
- **공개 저장소 위생**: `userinfo/raw/`, `userinfo/job_posts/`, `workspace/`, `output/`, `.omr/state/`의 실제 내용은 gitignore 대상입니다. 공개 repo에는 README, `.gitkeep`, schema, synthetic sample만 포함합니다.
- **fallback 명시**: 채용공고 URL 크롤링이나 문서 파싱이 실패하면 내용을 추측하지 않고, JD 텍스트/PDF/스크린샷을 `userinfo/job_posts/`에 추가하도록 안내합니다.
- **CLI/작성 분리**: `omr` CLI는 setup/status/doctor/eval만 담당합니다. `resume`은 alias입니다. 실제 LLM 기반 작성은 Codex 또는 Claude Code의 agent runtime에서 수행합니다.

## 라이선스

MIT
