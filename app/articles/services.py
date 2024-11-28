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

    def get_user_articles(self, user_id: int) -> ArticlesListReadDTO:
        user_articles = self._dao.get_by_owner_id(user_id)

        return ArticlesListReadDTO(user_articles)

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

    def search_articles(self, query: str) -> ArticlesListReadDTO:
        found_articles = self._dao.search_by_title_or_body(query)

        return ArticlesListReadDTO.model_validate(found_articles)

    def delete_article(self, article_id: int) -> None:
        article = self._dao.get_one(article_id)

        if not article:
            raise ArticleNotFound

        return self._dao.delete(article_id)

    def update_article(self, article_id: int, update_data: dict) -> ArticleReadDTO:
        article = self._dao.get_one(article_id)

        if not article:
            raise ArticleNotFound

        validated_article = ArticleCreateDTO(**update_data)
        updated_article = self._dao.update(article_id, **validated_article.model_dump())

        return ArticleReadDTO.model_validate(updated_article)
