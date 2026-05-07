# File Size Policy

이전 정책(150자 일률)이 과분할을 만들어 가독성·관리성을 해쳤다. 두 단계 tier로 재정의.

## Tier

| Tier | 한도 | 적용 대상 |
|------|------|---------|
| **Atomic** | ≤200자 | 단일 룰, 단일 예시, 단일 정책 항목 (에이전트가 선택적 Read 가능해야 가치 있음) |
| **Grouped** | ≤800자 | 같은 도메인의 정의/참조 묶음 (한 번에 같이 Read되는 게 자연스러운 것) |
| **Doc** | 제한 없음 | `docs/`, `references/output-templates/*.md` (사람이 보는 긴 설명) |

## Atomic 유지 영역
- `agents/{N}/rules/*.md` — 각 룰은 독립적, 선택적 적용
- `agents/{N}/policy/*.md` — 정책 항목별 분리 (output-cap, diff-only)
- `agents/{N}/examples/few-shot/*.md` — 각 예시는 독립적
- `agents/_common/*.md` — 공유 instruction (각 항목 한 개 룰)
- `agents/_techniques/*.md` — 기법 정의 (각 기법 한 개)
- `skills/orchestrator/teams/*.md` — Team별 분리
- `skills/orchestrator/phases/*.md` — Phase 단계별 분리
- `skills/orchestrator/policy/*.md` — 정책 항목별 분리

## Grouped로 통합한 영역 (이번 변경)
| 변경 전 | 변경 후 |
|---------|--------|
| `{agent}/{common,techniques,schema}.md` 3개 | `{agent}/references.md` |
| `{agent}/examples/cot/{reasoning,zero-shot}.md` | `{agent}/examples/cot.md` |
| `orchestrator/cache/*.md` 4개 | `orchestrator/cache.md` |
| `orchestrator/input-package/*.md` 4개 | `orchestrator/input-package.md` |
| `orchestrator/triage/*.md` 2개 | `orchestrator/triage.md` |
| `orchestrator/retry/*.md` 5개 | `orchestrator/retry-transitions.md` (기존 stub 통합) |
| `orchestrator/outputs/*.md` 6개 | `orchestrator/outputs.md` |
| `setup-kb/files/*.md` 5개 | `setup-kb/files.md` |
| `setup-kb/backend/*.md` 5개 | `setup-kb/backend-analysis.md` (기존 stub 흡수) |
| `setup-kb/frontend/*.md` 5개 | `setup-kb/frontend-analysis.md` (기존 stub 흡수) |
| `setup-kb/frameworks/*.md` 7개 | `setup-kb/frameworks.md` |
| `qa-expert/test-runners/*.md` 5개 | `qa-expert/test-runners.md` |

## 결정 기준 (앞으로 새 파일 만들 때)
1. "에이전트가 부분만 Read하면 토큰 절감 효과가 있는가?" → Yes면 Atomic
2. "한 개념을 여러 파일에 나누면 사람이 매번 다 열어봐야 하나?" → Yes면 Grouped
3. 의문이면 Grouped 우선 (병합 비용 < 분할 비용).
