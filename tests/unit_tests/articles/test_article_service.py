from unittest.mock import MagicMock, patch

import pytest

from app.articles.exceptions import ArticleNotFound
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


def test_get_article_by_id_not_found(article_service: ArticleService):
    article_service._dao.get_one.return_value = None

    with pytest.raises(ArticleNotFound):
        article_service.get_article_by_id(999)

    article_service._dao.get_one.assert_called_once_with(999)


def test_create_article_success(
    article_service: ArticleService, mock_article: MagicMock, mock_article_data: dict
) -> None:
    creator = MagicMock(id=1)

    article_service._dao.create.return_value = mock_article

    result = article_service.create_article(creator, mock_article_data)

    assert result.title == mock_article_data["title"]
    assert result.body == mock_article_data["body"]
    article_service._dao.create.assert_called_once_with(**mock_article_data, owner_id=1)


def test_create_article_missing_field(article_service: ArticleService):
    creator = MagicMock(id=1)
    article_data = {"body": "body without the tittle"}

    with pytest.raises(ValueError):
        article_service.create_article(creator, article_data)


def test_delete_article_success(article_service: ArticleService) -> None:
    article_id = 1

    article_service._dao.get_one.return_value = MagicMock(id=article_id)
    article_service._dao.delete.return_value = None

    article_service.delete_article(article_id)

    article_service._dao.delete.assert_called_once_with(article_id)


def test_delete_article_not_found(article_service: ArticleService) -> None:
    article_id = 999
    article_service._dao.get_one.return_value = None

    with pytest.raises(ArticleNotFound):
        article_service.delete_article(article_id)

    article_service._dao.get_one.assert_called_once_with(article_id)


def test_get_user_articles_success(article_service: ArticleService) -> None:
    user_id = 1
    mock_articles = [
        MagicMock(id=1, title="Article 1", body="Body 1", owner_id=user_id),
        MagicMock(id=2, title="Article 2", body="Body 2", owner_id=user_id),
    ]
    article_service._dao.get_by_owner_id.return_value = mock_articles

    result = article_service.get_user_articles(user_id)

    assert len(result.root) == 2
    assert result.root[0].title == "Article 1"
    assert result.root[1].title == "Article 2"
    article_service._dao.get_by_owner_id.assert_called_once_with(user_id)


def test_update_article_success(
    article_service: ArticleService, mock_article: MagicMock, mock_article_data: dict
) -> None:
    with patch.object(article_service, "_get_or_raise", return_value=None):
        article_id = 1
        article_service._dao.update.return_value = mock_article

        result = article_service.update_article(article_id, mock_article_data)

        assert result.title == mock_article_data["title"]
        assert result.body == mock_article_data["body"]

        article_service._dao.update.assert_called_once_with(
            article_id, **mock_article_data
        )
        article_service._get_or_raise.assert_called_once_with(article_id)


def test_update_article_not_found(
    article_service: ArticleService, mock_article_data: dict
) -> None:
    article_id = 999
    article_service._dao.get_one.return_value = None

    with pytest.raises(ArticleNotFound):
        article_service.update_article(article_id, mock_article_data)

    article_service._dao.get_one.assert_called_once_with(article_id)
