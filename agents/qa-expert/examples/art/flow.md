# ART 도구 흐름

1. `Read pyproject.toml` (러너 감지)
2. → 추론: pytest
3. `Write tests/test_*.py` (작성)
4. `Bash pytest -x ...` → 일시 중단
5. 결과 통합 → pass/fail 판정
