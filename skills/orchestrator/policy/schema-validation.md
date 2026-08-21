# 스키마 검증 (강제)

phase-4에서 각 산출물 .json을 `references/scripts/validate-output.py`로 검증.
exit 1이면 needs_fix 처리. exit 2(환경 오류)면 사용자 보고 후 중단.
