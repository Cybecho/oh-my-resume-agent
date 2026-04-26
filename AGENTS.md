# AGENTS: Codex 실행 지침

이 저장소는 로컬 경험 데이터 기준으로 자기소개서 파이프라인을 수행하는 에이전트 환경입니다. Codex는 기본적으로 로컬 데이터를 우선 사용합니다.

## 핵심 규칙

- 원천 데이터가 없는 내용은 작성하지 않는다.
- 수치/사실은 `data/experience_cards/`를 1차 근거로, 필요 시 `data/experience_bullets/claim_registry.yaml`과 `data/experiences/`로 보강한다.
- KOR 파이프라인 상태는 `output/{YYYYMMDD}_{회사명}/state.json`에 반영한다.
- EN resume 파이프라인 상태는 `output/{YYYYMMDD}_{회사명}/state_en.json`에 반영한다.
- EN 산출물은 `output/{YYYYMMDD}_{회사명}/en_resume/` 하위로 저장한다.

## 데이터 조회 우선순위

1. `data/experience_cards/*.md` (doc_type: `experience_card`)
2. `data/experience_cards/00_TAG_INDEX.md`, `13_모든경험_인덱스맵.md`, `14_경험_검색_선별_대시보드.md`
3. `data/experiences/_index.md` 및 `data/experiences/*.md`(legacy)
4. Notion MCP는 로컬 소스로 누락이 있을 때만 보조 수단으로 사용

## 사용 가능한 스킬

- `self-intro-pipeline`: 전체 7단계 자동 실행(`/자소서` 흐름)
- `company-research`: Step 1 단독 실행
- `jd-analysis`: Step 2~3 단독 실행
- `experience-matching`: Step 4~5 단독 실행
- `concept-planning`: Step 6 단독 실행
- `write-drafts`: Step 7 단독 실행
- `review-drafts`: 검수 단독 실행
- `resume-continue`: 중단/미완성 작업 이어서 진행
- `capture-feedback`: 결과 피드백 등록 및 가중치 반영 안내
- `en-resume-pipeline`: EN 코어 7단계 자동 실행(`/resume` 흐름, optional Step 8은 별도)
- `en-company-research`: EN Step 1 단독 실행
- `en-jd-analysis`: EN Step 2 단독 실행
- `en-evidence-matching`: EN Step 3 단독 실행
- `en-resume-plan`: EN Step 4 단독 실행
- `en-resume-write`: EN Step 5 단독 실행
- `en-ats-lint`: EN Step 6 단독 실행
- `en-resume-review`: EN Step 7 단독 실행
- `en-resume-publish`: EN Step 8(옵셔널) 단독 실행, markdown 결과를 로컬 DOCX + Figma(Remote MCP)로 발행
- `en-resume-continue`: EN 중단/미완성 작업 이어서 진행

## 참조 규칙

- 단계별 실행은 대응하는 `agents/*.md` 또는 `agents/en/*.md` 지침을 먼저 읽는다.
- 파이프라인 공통 규칙은 `.claude/rules/pipeline-rules.md`와 `templates/schemas/*.md`를 따른다.
- EN resume 흐름은 `.claude/rules/en-resume-rules.md`와 `templates/schemas/en/*.md`를 추가로 따른다.
- 경험카드 구조 변경/추가/삭제는 `data/experience_cards/MOC_운영정합성.md`의 실행 체크리스트를 기준으로 점검한다.
