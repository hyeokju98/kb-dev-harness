# 참조 (공통/기법/스키마)

## 공통 규칙
`agents/_common/` 하위 전부 Read.

## 프롬프트 기법
`agents/_techniques/` 정의 + `examples/` 하위 적용.

## 출력 스키마
`05_qa_result.md` → `references/output-templates/qa-result.schema.json`.
`conclusion.next_action`은 retry 전이와 동일 enum.
`_metadata` 필드 필수.
