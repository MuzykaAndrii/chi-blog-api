from app.articles.dao import ArticleDAO
from app.articles.dto import ArticlesListReadDTO


class ArticleService:
    """Service class for handling article-related operations."""

    def __init__(self, article_dao: ArticleDAO) -> None:
        self._dao = article_dao

    def get_all_articles(self) -> ArticlesListReadDTO:
        articles = self._dao.get_all()
        return ArticlesListReadDTO(articles)
