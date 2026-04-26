# resume-research — EN Step 1 단독

EN 회사 조사 단계를 단독 실행한다.

## 실행

1. `state_en.json` 읽기
2. `agents/en/CompanyResearcher.md` 읽기
3. `en_resume/01_company_research.md` 저장
4. step 1 완료 처리

## fallback

- 웹 조사 제한 시 JD-only 축소 프로파일 생성
- `fallback_mode: true`와 사유를 반드시 기록
