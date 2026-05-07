# Read Policy (Selective)

## 항상 Read (sticky)
role / context-budget / references

## 조건부 Read
- 외부 입력 (Asana/Figma) → `phase-1-input`, `phase-2-alignment`
- 신규 도메인 → `phase-2-alignment`, `phase-3-as-is`
- 변경 분석 → `phase-4-impact`, `phase-5-changelog`
- Figma 이미지 → `examples/multimodal-cot/figma-flow`
- 영향 표 → `rules/cite-line-numbers`, `rules/evidence-based`, `rules/good-example`
- 하위호환 의심 → `rules/explicit-breaking`, `rules/no-underestimate`
- 모호한 사례 → `examples/few-shot/*` 1~2개

## 끝(recency)
`output`
