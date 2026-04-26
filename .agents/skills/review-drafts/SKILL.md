---
name: review-drafts
description: "Run review step only (`/검수`) for fact-check, rubric scoring, and recommendation generation on produced drafts."
---

# 검수 단계 단독 실행

완성된 초안의 사실성·일관성·JD 적합도를 검증한다.

## 사전 조건

1. `output/{YYYYMMDD}_{회사명}/07_자소서/컨셉{1,2,3}.md` 존재 확인
2. `state.json` 확인

## 실행

1. `agents/검수선생.md` 읽기
2. 전 단계 결과(`01_기업조사.md`~`06_기획.md`, `07_자소서/*`)와 경험 원문 대비
3. `workspace/experience_cards/`와 `workspace/claims/claim_registry.yaml`를 우선 검증 소스로 사용
   - 기존 개인용 seed에서만 `data/experience_cards/`를 legacy fallback으로 사용
4. `08_검수리포트.md` 생성/갱신
5. `state.json`의 review 단계 완료 처리

## 완료 후

- 8항목 평가지표 요약(적합도, 일관성, 문체, 글자수)
- 우선권장 컨셉과 즉시 수정 포인트 제시
