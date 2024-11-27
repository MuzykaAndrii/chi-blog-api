from typing import Sequence
from sqlalchemy import select

from app.db.dao import BaseDAO
from .models import Article


class ArticleDAO(BaseDAO[Article]):
    """
    Data access object (DAO) for performing database operations on Article entities
    """

    model = Article

    def get_by_owner_id(self, user_id: int) -> Sequence[Article]:
        """Retrieves all articles written by a specific user."""

        query = select(Article).where(Article.owner_id == user_id)

        with self._sf() as session:
            return session.scalars(query).all()
