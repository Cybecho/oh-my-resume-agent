# 01. Objective — 무엇을 성공으로 볼 것인가

## 1. 최상위 Objective

누구나 public repo를 설치하고 자신의 이력 자료와 채용공고를 제공하면, Codex 또는 Claude Code 기반 에이전트가 근거 기반 한국어 자기소개서와 영문 Resume 초안을 생성할 수 있게 한다.

## 2. v0 Objective

v0의 성공 상태는 다음과 같다.

- 개인 정보가 제거된 public template repo가 존재한다.
- 사용자는 `curl` 또는 `npx` 계열 설치 경로로 프로젝트를 가져올 수 있다.
- 사용자는 `omr` 명령을 실행해 최초 설정 TUI를 볼 수 있다.
- 설정 완료 후 `omr` 명령은 현재 사용자 데이터 상태와 다음 행동을 안내한다.
- 사용자는 `userinfo/` 폴더에 자기 이력서, 자기소개서, 경력 자료를 넣을 수 있다.
- Codex와 Claude Code 양쪽에서 동일한 목적의 skill/agent 흐름을 사용할 수 있다.
- 채용공고 URL 접근 실패 시 복사/붙여넣기 또는 PDF 저장 fallback을 명확히 안내한다.
- 생성물은 사용자의 원천 데이터와 claim registry에 근거를 둘 수 있게 설계된다.

## 3. 사용자가 경험해야 하는 흐름

```text
설치
  ↓
omr 실행
  ↓
TUI 초기 설정
  ↓
userinfo/에 원본 자료 추가
  ↓
omr doctor로 준비 상태 확인
  ↓
Codex 또는 Claude Code 실행
  ↓
채용공고 URL/JD/직무명 입력
  ↓
KOR 자기소개서 또는 EN Resume 생성
  ↓
검수 리포트 확인
```

## 4. v0 In Scope

- public repo용 문서 구조 정리
- 개인 데이터 제거 전략 수립
- `userinfo/` 입력 폴더와 샘플 데이터 구조 도입
- `omr` CLI/TUI skeleton
- `omr init`, `omr doctor`, `omr status` 수준의 사용자 안내
- Codex `.agents/skills`와 Claude `.claude/skills` 실행 경로 정리
- KOR/EN pipeline 규칙 문서화
- URL 수집 실패 fallback 안내
- release hard gate와 평가 기준 문서화

## 5. v0 Out of Scope

- 모든 문서 포맷의 완전 자동 파싱
- HWP, PPTX, Excel, Notion URL의 완전 자동 ingestion
- 모든 채용 사이트의 크롤링 보장
- 이미지 기반 채용공고 OCR 완성
- `omr` CLI 내부에서 LLM 호출로 자기소개서 직접 생성
- DOCX/Figma publish 완성

## 6. 장기 Objective

장기적으로는 사용자 원본 자료가 어떤 형식이든 자동으로 분석해 경험 카드, claim registry, writing sample로 정규화하고, 채용공고 URL만으로 맞춤형 KOR/EN 지원 문서를 생성하는 배포형 멀티 에이전트 제품을 목표로 한다.
