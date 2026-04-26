---
name: experience-matching
description: "Run steps 4-5 (`/매칭`) for candidate pooling and final experience matching. Use when downstream steps need refreshed 매칭 results."
---

# 경험 매칭 단독 실행

JD 분석 결과 기반으로 경험 후보를 선별·정교화할 때 사용한다.

## 사전 조건

1. `output/{YYYYMMDD}_{회사명}` 폴더의 `state.json` 읽기
2. `02_JD분석.md`, `03_의도분석.md` 존재 확인

## 실행

1. `agents/기억선생.md`를 읽고 매칭 기준 확인
2. 후보 구성 순서:
   - `workspace/experience_cards/`의 `doc_type: experience_card` 기반 우선 조회
   - 수치/성과는 `workspace/claims/claim_registry.yaml`의 `approved` claim만 사용
   - 기존 개인용 seed에서만 `data/experience_cards/`, `data/experiences/_index.md`, `data/feedback/log.json`을 legacy fallback으로 보강
   - `workspace/`가 비어 있으면 `resume doctor`와 `userinfo/` 입력 안내를 먼저 제시
   - Notion MCP는 local 부족 시만 보완 조회
3. `04_경험풀.md` 생성/갱신
4. `05_경험매칭.md` 생성/갱신
5. `state.json`의 step 4,5를 완료 처리

## 완료 후

- 문항별 1순위/2순위 후보를 정리해 표시
- 문항별 미충족 역량 항목을 함께 제시
