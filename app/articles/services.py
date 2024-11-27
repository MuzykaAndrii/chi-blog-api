from app.articles.dao import ArticleDAO
from app.articles.dto import ArticleCreateDTO, ArticlesListReadDTO, ArticleReadDTO
from app.articles.exceptions import ArticleNotFound
from app.users.dto import UserReadDTO


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

    def create_article(
        self, creator: UserReadDTO, article_data: dict
    ) -> ArticleReadDTO:
        validated_article = ArticleCreateDTO(**article_data)

        article_dict = validated_article.model_dump()
        article_dict["owner_id"] = creator.id

        created_article = self._dao.create(**article_dict)

        return ArticleReadDTO.model_validate(created_article)
