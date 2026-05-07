# 산출물 위치

`_workspace/{run_id}/` 하위:

| 파일 | 내용 |
|------|------|
| `00_input/` | 사용자 입력 + MCP 외부 데이터 (Asana/Figma) |
| `01_planner_report.md` | planner 영향 분석 레포트 |
| `02_changelog.md` | 서비스 관점 변경 이력 |
| `03_architect_design.md` | 도메인 설계 + planner 보완 |
| `04_review_result.md` | reviewer 코드/아키텍처 리뷰 |
| `05_qa_result.md` | QA 테스트 작성/실행 + 통합 검증 |
| `cost.json` | 토큰/비용/실행 메트릭 (phase-7) |
| `.cache/{key}.json` | 단계별 캐시 |
| `.retry_count` | 재시도 카운터 |
