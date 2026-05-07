# 생성 파일

| 파일 | 역할 | 사용 에이전트 |
|------|------|------------|
| `context.md` | 아키텍처 컨텍스트 | 전체 (필수) |
| `.claude/CONTEXT-MAP.md` | 도메인-기능-파일 매핑 | planner, developer |
| `history.md` | 변경 이력 | 오케스트레이터 (충돌 방지) |
| `{dir}/directory.md` | 디렉토리별 설명 | developer, refactorer |
| `graphify-out/graph.json` | 코드 관계 그래프 | planner, reviewer |
