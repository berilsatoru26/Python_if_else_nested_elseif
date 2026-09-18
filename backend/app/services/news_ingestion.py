from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.db.models import GuideLink, GuideSource, NewsItem, NewsSource



def ingest_news_and_guides(db: Session) -> None:
    db.execute(delete(NewsItem))

    source = db.query(NewsSource).filter(NewsSource.name == "Official Feed").first()
    if source is None:
        source = NewsSource(name="Official Feed", type="rss", url="https://example.com/news.xml", is_active=True)
        db.add(source)
        db.flush()

    db.add_all(
        [
            NewsItem(
                source_id=source.id,
                game="Genshin Impact",
                category="redeem_code",
                title="New redeem code available",
                content="Use this limited-time code for primogems.",
                url="https://example.com/redeem",
                code_value="WELCOME123",
                valid_from=datetime.utcnow(),
                valid_to=datetime.utcnow() + timedelta(days=7),
                published_at=datetime.utcnow(),
            ),
            NewsItem(
                source_id=source.id,
                game="Honkai: Star Rail",
                category="update",
                title="Version update highlights",
                content="New banner and events announced.",
                url="https://example.com/update",
                published_at=datetime.utcnow(),
            ),
        ]
    )

    guide_source = db.query(GuideSource).filter(GuideSource.name == "Community Guides").first()
    if guide_source is None:
        guide_source = GuideSource(name="Community Guides", url="https://example.com/guides", is_trusted=True, is_active=True)
        db.add(guide_source)
        db.flush()

    if db.query(GuideLink).count() == 0:
        db.add_all(
            [
                GuideLink(
                    source_id=guide_source.id,
                    game="Genshin Impact",
                    title="Beginner progression guide",
                    url="https://example.com/guides/beginner",
                    tags_json=["beginner", "progression"],
                ),
                GuideLink(
                    source_id=guide_source.id,
                    game="Honkai: Star Rail",
                    title="Team-building guide",
                    url="https://example.com/guides/team-building",
                    tags_json=["teams", "builds"],
                ),
            ]
        )

    db.commit()
