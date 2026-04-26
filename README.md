# oh-my-resume-agent (자소서 선생)

> JD 입력 한 번이면 자기소개서 3세트가 뚝딱.

Public 배포용 저장소에서는 개인 이력/경험/생성 결과를 포함하지 않습니다. 사용자는 `userinfo/`에 원본 문서를 넣고, 에이전트가 정리한 개인 지식베이스는 `workspace/`에 생성하는 방향으로 확장합니다. 현재 공개 초기 커밋은 기존 자소서 선생 파이프라인의 agent/skill 뼈대와 배포 계획 문서를 보존합니다.

JD(채용공고) + 사용자 경험 데이터를 기반으로 **자기소개서 3세트**를 자동 생성하는 7단계 파이프라인 에이전트 시스템입니다.
Claude Code의 **Skill** 아키텍처 위에서 동작하며, `/자소서` 한 번이면 기업 조사부터 최종 검수까지 전 과정이 자동 실행됩니다.

---

## 아키텍처 개요

```
사용자 입력 (회사명, JD, 문항)
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  /자소서  (Master Skill — 전체 오케스트레이션)            │
│                                                         │
│  Step 1  조사선생 ──── 기업 조사 + Culture-Sync 어휘     │
│     │                                                   │
│  Step 2  JD분석선생 ── JD 구조화 + 역량 추출             │
│     │                                                   │
│  Step 3  인사관선생 ── 문항별 출제 의도 + 평가 기준       │
│     │                                                   │
│  Step 4  기억선생 ──── 경험 수집 (Notion + 로컬)         │
│     │                                                   │
│  Step 5  기억선생 ──── 문항-경험 정밀 매칭               │
│     │                                                   │
│  Step 6  기획선생 ──── 3가지 컨셉 설계                   │
│     │                                                   │
│  Step 7  필체선생 ──── 사용자 문체로 3세트 작성           │
│     │                                                   │
│  검수    검수선생 ──── 8항목 검수 + 수정 권고             │
└─────────────────────────────────────────────────────────┘
        │
        ▼
output/{YYYYMMDD}_{회사명}/
  ├── 01_기업조사.md ~ 06_기획.md
  ├── 07_자소서/컨셉1.md, 컨셉2.md, 컨셉3.md
  ├── 08_검수리포트.md
  └── state.json
```

### Skill과 Agent의 분리

| 구분 | 위치 | 역할 |
|------|------|------|
| **Skill** | `.claude/skills/*.md` | 사용자가 `/명령어`로 호출하는 짧은 오케스트레이션 |
| **Agent** | `agents/*.md` | 각 단계의 상세 지침 (핵심 지식, 수행 절차, 출력 스키마) |

Skill이 실행되면 대응하는 Agent 파일을 `Read`로 읽어 상세 지침을 따릅니다.
이 분리 덕분에 Skill 파일은 간결하게, Agent 파일은 풍부하게 유지됩니다.

---

## 스킬 구성 (9개)

| 명령어 | 대응 단계 | 용도 | 사용 에이전트 |
|--------|-----------|------|--------------|
| `/자소서` | 전체 | 7단계 전체 자동 실행 (마스터) | 전원 |
| `/조사` | Step 1 | 기업 조사 단독 재실행 | 조사선생 |
| `/분석` | Step 2-3 | JD 분석 + 의도 추론 재실행 | JD분석선생, 인사관선생 |
| `/매칭` | Step 4-5 | 경험 수집 + 매칭 재실행 | 기억선생 |
| `/기획` | Step 6 | 컨셉 기획 재실행 | 기획선생 |
| `/작성` | Step 7 | 자소서 작성 재실행 | 필체선생 |
| `/검수` | 검수 | 검수 리포트 재실행 | 검수선생 |
| `/이어서` | - | 이전 세션 복원 (state.json 기반) | - |
| `/피드백` | - | 합격/불합격 피드백 등록 | - |

**`/자소서`** 는 입력을 받은 뒤 Step 1~7 + 검수를 순차 실행합니다.
개별 스킬(`/조사`, `/분석` 등)은 특정 단계만 다시 돌리고 싶을 때 사용합니다.

---

## 에이전트 구성 (7명)

| 에이전트 | 영문 역할 | 담당 단계 | 핵심 역할 |
|----------|-----------|-----------|-----------|
| 조사선생 | Corporate Research Analyst | Step 1 | 기업 정보 + Culture-Sync 어휘 수집 |
| JD분석선생 | Job Description Analyst | Step 2 | JD 구조화, 필수/우대 역량 추출 |
| 인사관선생 | Hiring Manager Simulator | Step 3 | 문항별 출제 의도, 평가 기준, 차별화 포인트 분석 |
| 기억선생 | Portfolio Curator | Step 4-5 | Notion/로컬 경험 수집 + 문항별 정밀 매칭 |
| 기획선생 | Content Strategist | Step 6 | 3가지 차별화된 컨셉 축 설계 |
| 필체선생 | Ghostwriter | Step 7 | 사용자 문체 학습 + 3세트 자소서 작성 |
| 검수선생 | Editor-in-Chief | 검수 | 8항목 루브릭 평가 + 팩트체크 + 수정 권고 |

각 에이전트의 상세 지침은 `agents/{에이전트명}.md`에 정의되어 있습니다.

---

## 디렉토리 구조

```
딸깍자소서선생/
├── .claude/
│   ├── skills/              # 사용자 호출 스킬 (9개)
│   │   ├── 자소서.md         #   마스터: 전체 파이프라인
│   │   ├── 조사.md           #   Step 1 재실행
│   │   ├── 분석.md           #   Step 2-3 재실행
│   │   ├── 매칭.md           #   Step 4-5 재실행
│   │   ├── 기획.md           #   Step 6 재실행
│   │   ├── 작성.md           #   Step 7 재실행
│   │   ├── 검수.md           #   검수 재실행
│   │   ├── 이어서.md         #   세션 복원
│   │   └── 피드백.md         #   피드백 등록
│   ├── rules/
│   │   └── pipeline-rules.md # 전 스킬 공통 규칙
│   └── settings.local.json   # 도구 권한 설정
│
├── agents/                   # 에이전트 상세 지침 (7개)
│   ├── 조사선생.md
│   ├── JD분석선생.md
│   ├── 인사관선생.md
│   ├── 기억선생.md
│   ├── 기획선생.md
│   ├── 필체선생.md
│   └── 검수선생.md
│
├── data/                     # 사용자 데이터
│   ├── profile.md            #   기본 프로필 (이름, 학력, 경력 등)
│   ├── experiences/          #   주제별 경험 (STAR 포맷, legacy)
│   │   ├── _index.md         #     경험 인덱스
│   │   └── *.md              #     개별 경험 파일
│   ├── writing_samples/      #   과거 작성 글 (문체 학습용)
│   └── experience_cards/ # 경험카드 + 태그 인덱스/대시보드
│   └── feedback/
│       └── log.json          #   피드백 이력
│
├── templates/schemas/        # 단계별 출력 스키마 (6개)
│   ├── company_profile.md
│   ├── jd_analysis.md
│   ├── hiring_intent.md
│   ├── experience_pool.md
│   ├── concept_plan.md
│   └── review_rubric.md
│
├── output/                   # 파이프라인 산출물
│   └── {회사명}_{YYYYMMDD}/
│       ├── state.json        #   파이프라인 상태
│       ├── 01_기업조사.md
│       ├── 02_JD분석.md
│       ├── 03_의도분석.md
│       ├── 04_경험풀.md
│       ├── 05_경험매칭.md
│       ├── 06_기획.md
│       ├── 07_자소서/
│       │   ├── 컨셉1.md
│       │   ├── 컨셉2.md
│       │   └── 컨셉3.md
│       └── 08_검수리포트.md
│
├── CLAUDE.md                 # 프로젝트 마스터 설정
└── README.md                 # 이 파일
```

---

## 사전 준비

시스템을 사용하기 전에 아래 데이터를 준비하세요.

| 항목 | 경로 | 설명 |
|------|------|------|
| 프로필 | `data/profile.md` | 이름, 학력, 경력, 자격증, 핵심 역량 |
| 경험 | `data/experience_cards/*.md` | 경험카드 + 태그 인덱스 기반으로 구성된 로컬 풀 |
| 운영 MOC | `data/experience_cards/MOC_운영정합성.md` | 경험카드 정합성 점검, 실행 체크리스트, 롤백 가이드 |
| 문체 샘플 | `data/writing_samples/` | 본인이 직접 작성한 글 **최소 2개** (자소서, 블로그, 에세이 등) |
| Notion (선택) | - | 경험 데이터가 Notion에 있으면 MCP로 자동 연동 |

### 간단 사용 가이드

1. `data/profile.md`에 기본 정보(학력, 경력, 자격증, 핵심 역량) 작성
2. `data/experience_cards/`의 카드(01~13) 중 사용 가능한 항목 점검
   - 태그 기반 탐색은 `data/experience_cards/00_TAG_INDEX.md`, `14_경험_검색_선별_대시보드.md` 사용
   - 전체 맵은 `13_모든경험_인덱스맵.md` 확인
3. `/자소서` 실행
   - 회사명, 직무, JD, 문항(글자수 제한 포함)을 입력하면 자동으로 7단계+검수 진행
4. 결과는 `output/{YYYYMMDD}_{회사명}/`에서 확인
   - 최종 문항: `07_자소서/컨셉1.md~컨셉3.md`
   - 품질 점검: `08_검수리포트.md`
5. 수정이 필요하면 특정 단계만 재실행
   - `/기획`, `/작성`, `/매칭`, `/검수` 등으로 교체 실행

### 경험 카드 편집 요약

신규 경험을 추가하거나 수정할 때는 `00_TAG_INDEX`, `13_모든경험_인덱스맵`, `14_경험_검색_선별_대시보드`를 연동 관점에서 유지 점검하고,
규칙 변경 전후에는 `data/experience_cards/MOC_운영정합성.md`의 체크리스트를 실행하세요.

### 경험 파일 작성법

각 `.md` 파일은 STAR 형식을 따릅니다:

```markdown
# [경험/프로젝트명]

## 메타
- 기간: YYYY.MM - YYYY.MM
- 역할: (예: 팀 리더, 백엔드 개발자)
- 분류: (리더십, 기술역량, 협업, 문제해결, 기획력, 커뮤니케이션, 성장, 성과)
- 태그: [키워드1, 키워드2, ...]

## Situation
어떤 상황이었는지 (배경, 맥락)

## Task
내가 맡은 구체적 과제/역할

## Action
내가 한 구체적 행동 (가능한 한 상세히)

## Result
결과 (정량적 수치가 있으면 반드시 포함)

## 배운 점
이 경험에서 얻은 인사이트
```

경험카드(01~13) 추가/변경 시:
- `data/experience_cards/13_모든경험_인덱스맵.md`, `14_경험_검색_선별_대시보드.md`의 진입점/요약은 수동으로 점검하세요.
- 기존 `data/experiences/_index.md`는 호환 목적의 보조 인덱스로 유지하면 좋습니다.

---

## 사용법

### 1. Claude Code CLI (권장)

이 프로젝트의 기본 실행 환경입니다. `.claude/skills/*.md`를 네이티브로 인식하고, 파일명이 슬래시 커맨드로 자동 변환됩니다.

**설치**

```bash
npm install -g @anthropic-ai/claude-code
```

**실행**

```bash
cd /path/to/oh-my-resume-agent
claude
```

Claude Code REPL이 열리면 프로젝트 내 `.claude/skills/` 파일들이 자동 인식됩니다.
슬래시 명령어로 스킬을 호출하세요:

```
User> /자소서
```

- MCP 완전 지원 (Notion 등)
- `CLAUDE.md`, `.claude/rules/` 자동 로드
- 세션 간 `state.json` 기반 복원 (`/이어서`)

### 2. Claude Desktop

Claude Desktop 앱에서도 Skills를 사용할 수 있습니다.

**방법 1: Skills 디렉토리 인식**

프로젝트 폴더를 Claude Desktop에서 열면 `.claude/skills/` 파일이 자동 로드됩니다.
다만 CLI와 달리 명시적 슬래시 커맨드 호출이 아닌 **자동 로드** 중심으로 동작합니다.

**방법 2: ZIP 업로드**

Skills 파일을 ZIP으로 패키징 후 Settings > Add Skills에서 업로드할 수 있습니다.

**MCP 연동**

- `claude_desktop_config.json`에서 로컬 MCP 서버 설정 (Notion 등)
- Integrations(OAuth)로 클라우드 앱 직접 연동도 가능

### 3. VSCode — GitHub Copilot Agent

GitHub Copilot의 Agent mode에서 이 프로젝트의 지침을 사용하려면 파일 구조를 변환해야 합니다.

**Copilot이 인식하는 파일 구조:**

| 타입 | 경로 | 용도 |
|------|------|------|
| Custom Instructions | `.github/copilot-instructions.md` | 모든 Chat에 자동 적용되는 프로젝트 규칙 |
| Prompt Commands | `.github/prompts/*.prompt.md` | `/자소서`, `/조사` 등 커스텀 슬래시 커맨드 |
| Agent Skills | `.github/skills/{name}/SKILL.md` | 특화 태스크 (experimental, v1.108+) |

**이 프로젝트를 Copilot Agent에서 사용하려면:**

1. `.github/copilot-instructions.md` 생성 — `CLAUDE.md` + `pipeline-rules.md` 내용 이식
2. `.github/prompts/자소서.prompt.md` 등 생성 — `.claude/skills/*.md` 내용을 prompt 형식으로 변환
3. MCP 설정 — VSCode `settings.json`의 `mcp.servers`에 Notion MCP 등록

```
.github/
├── copilot-instructions.md          # CLAUDE.md + pipeline-rules.md 이식
├── prompts/
│   ├── 자소서.prompt.md             # 7단계 전체 파이프라인
│   ├── 조사.prompt.md               # Step 1
│   ├── 분석.prompt.md               # Step 2-3
│   ├── 매칭.prompt.md               # Step 4-5
│   ├── 기획.prompt.md               # Step 6
│   ├── 작성.prompt.md               # Step 7
│   ├── 검수.prompt.md               # 검수
│   ├── 이어서.prompt.md             # 세션 복원
│   └── 피드백.prompt.md             # 피드백
└── skills/                          # Agent Skills (experimental)
    └── ...
```

> **참고**: Agent Skills(`.github/skills/`)는 2026년 1월 기준 experimental 기능입니다. Prompt Commands(`.github/prompts/`)는 안정적으로 지원됩니다.

### 4. OpenAI Codex CLI

Codex는 자체 지침 체계를 사용하며, 별도 포팅이 필요합니다.

**Codex가 인식하는 파일 구조:**

| 타입 | 경로 | 용도 |
|------|------|------|
| 프로젝트 지침 | `AGENTS.md` (프로젝트 루트) | 전체 프로젝트 규칙 (자유 형식 Markdown) |
| Skills | `.agents/skills/{name}/SKILL.md` | 특화 태스크 정의 |

**이 프로젝트를 Codex에서 사용하려면:**

1. `AGENTS.md` 생성 — `CLAUDE.md` + `pipeline-rules.md` 내용 이식
2. `.agents/skills/{self-intro-pipeline,company-research,jd-analysis,experience-matching,concept-planning,write-drafts,review-drafts,resume-continue,capture-feedback,en-resume-pipeline,en-company-research,en-jd-analysis,en-evidence-matching,en-resume-plan,en-resume-write,en-ats-lint,en-resume-review,en-resume-publish,en-resume-continue}/SKILL.md` 생성
   - 기존 `.claude/skills/*.md`의 단계별 흐름을 Codex 전용으로 변환
3. 각 Codex 스킬 폴더에 `agents/openai.yaml`를 추가해 UI 노출 메타데이터(이름/요약/시작 프롬프트)를 구성
4. MCP: Agents SDK 연계 시 사용 가능, 기본 동작은 로컬 파일 기반 (Notion은 보조)

**제약**: Claude 전용 기능(MCP 자동 연동, subagent, Skill-Agent 분리 구조)은 동작하지 않습니다.

### 플랫폼별 파일 매핑

이 프로젝트의 파일이 각 플랫폼에서 어떻게 대응되는지 정리합니다.

| 이 프로젝트 파일 | Claude Code CLI | Claude Desktop | GitHub Copilot | OpenAI Codex |
|-----------------|-----------------|----------------|----------------|--------------|
| `CLAUDE.md` | 자동 로드 | 자동 로드 | `.github/copilot-instructions.md` | `AGENTS.md` |
| `.claude/skills/*.md` | `/명령어` 호출 | 자동 로드 | `.github/prompts/*.prompt.md` | `.agents/skills/` |
| `.claude/rules/` | 자동 적용 | 자동 적용 | `copilot-instructions.md`에 병합 | `AGENTS.md`에 병합 |
| `agents/*.md` | Skill이 Read 참조 | Skill이 Read 참조 | Prompt 내 인라인 또는 별도 참조 | SKILL.md 내 인라인 |
| Notion MCP | 완전 지원 | 완전 지원 | VSCode MCP 설정 | Agents SDK 경유 |

> **결론**: Claude Code CLI가 가장 완전한 지원을 제공합니다. 다른 플랫폼은 파일 변환 후 사용 가능합니다.

---

## 예시 사용법

### 예시 1: 전체 자동 실행

```
User> /자소서

Claude> 아래 정보를 입력해주세요:
        1. 회사명
        2. 지원 직무
        3. JD (채용공고 전문)
        4. 자소서 문항 + 글자수 제한

User> 삼성전자
      클라우드 엔지니어
      [JD 전문 붙여넣기]
      1. 지원동기 및 입사 후 포부 (1000자)
      2. 본인의 핵심 역량과 관련 경험 (1500자)
      3. 팀워크 경험과 배운 점 (1000자)

Claude> ═══ 딸깍자소서 선생 시작 ═══

        ── Step 1/7: 기업 조사 ──
        삼성전자 클라우드 사업부 조사 중...
        ✓ 01_기업조사.md 저장

        ── Step 2/7: JD 분석 ──
        ...
        ── Step 7/7: 자소서 작성 ──
        ✓ 07_자소서/컨셉1.md 저장
        ✓ 07_자소서/컨셉2.md 저장
        ✓ 07_자소서/컨셉3.md 저장

        ── 검수 ──
        ✓ 08_검수리포트.md 저장

        ═══ 완료 ═══

        [3세트 요약]
        컨셉1: "기술 전문가" — AWS 마이그레이션 중심
        컨셉2: "문제 해결사" — 장애 대응 + 비용 절감 중심
        컨셉3: "성장하는 리더" — 팀 리딩 + 학습 중심

        추천 순위: 컨셉2 > 컨셉1 > 컨셉3
```

### 예시 2: 특정 단계만 재실행

기획이 마음에 들지 않을 때 Step 6만 다시 돌릴 수 있습니다.

```
User> /기획

Claude> 기존 분석 결과를 기반으로 새로운 컨셉 3가지를 설계합니다...
        ✓ 06_기획.md 저장 (이전 버전 덮어쓰기)
```

### 예시 3: 세션 복원

대화가 끊겼거나 새 세션에서 이전 작업을 이어갈 때:

```
User> /이어서

Claude> 기존 세션을 탐색합니다...

        [1] 삼성전자_20260213 — Step 7 완료 (전체 완료)
        [2] 카카오_20260215 — Step 3까지 완료

        어떤 세션을 복원할까요?

User> 2

Claude> 카카오_20260215 복원. Step 4부터 이어서 진행합니다.
        ── Step 4/7: 경험 수집 ──
        ...
```

### 예시 4: 피드백 등록

합격/불합격 결과를 기록하면 이후 경험 매칭에 반영됩니다.

```
User> /피드백

Claude> 피드백 정보를 입력해주세요:
        - 회사명 / 세션
        - 사용 컨셉 번호
        - 결과 (서류통과/불합격)
        - (선택) 코멘트

User> 삼성전자 컨셉2 서류통과

Claude> ✓ feedback 저장 완료
        - 회사: 삼성전자
        - 컨셉: 2
        - 결과: 서류통과
        → 사용된 경험의 가중치가 상향 조정됩니다.
```

---

## 산출물 구조

각 실행의 산출물은 `output/{YYYYMMDD}_{회사명}/`에 저장됩니다.

| 파일 | 단계 | 내용 |
|------|------|------|
| `state.json` | - | 파이프라인 상태 (진행도, 입력 데이터) |
| `01_기업조사.md` | Step 1 | 기업 개요, 인재상, Culture-Sync 어휘 |
| `02_JD분석.md` | Step 2 | JD 구조화, 필수/우대 역량, 숨은 요구사항 |
| `03_의도분석.md` | Step 3 | 문항별 출제 의도, 평가 기준, 함정 |
| `04_경험풀.md` | Step 4 | 후보 경험 전체 목록 (Notion + 로컬) |
| `05_경험매칭.md` | Step 5 | 문항별 최적 경험 배치 |
| `06_기획.md` | Step 6 | 3가지 컨셉 설계 + 비교표 |
| `07_자소서/컨셉{1,2,3}.md` | Step 7 | 자기소개서 3세트 본문 |
| `08_검수리포트.md` | 검수 | 8항목 평가 + 팩트체크 + 수정 권고 |

---

## 핵심 규칙

- **허구 금지** — 사용자 원천 데이터(Notion/로컬)에 없는 경험은 절대 작성하지 않습니다
- **글자수 준수** — 각 문항의 글자수 제한을 반드시 지키며, 90~100% 범위를 목표로 합니다
- **한국어 응답** — 기업 영문명, 기술 용어, 직무명은 원문 유지합니다
- **Culture-Sync** — 기업 조사에서 추출한 문화 어휘를 자소서에 자연스럽게 반영합니다
- **상태 저장** — 매 단계 완료 시 `state.json`을 업데이트하여 세션 복원이 가능합니다

---

## 향후 계획

- **NotebookLM MCP 연동** — 경험 DB, 방법론 서적, 문체 샘플을 NotebookLM 노트북으로 관리
- **이력서 자동 생성** — 자소서 파이프라인과 연계한 이력서(Resume) 생성 기능
- **면접 준비 에이전트** — 작성된 자소서 기반 예상 질문 생성 + 모의 면접

---

## RESUME 선생 (EN 파이프라인)

같은 저장소에서 한국형 자소서 파이프라인과 분리된 EN 이력서 파이프라인을 함께 운영합니다.

### EN 파이프라인 단계

| Step | 에이전트 | 출력 |
|------|----------|------|
| 1 | CompanyResearcher | `en_resume/01_company_research.md` |
| 2 | JDAnalyst | `en_resume/02_jd_analysis.md` |
| 3 | EvidenceMatcher | `en_resume/03_evidence_selection.md` |
| 4 | ResumeArchitect | `en_resume/04_resume_plan.md` |
| 5 | ResumeWriter | `en_resume/05_resume/variant_A.md~C.md` |
| 6 | ATSLinter | `en_resume/06_ats_report.md` |
| 7 | ResumeReviewer | `en_resume/07_review_report.md` |
| 8 (Optional) | ResumePublisher | `en_resume/08_publish/08_publish_report.md`, `en_resume/08_publish/publish_manifest.json` |

### EN 명령어

- `/resume`: 코어 파이프라인 Step 1~7 실행
- `/resume-publish`: Optional Step 8 실행 (기본 target: `docx,figma`)
- `/resume-publish` 사전 준비: `docxtpl` 설치 + Figma Remote MCP 연결
- publish 설정 파일: `config/en_resume_publish.json` (`docx.template_path`, `figma.file_key`, `figma.page_node_id`, `figma.template_frame_name` 필수)
- DOCX 의존성 설치: `python3 -m pip install -r requirements/en_resume_publish.txt`
- Figma Remote 연결:
  - Claude Desktop: `Settings > Connectors`에서 `https://mcp.figma.com/mcp` 추가 후 OAuth
  - Codex Desktop: `codex mcp add figma --url https://mcp.figma.com/mcp` 후 `codex mcp login figma`

### EN 출력/상태 분리

- EN 출력 루트: `output/{YYYYMMDD}_{회사명}/en_resume/`
- EN 상태 파일: `output/{YYYYMMDD}_{회사명}/state_en.json`
- KOR 상태 파일(`state.json`)과 분리 운영
- Step 8 산출물 루트: `output/{YYYYMMDD}_{회사명}/en_resume/08_publish/`
- 하위호환: `state_version: 1` 세션은 읽을 때 step 8 보강 후 저장 시 `state_version: 2`로 승격
- `current_step` 규칙: step 7 완료 시 `8`, step 8 완료 시 `9`

### EN 핵심 규칙

- 데이터 우선순위: `experience_cards -> experience_bullets -> claim_registry`
- 수치 사용: `claim_registry.yaml`의 `approved` claim만 허용
- ATS 하드페일(이미지/표/다단/PII/필수연락처 누락) 0건 필수
- 기본 출력은 Variant 3개(A/B/C)
- Cover Letter는 코어 파이프라인 범위에서 제외(Phase 2)
- Step 8 게이트(수동): ATS pass + `top_pick` 존재 + Mandatory Fixes 없음
- Step 8 타깃: 로컬 `docx` + `figma`(remote)만 지원
