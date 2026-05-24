from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

import jwt

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token
from app.db.models import User
from app.services.auth_service import AuthService


def get_current_user(
    session_token: str | None = Cookie(default=None, alias=None),
    db: Session = Depends(get_db),
) -> User:
    token = session_token
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        ) from exc

    user_id = payload.get("sub")
    if not isinstance(user_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session payload",
        )
    user = AuthService(db).get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )
    return user


def get_current_user_with_cookie(
    db: Session = Depends(get_db),
    growthmind_session: str | None = Cookie(default=None),
) -> User:
    """Same as get_current_user but reads the cookie by its real name."""
    if growthmind_session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = decode_access_token(growthmind_session)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        ) from exc

    user_id = payload.get("sub")
    if not isinstance(user_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session payload",
        )
    user = AuthService(db).get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
        )
    return user
