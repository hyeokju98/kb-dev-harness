# 프레임워크 감지

| 감지 파일 | 프레임워크 | 분석 모드 |
|----------|-----------|----------|
| `manage.py` + `settings.py` | Django | backend-django |
| `next.config.*` + `app/` 또는 `pages/` | Next.js | frontend-nextjs |
| `nuxt.config.*` | Nuxt.js | frontend-nuxt |
| `main.py` + FastAPI import | FastAPI | backend-fastapi |
| `build.gradle` + `@SpringBoot` | Spring Boot | backend-spring |
| `vite.config.*` + `src/` | React/Vue (Vite) | frontend-spa |
| `package.json`만 | Node.js 일반 | backend-node |

매칭 우선순위: 위에서 아래로. 다중 매칭 시 첫 번째 사용.
