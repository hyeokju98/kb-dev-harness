# Read Policy (Selective)

## 항상 Read (sticky)
role / context-budget / references

## 조건부 Read
- 러너 감지 → `test-runners`
- 통합 정합성 → `integration-check`
- 1차 트리아지 → `triage`
- 변경 함수 단위 테스트 → `rules/must-execute`, `rules/diff-only`
- FAIL 대응 → `rules/no-direct-fix`, `rules/capture-30-lines`
- 모호한 케이스 → `examples/few-shot/*` 1~2개
- 절차 의심 → `procedure`

## 끝(recency)
`output-format`
