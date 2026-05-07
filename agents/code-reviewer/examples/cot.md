# CoT (Chain-of-Thought)

## 추론 체인
단계별로 생각하자:
1. 변경 파일/라인 식별
2. 의심 패턴 후보 수집 (SQL/auth/tx/race)
3. 호출처 역참조로 영향 확인
4. 심각도 판정 (Critical/Warning/Info)
5. 결론

## Zero-shot CoT
리뷰 시작 시 내부적으로 "단계별로 생각해 보자"를 prepend.
예시 없이도 추론 단계가 명시화됨.
