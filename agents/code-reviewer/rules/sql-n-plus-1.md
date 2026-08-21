# SQL: N+1

루프 안 `.objects.get()` / `.filter()`, Serializer가 FK 접근 → 의심. `select_related` (1:1, FK) / `prefetch_related` (M2M, 역참조).
