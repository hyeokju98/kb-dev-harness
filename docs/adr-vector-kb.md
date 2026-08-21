# ADR: Vector KB 도입 보류

상태: **deferred** (재검토 트리거 — KB 전체 Read 토큰이 컨텍스트의 30% 초과 시)

## 결정
markdown + graphify 기반 KB를 유지. 벡터 인덱스 도입은 보류.

## 검토한 후보
| 옵션 | 무게 | 적합 규모 |
|------|------|----------|
| numpy + npz | 0 deps | <1k chunk |
| sqlite-vec | 확장 1개 | 1k~100k |
| DuckDB + VSS | 단일 binary | 10k~1M |
| LanceDB | Rust crate | 100k~10M |
| ChromaDB persistent | Python | 10k~1M |
| Qdrant local | 단일 binary | 100k+ |

## 보류 이유
1. 현재 markdown KB는 사람이 읽기 좋은 chunk 단위 → graphify로 구조 질의 가능
2. 추가 의존성(임베딩 모델 + DB) 도입 비용
3. token-strategy P1~P3 행동 변경만으로 70%대 절감 예상 — 먼저 측정 필요

## 도입 시 권고안
1. Tier 1 = sqlite-vec (1파일, git 친화)
2. setup-kb Phase 6.5에 인덱싱 단계 추가
3. 에이전트는 "CONTEXT-MAP 전체 Read" 대신 "top-K query"로 전환
4. graphify(구조) + vector(의미) 병행

## 재검토 트리거
- 레포 chunk 수 1k 초과
- token-strategy 적용 후에도 KB 비중이 컨텍스트의 30% 초과
- 사용자 도메인 검색 요구가 빈번해짐
