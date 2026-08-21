# 참조 (공통/기법/스키마)

## 공통 규칙
`agents/_common/` 하위 전부 Read.
중복 정책(diff-only, output-cap, 비판적 사고, peer 통신 금지)은 거기서 관리.

## 프롬프트 기법
`agents/_techniques/`의 fewshot, cot, art, multimodal-cot 정의 Read.
적용 예시는 `examples/` 하위.

## 출력 스키마
`04_review_result.md` → `references/output-templates/review-result.schema.json`.
`issues[].rule`은 `agents/code-reviewer/rules/` 파일명과 일치.
`_metadata` 필드 필수 (`_metadata.schema.json`).
