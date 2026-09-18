from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.db.models import NewsItem
from app.db.session import get_db
from app.schemas.news import NewsItemResponse

router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=list[NewsItemResponse])
def list_news(
    game: str | None = Query(default=None),
    category: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    page_size = 20
    conditions = []
    if game:
        conditions.append(NewsItem.game == game)
    if category:
        conditions.append(NewsItem.category == category)

    query = select(NewsItem).order_by(NewsItem.published_at.desc())
    if conditions:
        query = query.where(and_(*conditions))

    query = query.offset((page - 1) * page_size).limit(page_size)
    return db.scalars(query).all()


@router.get("/redeem-codes/active", response_model=list[NewsItemResponse])
def get_active_redeem_codes(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    query = select(NewsItem).where(
        NewsItem.category == "redeem_code",
        NewsItem.code_value.is_not(None),
        (NewsItem.valid_to.is_(None) | (NewsItem.valid_to >= now)),
    )
    return db.scalars(query).all()


@router.get("/{news_id}", response_model=NewsItemResponse)
def get_news(news_id: int, db: Session = Depends(get_db)):
    item = db.get(NewsItem, news_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News item not found")
    return item
