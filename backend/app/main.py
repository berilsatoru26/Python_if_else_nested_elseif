from fastapi import FastAPI

from app.api.routes import accounts, auth, dashboard, guides, news, notifications
from app.core.config import get_settings
from app.core.rate_limit import RateLimitMiddleware
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.services.news_ingestion import ingest_news_and_guides

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.add_middleware(RateLimitMiddleware, max_requests=settings.rate_limit_per_minute)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(dashboard.router)
app.include_router(news.router)
app.include_router(guides.router)
app.include_router(notifications.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ingest_news_and_guides(db)
    finally:
        db.close()
