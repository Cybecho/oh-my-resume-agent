# 06. Oh-My 시리즈 철학과 `oh-my-resume-agent` 구조 방향

이 문서는 `oh-my-openagent`, `oh-my-codex`, `oh-my-gemini-cli` 계열의 공통 설계 철학을 정리하고, 현재 자소서선생 프로젝트를 `oh-my-resume-agent`로 발전시킬 때 차용할 구조와 차용하지 않을 구조를 정의한다.

핵심 결론은 다음이다.

> `oh-my-resume-agent`는 자소서 생성기 단독 앱이 아니라, Codex와 Claude Code 위에서 지원서 작성 workflow, 상태, 데이터 정규화, 검증, fallback을 제공하는 local-first agent harness여야 한다.

## 1. 참조한 oh-my 계열

공식/원본 저장소 기준으로 다음 계열을 참조한다.

- `oh-my-openagent` / `omo`: agent harness, discipline agents, `ultrawork`, planner/interview, model category routing, MCP/tooling 통합
  - <https://github.com/code-yeongyu/oh-my-openagent>
- `oh-my-codex` / `omx`: Codex CLI용 workflow layer, `$deep-interview`, `$ralplan`, `$team`, `$ralph`, `.omx/` 상태/계획/로그
  - <https://github.com/Yeachan-Heo/oh-my-codex>
- `oh-my-gemini-cli` / `omg`: Gemini CLI extension 기반 context-engineering workflow pack, workspace/taskboard, team-plan/exec/verify/fix, hook/state hygiene
  - <https://github.com/Joonghyun-Lee-Frieren/oh-my-gemini-cli>

## 2. oh-my 시리즈의 공통 철학

### 2.1 원래 엔진을 대체하지 않고 강화한다

oh-my 계열은 Codex, Gemini CLI, OpenCode 같은 기존 agent runtime을 대체하지 않는다. 대신 더 나은 prompt, skill, role, workflow, state, verification layer를 얹는다.

`oh-my-resume-agent`도 동일해야 한다.

- Codex와 Claude Code는 실제 agent 실행 엔진이다.
- `omr` CLI는 사용자의 데이터 준비, 설정, 상태 확인, doctor, guide를 담당한다. `resume`은 같은 CLI의 alias다.
- KOR/EN 자기소개서 생성은 기존 skill/agent pipeline에서 수행한다.

따라서 `omr` 명령이 “AI 생성 버튼”이 되면 안 된다. `omr`은 사용자의 로컬 작업공간을 agent가 잘 사용할 수 있게 준비하는 control plane이다.

### 2.2 단순한 진입점 뒤에 복잡한 orchestration을 숨긴다

oh-my 계열은 내부적으로는 복잡한 다중 agent orchestration을 쓰더라도, 사용자에게는 짧은 명령과 명확한 workflow를 제공한다.

`oh-my-resume-agent`의 public UX는 다음 정도로 단순해야 한다.

```bash
omr init
omr doctor
omr status
```

`resume` alias도 같은 명령을 실행하지만, 문서의 기본 예시는 `omr`을 사용한다.

사용자는 내부의 조사선생, JD분석선생, 기억선생, 필체선생 구조를 몰라도 된다. 다만 고급 사용자는 문서에서 해당 role catalog를 확인할 수 있어야 한다.

### 2.3 최상위 orchestrator와 역할별 specialist를 분리한다

oh-my-openagent는 orchestrator, planner, researcher, worker 같은 discipline agent 구조를 강조한다. oh-my-gemini-cli도 director, planner, architect, executor, reviewer, verifier 등 역할 분리를 명확히 둔다.

현재 자소서선생은 이미 domain-specific multi-agent 구조를 갖고 있다.

| 현재 자소서선생 | oh-my식 역할 |
| --- | --- |
| 자소서선생 / resume pipeline | Director / Orchestrator |
| 조사선생 | Researcher |
| JD분석선생 | JD Analyst |
| 인사관선생 | Hiring Manager Simulator |
| 기억선생 | Evidence Curator |
| 기획선생 | Planner / Strategist |
| 필체선생 | Writer |
| 검수선생 | Reviewer / Verifier |
| EN CompanyResearcher | Company Researcher |
| EN EvidenceMatcher | Evidence Mapper |
| EN ATSLinter | Parser Risk Auditor |
| EN ResumeReviewer | Final Reviewer |

즉, 기존 뼈대는 유지하고 public repo에서는 role catalog와 workflow contract를 더 명확히 문서화한다.

### 2.4 Clarify → Plan → Execute → Verify 루프를 명시한다

oh-my-codex는 `$deep-interview → $ralplan → $team/$ralph` 흐름을 권장한다. oh-my-gemini-cli는 `team-plan → team-prd → team-exec → team-verify → team-fix` 같은 staged loop를 둔다.

`oh-my-resume-agent`의 domain loop는 다음으로 정의한다.

```text
intake → normalize → match → draft → verify → publish
```

각 단계의 의미:

- `intake`: 사용자 원본 자료와 채용공고 입력 수집
- `normalize`: profile, experience card, claim, writing sample로 정규화
- `match`: JD/문항과 경험 근거 매칭
- `draft`: KOR 자기소개서/EN Resume 생성
- `verify`: 사실성, claim, 글자수, ATS, 문체 검증
- `publish`: 선택적 DOCX/Figma/제출용 문서 생성

현재 KOR 7단계 pipeline은 `match → draft → verify`에 강하다. public 배포 프로젝트에서는 `intake`와 `normalize`, 그리고 cross-session 상태 관리를 보강해야 한다.

### 2.5 상태를 파일로 남겨 재개 가능하게 만든다

oh-my-codex는 `.omx/`에 plans, logs, memory, runtime state를 둔다. oh-my-gemini-cli는 `.omg/state/workspace.json`, `.omg/state/taskboard.md` 같은 state artifact로 lane과 task를 추적한다.

`oh-my-resume-agent`는 `.omr/` 상태 계층을 도입한다.

```text
.omr/
  state/
    project.json
    user-profile.json
    ingestion.json
    job-intake.json
    doctor.json
  taskboard.md
  logs/
  plans/
```

주의:

- `.omr/state`에는 민감한 원문을 저장하지 않는다.
- 원본 파일 내용 대신 path, hash, status, evidence pointer만 저장한다.
- 실제 사용자 원본은 `userinfo/` 또는 `workspace/`에 두고 `.gitignore`로 보호한다.

### 2.6 Doctor와 smoke test를 제품 품질의 중심에 둔다

oh-my-codex는 `omx doctor`와 실제 실행 smoke test를 구분한다. 설치 형태가 정상이어도 실제 auth/runtime 호출은 실패할 수 있기 때문이다.

`oh-my-resume-agent`도 `omr doctor`를 핵심 명령으로 둔다.

검사 항목:

- `userinfo/` 존재 여부
- `workspace/` 존재 여부
- profile/experience/writing sample 후보 존재 여부
- claim registry 존재 여부
- Codex 표면 존재 여부
- Claude 표면 존재 여부
- output 쓰기 가능 여부
- parser/Playwright/OCR/DOCX 의존성 readiness
- 개인정보가 sample/public 경로에 남아 있지 않은지

v0에서는 `doctor`가 모든 기능을 통과시키지 못해도 된다. 대신 “무엇이 준비됐고 무엇이 아직 optional/unsupported인지”를 정확히 말해야 한다.

### 2.7 실패를 숨기지 않고 fallback과 blocker로 승격한다

oh-my-gemini-cli는 permission denied, lane drift, blocker를 명시적 상태로 다루는 철학을 가진다. 이 철학은 채용공고 크롤링과 문서 ingestion에 매우 중요하다.

금지:

```text
URL 크롤링 실패 → 대충 회사명으로 웹검색해서 JD를 추측 → 성공처럼 계속 진행
```

권장:

```text
URL 크롤링 실패 → blocker 기록 → 사용자에게 fallback 제시
1. 채용공고 본문 복사/붙여넣기
2. Ctrl+P로 PDF 저장 후 userinfo/job_posts/에 추가
3. 스크린샷 또는 이미지 공고를 OCR 입력으로 추가
```

자기소개서/Resume 영역은 사실성 리스크가 크므로 실패를 조용히 보정하면 안 된다.

### 2.8 Verification-first 문화를 유지한다

oh-my 계열은 “끝까지 한다”보다 “검증 가능한 완료”를 중시한다. `oh-my-resume-agent`는 특히 verification-first여야 한다.

검증 기준:

- 경험/수치가 원천 자료에 있는가
- claim이 `approved` 상태인가
- 글자수 제한을 지켰는가
- EN Resume가 ATS hard fail을 피했는가
- 사용자 문체와 과도하게 어긋나지 않는가
- 채용공고/JD와 연결되는가
- unsupported input을 추측으로 처리하지 않았는가

## 3. `oh-my-resume-agent`의 이름과 포지셔닝

### 3.1 추천 이름

```text
oh-my-resume-agent
```

### 3.2 추천 CLI 이름

1차 명령은 `omr`을 권장한다.

```bash
omr init
omr doctor
omr status
omr ingest
omr job
```

`resume`은 alias로 제공한다.

```bash
resume → omr
```

이유:

- `omr`은 oh-my 시리즈 namespace와 일관된다.
- `resume`은 일반 명령어라 충돌 가능성이 있다.
- 사용자는 README에서 둘 다 볼 수 있다.

### 3.3 추천 슬로건

```text
Your resume agent is not alone.
```

한국어 설명:

```text
지원서 작성도 혼자 하지 않는다.
```

제품 설명:

```text
Oh My Resume Agent is a local-first application-document agent harness for Codex and Claude Code.
```

한국어:

```text
Oh My Resume Agent는 Codex와 Claude Code 위에서 동작하는 로컬 우선 지원서 작성 에이전트 하네스입니다.
```

## 4. 기존 자소서선생 뼈대에서 유지할 것

현재 자소서선생의 핵심 pipeline은 유지한다.

```text
조사 → JD분석 → 의도분석 → 경험풀 → 경험매칭 → 기획 → 작성 → 검수
```

EN Resume pipeline도 유지한다.

```text
company research → jd analysis → evidence matching → resume plan → resume write → ATS lint → review → optional publish
```

유지해야 하는 원칙:

- 로컬 경험카드 우선
- 없는 경험/수치 생성 금지
- claim registry 기반 수치 검증
- KOR와 EN 상태 파일 분리
- 문체 샘플 기반 KOR 작성
- ATS hard fail 기반 EN 검수

## 5. 새로 얹을 oh-my식 control plane

기존 core pipeline 위에 다음 control plane을 얹는다.

```text
omr CLI/TUI
  ↓
.omr/state + taskboard
  ↓
userinfo/workspace 정규화
  ↓
Codex/Claude skill 실행 안내
  ↓
KOR/EN pipeline
  ↓
evaluation gates
```

추천 public repo 구조:

```text
oh-my-resume-agent/
├── AGENTS.md
├── CLAUDE.md
├── README.ko.md
├── README.en.md
├── package.json
├── bin/
│   └── omr
├── src/
│   ├── cli/
│   ├── doctor/
│   └── config/
├── agents/
│   ├── ko/
│   └── en/
├── skills/
│   ├── codex/
│   └── claude/
├── templates/
│   ├── schemas/
│   └── samples/
├── userinfo/
│   ├── raw/
│   └── README.md
├── workspace/
│   ├── profile/
│   ├── experience_cards/
│   ├── claims/
│   ├── writing_samples/
│   └── job_posts/
├── output/
└── .omr/
    ├── state/
    ├── logs/
    └── taskboard.md
```

## 6. 이전 계획안과의 연결

기존 `plan/` 문서의 Objective/Model/Evaluation 구조는 유지한다.

- `01_objective.md`: public 배포 목표
- `02_model.md`: CLI/TUI + ingestion + job intake + agent layer + evaluation layer
- `03_evaluation_metrics.md`: hard gate + weighted score
- `04_release_roadmap.md`: v0 public template → v1 ingestion → v2 web/JD robustness → v3 broad format

이 문서는 해당 계획 위에 oh-my 계열 철학을 추가한다.

정리하면:

| 기존 계획 | oh-my 철학으로 보강할 점 |
| --- | --- |
| `omr` CLI/TUI | `omr` control plane + `resume` alias |
| `userinfo/` | local-first intake boundary |
| `workspace/` | normalized agent-readable working set |
| KOR/EN skills | role catalog + canonical workflow |
| output state | `.omr/state` 상위 runtime state |
| evaluation metrics | doctor, taskboard, blocker, fallback, verification gates |

## 7. 차용할 것과 차용하지 않을 것

### 7.1 차용할 것

- 짧은 canonical command (`omr`)
- doctor/readiness check
- local state directory (`.omr/`)
- taskboard 기반 지원 작업 관리
- role-separated agents
- clarify/plan/execute/verify loop
- explicit blocker/fallback
- verification-first release gate
- Codex/Claude를 대체하지 않는 workflow layer 철학

### 7.2 차용하지 않을 것

- 초보 사용자에게 과도한 mode/command 노출
- 무제한 autonomous loop
- 사용자 승인 없는 claim 본문 사용
- 민감한 원문을 state에 저장
- 모든 문서 포맷/채용 사이트를 v0에서 완전 자동 지원한다고 약속
- Codex/Claude를 감추는 독자 LLM 실행기

## 8. v0 architecture delta

v0에서 기존 개인용 자소서선생에 추가할 최소 변화는 다음이다.

1. 프로젝트 이름과 README 포지셔닝을 `oh-my-resume-agent`로 정의
2. `omr` CLI 설계 (`resume` alias 포함)
3. `.omr/state`와 `.omr/taskboard.md` 설계
4. `userinfo/`와 `workspace/` 경계 도입
5. public sample data와 privacy gate 도입
6. Codex/Claude skill surface 정리
7. `omr doctor` 기준 정의
8. URL/JD fallback policy 문서화

v0에서 core writer/agent 품질을 크게 바꾸지 않는다. 기존 자소서선생의 KOR/EN pipeline을 유지한 채 public 배포에 필요한 harness 계층을 얹는다.

## 9. 최종 원칙

`oh-my-resume-agent`는 다음 문장으로 정의한다.

> 기존 AI CLI를 대체하지 않고, 지원서 작성에 필요한 데이터 준비, 역할 분리, 상태 관리, fallback, 검증 루프를 제공해 Codex와 Claude Code가 더 안전하게 지원 문서를 만들도록 돕는 local-first agent harness.

이 원칙을 지키면 현재 자소서선생의 뼈대를 유지하면서도 oh-my 시리즈의 철학을 자연스럽게 계승할 수 있다.
