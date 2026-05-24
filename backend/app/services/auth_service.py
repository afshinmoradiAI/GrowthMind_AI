from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.core.security import hash_password, verify_password
from app.db.models import User


class AuthError(Exception):
    pass


class AuthService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.logger = get_logger("service.auth")

    def register(
        self, email: str, password: str, display_name: str | None
    ) -> User:
        email_normalised = email.lower().strip()
        existing = self.session.execute(
            select(User).where(User.email == email_normalised)
        ).scalar_one_or_none()
        if existing is not None:
            raise AuthError("Email is already registered")

        user = User(
            email=email_normalised,
            hashed_password=hash_password(password),
            display_name=display_name,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.logger.info("user registered id=%s", user.id)
        return user

    def authenticate(self, email: str, password: str) -> User:
        email_normalised = email.lower().strip()
        user = self.session.execute(
            select(User).where(User.email == email_normalised)
        ).scalar_one_or_none()
        if user is None or not verify_password(password, user.hashed_password):
            raise AuthError("Invalid email or password")
        return user

    def get_by_id(self, user_id: str) -> User | None:
        return self.session.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()
