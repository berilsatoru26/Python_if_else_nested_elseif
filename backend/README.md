# GACHINGLAB Backend (FastAPI)

## Features implemented
- JWT auth (`/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`)
- Linked account APIs and sync trigger
- Progress/characters/achievements APIs
- Dashboard aggregate summary API
- News feed APIs (including active redeem codes)
- Guides APIs
- Notifications APIs
- In-memory rate limiting middleware
- Sensitive external account id encryption
- Worker entrypoint for periodic ingestion

## Run locally
1. Create a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Configure env values from `backend/.env.example`.
4. Start API:
   ```bash
   uvicorn app.main:app --app-dir backend --reload
   ```
5. (Optional) Start worker:
   ```bash
   python -m app.worker
   ```

## Notes
- Database schema is auto-created at startup via SQLAlchemy metadata.
- Replace placeholder news/guide ingestion with real provider integrations that comply with each source ToS.
