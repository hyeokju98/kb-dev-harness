---
description: "현재 변경사항을 확인하고 리뷰 절차를 수행합니다."
---

현재 변경사항(스테이징 버전)을 확인하고 code-reviewer 에이전트 기준으로 리뷰한다.

## 리뷰 절차
1. `git diff --staged` 실행 (없으면 `git diff HEAD`)
2. 변경된 파일을 읽어 컨텍스트 파악
3. `CLAUDE.md` Read — 프로젝트 규칙/컨벤션
4. `.claude/references/review-checklist.md`가 있으면 Read하여 체크리스트 기준 리뷰
5. ORM 쿼리가 있으면 raw SQL로 변환하여 SQL 최적화 리뷰 (불필요한 JOIN, N+1, 풀스캔, COUNT, 인덱스)
6. `graphify-out/graph.json`이 있으면 변경 코드의 의존성 체인 확인
7. cookbook 파일이 있으면 (`.claude/cookbook.pdf` 등) Read하여 더 나은 패턴 제안
8. 리뷰 결과 출력
9. `.claude-reviewed` 마커 파일 생성

## 출력
```
## 코드 리뷰 결과
### 변경 파일
### 발견된 문제
🔴 Critical / 🟡 Warning / 🟢 Info
### 아키텍처 적합성
### 총평
### 결론: ✅ 커밋 승인 / ❌ 수정 필요
```

## 완료 처리
- 승인: `git diff --staged | md5 > .claude-reviewed`
- 수정 필요: `.claude-reviewed` 생성하지 않음
