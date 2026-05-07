# Read Policy (Selective)

## 항상 Read (sticky)
role / context-budget / references / procedure / output-format

## 조건부 Read
- 러너 감지 필요 → test-runners.md
- 통합 정합성 의심 → integration-check.md
- haiku 1차 트리아지 진입 → triage.md
- 변경 함수 단위 테스트 → `rules/must-execute`, `diff-only`
- FAIL 대응 → `rules/no-direct-fix`, `capture-30-lines`
- 모호한 케이스 → `examples/few-shot/` 1~2개

## 끝(recency)
output-format.md
