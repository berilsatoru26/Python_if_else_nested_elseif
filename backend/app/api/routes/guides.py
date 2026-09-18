from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import GuideLink
from app.db.session import get_db
from app.schemas.guide import GuideLinkResponse

router = APIRouter(prefix="/guides", tags=["guides"])


@router.get("", response_model=list[GuideLinkResponse])
def list_guides(
    game: str | None = Query(default=None),
    tag: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
):
    page_size = 20
    query = select(GuideLink).order_by(GuideLink.created_at.desc())
    if game:
        query = query.where(GuideLink.game == game)

    guides = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()
    if tag:
        guides = [guide for guide in guides if tag in (guide.tags_json or [])]

    return guides


@router.get("/{guide_id}", response_model=GuideLinkResponse)
def get_guide(guide_id: int, db: Session = Depends(get_db)):
    guide = db.get(GuideLink, guide_id)
    if guide is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guide not found")
    return guide
