# `_workspace/` 스키마

에이전트 팀 실행 산출물 저장 위치. 각 실행마다 `run_id`로 격리된다.

## 디렉토리 구조

```
_workspace/
└── {run_id}/                           ← YYYYMMDD-HHMM-{slug}
    ├── 00_input/
    │   ├── requirements.md             ← 사용자 입력 원본
    │   ├── asana_data.md               ← MCP 수집 (성공 시)
    │   └── figma_data.md               ← WebFetch 수집 (성공 시)
    ├── 01_planner_report.md            ← planner 산출
    ├── 02_changelog.md                 ← planner 산출
    ├── 03_architect_design.md          ← architect 산출
    ├── 04_review_result.md             ← reviewer 산출
    └── 05_qa_result.md                 ← qa 산출 (pass/fail 포함)
```

## run_id 생성 규칙

- 형식: `YYYYMMDD-HHMM-{slug}`
- slug: 티켓 ID 있으면 티켓 ID, 없으면 요청 텍스트의 소문자 슬러그 (공백 → `-`, 특수문자 제거, 최대 30자)
- 예:
  - `20260421-1045-password-policy`
  - `20260421-1532-DEV-1234`

## 파일별 스키마

### 00_input/requirements.md
```markdown
# {title}
## 출처
{Asana URL | Figma URL | 직접 입력}
## 요청 내용
{원문 텍스트}
## 필수 항목 확인 (planner)
- [ ] 변경 대상 도메인/모듈
- [ ] 변경 유형
- [ ] 영향받는 사용자 유형
```

### 01_planner_report.md
`references/output-templates/planner-report.md` 템플릿을 따른다.

### 02_changelog.md
`references/output-templates/changelog.md` 템플릿을 따른다.

### 03_architect_design.md
```markdown
## planner 레포트 보완 사항
(planner가 놓친 간접 영향 — 없으면 "없음")

## 도메인 개요
## 모듈 구조
## 데이터 모델
## 의존관계
## 외부 연동
## 마이그레이션 전략
```

### 04_review_result.md
code-reviewer의 출력 형식을 그대로 저장.

### 05_qa_result.md
qa-expert의 출력 형식을 그대로 저장. **반드시 `결론: ✅ PASS / ❌ FAIL` 라인 포함.**

## 보존 정책

- `_workspace/{run_id}/`는 삭제하지 않음 (티켓별 이력)
- `history.md`의 엔트리에서 `_workspace/{run_id}/`를 링크
- git 포함 여부는 프로젝트 정책 (팀 공유 = 포함, 로컬만 = `.gitignore`)

## 재실행 규칙

- `/start-task`로 사전 분석한 run_id가 있으면 orchestrator가 해당 run_id 재사용 (사용자에게 확인)
- 재시도(상태 전이)는 동일 run_id 안에서 파일을 덮어쓴다 (`04_review_result.md`의 경우 이전 리뷰는 `04_review_result.v1.md` 등으로 보존 가능)
