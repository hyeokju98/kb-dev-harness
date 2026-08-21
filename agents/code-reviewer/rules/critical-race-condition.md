# Critical: Race Condition

SELECT → 조건 분기 → UPDATE를 락 없이 수행 → Critical. `select_for_update` 또는 분산 락 권고.
