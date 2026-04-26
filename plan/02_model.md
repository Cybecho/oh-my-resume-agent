# 02. Model — 실제 일을 수행하는 시스템 모델

여기서 Model은 단일 LLM 모델명이 아니라, 입력 자료를 처리하고 결과물을 생성하는 전체 에이전트 시스템을 의미한다.

## 1. 전체 시스템 모델

```text
resume CLI/TUI
  ├─ init / doctor / status / config
  └─ 사용자의 데이터 준비 상태 안내

Document Ingestion Layer
  ├─ userinfo/ 원본 파일 수집
  ├─ profile 후보 생성
  ├─ experience card 후보 생성
  ├─ claim 후보 생성
  └─ writing sample 후보 분리

Job Intake Layer
  ├─ 채용공고 URL 수집
  ├─ Playwright 접근
  ├─ 이미지/OCR 확장
  └─ 실패 시 복붙/PDF fallback

Agent Layer
  ├─ Codex/OpenAI skills
  ├─ Claude Code skills
  ├─ KOR self-intro pipeline
  └─ EN resume pipeline

Evaluation Layer
  ├─ fact check
  ├─ provenance check
  ├─ ATS check
  ├─ char limit check
  └─ release readiness check
```

## 2. `resume` CLI/TUI의 역할

`resume` 명령은 AI 생성기가 아니라 설정·검사·안내 도구다.

권장 명령:

```text
resume init      # 최초 설정 TUI
resume status    # 현재 사용자 데이터와 설정 상태 출력
resume doctor    # 설치/환경/데이터 준비 상태 검사
resume config    # Codex/Claude/경로 설정 확인 및 변경
resume paths     # userinfo, workspace, output 경로 표시
```

v0에서는 `resume`이 직접 LLM을 호출하지 않는다. 실제 생성 질의는 repo clone 위치에서 Codex 또는 Claude Code를 실행해 수행한다.

## 3. 권장 디렉터리 모델

public repo에서는 개인용 `data/`를 그대로 노출하지 않고, template/user workspace를 분리한다.

```text
userinfo/
  raw/
  notion_urls.md
  README.md

workspace/
  profile/
  experience_cards/
  experience_bullets/
  claims/
  writing_samples/
  job_posts/

output/
  {YYYYMMDD}_{company}/

templates/
  schemas/
  samples/

agents/
.agents/
.claude/
.github/
```

## 4. Document Ingestion Layer

v0에서는 ingestion을 완전 자동화하지 않고, 사용자가 넣어야 하는 자료와 결과 구조를 명확히 안내한다.

v1에서 자동화할 후보:

- PDF/DOCX/TXT/MD 읽기
- 기존 자기소개서에서 사건 단위 경험 후보 추출
- 반복 등장 사건을 하나의 experience card로 묶기
- 수치 표현을 claim 후보로 추출
- 문체 학습용 writing sample 분리

## 5. Job Intake Layer

채용공고 입력은 세 단계 fallback을 가진다.

1. URL에서 정적 HTML 텍스트 수집
2. Playwright로 렌더링 후 텍스트/이미지 수집
3. 실패 시 사용자에게 복사/붙여넣기 또는 `Ctrl+P` PDF 저장 안내

이미지 기반 공고 OCR은 v2 이후 기능으로 둔다.

## 6. Agent Layer

기존 agent 구조를 public repo에서도 유지하되, 개인 데이터 경로를 template workspace 기준으로 추상화해야 한다.

- Codex/OpenAI 표면: `.agents/skills`, `AGENTS.md`
- Claude Code 표면: `.claude/skills`, `CLAUDE.md`
- GitHub 표면: `.github/skills` 또는 prompt 문서

중요한 원칙:

- 각 표면이 동일한 Objective와 Evaluation 기준을 따라야 한다.
- skill drift를 방지하는 sync checker가 필요하다.
- EN skill은 `.github/skills`에 없는 현재 gap을 해결하거나 명시적으로 unsupported로 표시해야 한다.

## 7. Evaluation Layer

Evaluation Layer는 생성물 품질뿐 아니라 배포 가능성도 평가한다.

검사 후보:

- public repo에 개인 정보가 남아 있는지
- userinfo/workspace/output 경로가 준비되었는지
- state file과 산출물 파일이 일치하는지
- experience card frontmatter가 유효한지
- claim status가 approved인지
- Codex/Claude skill surface가 동기화되었는지
- Playwright/OCR/DOCX 의존성 준비 상태가 명확한지
