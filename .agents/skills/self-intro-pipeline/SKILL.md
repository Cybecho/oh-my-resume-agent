---
name: self-intro-pipeline
description: "Run the full 7-step workflow for `/자소서` (complete pipeline: 조사→분석→매칭→기획→작성→검수). Use local experience cards first and fall back to Notion only when local sources are insufficient."
---

# 전체 파이프라인 실행

사용자 요청이 아래 중 하나일 때 이 스킬을 사용한다.

- `/자소서` 흐름으로 전체 과정을 한 번에 실행할 때
- 회사명/직무/JD/문항이 준비된 상태에서 7단계를 순차 실행해야 할 때

## 실행 전 준비

1. 사용자 입력에서 `회사명`, `지원 직무`, `JD`, 문항 리스트(글자수 제한 포함)를 확보한다.
2. `output/`에 대상 폴더(`output/{YYYYMMDD}_{회사명}`)가 없으면 생성한다.
3. `state.json`를 초기화하거나 기존 파일을 읽어 현재 상태를 파악한다.
4. 다음 규칙으로 실행 가능 여부를 확인한다.
   - `/경험 데이터`는 `workspace/experience_cards/*.md`를 우선 사용
   - 수치/성과는 `workspace/claims/claim_registry.yaml`의 `approved` claim만 최종 사용
   - 문체는 `workspace/writing_samples/*.md`를 우선 사용
   - 기존 개인용 seed에서만 `data/experience_cards/`, `data/experiences/_index.md`, `data/writing_samples/`를 legacy fallback으로 사용
   - `workspace/`가 비어 있으면 `omr doctor`와 `userinfo/` 입력 안내를 먼저 제시
   - Notion MCP는 보강 수단으로만 사용

## 실행 순서

1. `agents/조사선생.md`를 읽고 Step 1 수행, `01_기업조사.md` 저장
2. `agents/JD분석선생.md`를 읽고 Step 2 수행, `02_JD분석.md` 저장
3. `agents/인사관선생.md`를 읽고 Step 3 수행, `03_의도분석.md` 저장
4. `agents/기억선생.md`를 읽고 Step 4-5 수행, `04_경험풀.md`, `05_경험매칭.md` 저장
5. `agents/기획선생.md`를 읽고 Step 6 수행, `06_기획.md` 저장
6. `agents/필체선생.md`를 읽고 Step 7 수행, `07_자소서/컨셉1.md`~`컨셉3.md` 저장
7. `agents/검수선생.md`를 읽고 검수 수행, `08_검수리포트.md` 저장
8. 매 단계 시작/완료 시 `state.json`의 `steps` 및 `current_step` 갱신

## 출력 정리

- 각 단계별 산출 파일과 요약을 사용자에게 즉시 공유
- 완성 후 3개 컨셉 요약, 추천 우선순위, 즉시 보완 포인트 제시
