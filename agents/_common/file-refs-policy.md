# file_refs 처리 (중복 Read 방지)

input package의 `file_refs`는 참조 후보일 뿐. 자동 Read 금지.

1. `upstream_summary`만 우선 Read
2. summary로 충분 → file_refs Read 생략
3. summary가 모호한 부분만 해당 file Read
