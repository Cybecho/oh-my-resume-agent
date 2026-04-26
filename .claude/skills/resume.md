# RESUME 선생 — EN 코어 파이프라인

영미권 이력서 생성을 위해 코어 7단계(조사→분석→증거매칭→기획→작성→ATS→검수)를 순차 실행한다.
문서화 단계(선택적 Step 8)는 `/resume-publish`에서만 수동 실행한다.

## 입력 받기

- 회사명
- 지원 직무
- JD 전문
- region (기본값: US)

## 초기화

1. `output/{YYYYMMDD}_{회사명}/en_resume/05_resume/` 폴더 생성
2. `state_en.json` 생성/초기화:
   - `pipeline: en_resume`
   - `state_version: 2`
   - `variant_count: 3`
   - `include_company_research: true`
   - `include_cover_letter: false`
   - `steps.8.status: not_requested` (`optional: true`)
3. KOR `state.json`은 수정하지 않는다

## 공통 규칙

- `.claude/rules/en-resume-rules.md`와 `.claude/rules/pipeline-rules.md`를 함께 따른다.

## 실행 순서

1. `agents/en/CompanyResearcher.md` -> `01_company_research.md`
2. `agents/en/JDAnalyst.md` -> `02_jd_analysis.md`
3. `agents/en/EvidenceMatcher.md` -> `03_evidence_selection.md`
4. `agents/en/ResumeArchitect.md` -> `04_resume_plan.md`
5. `agents/en/ResumeWriter.md` -> `05_resume/variant_A.md~C.md`
6. `agents/en/ATSLinter.md` -> `06_ats_report.md`
7. `agents/en/ResumeReviewer.md` -> `07_review_report.md`

각 단계 시작/완료마다 `state_en.json`의 step 상태를 갱신한다.
Step 8 publish는 자동 실행하지 않는다.
Step 7 완료 시 `current_step=8`로 갱신한다.

## 완료 후 표시

- Variant A/B/C 요약
- ATS 결과 (hard fail 유무)
- 추천본 1순위와 수정 권고
- Optional publish가 필요하면 `/resume-publish` 사용 안내
