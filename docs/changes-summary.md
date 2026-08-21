# Token-Saving Restructure — Changes Summary

본 문서는 토큰 절감 전략 도입을 위해 진행한 하네스 구조 개편의 전체 변경사항을 정리한다.

## 목적

- 멀티 에이전트 운영의 토큰 비용 절감
- 컨텍스트 최소화 + Structured Output + 재시도 루프 제한
- 에이전트/스킬/커맨드 정의를 atomic 파일 단위로 분할 (≤150자/파일)

## 변경 통계

| 영역 | 변경 전 | 변경 후 |
|------|---------|---------|
| agents (.md) | 6 | 146 |
| skills (.md) | 2 (SKILL.md 161+167줄) | 89 |
| commands (.md) | 2 | 23 |
| references (.json schemas) | 0 | 6 |
| docs (.md) | 2 | 4 |
| **합계 파일 수** | **12** | **268** |

모든 .md 파일은 **150자 이하**.

## 1. 신규 전략 문서

| 파일 | 내용 |
|------|------|
| `docs/token-strategy.md` | 토큰 절감 10원칙 + P1~P4 적용 로드맵 (누적 60~70% 절감 목표) |
| `docs/adr-vector-kb.md` | Vector KB 도입 보류 결정 + 재검토 트리거 |
| `docs/changes-summary.md` | (본 문서) 전체 변경사항 정리 |

## 2. 에이전트 분할 (`agents/`)

각 에이전트는 슬림 진입점 + 정의/룰/정책/예시 디렉토리로 분리.

### 공통 구조

```
agents/{name}.md                  ← 슬림 진입점 (frontmatter + 1줄)
agents/{name}/
├── role.md
├── context-budget.md
├── procedure.md (또는 phase-N.md)
├── output-format.md / output.md
├── schema.md                     ← JSON 스키마 포인터
├── techniques.md                 ← 프롬프트 기법 포인터
├── rules/                        ← atomic 룰
├── policy/                       ← P1 정책 (output-cap, diff-only)
└── examples/
    ├── few-shot/
    ├── cot/
    ├── art/
    └── multimodal-cot/ (planner only)
```

### 에이전트별 파일 수

| 에이전트 | 정의 | rules | policy | examples | 합계 |
|---------|-----|-------|--------|----------|-----|
| code-reviewer | 6 | 16 | 2 | 7 | 31 |
| planner | 8 | 7 | 1 | 8 | 24 |
| qa-expert | 11 | 4 | 1 | 6 | 22 |
| bug-debugger | 4 | 3 | 2 | 6 | 15 |
| code-refactorer | 3 | 7 | 2 | 6 | 18 |
| domain-architect | 5 | 3 | 1 | 6 | 15 |

### 공유 자원

- `agents/_techniques/` — Few-shot, CoT, ART, Multimodal CoT 정의 (4 파일)

## 3. 스킬 분할 (`skills/`)

### orchestrator (이전 161줄 → 50+ atomic 파일)

```
skills/orchestrator/
├── SKILL.md                      ← 슬림 진입점
├── role.md / required-reads.md / run-id.md / ...
├── teams/                        ← Team A/B/C 매핑
├── phases/                       ← Phase 0~7 atomic
├── retry/                        ← 5개 상태 전이 atomic
├── outputs/                      ← 산출물 6종 atomic
├── policy/
│   ├── loop-limit.md             ← P1 max=1 강제
│   └── retry-counter.md          ← `.retry_count` 카운터 메커니즘
├── examples/{few-shot,cot,art}/
└── techniques.md
```

### setup-kb (이전 167줄 → 38+ atomic 파일)

```
skills/setup-kb/
├── SKILL.md                      ← 슬림 진입점
├── role.md / modes.md / stale-detection.md / ...
├── frameworks/                   ← Django/Next.js/Nuxt/FastAPI/Spring/Vite/Node
├── phases/                       ← Phase 1~7 atomic
├── backend/                      ← URL/모델/로직/연동/이벤트
├── frontend/                     ← 라우트/API/컴포넌트/상태/타입
├── files/                        ← 생성 파일 5종 atomic
├── examples/{few-shot,cot,art}/
└── techniques.md
```

## 4. 커맨드 분할 (`commands/`)

```
commands/
├── self-review.md                ← 슬림
├── self-review/
│   ├── role.md
│   ├── procedure/01-diff.md ~ 09-marker.md
│   ├── output-format.md
│   └── completion.md
├── start-task.md                 ← 슬림
└── start-task/
    ├── role.md / input.md / team-create.md
    └── procedure/01~06.md
```

## 5. JSON 스키마 (`references/output-templates/`)

토큰 절감 원칙 3 (Structured Output) 구현. 다음 단계는 markdown이 아닌 JSON만 Read해도 작동.

| 스키마 | 용도 |
|--------|------|
| `planner-report.schema.json` | run_id, feature, requirements, AS-IS/TO-BE, impact 표 |
| `changelog.schema.json` | feature/api/data 변경 + 영향 + 리소스 |
| `architect-design.schema.json` | planner_supplements, module_structure, data_model, dependencies, migration |
| `review-result.schema.json` | issues (severity/rule/location/evidence), conclusion |
| `qa-result.schema.json` | tests_written, execution, failures, integration_check |
| `debug-result.schema.json` | error, log_flow, root_cause, resolution, recurrence |

### 설계 포인트

- 모든 스키마에 `run_id` 패턴 검증 (`YYYYMMDD-HHMM-{slug}`)
- `evidence.method`로 read/grep/graphify 출처 강제
- review-result `rule` 필드는 `agents/code-reviewer/rules/` 파일명과 매칭
- qa-result `next_action`은 retry-state-transition과 동일 enum
- `additionalProperties: false`로 verbose 출력 차단

## 6. P1 정책 적용 (token-strategy 즉시 효과)

### 출력 토큰 상한 (`agents/{name}/policy/output-cap.md`)

| 에이전트 | 상한 |
|---------|------|
| planner / domain-architect | 1500 |
| code-reviewer | 1000 |
| bug-debugger | 1000 |
| qa-expert | 800 |
| code-refactorer | 코드 diff 위주 |

### diff-only (`agents/{name}/policy/diff-only.md`)

- code-reviewer, code-refactorer, bug-debugger, qa-expert에 적용
- 변경 라인 + 직접 의존 심볼만, 역참조 ≤10개

### 재시도 루프 1회 (`skills/orchestrator/policy/`)

- `loop-limit.md` — max=1 강제
- `retry-counter.md` — `_workspace/{run_id}/.retry_count` 메커니즘

### reviewer 비판적 사고 완화 (`agents/code-reviewer/critical-thinking.md`)

- AS-IS: "반드시 1개+ 개선 제안" 강제 → 무한 nitpick
- TO-BE: Critical/Warning만 강제, Info는 선택

## 7. 프롬프트 엔지니어링 도입

각 에이전트(+ orchestrator + setup-kb)에 4개 기법 도입:

- **Few-shot**: 도메인 맞춤 입력→출력 데모 3~4개
- **CoT**: `reasoning.md` 단계별 추론 + `zero-shot.md` "단계별로 생각해 보자"
- **ART**: 도구 호출과 추론을 교차 결합한 흐름
- **Multimodal CoT**: planner에만 적용 (Figma 이미지 + 텍스트)

기법 정의는 `agents/_techniques/`에 공유, 각 에이전트는 `techniques.md` 포인터로 참조.

## 8. README 업데이트

- 재시도 정책 "최대 2회" → "P1: 최대 1회"
- 비판적 사고 reviewer 규칙 완화 반영
- "출력 스키마 (Structured Output)" 섹션 신설
- "디렉토리 구조 (Atomic 분할)" 섹션 신설
- 참고 문서에 token-strategy / adr-vector-kb / _techniques 추가

## 9. 검증

- 289개 .md 파일 모두 150자 이하 ✅
- 6개 JSON Schema draft 2020-12 ✅
- 플러그인 진입점 frontmatter 호환 ✅
- 기존 `_workspace/` 산출물 경로 변경 없음 ✅

## 10. P2 적용 (원칙 1, 2, 4, 8, 9)

### 원칙 9 — 공통 instruction (`agents/_common/`)

| 파일 | 내용 |
|------|------|
| `diff-only.md` | 변경 라인 + 직접 의존만 |
| `graphify-fallback.md` | graphify 우선, 없으면 Grep |
| `critical-thinking.md` | 이전 단계 무조건 수용 X |
| `required-reads.md` | CLAUDE.md, context.md 항상 |
| `output-cap-rule.md` | 산문 X, bullet, 초과 시 refs |
| `no-peer-comm.md` | Peer SendMessage 금지 |

각 에이전트에 `common.md` 포인터 추가.

### 원칙 1 — Pipeline 전환

- `skills/orchestrator/policy/pipeline.md` — 단방향 dispatch
- `phases/phase-2-execute.md` 통합

### 원칙 2 — Input Package

`skills/orchestrator/input-package/`:
- `format.md` — `{run_id, task_brief, upstream_summary, file_refs[]}`
- `task-brief.md` (≤500), `upstream-summary.md` (≤300), `file-refs.md`

다음 단계는 .json만 Read.

### 원칙 4 — Haiku 1차 트리아지

- `skills/orchestrator/triage/haiku-first.md` + `escalation.md`
- `agents/qa-expert/triage.md`, `agents/bug-debugger/triage.md`

Critical 후보 / 통합 의심 / 호출 depth≥3 시 opus.

### 원칙 8 — 캐싱

`skills/orchestrator/cache/`:
- `key.md` — `SHA256(paths + mtimes + brief)`
- `lookup.md` — `_workspace/{run_id}/.cache/{key}.json` 확인
- `storage.md` — 동일 run_id 영구
- `prompt-cache.md` — Anthropic 5분 TTL breakpoint

`policy/cache.md`로 강제.

## 11. 거버넌스/모니터링/품질 강화 (P3)

### 메타데이터 (`_metadata.schema.json`)
- 모든 산출물에 `owner / sensitivity / retention_days / created_by_agent / created_at` 필수
- 6개 기존 스키마에 `_metadata` required 추가
- `docs/data-governance.md` ADR (분류 정책, 라이프사이클, 감사)

### 비용 측정 (`cost.schema.json`)
- 스테이지별 tokens_in/out, model, duration, retries, cache_hit, cost_usd
- `policy/cost-tracking.md` + `phase-7-cleanup.md` 자동 작성

### 스키마 검증 (`references/scripts/validate-output.py`)
- jsonschema 기반 산출물 검증
- `policy/schema-validation.md` + `phase-4-result.md` 강제 호출
- exit 1=검증 실패, exit 2=환경 오류

## 12. 파일 정책 재정의 (`file-size-policy.md`)

이전 150자 일률 → 2-tier:
- **Atomic ≤200자**: rules / examples/few-shot / policy
- **Grouped ≤800자**: 같이 읽히는 묶음
- **Doc 무제한**: docs/, output-templates/*.md

### 통합 결과 (290 → 223 파일, -67)
| 변경 | 영향 |
|------|------|
| `{agent}/{common,techniques,schema}.md` → `references.md` | -12 |
| `examples/cot/{reasoning,zero-shot}.md` → `cot.md` | -8 |
| `orchestrator/cache/*.md` → `cache.md` | -3 |
| `orchestrator/input-package/*.md` → `input-package.md` | -3 |
| `orchestrator/triage/*.md` → `triage.md` | -1 |
| `orchestrator/retry/*.md` + stub → `retry-transitions.md` | -5 |
| `orchestrator/outputs/*.md` + workspace-layout → `outputs.md` | -6 |
| `setup-kb/files/*.md` + files-overview → `files.md` | -5 |
| `setup-kb/backend/*.md` → `backend-analysis.md` | -5 |
| `setup-kb/frontend/*.md` → `frontend-analysis.md` | -5 |
| `setup-kb/frameworks/*.md` → `frameworks.md` | -6 |
| `qa-expert/test-runners/*.md` → `test-runners.md` | -4 |

## 13. 미적용 (보류)

| 항목 | 위치 |
|------|------|
| Vector KB 인덱싱 | `adr-vector-kb.md` (트리거 충족 시 재검토) |
| 변경 승인 워크플로 (다중 결재) | data-governance.md 후속 |
| 감사 로그 자동 기록 (`audit.log`) | data-governance.md 후속 |
| 컴플라이언스 매핑 (GDPR/HIPAA) | data-governance.md 후속 |
