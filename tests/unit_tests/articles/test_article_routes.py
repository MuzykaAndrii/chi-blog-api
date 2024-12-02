from unittest.mock import MagicMock, patch

from flask.testing import FlaskClient
import pytest
from flask import Flask, json

from app.articles.services import ArticleService
from app.users.dto import UserReadDTO


@pytest.fixture
def app(mock_rbac):
    app = Flask(__name__)

    with patch("app.app.rbac", mock_rbac()):
        from app.articles.routes import router

        app.register_blueprint(router)

        yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def mock_article() -> dict:
    return {
        "id": 1,
        "title": "Python from scratch",
        "content": "some contests here",
        "user_id": 1,
    }


@pytest.fixture
def mock_article_json(mock_article: dict) -> str:
    return json.dumps(mock_article)


@pytest.fixture
def mock_current_user() -> MagicMock:
    user = MagicMock()
    user.id = 1
    user.name = "andrii"
    return user


@patch("app.articles.routes.articles_service")
def test_get_articles_list_without_search(
    articles_service: ArticleService,
    client: FlaskClient,
    mock_article: dict,
):
    mock_articles = [mock_article, mock_article]
    mock_articles_json = json.dumps(mock_articles)

    articles_service.get_all_articles.return_value = mock_articles_json

    response = client.get("/articles")

    assert response.status_code == 200
    assert response.json == mock_articles


@patch("app.articles.routes.articles_service")
def test_get_articles_list_with_search(
    articles_service: ArticleService,
    client: FlaskClient,
    mock_article: dict,
):
    search_q = "python"
    mock_articles = [mock_article]
    mock_articles_json = json.dumps(mock_articles)

    articles_service.search_articles.return_value = mock_articles_json

    response = client.get(f"/articles?query={search_q}")

    assert response.status_code == 200
    assert response.json == mock_articles
    articles_service.search_articles.assert_called_once_with(search_q)


@patch("app.articles.routes.articles_service")
def test_get_user_articles(
    articles_service: ArticleService,
    client: FlaskClient,
    mock_article: dict,
):
    user_id = 1
    mock_articles = [mock_article]
    mock_articles_json = json.dumps(mock_articles)

    articles_service.get_user_articles.return_value = mock_articles_json

    response = client.get(f"/users/{user_id}/articles")

    assert response.status_code == 200
    assert response.json == mock_articles
    articles_service.get_user_articles.assert_called_once_with(user_id)


@patch("app.articles.routes.articles_service")
def test_get_article_by_id(
    articles_service: ArticleService,
    client: FlaskClient,
    mock_article: dict,
    mock_article_json: str,
):
    article_id = mock_article["id"]
    articles_service.get_article_by_id.return_value = mock_article_json

    response = client.get(f"/articles/{article_id}")

    assert response.status_code == 200
    assert response.json == mock_article

    articles_service.get_article_by_id.assert_called_once_with(article_id)
