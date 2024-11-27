from typing import Sequence
from sqlalchemy import or_, select

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

    def search_by_title_or_body(self, query: str) -> Sequence[Article]:
        """Search for articles by a partial match in title or body."""

        search_query = select(Article).where(
            or_(
                Article.title.ilike(f"%{query}%"),
                Article.body.ilike(f"%{query}%"),
            )
        )
        with self._sf() as session:
            return session.scalars(search_query).all()
