from datetime import datetime, timedelta, timezone
from typing import Any

from cryptography.fernet import Fernet
from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)



def create_token(subject: str, expires_delta: timedelta, refresh: bool = False) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + expires_delta
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    secret = settings.jwt_refresh_secret_key if refresh else settings.jwt_secret_key
    return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)



def create_access_token(subject: str) -> str:
    settings = get_settings()
    return create_token(subject, timedelta(minutes=settings.access_token_expire_minutes), refresh=False)



def create_refresh_token(subject: str) -> str:
    settings = get_settings()
    return create_token(subject, timedelta(minutes=settings.refresh_token_expire_minutes), refresh=True)



def decode_token(token: str, refresh: bool = False) -> dict[str, Any]:
    settings = get_settings()
    secret = settings.jwt_refresh_secret_key if refresh else settings.jwt_secret_key
    return jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])



def encrypt_sensitive(value: str) -> str:
    key = get_settings().encryption_key.encode("utf-8")
    fernet = Fernet(key)
    return fernet.encrypt(value.encode("utf-8")).decode("utf-8")



def decrypt_sensitive(value: str) -> str:
    key = get_settings().encryption_key.encode("utf-8")
    fernet = Fernet(key)
    return fernet.decrypt(value.encode("utf-8")).decode("utf-8")
