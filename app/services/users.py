from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, data: UserCreate) -> User:
        hashed_password = pwd_context.hash(data.password)
        user = User(
            email=str(data.email),
            full_name=data.full_name,
            hashed_password=hashed_password,
            is_active=data.is_active,
        )
        return self.add(user)

    def update(self, user: User, data: UserUpdate) -> User:
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.is_active is not None:
            user.is_active = data.is_active
        if data.password:
            user.hashed_password = pwd_context.hash(data.password)
        self.db.commit()
        self.db.refresh(user)
        return user
