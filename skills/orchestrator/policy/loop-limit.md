# 재시도 루프 제한 (P1, 강제)

max=1. counter는 `_workspace/{run_id}/.retry_count` 파일.
초과 시 부분 결과 + 미해결 이슈 반환 후 종료.
