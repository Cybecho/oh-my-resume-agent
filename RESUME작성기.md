# RESUME 데이터 운영 가이드

## 1. 목적
- 이 문서는 영문 Resume 데이터 정제를 위한 운영 기준을 정의한다.
- 한글 자소서와 영문 Resume를 **같은 경험 원천**에서 파생할 수 있도록 데이터 레이어를 분리한다.
- 에이전트/스킬 구현이 아니라, 데이터 보관/정합성 관리에만 집중한다.

## 2. 단일 사실 원천 (SSOT)
- 사실 원천: `data/experience_cards/*.md`
- 보조 원천: `data/writing_samples/Archive_*.md`, `data/experiences/*.md`
- 영문 Resume용 표현 자산: `data/experience_bullets/`
- 기존 영문 Resume 원본: `data/RESUME/` (삭제 금지, 보존)
- 정규화 스냅샷: `data/RESUME/snapshots/en/`

## 3. 레이어 구조
- `data/experience_cards/`: 경험 사실, 태그, 맥락
- `data/experience_bullets/`: 경험별 영문 bullet 라이브러리 + claim registry
- `data/RESUME/index/`: 스냅샷/매핑 인덱스
- `data/RESUME/snapshots/en/`: 과거 영문 Resume 정규화 보관본
- `data/profile.md`: 한/영 공통 프로필 SSOT

## 4. 운영 원칙
1. 경험 사실은 `experience_cards`에서만 수정한다.
2. 영문 표현 변경은 `experience_bullets`에서만 수행한다.
3. 수치 표현은 `claim_registry.yaml`을 먼저 수정하고 bullet/스냅샷에 반영한다.
4. `data/RESUME` 원본은 제출 이력 보관본으로 취급하고 내용 수정하지 않는다.
5. 새 Resume를 작성할 때는 `output/`에 산출하고, 제출본 보관이 필요하면 스냅샷으로 추가한다.

## 5. 신규 Resume 추가 절차
1. `output/`에서 최종 영문 Resume를 확정한다.
2. `data/RESUME/snapshots/en/{YYYYMMDD}_{role-slug}.md`로 보관한다.
3. `data/RESUME/index/snapshot_index.yaml`에 메타데이터를 등록한다.
4. 사용한 경험 ID와 claim ID를 `experience_resume_map.yaml`에 업데이트한다.
5. 신규/수정 수치가 있으면 `claim_registry.yaml`의 evidence와 함께 등록한다.

## 6. 정합성 점검
- 모든 스냅샷은 최소 1개 이상의 `derived_from_experience_ids`를 가져야 한다.
- 모든 claim은 최소 1개 이상의 `evidence_paths`를 가져야 한다.
- `experience_bullets/EXP-XX.md`의 `experience_id`는 실제 카드 ID와 일치해야 한다.

## 7. 금지 사항
- `experience_cards` 사실과 다른 수치/성과를 새로 만들지 않는다.
- `data/RESUME` 원본 파일명/내용을 임의 변경하지 않는다.
- 한글 자소서용 기존 폴더(`experience_cards`, `writing_samples`) 구조를 깨지 않는다.

## 8. EN 파이프라인 연동 규약

- EN 자동 생성 파이프라인 출력은 `output/{YYYYMMDD}_{회사명}/en_resume/`에 저장한다.
- EN 상태 파일은 `output/{YYYYMMDD}_{회사명}/state_en.json`을 사용한다.
- 기본 산출물:
  1. `01_company_research.md` (fallback 허용)
  2. `02_jd_analysis.md`
  3. `03_evidence_selection.md`
  4. `04_resume_plan.md`
  5. `05_resume/variant_A.md`, `variant_B.md`, `variant_C.md`
  6. `06_ats_report.md`
  7. `07_review_report.md`
  8. (Optional, 수동) `08_publish/08_publish_report.md`, `08_publish/publish_manifest.json`
- Optional Step 8은 `/resume-publish`에서만 실행한다.
- Optional Step 8 기본 타깃은 `docx,figma`다.
- Step 8 게이트: ATS pass + `top_pick` 존재 + Mandatory Fixes 없음.
- Step 8 설정 파일: `config/en_resume_publish.json` (`docx.template_path`, `figma.file_key`, `figma.page_node_id`, `figma.template_frame_name` 포함).
- 하위호환: `state_version: 1`은 읽을 때 step 8 보강 후 저장 시 `state_version: 2`로 승격한다.
- `current_step` 규칙: step 7 완료 시 `8`, step 8 완료 시 `9`.
- ATS 하드페일 또는 claim 불일치가 있으면 제출 후보로 간주하지 않는다.
- 제출본 보관 절차는 기존 5장(신규 Resume 추가 절차)을 그대로 따른다.
