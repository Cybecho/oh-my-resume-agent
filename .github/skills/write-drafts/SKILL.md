---
name: write-drafts
description: "Run only step 7 (`/작성`) to generate three drafts from planning output. Use when writing outputs need to be refreshed."
---

# 작성 단계 단독 실행

기획안 기준으로 자소서 본문을 3개 컨셉으로 작성한다.

## 사전 조건

1. `output/{YYYYMMDD}_{회사명}` 존재 및 `state.json` 확인
2. `06_기획.md`, `05_경험매칭.md` 존재 확인
3. 문항별 char_limit이 확보되었는지 확인

## 실행

1. `agents/필체선생.md` 읽기
2. `data/writing_samples/` 전반을 문체 참조용으로 읽기
3. `data/experience_cards/*.md`를 우선 원천으로, 필요 시 legacy/보조 소스로 매칭 근거 확인
4. `07_자소서/컨셉1.md`, `컨셉2.md`, `컨셉3.md`를 저장
5. `state.json`의 step 7 완료 처리

## 완료 후

- 각 컨셉 첫 문장과 핵심 포인트를 간단히 요약
- 작성 결과 미세 수정 시 `/review-drafts` 또는 `/capture-feedback`와 연계 안내
