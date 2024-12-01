from datetime import datetime, timedelta, timezone

import pytest
import jwt
from unittest.mock import patch

from app.auth.exceptions import AuthenticationExpired, NotAuthenticated
from app.auth.jwt import JwtManager


@pytest.fixture
def jwt_manager():
    secret = "test_secret"
    alg = "HS256"
    exp_delta = timedelta(minutes=1)
    return JwtManager(alg, secret, exp_delta)


@pytest.fixture
def user_id():
    return 999


def test_auth_token_creation():
    alg = "mock alg"
    secret = "secret"
    exp_delta = timedelta(minutes=1)

    auth_token = JwtManager(alg, secret, exp_delta)

    assert auth_token._alg == alg
    assert auth_token._secret == secret
    assert auth_token._exp_delta == exp_delta


@patch("app.auth.jwt.datetime")
def test_create_token(mock_datetime, jwt_manager: JwtManager, user_id):
    mock_now = datetime(2034, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    mock_datetime.now.return_value = mock_now

    token = jwt_manager.create_token(user_id)
    decoded = jwt.decode(token, jwt_manager._secret, algorithms=[jwt_manager._alg])

    assert decoded["sub"] == str(user_id)
    expected_exp = mock_now + jwt_manager._exp_delta
    assert decoded["exp"] == expected_exp.timestamp()


def test_read_token(jwt_manager: JwtManager):
    sub = "mock sub"
    token = jwt.encode(
        payload={
            "exp": datetime(2034, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            "sub": sub,
        },
        key=jwt_manager._secret,
        algorithm=jwt_manager._alg,
    )

    assert jwt_manager.read_token(token) == sub


def test_read_token_expired(jwt_manager: JwtManager):
    expired_token = jwt.encode(
        payload={
            "exp": datetime(1999, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            "sub": "any sub",
        },
        key=jwt_manager._secret,
        algorithm=jwt_manager._alg,
    )

    with pytest.raises(AuthenticationExpired):
        jwt_manager.read_token(expired_token)


@patch("app.auth.jwt.jwt.decode")
def test_read_token_invalid_signature(mock_decode, jwt_manager: JwtManager):
    mock_decode.side_effect = jwt.InvalidSignatureError()

    with pytest.raises(NotAuthenticated):
        jwt_manager.read_token("head.payload.signature")


def test_read_token_invalid_token(jwt_manager: JwtManager):
    with pytest.raises(NotAuthenticated):
        jwt_manager.read_token("invalid.token.data")
