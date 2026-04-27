# 파이프라인 공통 규칙

이 규칙은 모든 Skill 실행 시 자동 적용된다.

## 출력 규칙

- 모든 산출물은 `output/{YYYYMMDD}_{회사명}/` 폴더에 저장한다
- 폴더가 없으면 생성한다
- 파일명은 `01_기업조사.md`, `02_JD분석.md` 등 번호 접두사를 붙인다
- Step 7 자소서는 `07_자소서/컨셉1.md`, `컨셉2.md`, `컨셉3.md`로 저장한다

## 상태 관리

- 매 단계 시작 시 `state.json`의 해당 step status를 `in_progress`로 변경한다
- 매 단계 완료 시 `state.json`의 해당 step status를 `completed`로, `completed_at`을 현재 시각으로, `current_step`을 다음 단계로 업데이트한다
- 중간에 실패하면 status를 `in_progress`로 남기고 사용자에게 알린다

## 데이터 무결성

- **허구 금지**: 사용자의 원천 데이터(Notion/로컬 파일)에 존재하지 않는 경험, 수치, 성과를 절대 창작하지 않는다
- **과장 금지**: 원천 데이터의 표현을 과도하게 부풀리지 않는다
- **출처 명시**: 경험 데이터를 사용할 때 어느 소스에서 가져왔는지 내부적으로 추적한다

- **Notion 의존성 배제**: Notion MCP는 보조 수단으로만 사용하며, 기본 동작은 로컬 데이터만으로 완료할 수 있어야 한다

## 경험 데이터 조회 순서

1. 정규화 카탈로그: `workspace/experience_cards/*.md`
   - `doc_type: experience_card` 블록과 `tags`를 우선 사용
2. Claim registry: `workspace/claims/claim_registry.yaml`
   - 최종 본문 수치는 `approved` claim만 사용
3. 문체 샘플: `workspace/writing_samples/*.md`
   - 사용자 문체 참조용으로 사용
4. 원본 입력: `userinfo/raw/`, `userinfo/job_posts/`
   - 원본은 정규화 전 경계로 취급하고, 생성 근거로 쓰기 전 `workspace/`로 구조화한다
5. Legacy fallback: `data/experience_cards/`, `data/experience_bullets/`, `data/experiences/`, `data/writing_samples/`
   - 기존 개인용 seed에만 존재하는 보조 소스
6. 소스 아카이브: `data/writing_samples/Archive_*.md`
   - `source:` 원문을 통한 근거 추적용 참조
7. legacy 경험 파일: `data/experiences/` 폴더
   - 기존 STAR 템플릿 자원 보조 소스
8. Notion MCP (`notion-search` → `notion-fetch`)
   - 설정된 경우에만 보강 수단으로 사용
9. 가능한 한 로컬과 보조 소스 모두 교차 검증 후 누락 없는 선별 수행

public template에서 `workspace/`가 비어 있으면 경험을 창작하지 말고 `omr init`, `omr doctor`, `userinfo/` 입력 안내를 먼저 제시한다.

## 언어 및 톤

- 한국어로 응답한다
- 기업 영문명, 기술 용어, 직무명은 원문 유지한다
- 자소서 본문은 사용자의 문체를 따른다 (`workspace/writing_samples/` 우선 참조, 기존 개인용 seed에서만 `data/writing_samples/`를 legacy fallback으로 사용)

## 진행상황 표시

- 각 단계 시작 시: `── Step N/7: {단계명} ──`
- 각 단계 완료 시: `✓ {파일명} 저장`
- 전체 완료 시: 3세트 요약 + 추천 순위 표시

## 글자수

- 각 자소서 문항의 `char_limit`을 반드시 지킨다
- 글자수는 공백 포함 기준이다
- 제한의 90~100% 범위를 목표로 한다 (너무 짧지 않게)

## 에이전트 지침 참조

- 각 단계 실행 시 반드시 `agents/{에이전트명}.md` 파일을 Read로 읽어 상세 지침을 확인한 후 수행한다
- 에이전트 지침에 명시된 핵심 지식, 수행 절차, 출력 스키마를 따른다
