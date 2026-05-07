# Read Policy (Selective)

## 항상 Read (sticky)
role / context-budget / references / output / phase-1-input / phase-4-impact

## 조건부 Read
- 외부 입력 있음 (Asana/Figma) → phase-1, phase-2-alignment
- 신규 도메인 → phase-2-alignment, phase-3-as-is
- 변경 분석 본격 → phase-4-impact, phase-5-changelog
- 모호한 사례 → `examples/few-shot/` 1~2개
- Figma 이미지 입력 → `examples/multimodal-cot/figma-flow.md`
- 영향 표 작성 → `rules/cite-line-numbers`, `evidence-based`, `good-example`
- 하위호환 의심 → `rules/explicit-breaking`, `no-underestimate`

## 끝(recency)
output.md (산출물 작성 직전)
