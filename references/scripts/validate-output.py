#!/usr/bin/env python3
"""
산출물 JSON 검증 스크립트.

사용:
    python3 validate-output.py <output.json> [<schema_id>]

schema_id 미지정 시 파일명에서 추론:
    01_planner_report.json   → planner-report
    02_changelog.json        → changelog
    03_architect_design.json → architect-design
    04_review_result.json    → review-result
    05_qa_result.json        → qa-result
    06_debug_result.json     → debug-result
    cost.json                → cost

종료코드: 0=통과, 1=검증 실패, 2=환경/입력 오류
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, RefResolver
except ImportError:
    print("ERROR: jsonschema 미설치. `pip install jsonschema` 실행.", file=sys.stderr)
    sys.exit(2)


SCHEMA_DIR = Path(__file__).resolve().parent.parent / "output-templates"

NAME_TO_SCHEMA = {
    "01_planner_report": "planner-report",
    "02_changelog": "changelog",
    "03_architect_design": "architect-design",
    "04_review_result": "review-result",
    "05_qa_result": "qa-result",
    "06_debug_result": "debug-result",
    "cost": "cost",
}


def infer_schema_id(path: Path) -> str | None:
    stem = path.stem
    if stem in NAME_TO_SCHEMA:
        return NAME_TO_SCHEMA[stem]
    return None


def load_schema(schema_id: str) -> dict:
    schema_path = SCHEMA_DIR / f"{schema_id}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"스키마 없음: {schema_path}")
    with schema_path.open(encoding="utf-8") as fp:
        return json.load(fp)


def build_resolver() -> RefResolver:
    """`_metadata.schema.json` 등 sibling $ref 해소."""
    store = {}
    for schema_file in SCHEMA_DIR.glob("*.schema.json"):
        with schema_file.open(encoding="utf-8") as fp:
            schema = json.load(fp)
        store[schema_file.name] = schema
        if "$id" in schema:
            store[schema["$id"]] = schema
    return RefResolver(base_uri=SCHEMA_DIR.as_uri() + "/", referrer={}, store=store)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2

    output_path = Path(sys.argv[1]).resolve()
    if not output_path.exists():
        print(f"ERROR: 산출물 파일 없음: {output_path}", file=sys.stderr)
        return 2

    schema_id = sys.argv[2] if len(sys.argv) >= 3 else infer_schema_id(output_path)
    if not schema_id:
        print(
            f"ERROR: 스키마 추론 실패. 파일명={output_path.name}. "
            f"두 번째 인자로 schema_id 명시.",
            file=sys.stderr,
        )
        return 2

    try:
        with output_path.open(encoding="utf-8") as fp:
            data = json.load(fp)
    except json.JSONDecodeError as exc:
        print(f"❌ JSON 파싱 실패: {exc}", file=sys.stderr)
        return 1

    try:
        schema = load_schema(schema_id)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    resolver = build_resolver()
    validator = Draft202012Validator(schema, resolver=resolver)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))

    if not errors:
        print(f"✅ {output_path.name} 검증 통과 ({schema_id})")
        return 0

    print(f"❌ {output_path.name} 검증 실패 ({schema_id}) — {len(errors)}건:", file=sys.stderr)
    for err in errors:
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        print(f"  - {loc}: {err.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
