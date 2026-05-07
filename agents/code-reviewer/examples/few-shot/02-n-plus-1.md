# Few-shot 2: N+1

입력: `for id in ids: Order.objects.get(id=id)`
출력: 🔴 Critical — 루프 내 단건 조회 N+1. `Order.objects.filter(id__in=ids).in_bulk()` 권고.
