# Soldoc Harness

Claude Code가 프로젝트를 이해하고 팀으로 작업할 수 있도록 Knowledge Base를 구축하는 플러그인.

**한 줄 요약:** `/setup-kb` 한 번 실행하면 Claude가 프로젝트 아키텍처를 파악하고, 이후 기능 개발/리팩토링/버그 수정을 에이전트 팀으로 자동화합니다.

## 왜 필요한가

Claude Code는 매 세션마다 프로젝트를 처음부터 파악합니다. 파일을 하나씩 읽어야 하고, 도메인 간 관계를 모르고, 이전 변경 이력을 알 수 없습니다.

이 플러그인은 프로젝트의 **Knowledge Base**를 구축하여:
- 새 세션에서 즉시 프로젝트를 파악할 수 있고
- "이 기능 변경하면 어디에 영향 가?" 질문에 근거 기반으로 답하고
- 에이전트 팀이 설계 → 구현 → 리뷰 → QA를 자동으로 수행합니다

**프론트엔드/백엔드 모두 지원합니다.** Django, Next.js, FastAPI, Spring 등 프레임워크를 자동 감지합니다.

## 설치

### 방법 1: GitHub에서 설치 (팀 공유)
```bash
# Claude Code에서
/plugin marketplace add <github-repo-url>
/plugin install soldoc-harness
/reload-plugins
```

### 방법 2: 프로젝트 settings.json에 등록 (clone만 하면 자동 적용)
`.claude/settings.json`에 추가:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "extraKnownMarketplaces": {
    "soldoc-harness": {
      "source": { "source": "github", "repo": "soldoc-kr/soldoc-harness" }
    }
  },
  "enabledPlugins": {
    "soldoc-harness@soldoc-harness": true
  }
}
```

### 방법 3: 로컬 설치 (개발 중)
```bash
/plugin marketplace add --source directory --path ~/Documents/dev/harness
/plugin install soldoc-harness
/reload-plugins
```

## 초기 설정 (프로젝트당 1회)

### Step 1: Knowledge Base 구축

```
/setup-kb
```

자동으로 프로젝트를 분석하여 다음 파일들을 생성합니다:

```
프로젝트/
├── context.md                  ← 아키텍처 컨텍스트 (레이어 구조, DB, 외부 연동)
├── history.md                  ← 에이전트 변경 이력
├── .claude/
│   └── CONTEXT-MAP.md          ← 도메인-기능-파일 매핑
├── {각 디렉토리}/
│   └── directory.md            ← 디렉토리별 설명
└── graphify-out/
    └── graph.json              ← 코드 관계 그래프 (선택, graphify 설치 시)
```

**프레임워크별 자동 감지:**

| 감지 | 분석 |
|------|------|
| Django (`manage.py`) | urls.py → models.py → settings/ 기반 분석 |
| Next.js (`next.config.*`) | app/ → hooks/ → components/ 기반 분석 |
| FastAPI (`FastAPI` import) | routers → schemas → models 기반 분석 |

### Step 2: (선택) graphify 설치

코드 간 관계 그래프를 구축하면 영향 분석의 정확도가 올라갑니다.

```bash
pip install graphifyy
```

`/setup-kb`에서 자동으로 감지하여 실행합니다. 없어도 동작하지만, 있으면 에이전트들이 코드 간 의존관계를 그래프 탐색으로 파악합니다.

### Step 3: (선택) 프로젝트별 에이전트 추가

보일러플레이트 규칙이 있는 프로젝트는 구현 에이전트를 직접 추가합니다:

```bash
# 프로젝트 .claude/agents/ 에 직접 생성
# 예: Django API 개발 에이전트
```

```markdown
# .claude/agents/api-developer.md
---
name: api-developer
description: "API 보일러플레이트 생성."
---
# API Developer
## 핵심 역할
- API_BOILERPLATE.md 규칙에 따라 코드 생성
...
```

## 사용법

### 기능 개발 사전 분석

```
/start-task 비밀번호 정책 변경 기능 추가
```

planner가 요구사항을 분석하고, architect가 설계안을 작성합니다.
정보가 부족하면 planner가 직접 질문합니다:
```
> 변경 대상 도메인이 어디인가요? (auth, medical, payment 등)
> 기존 API를 수정하나요, 새 API를 만드나요?
```

Asana 티켓이나 Figma 링크가 있으면 함께 전달할 수 있습니다:
```
/start-task https://app.asana.com/0/xxxxx
```

### 팀으로 개발 실행

```
soldoc-orchestrator
> 기능 개발: 비밀번호 정책 변경
```

자동으로 **Team A (기능 개발)**가 구성됩니다:
```
planner (opus) → 영향 분석
  ↓
architect (opus) → 도메인 설계
  ↓
developer (sonnet) → 코드 구현  ← 프로젝트별 에이전트
  ↓
reviewer (opus) + qa (opus) → 코드 리뷰 + QA (병렬)
```

### 리팩토링

```
soldoc-orchestrator
> 리팩토링: payment 모듈 정리
```

**Team B (코드 품질)**:
```
reviewer (opus) → 코드 분석 + 개선 방향
  ↓
refactorer (sonnet) → 리팩토링 실행
  ↓
reviewer-post (opus) → 변경사항 재리뷰
```

### 버그 수정

```
soldoc-orchestrator
> 버그: request_id dc50b69905664b52af09a35b16575588
```

**Team C (버그 대응)**:
```
debugger (opus) → 로그 분석 + 근본 원인 추적
  ↓
reviewer (opus) → 수정 코드 검증
```

### 코드 리뷰

```
/self-review
```

변경사항을 체크리스트 기준으로 리뷰하고, ORM 쿼리가 있으면 SQL 최적화도 검토합니다.

## Knowledge Base가 하는 일

에이전트들은 작업 전에 KB 파일을 읽어서 프로젝트를 파악합니다:

```
에이전트가 작업 시작
  ↓
CLAUDE.md 읽기 → "프로젝트 규칙이 뭐지?"
  ↓
context.md 읽기 → "아키텍처가 어떻게 생겼지?"
  ↓
CONTEXT-MAP.md 읽기 → "이 기능은 어떤 파일을 건드려야 하지?"
  ↓
history.md 읽기 → "최근에 뭐가 바뀌었지?"
  ↓
graphify query → "이 코드를 바꾸면 어디에 영향이 가지?"
  ↓
작업 시작
```

작업 완료 후:
```
history.md에 변경 이력 추가
  ↓
graphify --update로 그래프 갱신 (코드 변경 시)
```

## Advisor 전략

비용 효율을 위해 역할별로 모델을 분리합니다:

| 역할 | 모델 | 이유 |
|------|------|------|
| 계획/분석 (planner, architect) | **opus** | 요구사항 분석, 아키텍처 결정에 높은 추론 필요 |
| 리뷰/검증 (reviewer, qa, debugger) | **opus** | 버그/보안 판단에 높은 추론 필요 |
| 구현/실행 (developer, refactorer) | **sonnet** | 설계 확정 후 코드 생성은 빠른 모델로 충분 |

**불일치 시 opus 판단 우선.** sonnet이 구현한 코드가 opus의 설계와 다르면, opus(reviewer)가 수정을 요청합니다.

## 비판적 사고

에이전트들은 이전 단계의 산출물을 무조건 수용하지 않습니다:

- **architect** → planner 레포트의 영향 범위가 정확한지 검증
- **developer** → architect 설계에 비효율이 있으면 대안 제시
- **reviewer** → "통과"를 기본값으로 하지 않음. 반드시 1개 이상 개선 제안
- **qa** → architect 설계와 developer 코드를 교차 비교

## 에이전트 구성

### 플러그인 기본 (6개)

| 에이전트 | 하는 일 |
|---------|--------|
| **planner** | 요구사항 분석, AS-IS/TO-BE, 영향 범위, changelog. 정보 부족하면 질문 |
| **domain-architect** | 모듈 구조 설계, 데이터 모델링, 의존관계 분석 |
| **code-reviewer** | 버그/보안/아키텍처/SQL 최적화 리뷰. cookbook 파일 참조 |
| **code-refactorer** | 실제 코드 수정. 변경 범위 최소화, 기존 동작 보존 |
| **bug-debugger** | 로그 분석, 근본 원인 추적, 에러 전파 경로 파악 |
| **qa-expert** | 테스트 작성, 경계면 교차 비교 (입력↔출력 정합성) |

### 프로젝트별 추가 (선택)

| 에이전트 | 언제 추가하나 |
|---------|------------|
| **api-developer** | API 보일러플레이트 규칙이 있는 백엔드 프로젝트 |
| **page-builder** | 페이지 생성 규칙이 있는 프론트엔드 프로젝트 |
| **migration-writer** | DB 마이그레이션 규칙이 있는 프로젝트 |

프로젝트 `.claude/agents/`에 직접 추가하면 오케스트레이터가 자동으로 인식합니다.

## 파일 구조

```
프로젝트/
├── CLAUDE.md                       ← 프로젝트 규칙 (직접 작성)
├── context.md                      ← 아키텍처 (setup-kb 자동 생성)
├── history.md                      ← 변경 이력 (자동 갱신)
├── .claude/
│   ├── settings.json               ← 플러그인 설정
│   ├── CONTEXT-MAP.md              ← 도메인 맵 (setup-kb 자동 생성)
│   ├── agents/                     ← 프로젝트별 에이전트 (선택)
│   │   └── api-developer.md
│   └── references/
│       └── review-checklist.md     ← 프로젝트별 리뷰 체크리스트 (선택)
├── {각 디렉토리}/
│   └── directory.md                ← 디렉토리 설명 (setup-kb 자동 생성)
└── graphify-out/
    └── graph.json                  ← 코드 관계 그래프 (선택)
```

## FAQ

**Q: 프론트엔드에서도 쓸 수 있나요?**
A: 네. `/setup-kb`가 프레임워크를 자동 감지합니다 (Next.js, Nuxt, React/Vue 등). CONTEXT-MAP이 라우트-컴포넌트-훅 기준으로 생성됩니다.

**Q: graphify 없이도 되나요?**
A: 네. graphify는 선택 사항입니다. 없으면 에이전트가 Grep 기반으로 영향 분석합니다. 있으면 코드 간 관계를 그래프 탐색으로 보완하여 정확도가 올라갑니다.

**Q: 기존 CLAUDE.md가 있으면 어떻게 되나요?**
A: 건드리지 않습니다. CLAUDE.md는 프로젝트 규칙이므로 직접 관리합니다. `/setup-kb`는 context.md, CONTEXT-MAP.md 등 KB 파일만 생성합니다.

**Q: 팀원에게 어떻게 공유하나요?**
A: `.claude/settings.json`에 플러그인이 등록되어 있으므로, 팀원이 `git pull` 후 `/reload-plugins`만 하면 됩니다. KB 파일이 git에 포함되어 있으면 `/setup-kb`도 건너뛸 수 있습니다.

**Q: KB 파일을 git에 올려야 하나요?**
A: 권장합니다. context.md, CONTEXT-MAP.md, directory.md는 팀 전체가 공유하면 좋습니다. graphify-out/은 용량이 크므로 .gitignore에 추가해도 됩니다 (각자 로컬에서 `/setup-kb`로 생성).
