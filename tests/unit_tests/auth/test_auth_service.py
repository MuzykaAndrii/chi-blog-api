from datetime import timedelta
from unittest.mock import MagicMock
from flask import Flask
import pytest
from app.auth.jwt import JwtManager
from app.auth.services import AuthService


@pytest.fixture
def jwt_manager():
    return JwtManager("HS256", "test_secret", timedelta(days=1))


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

    assert response.status_code == 200
    assert "token" in response.get_json()
