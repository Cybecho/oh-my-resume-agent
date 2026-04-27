# 자소서 선생 배포 프로젝트 계획 문서

이 폴더는 기존 개인용 자소서 선생 저장소를 제3자가 사용할 수 있는 public 배포형 프로젝트로 전환하기 위한 실행 계획 문서 세트입니다.

핵심 목표는 사용자가 저장소를 설치하고 `userinfo/`에 자신의 이력서·자기소개서·경력 자료를 넣으면, Codex 또는 Claude Code에서 동일한 에이전트 파이프라인을 사용해 근거 기반 한국어 자기소개서와 영문 Resume 초안을 생성할 수 있게 만드는 것입니다.

## 읽는 순서

1. `00_repository_findings.md` — 현재 저장소 분석 결과와 배포 gap
2. `01_objective.md` — public 배포 프로젝트의 목표(Objective)
3. `02_model.md` — 실제 일을 수행하는 시스템 모델(Model)
4. `03_evaluation_metrics.md` — 통과/실패를 판정하는 평가 기준(Evaluation Metric)
5. `04_release_roadmap.md` — v0~v3 단계별 릴리스 계획
6. `05_agent_handoff.md` — 다음 에이전트가 바로 수행할 작업 순서
7. `06_oh_my_resume_agent_philosophy.md` — oh-my 시리즈 철학과 `oh-my-resume-agent` 구조 방향

## 현재 결론

- v0는 “완전 자동 문서 파서”가 아니라 **public template repo + TUI 설정 + Codex/Claude 실행 경로 + 기본 데이터 구조화**에 집중한다.
- `omr` 명령은 AI 생성기가 아니라 사용자 데이터 설정·검사·상태 안내 CLI/TUI로 둔다.
- oh-my 시리즈 철학에 맞춰 1차 CLI 이름은 `omr`, `resume`은 alias로 제공한다.
- 실제 자기소개서/Resume 생성은 기존처럼 Codex 또는 Claude Code의 skill/agent 파이프라인에서 수행한다.
- 평가 기준은 hard gate와 weighted score를 함께 사용한다.

## 구현 원칙

- public repo에는 개인 정보와 실제 지원 산출물을 포함하지 않는다.
- 사용자의 원천 데이터에 없는 경험, 수치, 성과를 생성하지 않는다.
- Codex와 Claude Code 양쪽에서 사용할 수 있는 표면을 유지한다.
- 크롤링/문서 파싱이 실패하면 조용히 추측하지 않고 fallback 절차를 안내한다.
