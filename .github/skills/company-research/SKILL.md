---
name: company-research
description: "Run only step 1 (`/조사`) for company research and culture extraction. Use when 조사 phase is missing or re-run is requested."
---

# 기업 조사 스텝 단독 실행

이 스킬은 Step 1 재실행이나 조사 누락 복구에 사용한다.

## 사전 조건

1. 대상 회사 폴더/`output` 상태 확인
2. 회사명/직무/필요 기본 문맥이 확보되었는지 확인
3. `state.json` 존재 여부 확인

## 실행

1. `agents/조사선생.md`를 읽어 조사 지침 확인
2. 기업 조사 수행 (웹 조사 포함: WebSearch/WebFetch)
3. Culture-Sync 용어/어휘 추출 포함
4. 결과를 `output/{YYYYMMDD}_{회사명}/01_기업조사.md`에 저장
5. `state.json`의 step 1 상태를 완료로 갱신

## 완료 후

- 조사 결과 핵심 3~5줄 요약 후 Step 2 실행 가능 여부 안내
