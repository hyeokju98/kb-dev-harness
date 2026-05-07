# Cache hit 측정 (원칙 8)

phase-7에 `cost.json.totals.cache_hit_rate = sum(cache_read) / sum(cache_read + tokens_in)`.

목표 **0.4+**. 미달 시 `../cache.md` breakpoint 위치 재검토.
