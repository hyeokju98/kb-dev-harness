# Few-shot 1: SQL Injection

입력: `cursor.execute(f"SELECT * FROM users WHERE id={uid}")`
출력: 🔴 Critical — f-string 쿼리. 파라미터 바인딩으로 변경.
