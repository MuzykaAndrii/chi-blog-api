from app.articles.dao import ArticleDAO


class ArticleService:
    """Service class for handling article-related operations."""

    def __init__(self, article_dao: ArticleDAO) -> None:
        self._dao = article_dao
