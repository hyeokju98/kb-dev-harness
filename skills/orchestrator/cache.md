# 캐시 (원칙 8)

## 키
`SHA256(file_paths + file_mtimes + task_brief)`. 입력 동일 → 키 동일 → 이전 산출물 재사용.

## Lookup
각 단계 dispatch 전:
1. 키 계산
2. `_workspace/{run_id}/.cache/{key}.json` 확인
3. 있으면 산출물 복사, 에이전트 호출 skip
4. 없으면 dispatch 후 결과 저장

## Storage
위치: `_workspace/{run_id}/.cache/{key}.json`
내용: 단계 산출물 + 메타(에이전트, 모델, ts)
TTL: 동일 run_id 내 영구.

## Anthropic Prompt Cache (5분 TTL)

### Prompt 구조 (breakpoint 위치)
```
[시스템] CLAUDE.md + agents/_common/* + agents/_techniques/*
[CACHE BREAKPOINT 1]  ← 모든 에이전트 호출 공유
[에이전트] {name}/role + context-budget + references + read-policy
[CACHE BREAKPOINT 2]  ← 같은 에이전트 반복 호출 시 hit
[작업] task_brief + upstream_summary + file_refs
```

측정은 `policy/cache-measurement.md` (목표 hit_rate 0.4+).
