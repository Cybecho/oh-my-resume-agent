# 03. Evaluation Metric — 잘 되었는지 판정하는 기준

평가 기준은 “좋아 보인다”가 아니라, 다른 에이전트가 통과할 때까지 반복 개선할 수 있는 hard gate와 점수 기준으로 정의한다.

## 1. Release Hard Gates

하나라도 실패하면 v0 public release를 하면 안 된다.

### Privacy Gates

- public repo에 실제 개인 프로필, 실명, 연락처, 실제 지원 회사 산출물이 남아 있지 않다.
- 샘플 데이터는 synthetic 또는 명시적 anonymized data만 사용한다.
- `.gitignore` 또는 템플릿 구조가 사용자의 `userinfo/raw` 민감 파일을 보호한다.

### Install Gates

- 설치 경로가 README에 명확하다.
- `resume init`이 최초 설정 흐름을 안내한다.
- `resume doctor`가 필수 환경과 데이터 상태를 검사한다.
- macOS/Linux 기준 PATH 또는 shell 설정 안내가 있다.

### Agent Compatibility Gates

- Codex 실행 경로가 문서화되어 있다.
- Claude Code 실행 경로가 문서화되어 있다.
- 동일한 KOR/EN pipeline 개념이 두 표면에서 유지된다.
- unsupported 표면은 명시적으로 표시된다.

### Data Integrity Gates

- 경험·성과·수치는 원천 자료 또는 claim registry에 연결된다.
- `candidate` claim은 최종 본문 수치로 자동 사용하지 않는다.
- 생성물은 provenance 또는 내부 근거 추적이 가능하다.

### Job Intake Gates

- 채용공고 URL 수집 실패를 감지한다.
- 실패 시 복사/붙여넣기 또는 PDF 저장 fallback을 안내한다.
- 크롤링 실패를 성공처럼 포장하지 않는다.

### Documentation Gates

- README는 한국어와 영어 사용자를 모두 고려한다.
- `resume` 명령 사용법이 별도 섹션으로 정리되어 있다.
- v0에서 지원하지 않는 기능이 명확히 표시되어 있다.

## 2. Weighted Release Score

Hard gate가 모두 통과한 뒤 weighted score를 계산한다.

| 항목 | 비중 | 측정 예시 |
| --- | ---: | --- |
| 설치/온보딩 성공률 | 20% | clean macOS/Linux에서 init/doctor 성공 |
| 사용자 문서 정규화 품질 | 20% | sample 자료가 profile/experience/claim/writing sample로 분리됨 |
| 채용공고 수집/분석 품질 | 15% | URL/붙여넣기/PDF fallback 시나리오 처리 |
| 생성물 품질 | 20% | KOR 자소서/EN Resume 샘플 결과의 구조·가독성·직무 적합도 |
| 사실성/근거 추적성 | 15% | 수치·경험 claim provenance 확인 |
| Codex/Claude 호환성 | 10% | 양쪽 표면에서 동일 흐름 재현 |

v0 release 기준:

```text
All hard gates pass
AND weighted score >= 85 / 100
```

## 3. 자동 검사 후보

v0에서 구현할 수 있는 checker 후보:

- `resume doctor`
  - 필수 폴더 존재
  - 설정 파일 존재
  - sample data 존재
  - Codex/Claude 안내 파일 존재
- `resume eval privacy`
  - 금지 경로 또는 실제 output 포함 여부 확인
- `resume eval skills`
  - `.agents`, `.claude`, `.github` skill surface drift 확인
- `resume eval data`
  - experience card frontmatter 검사
  - claim registry status 검사
- `resume eval output`
  - state file과 output artifact 일치 검사
- `resume eval publish`
  - DOCX template, docxtpl, Figma config readiness 검사

## 4. Human-in-the-loop 평가

초기에는 자동 점수만으로 충분하지 않다. 다음 항목은 사람이 함께 평가한다.

- 경험카드가 실제 사용자의 사건을 과도하게 쪼개거나 합치지 않았는가
- 자기소개서 문체가 사용자답게 보이는가
- 지원동기가 회사 팬심이나 학습 욕구가 아니라 기여 중심인가
- EN Resume가 ATS 친화적이면서도 과장되지 않았는가

## 5. 반복 개선 루프

```text
Objective 확인
  ↓
Model 실행
  ↓
Evaluation 측정
  ↓
Hard gate 실패 → 수정
  ↓
Score 미달 → 개선
  ↓
Release 기준 통과
```

이 루프를 문서, 코드, repo 전체에 적용한다.
