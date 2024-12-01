from unittest.mock import MagicMock

import pytest

from app.articles.dao import ArticleDAO


@pytest.fixture
def article_dao() -> ArticleDAO:
    mock_session_factory = MagicMock()
    return ArticleDAO(mock_session_factory)


def test_get_by_owner_id(article_dao: ArticleDAO):
    mock_session = MagicMock()
    article_dao._sf.return_value.__enter__.return_value = mock_session
    mock_session.scalars.return_value.all.return_value = [
        MagicMock(id=1, title="Article 1", body="Body of article 1", owner_id=1),
        MagicMock(id=2, title="Article 2", body="Body of article 2", owner_id=1),
    ]

    result = article_dao.get_by_owner_id(1)

    assert len(result) == 2
    assert result[0].title == "Article 1"
    assert result[1].title == "Article 2"
