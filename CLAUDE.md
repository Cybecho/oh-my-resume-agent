# 딸깍자소서 선생

JD + 사용자 경험 데이터를 기반으로 자기소개서 3세트를 자동 생성하는 7단계 파이프라인 에이전트 시스템.

---

## 파이프라인 요약

| Step | 에이전트 | 입력 | 출력 | 도구 |
|------|----------|------|------|------|
| 1 | 조사선생 | 회사명 | 01_기업조사.md | WebSearch, WebFetch |
| 2 | JD분석선생 | JD + Step1 | 02_JD분석.md | 분석 |
| 3 | 인사관선생 | Step1~2 + 문항 | 03_의도분석.md | 분석 |
| 4-5 | 기억선생 | Step2~3 + 경험DB | 04_경험풀.md, 05_경험매칭.md | Read |
| 6 | 기획선생 | Step1,3,5 | 06_기획.md | 분석 |
| 7 | 필체선생 | Step5~6 + 문체샘플 | 07_자소서/컨셉{1,2,3}.md | Read, Write |
| 검수 | 검수선생 | 전 단계 output | 08_검수리포트.md | Read |

---

## 디렉토리 구조

```
agents/          → 에이전트 상세 지침 (7개). Skill이 Read로 참조
.claude/skills/  → 사용자가 /명령어로 호출하는 Skill (9개)
.claude/rules/   → 전 Skill 공통 규칙
data/            → 사용자 데이터
  profile.md            기본 프로필
  experiences/          주제별 경험 (STAR 포맷, legacy)
  writing_samples/      과거 작성 글 (문체 학습용)
  experience_cards/  경험 카드 + 태그 인덱스/대시보드
  feedback/        피드백 이력 (log.json)
output/          → 파이프라인 산출물. {YYYYMMDD}_{회사명}/ 단위
templates/schemas/ → 각 단계 출력 스키마
```

---

## 사용 가능 Skill

| 명령어 | 용도 |
|--------|------|
| `/자소서` | 7단계 전체 자동 실행 (메인) |
| `/조사` | Step 1 단독 재실행 |
| `/분석` | Step 2-3 단독 재실행 |
| `/매칭` | Step 4-5 단독 재실행 |
| `/기획` | Step 6 단독 재실행 |
| `/작성` | Step 7 단독 재실행 |
| `/검수` | 검수 단독 재실행 |
| `/이어서` | 이전 세션 복원 |
| `/피드백` | 결과 피드백 등록 |

---

## 경험 데이터 조회 우선순위

1. **로컬 카탈로그 우선** — `data/experience_cards/`의 `doc_type: experience_card` 카드 조회
2. **로컬 보조** — `00_TAG_INDEX.md`, `13_모든경험_인덱스맵.md`, `14_경험_검색_선별_대시보드.md`
3. **legacy 소스 보조** — `data/experiences/` STAR 형식 파일, `data/experiences/_index.md`
4. **Notion MCP(옵션)** — `notion-search` → `notion-fetch`로 보완 조회

기본 파이프라인은 1~3번에서 누락 없는 후보를 구성한 뒤, 필요 시 4번으로 보완한다.

---

## state.json 스키마

각 `output/{YYYYMMDD}_{회사명}/state.json`에 파이프라인 상태를 기록한다.

```json
{
  "company": "회사명",
  "position": "직무",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "current_step": 1,
  "jd_text": "JD 전문",
  "questions": [
    { "id": 1, "text": "문항 텍스트", "char_limit": 1000 }
  ],
  "steps": {
    "1": { "status": "pending|in_progress|completed", "file": "01_기업조사.md", "completed_at": "" },
    "2": { "status": "pending", "file": "02_JD분석.md" },
    "3": { "status": "pending", "file": "03_의도분석.md" },
    "4": { "status": "pending", "file": "04_경험풀.md" },
    "5": { "status": "pending", "file": "05_경험매칭.md" },
    "6": { "status": "pending", "file": "06_기획.md" },
    "7": { "status": "pending", "file": null },
    "review": { "status": "pending", "file": "08_검수리포트.md" }
  }
}
```

---

## 핵심 규칙

- **허구 금지**: 사용자 원천 데이터(Notion/로컬)에 없는 경험은 절대 작성하지 않는다
- **글자수 준수**: 각 문항의 char_limit을 반드시 지킨다
- **한국어 응답**: 기업 영문명·기술 용어는 원문 유지
- **진행상황 표시**: 각 단계 시작/완료를 사용자에게 표시한다
- **상태 저장**: 매 단계 완료 시 state.json을 업데이트한다

---

## RESUME 선생 (EN)

영미권 Resume 파이프라인은 KOR 파이프라인과 상태/출력을 분리해 운영한다.

### EN 파이프라인 요약

| Step | 에이전트 | 출력 |
|------|----------|------|
| 1 | CompanyResearcher | en_resume/01_company_research.md |
| 2 | JDAnalyst | en_resume/02_jd_analysis.md |
| 3 | EvidenceMatcher | en_resume/03_evidence_selection.md |
| 4 | ResumeArchitect | en_resume/04_resume_plan.md |
| 5 | ResumeWriter | en_resume/05_resume/variant_A.md~C.md |
| 6 | ATSLinter | en_resume/06_ats_report.md |
| 7 | ResumeReviewer | en_resume/07_review_report.md |
| 8 (Optional) | ResumePublisher | en_resume/08_publish/08_publish_report.md, en_resume/08_publish/publish_manifest.json |

> Step 8은 `/resume-publish`로 수동 실행한다. `/resume` 코어 파이프라인은 1~7만 실행한다.

### EN 상태 파일

`output/{YYYYMMDD}_{회사명}/state_en.json`

```json
{
  "pipeline": "en_resume",
  "state_version": 2,
  "company": "Company Name",
  "position": "Target Role",
  "region": "US",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "current_step": 1,
  "jd_text": "Full JD text",
  "variant_count": 3,
  "include_company_research": true,
  "include_cover_letter": false,
  "steps": {
    "1": { "status": "pending|in_progress|completed", "file": "en_resume/01_company_research.md", "completed_at": "" },
    "2": { "status": "pending|in_progress|completed", "file": "en_resume/02_jd_analysis.md", "completed_at": "" },
    "3": { "status": "pending|in_progress|completed", "file": "en_resume/03_evidence_selection.md", "completed_at": "" },
    "4": { "status": "pending|in_progress|completed", "file": "en_resume/04_resume_plan.md", "completed_at": "" },
    "5": { "status": "pending|in_progress|completed", "file": "en_resume/05_resume/", "completed_at": "" },
    "6": { "status": "pending|in_progress|completed", "file": "en_resume/06_ats_report.md", "completed_at": "" },
    "7": { "status": "pending|in_progress|completed", "file": "en_resume/07_review_report.md", "completed_at": "" },
    "8": {
      "status": "not_requested|in_progress|completed|blocked",
      "optional": true,
      "file": "en_resume/08_publish/08_publish_report.md",
      "targets": ["docx", "figma"],
      "completed_at": "",
      "blocked_reason": ""
    }
  }
}
```

### EN 규칙

- KOR `state.json`과 분리 관리
- 사실 우선순위: cards -> bullets -> claims
- approved claim 외 수치 사용 금지
- ATS 하드페일 0건 필수
- optional Step 8 publish gate: ATS pass + top_pick 존재 + mandatory fixes 없음
- Step 8 타깃: 로컬 `docx` + `figma`(remote MCP)만 허용
- 하위호환: `state_version: 1`을 읽으면 `steps.8` 보강 후 다음 저장 시 `state_version: 2`로 승격
- Step 8 설정: `config/en_resume_publish.json` 사용 (`docx.template_path`, `figma.file_key`, `figma.page_node_id`, `figma.template_frame_name`)
- `current_step` 규칙: step 7 완료 시 `8`, step 8 완료 시 `9`
