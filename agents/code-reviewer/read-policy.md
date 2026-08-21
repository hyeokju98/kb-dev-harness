# Read Policy (Selective)

## 항상 Read (sticky 시작)
critical-thinking / role / context-budget / references

## 조건부 Read (diff 패턴 매칭)
- SQL/ORM (`cursor.execute`, `.objects.`, `SELECT/UPDATE`) → `rules/sql-*`
- 인증/권한 (`@login_required`, `permission_classes`) → `rules/critical-auth-missing`
- 트랜잭션 (`atomic`, `commit`) → `rules/critical-tx-missing`, `rules/sql-transaction-boundary`
- 시크릿 (`API_KEY`, `password=`) → `rules/critical-secret-hardcoded`
- 외부 호출 (`requests.`, `httpx.`, `fetch`) → `rules/warning-no-exception`
- 일반 변경 → `rules/warning-*`, `rules/info-*`
- 처음 보는 패턴 → `examples/few-shot/*` 1~2개
- 절차 의심 → `procedure`

## 끝(recency)
`output-format` (출력 직전)
