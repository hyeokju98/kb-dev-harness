# Few-shot 3: 트랜잭션 누락

입력: `Order.create; Payment.create; Inventory.dec` (atomic 없음)
출력: 🔴 Critical — 멀티 테이블 write에 `@transaction.atomic` 필요.
