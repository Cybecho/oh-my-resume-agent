---
name: capture-feedback
description: "Collect post-submission feedback (`/피드백`) and append it to `workspace/feedback/log.json` so future matching and drafting can reflect outcomes."
---

# 피드백 수집

자소서 제출 후 반응을 기록해 다음 매칭·작성 단계의 가중치 반영 기반을 만든다.

## 1) 대상 확인

1. `output/` 폴더에서 완료된 작업 목록 수집
2. 사용자가 대상 회사/지원 직무를 선택하도록 요청

## 2) 피드백 입력

- 결과: 서류통과 / 탈락 / 면접통과 / 최종합격 / 기타
- 사용 컨셉: 컨셉1/2/3
- 효과적이었던 점(옵션)
- 아쉬웠던 점(옵션)
- 메모(옵션)

## 3) 저장

`workspace/feedback/log.json`에 아래 필드를 추가한다. 기존 개인용 seed에서만 `data/feedback/log.json`를 legacy fallback으로 사용한다.

```json
{
  "date": "YYYY-MM-DD",
  "company": "회사명",
  "position": "직무",
  "result": "결과",
  "concept_used": "컨셉",
  "effective_experiences": ["경험명"],
  "effective_expressions": ["표현"],
  "weak_points": ["보완점"],
  "notes": "메모"
}
```

## 4) 반영 안내

- `서류통과/면접통과/최종합격` 경험은 우선순위 강화
- 효과적이었던 표현은 작성 톤/문체 반영 후보로 전달
- 아쉬운 점은 기획·작성 단계 회피 항목으로 전달

## 완료 후

- 저장 성공 메시지와 함께 다음 번 `/매칭`/`/자소서`에 반영될 점을 간단히 안내
