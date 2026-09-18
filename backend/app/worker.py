import time

from app.db.session import SessionLocal
from app.services.news_ingestion import ingest_news_and_guides



def run_worker(poll_seconds: int = 900) -> None:
    while True:
        db = SessionLocal()
        try:
            ingest_news_and_guides(db)
        finally:
            db.close()
        time.sleep(poll_seconds)


if __name__ == "__main__":
    run_worker()
