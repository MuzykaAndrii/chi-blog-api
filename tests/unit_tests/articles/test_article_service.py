from unittest.mock import MagicMock

import pytest

from app.articles.services import ArticleService
from app.articles.dao import ArticleDAO


@pytest.fixture
def article_service() -> ArticleService:
    mock_dao = MagicMock(ArticleDAO)
    return ArticleService(mock_dao)


def test_create_article(article_service: ArticleService):
    article_data = {"title": "New Article", "body": "Body of the article"}
    mock_article = MagicMock(**article_data)

    article_service._dao.create.return_value = mock_article

    result = article_service.create_article(
        creator=MagicMock(id=1),
        article_data=article_data,
    )

    assert result.title == article_data["title"]
    assert result.body == article_data["body"]
