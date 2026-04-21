---
description: "기획/요구사항을 받아 설계안, 변경사항, 영향 범위를 정리합니다."
---

기능 개발 사전 분석. planner + domain-architect 팀으로 실행한다.

## 입력
`$ARGUMENTS`로 Asana URL, Figma 링크, 요구사항 텍스트 중 하나 이상을 받는다.

## 실행 절차

### 1. 필수 읽기 + KB 확인
CLAUDE.md, `context.md`, `history.md`(최근 10건만)를 Read. `context.md`가 없으면 `/setup-kb` 안내.

### 2. run_id 생성
`YYYYMMDD-HHMM-{slug}` 형식. slug는 티켓 ID 또는 요청 텍스트의 소문자 슬러그.

### 3. MCP 연동 확인 및 데이터 수집
- Asana URL → MCP 호출 시도. 실패 시 텍스트 입력 안내
- Figma URL → WebFetch 시도. 실패 시 텍스트 입력 안내
- 수집 데이터를 `_workspace/{run_id}/00_input/`에 저장

### 4. 팀 구성 및 실행
```
TeamCreate(team_name: "analysis-team-{run_id}", members: [
  { name: "planner", agent_type: "planner", model: "opus",
    prompt: "run_id={run_id}. 산출물: _workspace/{run_id}/01_planner_report.md, 02_changelog.md ..." },
  { name: "architect", agent_type: "domain-architect", model: "opus",
    prompt: "run_id={run_id}. 산출물: _workspace/{run_id}/03_architect_design.md ..." }
])
```

### 5. 결과 종합
산출물 Read → 사용자에게 요약 보고.

### 6. 정리
TeamDelete 후 `history.md`에 변경 이력 추가 (run_id 포함).
