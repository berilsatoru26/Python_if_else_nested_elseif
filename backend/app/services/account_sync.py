from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models import Achievement, Character, LinkedAccount, ProgressSnapshot



def sync_account(db: Session, account: LinkedAccount) -> None:
    existing_snapshot = db.scalar(
        select(ProgressSnapshot)
        .where(ProgressSnapshot.linked_account_id == account.id)
        .order_by(ProgressSnapshot.snapshot_time.desc())
    )

    db.add(
        ProgressSnapshot(
            linked_account_id=account.id,
            snapshot_time=datetime.utcnow(),
            level=(existing_snapshot.level + 1 if existing_snapshot else 1),
            world_level=min((existing_snapshot.world_level + 1 if existing_snapshot else 1), 9),
            stats_json={"sync_source": account.provider, "region": account.region},
        )
    )

    db.execute(delete(Character).where(Character.linked_account_id == account.id))
    db.execute(delete(Achievement).where(Achievement.linked_account_id == account.id))

    db.add_all(
        [
            Character(
                linked_account_id=account.id,
                character_name="Traveler",
                rarity=5,
                level=80,
                element="Anemo",
                metadata_json={"weapon": "Sword"},
            ),
            Character(
                linked_account_id=account.id,
                character_name="Noelle",
                rarity=4,
                level=70,
                element="Geo",
                metadata_json={"weapon": "Claymore"},
            ),
        ]
    )

    db.add_all(
        [
            Achievement(
                linked_account_id=account.id,
                achievement_key="first_domain_clear",
                title="First Domain Clear",
                is_unlocked=True,
                unlocked_at=datetime.utcnow(),
            ),
            Achievement(
                linked_account_id=account.id,
                achievement_key="collect_100_items",
                title="Collector I",
                is_unlocked=False,
            ),
        ]
    )
