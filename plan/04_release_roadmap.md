# 04. Release Roadmap

이 로드맵은 개인용 저장소를 public 배포형 자소서 선생 프로젝트로 전환하기 위한 단계별 계획이다.

## v0 — Public Template Release

목표: 다른 사람이 안전하게 설치하고 자신의 데이터를 준비할 수 있는 template repo를 만든다.

주요 작업:

- 개인 데이터 제거 또는 synthetic sample로 교체
- `userinfo/` 입력 폴더 도입
- `workspace/` 정규화 산출 폴더 도입
- `resume` CLI/TUI skeleton 추가
- `resume init`, `resume status`, `resume doctor` 제공
- Codex/Claude 실행 README 정리
- KOR/EN pipeline 문서 정리
- URL 실패 fallback 안내 문서화
- release hard gate 문서화

완료 기준:

- clean clone 후 설치 안내를 따라갈 수 있다.
- `resume doctor`가 현재 준비 상태를 설명한다.
- sample data 기준으로 다음 에이전트가 KOR/EN 실행을 시작할 수 있다.

## v1 — Real Ingestion

목표: 사용자의 기본 문서에서 경험 후보와 claim 후보를 자동 정리한다.

주요 작업:

- PDF/DOCX/TXT/MD ingestion
- 기존 자기소개서에서 반복 사건 감지
- 사건 단위 experience card 후보 생성
- 수치 claim 후보 추출
- writing sample 분리
- 사용자가 승인/수정할 review flow 추가

완료 기준:

- sample raw documents에서 profile/experience/claim/writing sample 후보가 생성된다.
- 사람이 승인하기 전까지 candidate claim은 최종 생성물에 자동 사용되지 않는다.

## v2 — Web/JD Robustness

목표: 채용공고 URL 처리와 실패 fallback을 견고하게 만든다.

주요 작업:

- 정적 HTML 수집
- Playwright 렌더링 수집
- 채용공고 이미지 OCR 후보 처리
- 크롤링 실패 감지
- 복붙/PDF fallback 안내 자동 출력
- JD 텍스트와 원본 URL provenance 저장

완료 기준:

- URL 성공/실패/이미지 중심 공고 시나리오가 구분된다.
- 실패 시 사용자가 다음 행동을 명확히 알 수 있다.

## v3 — Broad Format + External Sources

목표: 넓은 입력 포맷과 외부 지식 소스를 안정적으로 지원한다.

주요 작업:

- Excel/PPTX/HWP ingestion
- Notion URL 또는 Notion MCP 연동
- 사용자 데이터 품질 대시보드
- claim approval UI/TUI
- DOCX/Figma publish 안정화

완료 기준:

- 다양한 원본 포맷에서 동일한 workspace 구조로 정규화된다.
- publish 단계가 실제 제출용 문서 생성까지 완료한다.

## 권장 우선순위

1. v0 template와 privacy gate
2. `resume` CLI/TUI skeleton
3. skill surface sync
4. sample data와 README bilingual 정리
5. ingestion 자동화
6. Playwright/OCR
7. broad format과 Notion
