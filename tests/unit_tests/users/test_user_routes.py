import functools
from unittest.mock import MagicMock, patch

from flask.testing import FlaskClient
import pytest
from flask import Flask, json

from app.users.services import UserService


class MockRBAC:
    def permission_required(self, permission):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator


@pytest.fixture
def app():
    app = Flask(__name__)

    with patch("app.app.rbac", MockRBAC()):
        from app.users.routes import router

        app.register_blueprint(router)

        yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def mock_user() -> dict:
    return {"id": 1, "name": "andry"}


@pytest.fixture
def mock_user_json(mock_user: dict) -> str:
    return json.dumps(mock_user)


@patch("app.users.routes.user_service")
def test_get_users_list_without_search(user_service: UserService, client: FlaskClient):
    mock_users = [{"id": 1, "name": "user1"}, {"id": 2, "name": "user2"}]
    mock_users_json = json.dumps(mock_users)

    user_service.get_all_users.return_value = mock_users_json

    response = client.get("/users")

    assert response.status_code == 200
    assert response.json == mock_users


@patch("app.users.routes.user_service")
def test_get_users_list_with_search(
    user_service: UserService,
    client: FlaskClient,
    mock_user: dict,
):
    search_q = "andry"

    mock_users = [mock_user]
    mock_users_json = json.dumps(mock_users)
    user_service.search_users_by_name.return_value = mock_users_json

    response = client.get(f"/users?name={search_q}")

    assert response.status_code == 200
    assert response.json == mock_users
    user_service.search_users_by_name.assert_called_once_with(search_q)


@patch("app.users.routes.user_service")
def test_get_user_by_id(
    user_service: UserService,
    client: FlaskClient,
    mock_user: dict,
    mock_user_json: str,
):
    user_service.get_user_by_id.return_value = mock_user_json

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json == mock_user

    user_service.get_user_by_id.assert_called_once_with(1)


@patch("app.users.routes.user_service")
def test_create_user(
    user_service: UserService,
    client: FlaskClient,
    mock_user: dict,
    mock_user_json: str,
):
    user_service.create.return_value = mock_user_json

    response = client.post("/users", json=mock_user_json)

    assert response.status_code == 201
    assert response.json == mock_user

    user_service.create.assert_called_once_with(mock_user_json)


@patch("app.users.routes.user_service")
def test_update_user(
    user_service: UserService,
    client: FlaskClient,
    mock_user: dict,
    mock_user_json: str,
):
    user_id = mock_user["id"]
    user_service.update_user.return_value = mock_user_json

    response = client.put(f"/users/{user_id}", json=mock_user_json)

    assert response.status_code == 200
    assert response.json == mock_user

    user_service.update_user.assert_called_once_with(user_id, mock_user_json)


@patch("app.users.routes.user_service")
def test_delete_user(
    user_service: UserService,
    client: FlaskClient,
):
    user_id = 1
    user_service.delete_user.return_value = None

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert response.data == b""

    user_service.delete_user.assert_called_once_with(user_id)
