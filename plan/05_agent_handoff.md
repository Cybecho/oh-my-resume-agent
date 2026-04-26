# 05. Agent Handoff — 다음 에이전트 실행 지침

이 문서는 다음 에이전트가 public 배포 프로젝트를 이어받아 실행하기 위한 작업 순서와 주의사항을 정리한다.

## 1. 반드시 먼저 읽을 파일

1. `plan/README.md`
2. `plan/00_repository_findings.md`
3. `plan/01_objective.md`
4. `plan/02_model.md`
5. `plan/03_evaluation_metrics.md`
6. `plan/04_release_roadmap.md`

그 다음 현재 repo의 다음 파일을 읽는다.

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/rules/pipeline-rules.md`
- `.claude/rules/en-resume-rules.md`
- `.agents/skills/self-intro-pipeline/SKILL.md`
- `.agents/skills/en-resume-pipeline/SKILL.md`

## 2. 첫 번째 실행 목표

첫 구현 목표는 “public repo v0 skeleton”이다.

구체 작업:

1. 개인 데이터 제거 목록 작성
2. public sample data 설계
3. `userinfo/`와 `workspace/` 구조 설계
4. `resume` CLI 패키지 방식 결정
5. `resume init/status/doctor` 최소 기능 구현
6. Codex/Claude 실행 문서 정리
7. evaluation checker 최소 버전 설계

## 3. 결정해야 할 사항

구현 전에 다음 결정을 명확히 한다.

- CLI 구현 언어:
  - Node 기반이면 `npx` 배포가 자연스럽다.
  - Python 기반이면 문서 파싱 생태계가 편하지만 `npx` 목표와 거리가 있다.
  - v0 권장: Node CLI로 TUI/doctor를 만들고, 문서 파싱은 후속 버전에서 Python helper를 붙인다.
- public sample data:
  - 실제 사용자 데이터는 포함하지 않는다.
  - synthetic profile, synthetic experience card, synthetic writing sample을 만든다.
- README 언어:
  - 한국어 README를 기본으로 하되 English Quickstart를 포함한다.
  - 이후 `README.ko.md`, `README.en.md` 분리 가능.
- GitHub skill 표면:
  - EN skill을 `.github/skills`에 미러링할지
  - 아니면 GitHub 표면은 v0 unsupported로 명시할지 결정한다.

## 4. 구현 시 주의사항

- public repo로 옮기기 전 개인 데이터가 남아 있는지 반드시 검사한다.
- 기존 `output/`의 실제 회사명/지원 결과 산출물은 sample로 쓰지 않는다.
- claim registry의 `candidate` claim은 최종 생성 본문 수치로 사용하지 않는다.
- Playwright/OCR/HWP/Notion은 v0에서 “지원 예정”으로 두고, 실패 fallback을 먼저 만든다.
- `resume` CLI는 AI 생성 실행기가 아니라 설정/상태/검증 안내 도구로 유지한다.
- 실제 생성은 Codex 또는 Claude Code agent/skill에서 수행한다.

## 5. 추천 작업 순서

```text
1. public 전환용 branch 생성
2. privacy inventory 작성
3. sample data 설계
4. package manifest 추가
5. resume CLI skeleton 구현
6. README bilingual quickstart 작성
7. Codex/Claude skill sync 정책 정리
8. evaluation checker 추가
9. sample run 검증
10. v0 release checklist 통과
```

## 6. v0 완료 체크리스트

- [ ] public repo에 개인 정보가 없다.
- [ ] `userinfo/` 구조가 문서화되어 있다.
- [ ] `resume init`이 최초 설정을 안내한다.
- [ ] `resume status`가 현재 상태를 출력한다.
- [ ] `resume doctor`가 준비 상태와 누락 항목을 알려준다.
- [ ] Codex 실행법이 문서화되어 있다.
- [ ] Claude Code 실행법이 문서화되어 있다.
- [ ] KOR/EN pipeline이 public sample 기준으로 설명된다.
- [ ] 채용공고 URL 실패 fallback이 문서화되어 있다.
- [ ] release hard gate와 weighted score가 문서화되어 있다.

## 7. 검증 명령 후보

구현 후 다음 검증을 추가한다.

```bash
find plan -maxdepth 1 -type f | sort
resume doctor
resume status
git grep -n "실제 개인 식별자 후보"
```

현재 repo에는 package manifest가 없으므로 실제 `resume` 명령 검증은 CLI 구현 이후 가능하다.
