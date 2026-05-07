# Changelog

본 문서는 [Keep a Changelog](https://keepachangelog.com/) 형식과 [Semantic Versioning](https://semver.org/)을 따른다.

## [2.0.0] — 2026-05-07

대규모 재구조 릴리스. 토큰 절감 10원칙 + atomic 분할 + 거버넌스/검증 인프라 도입.

### Added
- **토큰 절감 전략 문서**: `docs/token-strategy.md` (10원칙 + P1~P4 로드맵)
- **공통 instruction**: `agents/_common/` (diff-only, graphify-fallback, peer 통신 금지 등)
- **프롬프트 기법 정의**: `agents/_techniques/` (Few-shot / CoT / ART / Multimodal CoT)
- **각 에이전트 examples/**: 도메인 맞춤 few-shot, cot, art 예시
- **JSON Schema 8종**: `references/output-templates/`
  - planner-report / changelog / architect-design / review-result / qa-result / debug-result
  - `_metadata.schema.json` (모든 산출물 required)
  - `cost.schema.json` (스테이지별 토큰/모델/비용 측정)
- **검증 스크립트**: `references/scripts/validate-output.py` (jsonschema 기반)
- **거버넌스 ADR**: `docs/data-governance.md` (분류/라이프사이클/감사)
- **파일 정책 문서**: `docs/file-size-policy.md` (Atomic ≤200 / Grouped ≤800 tier)
- **Vector KB ADR**: `docs/adr-vector-kb.md` (보류 결정 + 재검토 트리거)
- **변경 요약 문서**: `docs/changes-summary.md`
- **Orchestrator 신규 모듈**:
  - `policy/{loop-limit, retry-counter, pipeline, cache, schema-validation, cost-tracking}.md`
  - `cache.md` / `input-package.md` / `triage.md` / `retry-transitions.md` / `outputs.md`
- `.gitignore` (IDE/OS/Python 캐시 제외)

### Changed
- **에이전트 6개를 atomic 디렉토리로 분리**: `agents/{name}/{role, context-budget, procedure, output-format, references, rules/, policy/, examples/}`
- **스킬 2개 분리**: `skills/orchestrator/` (50+ atomic) + `skills/setup-kb/` (38+ atomic)
- **커맨드 2개 분리**: `commands/{self-review, start-task}/` 단계별 atomic
- **재시도 정책 강화**: 최대 2회 → **1회** (P1), 카운터 메커니즘 명시
- **모델 분리 강화**: qa/debugger 1차 **haiku** 트리아지 + opus escalation
- **reviewer 비판적 사고 완화**: Critical/Warning만 강제, Info는 선택 (nitpick 루프 방지)
- **README 갱신**: 출력 스키마 표 + 디렉토리 구조 + KB Read 패턴 명확화
- **6개 기존 스키마**: `_metadata` required 필드 추가

### Removed (Internal Restructure)
- 과분할 정정으로 67개 atomic 파일이 grouped 파일로 통합 (290 → 223 .md)
- 통합 대상:
  - `{agent}/{common, techniques, schema}.md` 3개 → `references.md`
  - `examples/cot/{reasoning, zero-shot}.md` → `cot.md`
  - `orchestrator/cache/*` 4개 → `cache.md`
  - `orchestrator/input-package/*` 4개 → `input-package.md`
  - `orchestrator/triage/*` 2개 → `triage.md`
  - `orchestrator/retry/*` 5개 + stub → `retry-transitions.md`
  - `orchestrator/outputs/*` 6개 + workspace-layout → `outputs.md`
  - `setup-kb/files/*` 5개 + stub → `files.md`
  - `setup-kb/backend/*` 5개 → `backend-analysis.md`
  - `setup-kb/frontend/*` 5개 → `frontend-analysis.md`
  - `setup-kb/frameworks/*` 7개 → `frameworks.md`
  - `qa-expert/test-runners/*` 5개 → `test-runners.md`

### Breaking Changes
- 모든 산출물 JSON Schema에 `_metadata` 필수 추가 — 이전 산출물은 `_metadata` 추가 후 재검증 필요
- 에이전트/스킬/커맨드 내부 디렉토리 구조 변경 — 외부에서 특정 atomic 파일을 직접 참조하던 경우 갱신 필요
- 플러그인 진입점(`agents/{name}.md`, `skills/{name}/SKILL.md`, `commands/{name}.md`) frontmatter는 유지

### Validation
- 모든 .md tier 통과 (atomic ≤200, grouped ≤800)
- 8개 JSON Schema syntax 통과 (Draft 2020-12)
- Python 스크립트 syntax 통과
- 깨진 cross-reference 0건

### Migration Guide
- `pip install jsonschema` (validate-output.py 의존성)
- 기존 `_workspace/{run_id}/` 산출물에 `_metadata` 필드 수동 추가 또는 재실행
- 외부에서 이전 atomic 경로(예: `cache/lookup.md`)를 참조하던 곳을 통합 경로(`cache.md`)로 갱신

### Deferred
- Vector KB 인덱싱 (`docs/adr-vector-kb.md` 트리거 충족 시 재검토)
- 다중 결재 워크플로
- 감사 로그 자동 기록 (`audit.log`)
- 컴플라이언스 매핑 (GDPR / HIPAA / SOX)

---

## [1.1.0] — 이전

자가평가 반영 — QA 실행, 재시도 상태전이, 컨텍스트 예산, 스키마 문서화.

## [1.0.x] — 초기

KB 기반 에이전트 팀 하네스 플러그인 초기 구성.
