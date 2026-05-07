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

## Anthropic Prompt Cache
공통 시스템 프롬프트(공유 instruction)는 cache breakpoint 앞에 배치.
요청별 변동 부분은 breakpoint 뒤. 5분 TTL.
