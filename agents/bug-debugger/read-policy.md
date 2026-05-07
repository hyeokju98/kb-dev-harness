# Read Policy (Selective)

## 항상 Read (sticky)
role / context-budget / references / procedure / output

## 조건부 Read
- haiku 1차 진입 → triage.md
- 재발 의심 → `rules/check-recurrence`
- 호출 체인 추적 (graphify 미설치) → `rules/graphify-fallback`
- 수정 후 영향 → `rules/post-fix-review`
- diff-only 적용 → `policy/diff-only`, `policy/output-cap`
- 처음 보는 traceback 패턴 → `examples/few-shot/01-traceback`

## 끝(recency)
output.md
