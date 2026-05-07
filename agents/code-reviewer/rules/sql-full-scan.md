# SQL: 풀스캔 위험

- 인덱스 없는 컬럼 filter
- `LIKE '%xxx%'` (좌측 와일드카드)
- `OR`로 묶인 다른 컬럼 → UNION 분리 검토
