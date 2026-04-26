# resume-publish — EN Optional Step 8

EN 최종 리뷰 마크다운을 로컬 DOCX + Figma 산출물로 변환하는 선택 단계다.

## 입력

- `targets` (선택): `docx`, `figma` (기본 `docx,figma`)
- `session` (선택): `output/{YYYYMMDD}_{회사명}` 경로
- `force` (기본 false): 게이트 우회는 권장하지 않음

## 사전 조건

- `docxtpl` 의존성이 설치되어 있어야 한다 (`requirements/en_resume_publish.txt`).
- Figma는 remote MCP(`https://mcp.figma.com/mcp`)로 연결되어 있어야 한다.

## 실행

1. Prepare 실행:
   - `python3 scripts/en_resume_publish.py prepare --targets <docx,figma> [--session <path>] [--force]`
2. Prepare 단계:
   - session 선택, gate 검증, DOCX 로컬 생성, manifest/report 초기 기록
   - `state_version=1`이면 `steps.8` 보강 후 `state_version=2`로 승격
3. `figma` 타깃이 있고 prepare 결과가 `in_progress`면 Figma MCP 실행
4. Finalize 실행:
   - `python3 scripts/en_resume_publish.py finalize [--session <path>] --figma-status <success|failed|skipped> [--figma-node-id <id>] [--figma-url <url>] [--figma-error <error>]`
5. Finalize 단계:
   - figma 결과 반영 후 step 8 최종 판정
   - all success -> `completed` + `current_step=9`, 아니면 `blocked`

## 규칙

- Step 8은 `/resume`에서 자동 실행하지 않는다.
- 문서 생성 원본은 `top_pick` variant만 허용한다.
- KOR `state.json`은 수정하지 않는다.
