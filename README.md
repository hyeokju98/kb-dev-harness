# Soldoc Harness (`kb-dev-harness`)

Claude Code가 프로젝트를 이해하고 팀으로 작업할 수 있도록 Knowledge Base를 구축하는 플러그인.

**한 줄 요약:** `/setup-kb` 한 번 실행하면 Claude가 프로젝트 아키텍처를 파악하고, 이후 기능 개발/리팩토링/버그 수정을 에이전트 팀으로 자동화합니다. QA 에이전트는 **실제 테스트를 실행**하고 pass/fail을 리턴합니다.

> 레포명은 `kb-dev-harness`, 플러그인 식별자는 `soldoc-harness`입니다. 같은 것이며, 아래 설치 커맨드의 표기를 그대로 사용하세요.

## 왜 필요한가

Claude Code는 매 세션마다 프로젝트를 처음부터 파악합니다. 파일을 하나씩 읽어야 하고, 도메인 간 관계를 모르고, 이전 변경 이력을 알 수 없습니다.

이 플러그인은 프로젝트의 **Knowledge Base**를 구축하여:
- 새 세션에서 즉시 프로젝트를 파악할 수 있고
- "이 기능 변경하면 어디에 영향 가?" 질문에 근거 기반으로 답하고
- 에이전트 팀이 설계 → 구현 → 리뷰 → **테스트 실행**까지 자동 수행합니다

**프론트엔드/백엔드 모두 지원.** Django, Next.js, FastAPI, Spring 등 프레임워크를 자동 감지합니다.

## 설치

### 빠른 시작 (2줄)

```
/plugin marketplace add https://github.com/hyeokju98/kb-dev-harness.git
/plugin install soldoc-harness@soldoc-harness
```

설치 후 `/setup-kb`로 프로젝트 KB를 구축합니다.

### 팀 공유 (settings.json)

팀원이 `git pull`만 하면 자동 적용되게 하려면 `.claude/settings.json`에 추가:

```json
{
  "extraKnownMarketplaces": {
    "soldoc-harness": {
      "source": { "source": "git", "url": "https://github.com/hyeokju98/kb-dev-harness.git" }
    }
  },
  "enabledPlugins": {
    "soldoc-harness@soldoc-harness": true
  }
}
```

### 로컬 개발

이 레포 자체를 수정하며 쓰려면:

```
/plugin marketplace add ~/Documents/dev/harness
/plugin install soldoc-harness@soldoc-harness
```

## 초기 설정 (프로젝트당 1회)

### Step 1: Knowledge Base 구축

```
/setup-kb
```

자동 생성 파일:

```
프로젝트/
├── context.md                  ← 아키텍처 (레이어, DB, 외부 연동)
├── history.md                  ← 에이전트 변경 이력
├── .claude/
│   └── CONTEXT-MAP.md          ← 도메인-기능-파일 매핑
├── {각 디렉토리}/
│   └── directory.md            ← 디렉토리별 설명
└── graphify-out/
    └── graph.json              ← 코드 관계 그래프 (선택)
```

**프레임워크별 자동 감지:**

| 감지 | 분석 |
|------|------|
| Django (`manage.py`) | urls.py → models.py → settings/ |
| Next.js (`next.config.*`) | app/ → hooks/ → components/ |
| FastAPI (`FastAPI` import) | routers → schemas → models |
| Spring Boot (`build.gradle` + `@SpringBoot`) | controllers → services → repositories |

### Step 2: (선택) KB 갱신 정책

KB는 한 번 만들고 방치하면 stale해집니다. orchestrator가 매 실행마다 stale을 감지하여 경고합니다:

- `context.md` 이후 **커밋 50개 초과** → `--refresh` 권장
- 최상위 디렉토리 신설/CONTEXT-MAP에 없는 도메인 발견 → `--refresh` 권장

수동 갱신:
```
/setup-kb --refresh
```

증분 모드로 변경된 도메인의 `directory.md`와 `CONTEXT-MAP.md` 해당 섹션만 갱신합니다.

### Step 3: (선택) graphify 설치

코드 간 관계 그래프가 있으면 영향 분석의 정확도가 올라갑니다.

```bash
pip install graphifyy
```

없으면 모든 에이전트가 **Grep 기반 역참조 추적으로 자동 fallback**합니다. 동작은 하며, 간접 의존성 탐색 범위만 좁아집니다.

### Step 4: (선택) 프로젝트별 developer 에이전트 추가

**중요:** 이 플러그인은 구현(developer) 에이전트를 포함하지 않습니다. 보일러플레이트 규칙이 프로젝트마다 다르기 때문입니다. Team A(기능 개발)를 완전히 쓰려면 프로젝트의 `.claude/agents/`에 직접 추가하세요.

샘플 템플릿을 제공합니다:
- `references/sample-agents/api-developer.md` — Django DRF 스타일
- `references/sample-agents/page-builder.md` — Next.js 스타일

프로젝트 `.claude/agents/`로 복사하고 프로젝트 규칙을 덧붙여 쓰세요.

## 사용법

### 기능 개발 사전 분석

```
/start-task 비밀번호 정책 변경 기능 추가
```

planner가 요구사항을 분석하고, architect가 설계안을 작성합니다. 정보가 부족하면 planner가 **필수 항목**(변경 도메인, 변경 유형, 영향 사용자 유형)을 물어봅니다. 3회 이상 반복 질문하지 않습니다.

Asana 티켓이나 Figma 링크도 전달 가능:
```
/start-task https://app.asana.com/0/xxxxx
```

### 팀으로 개발 실행

```
soldoc-orchestrator
> 기능 개발: 비밀번호 정책 변경
```

**Team A (기능 개발)** 파이프라인:
```
planner (opus) → 영향 분석 (근거: CONTEXT-MAP + Grep 역참조 + graphify 교차검증)
  ↓
architect (opus) → 도메인 설계 (planner 레포트 비판적 검증 포함)
  ↓
developer (sonnet) → 코드 구현  ← 프로젝트별 에이전트
  ↓
reviewer (opus) → 코드 리뷰 (N+1, 트랜잭션, 보안 Critical/Warning/Info)
  ↓
qa (opus) → 테스트 작성 + 실제 실행 + pass/fail 리턴
```

### 리팩토링

```
soldoc-orchestrator
> 리팩토링: payment 모듈 정리
```

**Team B (코드 품질)**:
```
reviewer (opus) → 개선 방향 분석
  ↓
refactorer (sonnet) → 리팩토링 실행 (참조 관계 사전 확인)
  ↓
reviewer-post (opus) → 재리뷰
```

### 버그 수정

```
soldoc-orchestrator
> 버그: request_id dc50b69905664b52af09a35b16575588
```

**Team C (버그 대응)**:
```
debugger (opus) → 로그 분석 + 근본 원인 + 재발 여부 확인
  ↓
reviewer (opus) → 수정 코드 검증
```

### 코드 리뷰

```
/self-review
```

변경사항을 체크리스트 기준으로 리뷰하고, ORM 쿼리가 있으면 SQL 최적화도 검토합니다. 승인 시 `.claude-reviewed` 마커를 생성합니다(커밋 훅에서 "리뷰 완료" 확인용).

## 재시도 상태 전이

reviewer/qa에서 문제가 발견되면 **적절한 단계로 되돌립니다** (최대 2회):

| 실패 단계 | 되돌릴 대상 | 이유 |
|----------|------------|------|
| reviewer: Critical 지적 | developer | 코드 수정 |
| reviewer: 아키텍처 부적합 | architect | 설계 재검토 |
| qa: 테스트 FAIL | developer | 버그 수정 |
| qa: 통합 정합성 불일치 | architect | 경계면 재설계 |
| architect: planner 보완사항 다수 | planner | 영향 분석 재작성 |

2회 후에도 실패하면 사용자에게 수동 개입 요청.

## `_workspace/` 정책 (run_id)

각 실행마다 고유 `run_id`를 생성해 산출물을 분리합니다:

```
_workspace/
└── 20260421-1045-password-policy/      ← {YYYYMMDD-HHMM}-{slug}
    ├── 00_input/
    │   ├── requirements.md
    │   ├── asana_data.md               (수집 성공 시)
    │   └── figma_data.md               (수집 성공 시)
    ├── 01_planner_report.md
    ├── 02_changelog.md
    ├── 03_architect_design.md
    ├── 04_review_result.md
    └── 05_qa_result.md
```

이전 실행 이력이 보존되므로 티켓별 기록으로 활용 가능.

## Knowledge Base가 하는 일

에이전트들은 작업 전에 KB 파일을 읽어 프로젝트를 파악합니다. **각 에이전트는 자기 역할에 필요한 파일만** 읽습니다 (컨텍스트 예산 제어):

| 에이전트 | 읽는 것 | 읽지 않는 것 |
|---------|--------|-------------|
| planner | CLAUDE + CONTEXT-MAP + context + history | — |
| architect | CLAUDE + context + CONTEXT-MAP(해당 도메인) + planner 레포트 | history 전체 |
| reviewer | CLAUDE + context + CONTEXT-MAP(변경 도메인) | history, 무관한 도메인 |
| refactorer | CLAUDE + context | history, CONTEXT-MAP 전체 |
| debugger | CLAUDE + context + history + CONTEXT-MAP(에러 도메인) | — |
| qa | CLAUDE + context + architect 설계 | history, CONTEXT-MAP 전체 |

## Advisor 전략 (모델 분리)

| 역할 | 모델 | 이유 |
|------|------|------|
| 계획/분석 (planner, architect) | **opus** | 요구사항·아키텍처에 높은 추론 |
| 리뷰/검증 (reviewer, qa, debugger) | **opus** | 버그·보안 판단에 높은 추론 |
| 구현/실행 (developer, refactorer) | **sonnet** | 설계 확정 후 코드 생성은 빠른 모델로 충분 |

**불일치 시 opus 판단 우선.** sonnet 구현이 opus 설계와 다르면 reviewer가 수정 요청.

## 비판적 사고

- **architect** → planner 영향 범위 검증, 누락/과대평가 명시
- **developer** → architect 설계에 비효율 있으면 대안 제시
- **reviewer** → "통과" 기본값 금지. **반드시 1개+ 개선 제안**
- **qa** → 테스트 실행 + architect ↔ developer 교차 비교

## 에이전트 구성

### 플러그인 기본 (6개)

| 에이전트 | 하는 일 |
|---------|--------|
| **planner** | 요구사항 분석, AS-IS/TO-BE, 영향 범위(근거 기반), changelog |
| **domain-architect** | 모듈 구조 설계, 데이터 모델링, 의존관계 분석 |
| **code-reviewer** | N+1/SQL/트랜잭션/보안/아키텍처 리뷰. Critical/Warning/Info 분류 |
| **code-refactorer** | 참조 관계 사전 확인 후 리팩토링. 변경 범위 최소화 |
| **bug-debugger** | 로그 분석, 호출 체인 추적, 재발 여부 확인 |
| **qa-expert** | 테스트 작성 + **실제 실행**(pytest/vitest/...) + pass/fail 리턴 |

### 프로젝트별 추가 (샘플 제공)

`references/sample-agents/`에 템플릿:
- `api-developer.md` (백엔드 API)
- `page-builder.md` (프론트엔드 페이지)

프로젝트의 `.claude/agents/`로 복사해서 규칙을 보강해 쓰세요.

## 파일 구조

```
프로젝트/
├── CLAUDE.md                       ← 프로젝트 규칙 (직접 작성)
├── context.md                      ← 아키텍처 (setup-kb 자동 생성)
├── history.md                      ← 변경 이력 (자동 갱신)
├── .claude/
│   ├── settings.json
│   ├── CONTEXT-MAP.md              ← 도메인 맵 (setup-kb 자동 생성)
│   ├── agents/                     ← 프로젝트별 에이전트 (developer 등)
│   │   └── api-developer.md
│   └── references/
│       └── review-checklist.md     ← 프로젝트별 리뷰 체크리스트
├── _workspace/                     ← 에이전트 실행 산출물 (run_id별)
│   └── {run_id}/
│       ├── 00_input/
│       ├── 01_planner_report.md
│       └── ...
├── {각 디렉토리}/
│   └── directory.md                ← 디렉토리 설명 (setup-kb 자동 생성)
└── graphify-out/
    └── graph.json                  ← 코드 관계 그래프 (선택)
```

## review-checklist 사용 패턴

플러그인의 `references/review-checklist.md`는 **공통 기본 체크리스트**입니다. 프로젝트별 규칙을 추가하려면 이 파일을 `.claude/references/review-checklist.md`로 복사하고 프로젝트 고유 항목을 덧붙이세요. reviewer, qa-expert, self-review가 프로젝트 경로를 먼저 확인합니다.

## FAQ

**Q: 프론트엔드에서도 쓸 수 있나요?**
A: 네. 프레임워크 자동 감지. CONTEXT-MAP이 라우트-컴포넌트-훅 기준으로 생성됩니다.

**Q: graphify 없으면 기능이 줄어드나요?**
A: 아니오. 모든 에이전트가 **Grep 기반 역참조 추적**으로 자동 fallback합니다. graphify는 간접 의존성 정확도를 높여주는 **선택** 도구입니다.

**Q: 기존 CLAUDE.md가 있으면?**
A: 건드리지 않습니다. `/setup-kb`는 KB 파일(context.md, CONTEXT-MAP.md, directory.md, history.md)만 생성/갱신합니다.

**Q: KB 파일을 git에 올려야 하나요?**
A: 권장합니다. `context.md`, `CONTEXT-MAP.md`, `directory.md`는 팀 공유가 유리합니다. `graphify-out/`은 용량이 크니 `.gitignore` 추가 가능(로컬에서 `/setup-kb`로 재생성).

**Q: `_workspace/`는 git에 올리나요?**
A: 선택입니다. 티켓별 산출물을 팀 공유하고 싶으면 올리고, 로컬만 보존할 거면 `.gitignore`에 추가.

**Q: QA가 실제로 테스트를 돌린다고?**
A: 네. pytest/vitest/jest/gradle test 등을 프로젝트 환경에서 감지해 실행하고 pass/fail을 리턴합니다. FAIL이면 orchestrator가 developer로 되돌립니다 (최대 2회 재시도).

## 참고 문서

- [`docs/kb-schema.md`](docs/kb-schema.md) — KB 파일 공식 스키마 (context / CONTEXT-MAP / directory / history)
- [`docs/workspace-schema.md`](docs/workspace-schema.md) — `_workspace/{run_id}/` 산출물 구조
