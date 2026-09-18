import time

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models import Achievement, Character, LinkedAccount, NewsItem, GuideLink, User
from app.db.session import get_db
from app.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
CACHE_SECONDS = 60
_cache_data: dict[int, tuple[float, DashboardSummary]] = {}


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = time.time()
    cached = _cache_data.get(current_user.id)
    if cached and now - cached[0] < CACHE_SECONDS:
        return cached[1]

    account_ids_subquery = select(LinkedAccount.id).where(LinkedAccount.user_id == current_user.id)

    total_accounts = db.scalar(select(func.count()).select_from(LinkedAccount).where(LinkedAccount.user_id == current_user.id)) or 0
    total_characters = db.scalar(
        select(func.count()).select_from(Character).where(Character.linked_account_id.in_(account_ids_subquery))
    ) or 0
    unlocked_achievements = db.scalar(
        select(func.count())
        .select_from(Achievement)
        .where(Achievement.linked_account_id.in_(account_ids_subquery), Achievement.is_unlocked.is_(True))
    ) or 0
    latest_news_count = db.scalar(select(func.count()).select_from(NewsItem)) or 0
    guides_count = db.scalar(select(func.count()).select_from(GuideLink)) or 0

    summary = DashboardSummary(
        total_accounts=total_accounts,
        total_characters=total_characters,
        unlocked_achievements=unlocked_achievements,
        latest_news_count=latest_news_count,
        guides_count=guides_count,
    )
    _cache_data[current_user.id] = (now, summary)
    return summary
