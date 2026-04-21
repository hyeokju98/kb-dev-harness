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
3. `history.md` — 변경 이력 (최근 10건만. 전체 파일이 크면 `tail`로 자름)

## run_id 정책

각 실행마다 고유 `run_id`를 생성하여 `_workspace/{run_id}/` 하위에 산출물을 저장한다.

- 형식: `YYYYMMDD-HHMM-{slug}` (예: `20260421-1045-password-policy`)
- slug: 티켓 ID가 있으면 티켓 ID, 없으면 요청 텍스트에서 소문자 슬러그
- 팀원에게 전달할 프롬프트에 `{run_id}`를 치환해서 넘긴다

### 산출물 위치
```
_workspace/{run_id}/
├── 00_input/            ← 사용자 입력, Asana/Figma 수집 데이터
├── 01_planner_report.md
├── 02_changelog.md
├── 03_architect_design.md
├── 04_review_result.md
└── 05_qa_result.md
```

## KB stale 감지

Phase 0 직후 다음을 확인한다:
- `context.md` mtime 이후 커밋이 **50개 초과**인가?
- 커밋 후 변경된 파일 중 **최상위 디렉토리가 새로 생겼는가**?

하나라도 해당하면 사용자에게 경고:
> "KB가 오래됐습니다 (N개 커밋 경과). `/setup-kb --refresh` 실행을 권장합니다. 그대로 진행하시겠습니까?"

## 변경 이력 기록

작업 완료 후 `history.md`에 최신순으로 추가. 형식:
```
## [{date}] {run_id} — {title}
- Team: {A|B|C}
- 결과: {approved|needs_fix}
- 산출: _workspace/{run_id}/
- 요약: {1~2줄}
```

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

### Phase 0: KB 확인 + stale 감지
- `context.md` 존재 여부 확인. 없으면 "먼저 `/setup-kb`를 실행하세요" 안내 후 중단
- KB stale 감지(위 정책) — 오래되면 경고
- `_workspace/` 존재 → 과거 실행 이력. 새 `run_id`로 진행

### Phase 1: 팀 선택
| 키워드 | 팀 |
|--------|-----|
| 기능 개발, 새 기능, API, 기획 | **Team A** |
| 리팩토링, 품질 개선, 성능 | **Team B** |
| 버그, 에러, 디버깅, 장애 | **Team C** |

### Phase 1.5: run_id 생성 + 입력 데이터 준비
1. `run_id` 생성 (위 정책)
2. `_workspace/{run_id}/00_input/` 디렉토리 생성
3. (Team A) 사용자 입력을 `_workspace/{run_id}/00_input/requirements.md`에 저장
4. (Team A) MCP로 외부 데이터 수집 시도 (Asana → `asana_data.md`, Figma → `figma_data.md`). 실패 시 텍스트 입력 안내

> `/start-task`로 사전 분석을 이미 실행한 경우 기존 `run_id`를 재사용한다 (사용자에게 확인).

### Phase 2: 팀 구성 및 실행
선택된 팀의 `TeamCreate` + `TaskCreate` 실행. **각 에이전트 prompt에 `run_id`와 산출물 경로를 명시적으로 전달한다.**

### Phase 3: 모니터링 + 재시도 상태 전이
- `TaskGet`으로 진행 상황 모니터링
- 팀원 간 `SendMessage`로 피드백 교환

**재시도 상태 전이 (최대 2회):**

| 실패 단계 | 되돌릴 대상 | 이유 |
|----------|------------|------|
| reviewer가 Critical 지적 | → developer | 코드 수정 |
| reviewer가 아키텍처 부적합 지적 | → architect | 설계 재검토 |
| qa가 테스트 FAIL | → developer | 버그 수정 |
| qa가 통합 정합성 불일치 | → architect | 경계면 재설계 |
| architect가 planner 보완 사항 많음 | → planner | 영향 분석 재작성 |

재시도 2회 후에도 실패면 사용자에게 수동 개입 요청.

### Phase 4: 결과 종합 + 리뷰 마커
- 산출물 Read → 사용자에게 보고
- 승인 시: `git diff --staged | md5 > .claude-reviewed` (self-review와 동일 포맷)
- 이 마커는 이후 커밋 훅이나 PR 생성 단계에서 "리뷰 완료 여부" 확인에 사용

### Phase 5: history.md 업데이트
위 형식으로 기록.

### Phase 6: KB 갱신
- `graphify-out/graph.json`이 있으면 `/graphify --update`로 변경된 코드의 그래프 갱신 (코드만 변경 시 AST만 재실행, 토큰 비용 없음)
- 변경된 도메인의 `directory.md` 갱신 필요 여부 확인

### Phase 7: 정리
`TeamDelete` → `_workspace/{run_id}/` 보존 (티켓별 이력으로 활용)

## 에러 핸들링
| 상황 | 전략 |
|------|------|
| KB 파일 없음 | `/setup-kb` 안내 |
| KB stale 의심 | 사용자 확인 후 진행 or `/setup-kb --refresh` |
| 팀원 실패 | 재시작 시도 (1회) |
| Critical 발견 | 수정 요청 → 재리뷰 (최대 2회, 위 상태 전이표) |
| 타임아웃 | 부분 결과로 진행 |
