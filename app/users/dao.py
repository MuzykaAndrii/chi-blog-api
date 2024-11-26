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
