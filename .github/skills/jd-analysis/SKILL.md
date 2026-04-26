---
name: jd-analysis
description: "Run steps 2-3 (`/분석`) for JD analysis + hiring-intent interpretation. Use after step 1 completion or when analysis artifacts are missing."
---

# JD 분석/의도 추론 단독 실행

JD 본문과 문항 의도를 재해석해야 할 때 사용한다.

## 사전 조건

1. `output/{YYYYMMDD}_{회사명}` 폴더와 `state.json` 확인
2. Step 1 산출물(`01_기업조사.md`) 존재 확인
3. JD 텍스트가 확보되었는지 확인

## 실행

1. `agents/JD분석선생.md`를 읽고 JD에서 필수/우대/우대요건을 구조화
2. `output/{YYYYMMDD}_{회사명}/02_JD분석.md` 저장
3. `agents/인사관선생.md`를 읽고 문항별 출제 의도/평가 포인트/차별 포인트 도출
4. `output/{YYYYMMDD}_{회사명}/03_의도분석.md` 저장
5. `state.json`의 step 2,3 상태를 완료로 갱신

## 완료 후

- 문항별 핵심 역량 TOP 3와 JD 적합도 기준점을 출력
- 다음 단계는 `experience-matching` 실행 유도
