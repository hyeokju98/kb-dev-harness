# Read Policy (Selective)

## 항상 Read (sticky 시작)
critical-thinking / role / context-budget / references / output-format / procedure

## 조건부 Read (diff 패턴 매칭)
- SQL/ORM (`cursor.execute`, `.objects.`, `SELECT/UPDATE`) → `rules/sql-*.md`
- 인증/권한 변경 (`@login_required`, `permission_classes`) → `rules/critical-auth-missing`
- 트랜잭션 변경 (`atomic`, `commit`) → `rules/critical-tx-missing`, `sql-transaction-boundary`
- 시크릿 의심 (`API_KEY`, `password=`) → `rules/critical-secret-hardcoded`
- 외부 호출 (`requests.`, `httpx.`, `fetch`) → `rules/warning-no-exception`
- 일반 변경 → `rules/warning-*`, `info-*`
- 처음 보는 패턴 → `examples/few-shot/` 1~2개

## 끝(recency) Read
output-format.md (출력 직전 재확인)
