from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_user_with_cookie
from app.core.security import create_access_token
from app.db.models import User
from app.schemas.auth import AuthSuccess, LoginRequest, RegisterRequest, UserOut
from app.services.auth_service import AuthError, AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_session_cookie(response: Response, user_id: str) -> None:
    token = create_access_token(user_id)
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        max_age=settings.jwt_expires_minutes * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        path="/",
    )


@router.post(
    "/register", response_model=AuthSuccess, status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> AuthSuccess:
    service = AuthService(db)
    try:
        user = service.register(
            email=payload.email,
            password=payload.password,
            display_name=payload.display_name,
        )
    except AuthError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    _set_session_cookie(response, user.id)
    return AuthSuccess(user=UserOut.model_validate(user))


@router.post("/login", response_model=AuthSuccess)
def login(
    payload: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> AuthSuccess:
    service = AuthService(db)
    try:
        user = service.authenticate(payload.email, payload.password)
    except AuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    _set_session_cookie(response, user.id)
    return AuthSuccess(user=UserOut.model_validate(user))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    response.delete_cookie(settings.cookie_name, path="/")


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user_with_cookie)) -> UserOut:
    return UserOut.model_validate(user)
