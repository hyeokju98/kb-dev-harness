# 재시도 상태 전이 (P1: max=1)

`policy/loop-limit.md` 강제. 카운터: `_workspace/{run_id}/.retry_count`.

## 전이 규칙
| 실패 단계 | 되돌릴 대상 | 이유 |
|----------|------------|------|
| reviewer Critical | → developer | 코드 수정 |
| reviewer 아키텍처 부적합 | → architect | 설계 재검토 |
| qa 테스트 FAIL | → developer | 버그 수정 |
| qa 통합 정합성 불일치 | → architect | 경계면 재설계 |
| architect가 planner 보완 다수 | → planner | 영향 분석 재작성 |

1회 후 실패 시 부분 결과 + 미해결 이슈 반환 후 사용자 개입 요청.
