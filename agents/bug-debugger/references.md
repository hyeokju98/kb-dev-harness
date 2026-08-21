# 참조 (공통/기법/스키마)

## 공통 규칙
`agents/_common/` 하위 전부 Read.

## 프롬프트 기법
`agents/_techniques/` 정의 + `examples/` 적용.

## 출력 스키마
디버깅 결과 → `references/output-templates/debug-result.schema.json`.
`recurrence.is_recurring=true`면 history 발췌 필수.
`_metadata` 필드 필수.
