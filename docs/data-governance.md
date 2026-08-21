# Data Governance Policy

상태: **active** (메타데이터 스키마 적용 시점부터 강제)

## 목적

산출물의 ownership, sensitivity, retention을 명시적으로 관리하여 거버넌스 격차(전체 점검 4번)를 좁힌다.

## 메타데이터 표준

모든 에이전트 산출물은 `_metadata` 필드를 가진다. 정의는 `references/output-templates/_metadata.schema.json`.

| 필드 | 필수 | 설명 |
|------|-----|------|
| `owner` | ✅ | 산출물 책임자 (사용자 이메일 또는 팀 핸들) |
| `sensitivity` | ✅ | `public / internal / confidential / restricted` |
| `retention_days` | ✅ | 보관 기간(일). 0=즉시 삭제 가능, 미정의=무기한 |
| `created_by_agent` | ✅ | 생성 에이전트 식별자 |
| `created_at` | ✅ | ISO 8601 datetime |
| `model` | 선택 | `opus / sonnet / haiku` |
| `evidence_methods` | 선택 | `read / grep / graphify` 다중 |

## 분류 정책

| sensitivity | 예 | retention_days |
|-------------|------|----------------|
| public | OSS 프로젝트 changelog | 무기한 |
| internal | 사내 프로젝트 영향 분석, 리뷰 | 365 |
| confidential | 보안 결함 디버깅 결과 | 90 |
| restricted | 인증/결제/PII 관련 산출물 | 30 + 별도 승인 필요 |

## 라이프사이클

- **생성**: orchestrator가 dispatch 직전에 `_metadata` 채워서 input-package에 포함
- **검증**: phase-4에서 `validate-output.py`로 스키마 검증 (필수 필드 누락 시 fail)
- **만료**: `_workspace/{run_id}/` mtime + `retention_days` 경과 시 사용자에게 정리 권고
- **삭제**: 사용자 명시 동의 후 manual

## 접근 제어

현재 파일시스템 권한 위임. 향후 보강 후보:
- `restricted` 산출물은 `.gitignore`에 자동 추가 안내
- 사내 보안 정책에 따라 별도 저장소로 격리

## 감사

`history.md`에 run_id별 ownership 메타 1줄 추가:
```
## [{date}] {run_id} — {title}
- owner: {owner}
- sensitivity: {sensitivity}
- retention: {retention_days}d
```

## 미적용 (후속)

- 변경 승인 워크플로 (다중 결재)
- 감사 로그 (`_workspace/audit.log`)
- 컴플라이언스 매핑 (GDPR/HIPAA/SOX)
- 데이터 lineage 자동 추적
