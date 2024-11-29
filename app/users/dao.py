from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.dao import BaseDAO
from app.rbac.models import Role
from .models import User


class UserDAO(BaseDAO[User]):
    """
    Data access object (DAO) for performing database operations on User entities
    """

    model = User

    def get_by_email(self, email: str) -> User | None:
        """Retrieves a user by their email address."""

        with self._sf() as session:
            return session.scalar(select(User).where(User.email == email))

    def search_by_name(self, name: str) -> Sequence[User]:
        """Searches for users by a partial or full name match."""
        query = select(User).where(User.username.ilike(f"%{name}%"))

        with self._sf() as session:
            return session.scalars(query).all()

    def get_with_permissions(self, user_id: int) -> User | None:
        query = (
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.role).selectinload(Role.permissions))
        )
        with self._sf() as session:
            return session.scalar(query)
