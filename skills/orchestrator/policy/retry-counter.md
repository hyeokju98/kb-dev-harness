# 재시도 카운터

각 단계 재시도 전 `_workspace/{run_id}/.retry_count` 파일을 Read.
값이 0이면 재시도 후 1로 증가. 1이면 재시도 거부 → 사용자 보고.
