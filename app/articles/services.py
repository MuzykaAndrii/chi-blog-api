from app.articles.dao import ArticleDAO
from app.articles.dto import ArticlesListReadDTO, ArticleReadDTO
from app.articles.exceptions import ArticleNotFound


class ArticleService:
    """Service class for handling article-related operations."""

    def __init__(self, article_dao: ArticleDAO) -> None:
        self._dao = article_dao

    def get_all_articles(self) -> ArticlesListReadDTO:
        articles = self._dao.get_all()
        return ArticlesListReadDTO(articles)

    def get_article_by_id(self, article_id: int) -> ArticleReadDTO:
        article = self._dao.get_one(article_id)

        if not article:
            raise ArticleNotFound

        return ArticleReadDTO.model_validate(article)
