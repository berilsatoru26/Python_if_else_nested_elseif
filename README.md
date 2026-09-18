# GACHINGLAB MVP Scaffold

This repository now includes an MVP scaffold for **GACHINGLAB**, a cross-platform app concept that centralizes gacha account progress, gacha news, and guide links.

## Repository structure
- `/backend` – FastAPI API with PostgreSQL-ready schema and endpoints.
- `/gachinglab_app` – Flutter app shell with core screen structure.
- `Part*.py` – Original beginner Python if/else practice files retained as legacy examples.

## Implemented backend endpoints
- Auth: `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `POST /auth/logout`
- Accounts: `GET/POST /accounts`, `GET/DELETE /accounts/{id}`, `POST /accounts/{id}/sync`
- Progress: `GET /accounts/{id}/progress/latest`
- Characters: `GET /accounts/{id}/characters`
- Achievements: `GET /accounts/{id}/achievements`
- Dashboard: `GET /dashboard/summary`
- News: `GET /news`, `GET /news/{id}`, `GET /news/redeem-codes/active`
- Guides: `GET /guides`, `GET /guides/{id}`
- Notifications: `GET /notifications`, `PATCH /notifications/{id}/read`

## Flutter shell
`gachinglab_app/lib` contains navigation and placeholders for:
- Login
- Dashboard
- Linked accounts and account detail tabs
- News feed
- Guides list
- Notifications
- Settings

## Next steps
- Replace placeholder sync/ingestion logic with real integrations.
- Add full auth/session handling in Flutter.
- Add automated tests and CI pipelines for API + Flutter builds.
