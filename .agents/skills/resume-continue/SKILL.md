---
name: resume-continue
description: "Resume a partial workflow like `/이어서` by scanning `output/` state files and continuing from the next incomplete step."
---

# 이어서 작업

중단된 작업이 있을 때 다음 미완성 단계로 복원 실행한다.

## 실행

1. `output/` 폴더를 스캔해 작업 폴더 목록 수집
2. 각 폴더의 `state.json`을 읽어 현재 상태 점검
3. 미완성 항목이 있으면 최신/지정 폴더 기준으로 아래 규칙 적용
   - `step` 누락/미완료 → 해당 단계부터 재개
   - 결과 파일 누락 → 해당 단계부터 재실행
   - `in_progress` 상태 발견 → 해당 단계 처음부터 다시 실행
4. 이어서 실행 가능한 단계가 없으면 종료 메시지와 함께 새 파이프라인 시작을 제안

## 처리 순서 예시

- 1 미완료 → company-research
- 2/3 미완료 → jd-analysis
- 4/5 미완료 → experience-matching
- 6 미완료 → concept-planning
- 7 미완료 → write-drafts
- review 미완료 → review-drafts

## 완료 후

- 현재 진행상태와 다음 단계 제안을 한 줄로 표시
