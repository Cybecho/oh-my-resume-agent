# 00. 현재 저장소 분석 결과

이 문서는 public 배포 프로젝트를 설계하기 위해 현재 개인용 저장소에서 확인한 사실과 gap을 정리한다.

## 1. 현재 저장소 성격

현재 저장소는 개인 경험 데이터 기반의 한국어 자기소개서 및 영문 Resume 생성 에이전트 시스템이다.

구조적으로는 다음 계층을 가진다.

- 데이터 계층: `data/profile.md`, `data/experience_cards/`, `data/experience_bullets/`, `data/writing_samples/`
- KOR 에이전트 계층: `agents/*.md`
- EN 에이전트 계층: `agents/en/*.md`
- Skill 계층: `.agents/skills/`, `.claude/skills/`, `.github/skills/`
- 출력 스키마 계층: `templates/schemas/`
- 실행 결과 계층: `output/{YYYYMMDD}_{회사명}/`
- 보조 스크립트: `scripts/en_resume_publish.py`

## 2. 확인된 수량

읽기 전용 탐색 기준:

- KOR agents: 7개
- EN agents: 8개
- `.agents/skills`: 19개
- `.claude/skills`: 19개
- `.github/skills`: 9개
- `data/experience_cards/*.md`: 17개
- `templates/schemas/**/*.md`: 14개
- package manifest: 0개 (`package.json`, `pyproject.toml` 없음)
- 기존 CLI성 스크립트: 1개 (`scripts/en_resume_publish.py`)

## 3. KOR 파이프라인

KOR 자기소개서 파이프라인은 7단계와 검수로 구성된다.

1. 조사선생 — 기업 조사, 인재상, Culture-Sync 어휘 추출
2. JD분석선생 — JD 구조화, 필수/우대 역량 추출
3. 인사관선생 — 문항별 출제 의도와 평가 기준 분석
4. 기억선생 — 경험 후보 수집
5. 기억선생 — 문항별 경험 매칭
6. 기획선생 — 3개 컨셉 설계
7. 필체선생 — 사용자 문체 기반 자기소개서 3세트 작성
8. 검수선생 — 팩트체크, 글자수, JD 적합도, 추천 컨셉 검수

산출물은 `output/{YYYYMMDD}_{회사명}/state.json`과 `01_기업조사.md`~`08_검수리포트.md`로 관리된다.

## 4. EN Resume 파이프라인

EN Resume는 KOR 상태와 분리되어 `state_en.json` 및 `en_resume/` 하위 산출물을 사용한다.

1. CompanyResearcher — 회사/직무 조사
2. JDAnalyst — Resume 관점 JD 분석
3. EvidenceMatcher — 경험/claim 매칭
4. ResumeArchitect — variant A/B/C 설계
5. ResumeWriter — Resume variant 작성
6. ATSLinter — ATS hard-fail 및 점수 검사
7. ResumeReviewer — 최종 리뷰와 top pick 선정
8. ResumePublisher — 선택적 DOCX/Figma publish

Step 8은 수동 실행 전용이며, 현재 `templates/docx/en_resume_template.docx`와 `docxtpl` 의존성이 없어 DOCX publish는 준비되지 않았다.

## 5. 데이터 계층

현재 데이터 우선순위는 다음과 같다.

1. `data/experience_cards/*.md`
2. `data/experience_cards/00_TAG_INDEX.md`
3. `data/experience_cards/13_모든경험_인덱스맵.md`
4. `data/experience_cards/14_경험_검색_선별_대시보드.md`
5. `data/experience_bullets/*.md`
6. `data/experience_bullets/claim_registry.yaml`
7. `data/experiences/` legacy 자료
8. Notion MCP 보조 조회

EN Resume에서는 수치 claim 사용 시 `claim_registry.yaml`의 `approved` claim만 사용하도록 규칙화되어 있다.

## 6. 배포 전환 gap

public repo로 전환하려면 다음 gap을 해결해야 한다.

- 개인 정보와 실제 지원 산출물 제거 또는 샘플화
- public sample data 작성
- `userinfo/` 입력 폴더 도입
- `resume` 명령어용 CLI/TUI 패키지 추가
- `package.json` 또는 `pyproject.toml` 신규 설계
- Codex/Claude/GitHub skill surface 동기화
- `.github/skills`에 EN skill이 없는 문제 정리
- `self-intro-pipeline` mirror drift 제거
- 문서 ingestion 파이프라인 신규 설계
- 채용공고 URL 수집/Playwright/OCR/fallback 설계
- README 한국어/영어 분리 또는 병기
- 설치/doctor/evaluation checker 추가

## 7. v0 설계상 중요한 판단

v0에서 모든 문서 포맷과 모든 채용 사이트를 완전 자동 지원하려 하면 범위가 과도하다. 따라서 v0는 public template repo, TUI 설정, 기본 userinfo 안내, Codex/Claude 실행 경로, 검증 기준을 먼저 안정화하는 것이 적절하다.
