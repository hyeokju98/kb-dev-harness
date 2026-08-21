# SQL: 트랜잭션 경계

- 멀티 테이블 write에 트랜잭션 없음 → Critical
- 트랜잭션 안에서 외부 API 호출 → Warning (롤백 불가, 락 장기 유지)
