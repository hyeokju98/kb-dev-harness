# KB 파일 스키마

`/setup-kb`가 생성하는 Knowledge Base 파일들의 공식 스키마. 커스텀 에이전트를 만들 때 이 문서를 기준으로 파일을 참조/갱신하세요.

## context.md (프로젝트 루트)

**목적:** 아키텍처 개요. 전체 에이전트의 필수 읽기 대상.

**최대 크기 권장:** 400줄 (초과 시 요약 필요 — 컨텍스트 예산 보호)

**섹션:**
```markdown
# {프로젝트명}

## 개요
(한 줄)

## 기술 스택
- 언어 / 런타임 / 프레임워크 / DB / 외부 서비스

## 디렉토리 구조 (역할별)
- {top-level dir} — {역할}

## 설정 환경
- dev / stage / prod 차이

## 레이어 구조 (백엔드인 경우)
Request → Controller → Service → DB → Response

## DB 구조 (백엔드인 경우)
- ORM, 라우팅, 주요 테이블

## URL/API 구조 (백엔드인 경우)
- 엔드포인트 prefix별 분류

## 라우트 구조 (프론트인 경우)
- app/ or pages/ 기반

## 상태 관리 (프론트인 경우)
- Context / Redux / Zustand / Recoil 등

## 외부 연동
- API / 메시징 / 결제 등

## 이벤트/큐
- Celery / SQS / Kafka 등
```

## .claude/CONTEXT-MAP.md

**목적:** 도메인-기능-파일 매핑. "이 기능 변경하려면 어느 파일 건드려야 해?"에 답한다.

**핵심 원칙:** 한 섹션은 한 도메인에 대응. **부분 읽기를 전제**로 설계 (에이전트가 도메인 섹션만 Read).

### 백엔드 스키마
```markdown
## 도메인: {domain_name}

### 기능-API-파일 매핑
| 기능 | API | 파일 매핑 |
|------|-----|----------|
| {기능} | {METHOD /path} | models: {path}, service: {path}, view: {path} |

### 외부 연동
| 시스템 | 호출 파일 | 용도 |

### 이벤트
| 이벤트 | 발행 파일 | 소비 파일 |

### 기능 → 파일 가이드
| "이런 기능이면" | 생성/수정할 파일 |
```

### 프론트엔드 스키마
```markdown
## 도메인: {domain_name}

### 기능-라우트-파일 매핑
| 기능 | 라우트 | 파일 매핑 |
|------|--------|----------|
| {기능} | /path | page: {path}, hook: {path}, component: {path} |

### API 연동
| 백엔드 API | 프론트 훅 | 사용 페이지 |

### 컴포넌트
| 도메인 | 컴포넌트 | 사용 페이지 |

### 기능 → 파일 가이드
| "이런 기능이면" | 생성/수정할 파일 |
```

## {디렉토리}/directory.md

**목적:** 디렉토리별 역할 설명. developer/refactorer가 파일 탐색 전에 읽는다.

**스키마:**
```markdown
# {디렉토리명}

## 역할
(한 줄)

## 하위 구조
{tree}

## 주요 기능
- {기능1}: {파일}
- {기능2}: {파일}

## 관련 레이어
- 입력: (호출하는 상위 레이어)
- 출력: (의존하는 하위 레이어)
```

## history.md (프로젝트 루트)

**목적:** 에이전트가 수행한 변경 이력. orchestrator가 중복/충돌 감지에 사용.

**정렬:** 최신순 (새 항목이 위)

**엔트리 스키마:**
```markdown
## [{YYYY-MM-DD}] {run_id} — {title}
- Team: {A|B|C}
- 결과: {approved|needs_fix}
- 산출: _workspace/{run_id}/
- 요약: {1~2줄}
```

## graphify-out/graph.json (선택)

`graphify` 패키지가 생성하는 코드 관계 그래프. 스키마는 graphify 자체 문서 참조. 이 플러그인은 `/graphify query` 인터페이스만 사용.

## 갱신 규칙

- **전체 재생성:** `/setup-kb` (KB 없을 때)
- **증분 갱신:** `/setup-kb --refresh` (변경된 도메인만)
- **자동 감지:** orchestrator가 실행 전 stale 판단 → 사용자에게 `--refresh` 권장
  - 기준 1: `context.md` 이후 커밋 50개 초과
  - 기준 2: 최상위 디렉토리 신설
  - 기준 3: CONTEXT-MAP에 없는 도메인 폴더 발견

## 읽는 주체별 권장 범위 (컨텍스트 예산)

| 에이전트 | context | CONTEXT-MAP | directory | history |
|---------|---------|-------------|-----------|---------|
| planner | 전체 | 전체 | 변경 도메인 | 최근 10건 |
| architect | 전체 | 관련 도메인 섹션 | 변경 도메인 | ✕ |
| developer | 전체 | 해당 도메인 섹션 | 해당 도메인 | ✕ |
| reviewer | 전체 | 변경 도메인 섹션 | ✕ | ✕ |
| refactorer | 전체 | ✕ | 해당 도메인 | ✕ |
| debugger | 전체 | 에러 도메인 섹션 | 에러 도메인 | 최근 10건 |
| qa | 전체 | ✕ | ✕ | ✕ |
