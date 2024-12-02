from unittest.mock import MagicMock

import pytest

from app.users.services import UserService
from app.users.dao import UserDAO


@pytest.fixture
def user_service() -> UserService:
    mock_dao = MagicMock(UserDAO)
    mock_roles = MagicMock()
    return UserService(mock_dao, mock_roles)


@pytest.fixture
def mock_user_read_data() -> dict:
    return {
        "id": 1,
        "username": "andry",
        "email": "andrymyzik@gmail.com",
        "role": "admin",
    }


@pytest.fixture
def mock_user_read(mock_user_read_data: dict) -> MagicMock:
    return MagicMock(**mock_user_read_data)


def test_get_user_by_id_success(user_service: UserService, mock_user_read: MagicMock):
    user_service._dao.get_one.return_value = mock_user_read

    result = user_service.get_user_by_id(mock_user_read.id)

    assert result.username == mock_user_read.username
    assert result.email == mock_user_read.email
    user_service._dao.get_one.assert_called_once_with(mock_user_read.id)
