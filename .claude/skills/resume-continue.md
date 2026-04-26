# resume-continue — EN 세션 복원

중단된 EN Resume 작업을 `state_en.json` 기준으로 이어서 진행한다.

## 실행

1. `output/*/state_en.json` 스캔
   - `state_version=1` 또는 `steps.8` 누락 시 step 8은 `not_requested`로 간주
2. 최신 미완료 세션 선택
3. 첫 미완료 step부터 재실행:
   - 1 조사
   - 2 분석
   - 3 매칭
   - 4 기획
   - 5 작성
   - 6 ATS
   - 7 검수
4. step 1~7 완료 + step 8이 `in_progress`면 step 8 복구 실행
5. step 1~7 완료 + step 8이 `not_requested|completed|blocked`면 파이프라인 완료로 처리하고 `/resume-publish` 안내
6. 미완료가 없으면 새 `/resume` 시작 안내
