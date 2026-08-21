# Stale 감지 기준

orchestrator가 호출 전 판단:
- `context.md` mtime 이후 커밋 50개 초과
- 최상위 디렉토리 신규
- CONTEXT-MAP에 없는 도메인 폴더 발견

하나라도 해당 시 `--refresh` 권장.
