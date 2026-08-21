# 참조 (공통/기법/스키마)

## 공통 규칙
`agents/_common/` 하위 전부 Read.

## 프롬프트 기법
`agents/_techniques/`의 fewshot, cot, art, multimodal-cot Read.
적용 예시는 `examples/` 하위.

## 출력 스키마
- `01_planner_report.md` → `references/output-templates/planner-report.schema.json`
- `02_changelog.md` → `changelog.schema.json`
- `_metadata` 필드 필수.
