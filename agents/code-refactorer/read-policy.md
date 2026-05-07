# Read Policy (Selective)

## 항상 Read (sticky)
role / context-budget / references / dependency-check

## 조건부 Read
- 이름/시그니처 변경 → dependency-check + `rules/preserve-behavior`
- 중복 추출 → `rules/dedupe`, `examples/few-shot/01-extract`
- N+1 제거 → `rules/n-plus-1`, `examples/few-shot/02-n-plus-1-fix`
- 긴 함수 분리 → `rules/long-function`, `examples/few-shot/03-split-function`
- 변경 범위 제한 → `policy/diff-only`, `rules/minimize-scope`
- 컨벤션 우선 → `rules/convention-first`

## 끝(recency)
변경 의도 1~2줄 + diff
