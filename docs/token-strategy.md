# Token Saving Strategy

soldoc-harness가 멀티 에이전트 운영에서 소비하는 토큰을 줄이기 위한 설계 원칙.
현재 하네스는 Team(A/B/C) 기반 협업 구조이며, 각 에이전트가 `CLAUDE.md / context.md / CONTEXT-MAP.md / history.md`를 중복 로딩하고 자연어 산출물을 주고받기 때문에 토큰 비용이 상승한다. 본 문서는 그 비용을 구조적으로 낮추는 10개 원칙과, 각 원칙을 하네스에 매핑한 적용안을 정의한다.

---

## 결론

> **Team(대화형 협업) → Pipeline(단방향, 구조화 출력)** 으로 전환한다.
> 모든 에이전트는 "최소 입력 + JSON/structured 출력"을 따르며, 자연어 협업·전체 컨텍스트 공유·무제한 reflection 루프를 제거한다.

---

## 문제의 본질

| 항목 | 현재 구조의 비용 |
|------|----------------|
| 여러 agent가 서로 대화 (`SendMessage`) | 토큰 기하급수 증가 |
| 전체 컨텍스트 공유 (KB 4종 통째 Read) | 매 호출마다 중복 비용 |
| 자연어 기반 협업 (markdown 보고서 교환) | 파싱·재해석 비용 |
| QA / reflection 루프 (재시도 최대 2회 × 5상태 전이) | 비용 폭발의 핵심 |

---

## 10개 원칙 및 하네스 적용안

### 1. 구조 바꾸기 — Team → Pipeline
- **원칙**: 양방향 협업 제거. 단방향 흐름(`A → B → C`)만 유지.
- **하네스 적용**:
  - `skills/orchestrator/SKILL.md` Phase 3의 "팀원 간 `SendMessage` 피드백 교환" 제거.
  - 재시도가 필요한 경우에도 이전 단계로 "되돌리는" 대신, **다음 단계가 reject 사유를 받아 새 입력으로 재실행**한다(상태 머신화).
  - `TeamCreate`는 유지하되, 에이전트 간 통신 채널은 차단하고 orchestrator만 dispatch.

### 2. 컨텍스트 최소화 — 요약 상태만 전달
- **원칙**: 전체 대화/이전 산출물 통째 전달 금지. 다음 단계가 필요로 하는 **요약 상태**만 전달.
- **하네스 적용**:
  - 에이전트 입력 패키지 = `{run_id, task_brief(≤500토큰), upstream_summary(≤300토큰), file_refs[]}`.
  - 이전 단계 산출물은 파일 경로(`_workspace/{run_id}/01_planner_report.md`)만 넘기고, 다음 단계가 **필요한 섹션만** Read.
  - 공통 KB(`CLAUDE.md`, `context.md`)는 입력에 포함하지 않는다 — 에이전트가 자기 책임 영역만 자율 Read.

### 3. 자연어 제거 — Structured Output 강제
- **원칙**: 설명·토론 금지. JSON 스키마로 출력.
- **하네스 적용**:
  - 모든 에이전트 출력에 **두 파일** 발행:
    - `NN_*.json` — 기계가 읽는 구조화 데이터 (다음 단계 입력용)
    - `NN_*.md` — 사람이 읽는 보고서 (선택, 최종 단계만)
  - `references/output-templates/`에 JSON 스키마 추가:
    - `planner-report.schema.json`
    - `architect-design.schema.json`
    - `review-result.schema.json`
    - `qa-result.schema.json`
  - 다음 단계는 `.md`가 아닌 `.json`만 Read.

### 4. Agent 역할 + 모델 분리 강화
- **원칙**: opus = "생각", 그 외 = 저가 모델.
- **하네스 적용** (현재 매핑 유지·강화):
  | 단계 | 모델 | 비고 |
  |------|------|------|
  | planner / architect / reviewer | **opus** | 판단·설계 |
  | developer / refactorer | **sonnet** | 구현 |
  | qa / debugger 1차 트리아지 | **haiku** | diff 스캐닝, 패턴 매칭 |
  | qa 심층 분석 (haiku가 escalate) | **opus** | 필요 시만 |
  - `agents/qa-expert.md`, `agents/bug-debugger.md`에 "1차는 haiku로 diff만 스캔, 의심 발견 시 opus로 escalate" 규칙 추가.

### 5. QA 최적화 — diff-only
- **원칙**: 전체 코드 검사 금지. **변경된 라인 + 직접 의존 심볼만**.
- **하네스 적용**:
  - `agents/qa-expert.md`, `agents/code-reviewer.md`의 입력을 `git diff --staged`로 한정.
  - 의존성 추적은 graphify 그래프 우선(없으면 Grep), **변경 심볼당 최대 N=10 역참조**까지만 펼침.
  - 변경 없는 파일 Read 금지.

### 6. 반복 루프 제한 — max 1회
- **원칙**: reflection/critique 1회 제한. 그 이상이면 사용자 개입.
- **하네스 적용**:
  - `skills/orchestrator/SKILL.md` Phase 3 재시도 정책: **최대 2회 → 1회**로 축소.
  - 1회 재시도 후에도 실패하면 **부분 결과 + 미해결 이슈 목록** 반환 후 종료.
  - reviewer "반드시 1개+ 개선 제안" 규칙(`agents/code-reviewer.md`)을 **Critical/Warning만 강제**로 완화 — Info 강제는 무한 nitpick의 원인.

### 7. 문서/RAG 최적화 — chunk + 요약
- **원칙**: 문서 통째 로딩 금지. 필요한 chunk + 요약만.
- **하네스 적용**:
  - `setup-kb` 산출물에 **요약 인덱스 추가**: `context.md.summary`(≤300토큰), `CONTEXT-MAP.md.index`(도메인명 + 라인 범위만).
  - 에이전트는 요약 인덱스 → 필요 섹션만 `Read(offset, limit)`.
  - `history.md`는 최근 10건만 `tail`로 자르되, 그것도 요약본(`history.summary.md`)을 우선 읽고 상세는 필요 시.
  - graphify는 그 자체가 chunk 메커니즘 → 적극 활용.

### 8. 캐싱 필수
- **원칙**: 동일 입력에 동일 출력이 나오는 작업은 재호출 금지.
- **하네스 적용**:
  - `_workspace/{run_id}/.cache/` 디렉토리에 단계별 입력 해시 저장.
  - 입력 해시(파일 경로 + 변경 mtime + brief 해시) 일치 시 **이전 산출물 재사용**.
  - Anthropic prompt cache 활용: 시스템 프롬프트(공통 부분)를 cache breakpoint 앞에 배치.

### 9. 시스템 프롬프트 경량화
- **원칙**: 공통 프롬프트 중복 제거.
- **하네스 적용**:
  - `agents/*.md` frontmatter 아래 "Context Budget", "비판적 사고 규칙", "출력 원칙" 섹션이 6개 에이전트에 중복 → **`agents/_common.md`로 추출**하고 각 에이전트는 차이점만 기술.
  - orchestrator의 모델 분리표·재시도표도 공통 reference로 이동.
  - 목표: 에이전트당 instruction 길이 **현재 평균 60줄 → 30줄 이하**.

### 10. 출력 제한 — schema 강제 + verbose 금지
- **원칙**: verbose 응답 금지. 사전 정의 schema만.
- **하네스 적용**:
  - 각 에이전트 출력에 **토큰 상한** 명시:
    | 에이전트 | 상한 |
    |---------|------|
    | planner | 1500 |
    | architect | 1500 |
    | reviewer | 1000 |
    | qa | 800 |
    | debugger | 1000 |
    | refactorer | 코드 diff만 |
  - 상한 초과 시 "핵심 N개만, 나머지는 references" 자동 truncate.
  - 모든 markdown 보고서는 **bullet 위주, 산문 금지**.

---

## 우선순위 적용 로드맵

| Phase | 작업 | 예상 절감 효과 |
|-------|------|--------------|
| **P1 (즉시)** | 원칙 5(diff-only), 6(루프 1회), 10(토큰 상한) — 기존 .md 수정만으로 가능 | -30~40% |
| **P2 (단기)** | 원칙 2(요약 입력), 7(KB 인덱스), 9(공통 추출) | -20~25% |
| **P3 (중기)** | 원칙 1(Pipeline 전환), 3(JSON 스키마), 4(haiku 도입) | -25~30% |
| **P4 (장기)** | 원칙 8(캐싱 인프라) | -10~15% |

**누적 목표: 현재 대비 약 60~70% 토큰 절감.**

---

## 측정·검증

각 Phase 적용 전후로 다음을 측정한다 (orchestrator가 `_workspace/{run_id}/cost.json`에 기록):
- 단계별 입력/출력 토큰
- 재시도 횟수
- 캐시 히트율
- 총 비용 (USD)

회귀 방지: P1~P4 적용 후 동일 티켓을 베이스라인과 비교.

---

## 비목표 (Out of Scope)

- 모델을 더 작은 외부 모델로 교체하는 것은 본 전략의 범위가 아니다 (Anthropic 모델 내 분리만).
- 사용자 워크플로우 자체(예: `/start-task` 단계 축소)는 별도 검토 대상.
- 토큰 절감을 위해 **품질 게이트(reviewer Critical, qa 통합 검증)를 제거하지 않는다**. 줄이는 것은 verbose·중복·무한 루프뿐이다.
