from datetime import timedelta
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify
from flask.testing import FlaskClient
import pytest
from app.auth.exceptions import NotAuthenticated
from app.auth.jwt import JwtManager
from app.auth.services import AuthService


@pytest.fixture
def jwt_manager() -> JwtManager:
    manager = MagicMock()
    manager.create_token.return_value = "jwt token"
    return manager


@pytest.fixture
def mock_user_service():
    mock_service = MagicMock()
    mock_service.get_by_credentials.return_value = MagicMock(id=1)
    mock_service.get_user_by_id.return_value = MagicMock(id=1)
    return mock_service


@pytest.fixture
def auth_service(jwt_manager, mock_user_service) -> AuthService:
    return AuthService(jwt_manager, mock_user_service)


def test_login_user(test_app: Flask, auth_service: AuthService):
    credentials = {"username": "test", "password": "1234567890"}

    with test_app.test_request_context():
        response = auth_service.login_user(credentials)

    json_response = response.get_json()

    assert response.status_code == 200
    assert "token" in json_response.keys()
    assert "jwt token" in json_response.values()


def test_login_user_invalid_credentials(auth_service: AuthService, mock_user_service):
    mock_user_service.get_by_credentials.side_effect = NotAuthenticated

    credentials = {"username": "test", "password": "wrongpassword"}

    with pytest.raises(NotAuthenticated):
        auth_service.login_user(credentials)


def test_get_current_user(auth_service: AuthService, client: FlaskClient):
    client.set_cookie(auth_service.cookie_name, "some token")

    with client.application.test_request_context():
        user = auth_service.get_current_user()
        assert user.id == 1


def test_login_required(auth_service: AuthService, test_app: Flask):
    with patch.object(auth_service, "get_current_user", return_value=None):

        @auth_service.login_required
        def protected_route(*args, **kwargs):
            return jsonify({"success": "Access granted"})

        with test_app.test_request_context():
            response, status_code = protected_route()
            assert status_code == 401
            assert response.get_json() == {"error": "not authenticated"}
