# Read Policy (Selective)

## 항상 Read (sticky)
role / context-budget / references

## 조건부 Read
- 1차 트리아지 → `triage`
- 재발 의심 → `rules/check-recurrence`
- 호출 체인 추적 (graphify 미설치) → `rules/graphify-fallback`
- 수정 후 영향 → `rules/post-fix-review`
- diff-only 적용 → `policy/diff-only`, `policy/output-cap`
- 처음 보는 traceback → `examples/few-shot/01-traceback`
- 절차 의심 → `procedure`

## 끝(recency)
`output`
