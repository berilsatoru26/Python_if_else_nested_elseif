from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.security import encrypt_sensitive
from app.db.models import Achievement, AuditLog, Character, LinkedAccount, ProgressSnapshot, User
from app.db.session import get_db
from app.schemas.account import (
    AchievementResponse,
    CharacterResponse,
    LinkedAccountCreate,
    LinkedAccountResponse,
    ProgressSnapshotResponse,
)
from app.services.account_sync import sync_account

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=list[LinkedAccountResponse])
def list_accounts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    accounts = db.scalars(select(LinkedAccount).where(LinkedAccount.user_id == current_user.id)).all()
    return accounts


@router.post("", response_model=LinkedAccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    payload: LinkedAccountCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    encrypted_external_id = encrypt_sensitive(payload.external_account_id)
    account = LinkedAccount(
        user_id=current_user.id,
        game=payload.game,
        provider=payload.provider,
        region=payload.region,
        external_account_id=encrypted_external_id,
        status="active",
    )
    db.add(account)
    db.flush()
    db.add(
        AuditLog(
            user_id=current_user.id,
            action="account_linked",
            details=f"Linked account for game={payload.game}, region={payload.region}, at={datetime.utcnow().isoformat()}",
        )
    )
    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}", response_model=LinkedAccountResponse)
def get_account(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.get(LinkedAccount, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.get(LinkedAccount, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    db.delete(account)
    db.add(AuditLog(user_id=current_user.id, action="account_deleted", details=f"Deleted account_id={account_id}"))
    db.commit()
    return None


@router.post("/{account_id}/sync")
def trigger_sync(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.get(LinkedAccount, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    sync_account(db, account)
    db.add(AuditLog(user_id=current_user.id, action="account_sync_triggered", details=f"Synced account_id={account_id}"))
    db.commit()
    return {"message": "Sync completed"}


@router.get("/{account_id}/progress/latest", response_model=ProgressSnapshotResponse)
def get_latest_progress(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.get(LinkedAccount, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    latest = db.scalar(
        select(ProgressSnapshot)
        .where(ProgressSnapshot.linked_account_id == account_id)
        .order_by(ProgressSnapshot.snapshot_time.desc())
    )
    if not latest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No progress snapshot found")

    return latest


@router.get("/{account_id}/characters", response_model=list[CharacterResponse])
def get_characters(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.get(LinkedAccount, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    characters = db.scalars(select(Character).where(Character.linked_account_id == account_id)).all()
    return characters


@router.get("/{account_id}/achievements", response_model=list[AchievementResponse])
def get_achievements(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.get(LinkedAccount, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    achievements = db.scalars(select(Achievement).where(Achievement.linked_account_id == account_id)).all()
    return achievements
