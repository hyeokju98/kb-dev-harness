---
name: setup-kb
description: "프로젝트 Knowledge Base 초기 구축. 아키텍처 파악, 도메인 맵, 디렉토리 문서화, graphify 그래프 생성. '하네스 초기화', 'KB 구축', 'setup', '프로젝트 세팅', '초기 설정' 요청 시 사용."
---

# Setup Knowledge Base

프로젝트에 진입하면 가장 먼저 실행하는 스킬. 에이전트들이 참조할 Knowledge Base 파일을 생성한다.

## 생성 파일

| 파일 | 역할 | 사용하는 에이전트 |
|------|------|----------------|
| `context.md` | 아키텍처 컨텍스트 | 전체 에이전트 (필수 읽기) |
| `.claude/CONTEXT-MAP.md` | 도메인-기능-파일 매핑 | planner (영향 분석), developer (파일 위치) |
| `history.md` | 변경 이력 | 오케스트레이터 (충돌 방지) |
| `{dir}/directory.md` | 디렉토리별 설명 | developer, refactorer (파일 탐색) |
| `graphify-out/graph.json` | 코드 관계 그래프 | planner (영향 분석 교차 검증), code-reviewer (의존성 확인) |

## 실행 절차

### Phase 1: 프로젝트 탐색 및 프레임워크 감지

1. `CLAUDE.md` 읽기 — 프로젝트 규칙 파악
2. 디렉토리 구조 탐색 — 최상위 폴더 목록, 주요 파일 확인
3. 프레임워크 감지:

| 감지 파일 | 프레임워크 | 분석 모드 |
|----------|-----------|----------|
| `manage.py` + `settings.py` | Django | backend-django |
| `next.config.*` + `app/` or `pages/` | Next.js | frontend-nextjs |
| `nuxt.config.*` | Nuxt.js | frontend-nuxt |
| `main.py` + `FastAPI` import | FastAPI | backend-fastapi |
| `build.gradle` + `@SpringBoot` | Spring Boot | backend-spring |
| `vite.config.*` + `src/` | React/Vue (Vite) | frontend-spa |
| `package.json`만 | Node.js 일반 | backend-node |

### Phase 2: context.md 생성

프로젝트 루트에 `context.md`를 생성한다.

**공통 포함 내용:**
- 프로젝트 개요 (한 줄)
- 기술 스택
- 디렉토리 구조 (역할별)
- 설정 환경 (dev/stage/prod)

**백엔드 추가 분석:**
- 레이어 구조 (데이터 흐름: Request → Controller → Service → DB → Response)
- DB 구조 (ORM 모델, 라우팅, 주요 테이블)
- URL/API 구조 (엔드포인트 prefix별)
- 외부 연동 목록 (API, 메시징, 결제 등)
- 이벤트/큐 시스템 (Celery, SQS, Kafka 등)

**프론트엔드 추가 분석:**
- 라우트 구조 (app/ or pages/ 기반)
- 컴포넌트 계층 (공통/도메인별)
- 상태 관리 (Context, Redux, Zustand, Recoil 등)
- API 연동 패턴 (hooks, API client, fetch 래퍼)
- 스타일링 (CSS Module, Tailwind, Styled Components 등)

### Phase 3: CONTEXT-MAP.md 생성

`.claude/CONTEXT-MAP.md`에 도메인 컨텍스트 맵을 생성한다.

#### 백엔드 분석 방식

| 분석 대상 | 방법 | 추출 정보 |
|----------|------|----------|
| URL 라우팅 | urls.py / router 파일 읽기 | 엔드포인트 → View 매핑 |
| 모델 | models.py / schema 파일 | 테이블 구조, 관계 |
| 비즈니스 로직 | service/ or library/ 탐색 | 도메인별 로직 파일 |
| 외부 연동 | interface/ or adapter/ 탐색 | 연동 시스템 목록 |
| 이벤트 | tasks.py, consumer 파일 | 이벤트 발행/소비 흐름 |

**출력 구조:**
```markdown
## 도메인별 기능-API-파일 매핑
| 기능 | API | 파일 매핑 |
## 외부 연동 매핑
| 시스템 | 호출 도메인 | 용도 |
## 이벤트 흐름 매핑
| 이벤트 | 발행 | 소비 |
## 기능→파일 가이드
| "이런 기능이면" | 생성할 파일 |
```

#### 프론트엔드 분석 방식

| 분석 대상 | 방법 | 추출 정보 |
|----------|------|----------|
| 라우트 | app/ or pages/ 파일 구조 | URL → Page 매핑 |
| API 호출 | hooks/ or lib/api/ 탐색 | 백엔드 API → 프론트 훅 매핑 |
| 컴포넌트 | components/ 탐색 | 공통/도메인별 컴포넌트 |
| 상태 관리 | stores/ or contexts/ 탐색 | 전역 상태 목록 |
| 타입 | types/ or interfaces/ 탐색 | API 응답 타입 정의 |

**출력 구조:**
```markdown
## 도메인별 기능-라우트-파일 매핑
| 기능 | 라우트 | 파일 매핑 |
## API 연동 매핑
| 백엔드 API | 프론트 훅 | 사용 페이지 |
## 컴포넌트 매핑
| 도메인 | 컴포넌트 | 사용 페이지 |
## 기능→파일 가이드
| "이런 기능이면" | 생성할 파일 |
```

### Phase 4: directory.md 일괄 생성

주요 디렉토리마다 `directory.md`를 생성한다:
- 역할 (한 줄)
- 하위 구조 (파일 트리)
- 주요 기능
- 관련 레이어 (입력/출력)

### Phase 5: history.md 초기화

프로젝트 루트에 `history.md`를 생성한다:
```markdown
# 변경 이력 (History)

에이전트가 수행한 변경사항을 기록한다. 최신순 정렬.

---
```

### Phase 6: graphify 실행 (코드 관계 그래프)

프로젝트 코드 간 관계를 그래프로 추출한다.

1. graphify 설치 확인 (`python3 -c "import graphify"`)
2. 설치되어 있으면 프로젝트 루트에서 실행:
   - AST 추출 (코드 파일 — 토큰 비용 없음)
   - Semantic 추출 (docs/images만 — 코드는 AST로 충분)
3. `graphify-out/graph.json` 생성
4. 미설치 시 건너뛰고 안내: "graphify가 없습니다. `pip install graphifyy`로 설치하면 코드 관계 그래프를 활용할 수 있습니다."

### Phase 7: 검증

생성된 파일을 확인하고 사용자에게 보고:
- 생성된 파일 목록
- 감지된 프레임워크 + 분석 모드
- 도메인 수
- 디렉토리 문서 수
- graphify: 노드/엣지/커뮤니티 수 (실행한 경우)

## 작업 원칙
- 프로젝트 구조를 코드에서 직접 읽고 파악한다 — 추측하지 않음
- 프레임워크에 맞는 분석을 수행한다
- 기존 KB 파일이 있으면 덮어쓰지 않고 업데이트 여부를 사용자에게 확인
