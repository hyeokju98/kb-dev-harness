# 테스트 러너

프로젝트 환경에서 감지하여 변경 파일만 실행.

| 감지 | 명령 |
|------|------|
| `pytest.ini` 또는 `pyproject.toml`에 `[tool.pytest]` | `pytest -x --tb=short {파일}` |
| `package.json`에 `vitest` | `npx vitest run {파일}` |
| `package.json`에 `jest` | `npx jest {파일}` |
| `build.gradle` + Spring | `./gradlew test --tests {클래스}` |
| `manage.py` (Django) | `python manage.py test {앱}` |

전체 스위트 실행 X. 변경 파일에 해당하는 테스트만 선택 실행.
