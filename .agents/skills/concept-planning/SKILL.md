---
name: concept-planning
description: "Run step 6 (`/기획`) for concept planning after matching. Recreates 3 concepts and experiment-ready story mapping."
---

# 기획 단계 단독 실행

매칭 결과를 바탕으로 자소서 컨셉(3안)을 설계한다.

## 사전 조건

1. `output/{YYYYMMDD}_{회사명}` 하위의 `state.json` 확인
2. `01_기업조사.md`, `03_의도분석.md`, `05_경험매칭.md` 존재 확인

## 실행

1. `agents/기획선생.md` 읽기
2. 문항별 핵심 의도와 후보 경험을 3개 축(안전형/성과형/성장형 등)으로 정렬
3. `06_기획.md` 저장
4. `state.json`의 step 6 완료 처리

## 완료 후

- 3개 컨셉 핵심 메시지를 간단히 비교 제시
- 다음 단계로 `write-drafts` 실행 안내
