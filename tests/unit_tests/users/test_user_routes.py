from unittest.mock import MagicMock, patch

from flask.testing import FlaskClient
import pytest
from flask import Flask, json

from app.users.services import UserService


class MockRBAC:
    def permission_required(self, permission):
        def decorator(func):
            return func

        return decorator


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)

    with patch("app.users.routes.user_service", MagicMock(UserService)):
        with patch("app.users.routes.rbac", MockRBAC()):
            from app.users.routes import router

            app.register_blueprint(router)

    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@patch("app.users.routes.user_service")
def test_get_users_list_with_search(user_service: UserService, client: FlaskClient):
    search_q = "andry"

    mock_users = [{"id": 1, "name": "andry"}]
    mock_users_json = json.dumps(mock_users)
    user_service.search_users_by_name.return_value = mock_users_json

    response = client.get(f"/users?name={search_q}")

    assert response.status_code == 200
    assert response.json == mock_users
    user_service.search_users_by_name.assert_called_once_with(search_q)
