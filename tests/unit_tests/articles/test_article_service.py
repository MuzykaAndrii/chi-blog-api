from unittest.mock import MagicMock

import pytest

from app.articles.services import ArticleService
from app.articles.dao import ArticleDAO


@pytest.fixture
def article_service() -> ArticleService:
    mock_dao = MagicMock(ArticleDAO)
    return ArticleService(mock_dao)


@pytest.fixture
def mock_article_data() -> dict:
    return {"title": "New Article", "body": "Body of the article"}


@pytest.fixture
def mock_article(mock_article_data) -> MagicMock:
    return MagicMock(**mock_article_data)


def test_create_article(
    article_service: ArticleService, mock_article_data: dict, mock_article: MagicMock
):
    article_service._dao.create.return_value = mock_article

    result = article_service.create_article(
        creator=MagicMock(id=1),
        article_data=mock_article_data,
    )

    assert result.title == mock_article_data["title"]
    assert result.body == mock_article_data["body"]

    article_service._dao.create.assert_called_once_with(**mock_article_data, owner_id=1)


def test_get_article_by_id(
    article_service: ArticleService, mock_article_data: dict, mock_article: MagicMock
):
    article_service._dao.get_one.return_value = mock_article

    result = article_service.get_article_by_id(1)

    assert result.title == mock_article_data["title"]
    assert result.body == mock_article_data["body"]

    article_service._dao.get_one.assert_called_once_with(1)
