from typing import Sequence
from sqlalchemy import select

from app.db.dao import BaseDAO
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
