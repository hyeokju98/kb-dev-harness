# Input Package (원칙 2)

전체 컨텍스트 X. 요약 + 파일 경로만.

## 포맷
필드: `run_id`, `task_brief` (≤500토큰), `upstream_summary` (≤300토큰), `file_refs[]`.

## task_brief
≤500 토큰. 사용자 요청을 에이전트 역할에 맞춰 압축한 1~2 단락. 전체 대화 X.

## upstream_summary
≤300 토큰. 이전 단계 산출물을 핵심 결정 + 미해결 이슈 위주로 요약. 전체 본문 X.

## file_refs
이전 산출물 파일 경로 배열. 다음 단계는 .json만 Read하고 .md는 보조.
