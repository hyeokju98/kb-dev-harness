---
description: "기획/요구사항을 받아 설계안, 변경사항, 영향 범위를 정리합니다."
---

기능 개발 사전 분석. planner + domain-architect 팀으로 실행한다.

## 입력
`$ARGUMENTS`로 Asana URL, Figma 링크, 요구사항 텍스트 중 하나 이상을 받는다.

## 실행 절차

### 1. 필수 읽기 + KB 확인
CLAUDE.md, `context.md`, `history.md`를 Read한다. `context.md`가 없으면 `/setup-kb` 안내.

### 2. MCP 연동 확인 및 데이터 수집
- Asana URL → MCP 호출 시도. 실패 시 텍스트 입력 안내
- Figma URL → WebFetch 시도. 실패 시 텍스트 입력 안내
- 수집 데이터를 `_workspace/00_input/`에 저장

### 3. 팀 구성 및 실행
```
TeamCreate(team_name: "analysis-team", members: [
  { name: "planner", agent_type: "planner", model: "opus", prompt: "..." },
  { name: "architect", agent_type: "domain-architect", model: "opus", prompt: "..." }
])
```

### 4. 결과 종합
산출물 Read → 사용자에게 요약 보고.

### 5. 정리
TeamDelete 후 `history.md`에 변경 이력 추가.
