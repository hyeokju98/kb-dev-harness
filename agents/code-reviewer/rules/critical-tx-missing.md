# Critical: 트랜잭션 누락

여러 테이블 write에 `@transaction.atomic` 등 트랜잭션 경계 없음 → Critical.
