---
name: soldoc-orchestrator
description: "에이전트 팀 오케스트레이터. 기능 개발, 코드 품질, 버그 대응 등 작업 유형에 맞는 팀을 구성하고 조율. '기능 개발', '새 기능', 'API 개발', '리팩토링', '품질 개선', '버그 수정', '에러 분석', '팀 구성' 요청 시 사용."
---

# Orchestrator

작업 유형에 따라 적합한 에이전트 팀을 구성하고 파이프라인을 실행한다.

## 필수 사전 읽기

**모든 팀 실행 전에 반드시 Read:**
1. `CLAUDE.md` — 프로젝트 규칙
2. `context.md` — 아키텍처 컨텍스트 (없으면 `/setup-kb` 안내)
3. `history.md` — 변경 이력

## 변경 이력 기록

작업 완료 후 `history.md`에 추가 (최신순).

## Advisor 전략 (모델 분리)

| 역할 | 모델 | 에이전트 |
|------|------|---------|
| 계획/분석/리뷰 | **opus** | planner, domain-architect, code-reviewer, qa-expert, bug-debugger |
| 구현/실행 | **sonnet** | api-developer, code-refactorer |

## 비판적 사고 규칙

모든 에이전트는 이전 단계 산출물을 무조건 수용하지 않는다:
- architect → planner 영향 범위 검증, 누락 시 피드백
- developer → architect 설계에 비효율 있으면 대안 제시
- reviewer → "통과" 기본값 금지, 반드시 1개+ 개선 제안
- qa → architect 설계 vs developer 코드 교차 비교
- Opus↔Sonnet 불일치 시 Opus 판단 우선

## 팀 구성

### Team A: 기능 개발
| 팀원 | 에이전트 | 모델 |
|------|---------|------|
| planner | planner | opus |
| architect | domain-architect | opus |
| developer | (프로젝트별 구현 에이전트) | sonnet |
| reviewer | code-reviewer | opus |
| qa | qa-expert | opus |

> developer는 프로젝트마다 보일러플레이트 규칙이 다르므로 플러그인에 포함하지 않는다. 프로젝트의 `.claude/agents/`에 직접 정의하라 (예: `api-developer.md`). developer 에이전트가 없으면 architect 설계안까지만 생성하고 구현은 사용자가 직접 수행.

### Team B: 코드 품질
| 팀원 | 에이전트 | 모델 |
|------|---------|------|
| reviewer | code-reviewer | opus |
| refactorer | code-refactorer | sonnet |
| reviewer-post | code-reviewer | opus |

### Team C: 버그 대응
| 팀원 | 에이전트 | 모델 |
|------|---------|------|
| debugger | bug-debugger | opus |
| reviewer | code-reviewer | opus |

## 워크플로우

### Phase 0: KB 확인
- `context.md` 존재 여부 확인. 없으면 "먼저 `/setup-kb`를 실행하세요" 안내 후 중단
- `_workspace/` 존재 → 부분 재실행 or 새 실행 판단

### Phase 1: 팀 선택
| 키워드 | 팀 |
|--------|-----|
| 기능 개발, 새 기능, API, 기획 | **Team A** |
| 리팩토링, 품질 개선, 성능 | **Team B** |
| 버그, 에러, 디버깅, 장애 | **Team C** |

### Phase 1.5: 입력 데이터 준비 (Team A만)
Team A 선택 시, planner에게 전달할 입력 데이터를 준비한다:
1. `_workspace/` 및 `_workspace/00_input/` 디렉토리 생성
2. 사용자 입력(Asana URL, Figma 링크, 텍스트 요구사항)을 `_workspace/00_input/requirements.md`에 저장
3. MCP 도구로 외부 데이터 수집 시도 (Asana → `asana_data.md`, Figma → `figma_data.md`). 실패 시 텍스트 입력 안내

> `/start-task`로 사전 분석을 이미 실행한 경우 `_workspace/`가 존재하므로 이 단계를 건너뛴다.

### Phase 2: 팀 구성 및 실행
선택된 팀의 `TeamCreate` + `TaskCreate` 실행. 각 에이전트 prompt에 KB 파일 경로 포함.

### Phase 3: 모니터링
- `TaskGet`으로 진행 상황 모니터링
- 팀원 간 `SendMessage`로 피드백 교환
- 수정 → 재리뷰 최대 2회

### Phase 4: 결과 종합
산출물 Read → 사용자에게 보고 → `history.md` 업데이트

### Phase 5: KB 갱신
- `graphify-out/graph.json`이 있으면 `/graphify --update`로 변경된 코드의 그래프 갱신 (코드만 변경 시 AST만 재실행, 토큰 비용 없음)
- 변경된 도메인의 `directory.md` 갱신 필요 여부 확인

### Phase 6: 정리
`TeamDelete` → `_workspace/` 보존

## 에러 핸들링
| 상황 | 전략 |
|------|------|
| KB 파일 없음 | `/setup-kb` 안내 |
| 팀원 실패 | 재시작 시도 |
| Critical 발견 | 수정 요청 → 재리뷰 (최대 2회) |
| 타임아웃 | 부분 결과로 진행 |
