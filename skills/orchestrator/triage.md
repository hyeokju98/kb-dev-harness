# Triage (원칙 4 — Haiku 1차)

## Haiku 1차
qa, debugger 작업 시작 시 먼저 haiku로 dispatch. diff 패턴 스캔만 수행.
의심 발견 시 opus로 escalate.

## Opus Escalation 트리거
- Critical 후보 (SQL/auth/tx/race)
- 통합 정합성 의심
- 복잡한 호출 체인 (depth ≥3)
- haiku 신뢰도 부족 신호 (출력 모호/contradiction)
