from unittest.mock import MagicMock

import pytest

from app.users.exceptions import UserNotFound
from app.users.services import UserService
from app.users.dao import UserDAO


@pytest.fixture
def user_service() -> UserService:
    mock_dao = MagicMock(UserDAO)
    mock_role_getter = MagicMock(default_role_id=1)
    return UserService(mock_dao, mock_role_getter)


@pytest.fixture
def mock_user_read_data() -> dict:
    return {
        "id": 1,
        "username": "andry",
        "email": "andrymyzik@gmail.com",
        "role": "viewer",
    }


@pytest.fixture
def mock_user_read(mock_user_read_data: dict) -> MagicMock:
    return MagicMock(**mock_user_read_data)


@pytest.fixture
def mock_user_create_data() -> dict:
    return {
        "username": "andry",
        "email": "andrymyzik@gmail.com",
        "password": "password123",
        "role_id": 1,
    }


def test_get_user_by_id_success(user_service: UserService, mock_user_read: MagicMock):
    user_service._dao.get_one.return_value = mock_user_read

    result = user_service.get_user_by_id(mock_user_read.id)

    assert result.username == mock_user_read.username
    assert result.email == mock_user_read.email
    user_service._dao.get_one.assert_called_once_with(mock_user_read.id)


def test_get_user_by_id_not_found(user_service: UserService):
    user_id = 999
    user_service._dao.get_one.return_value = None

    with pytest.raises(UserNotFound):
        user_service.get_user_by_id(user_id)

    user_service._dao.get_one.assert_called_once_with(999)


def test_search_users_by_name_success(user_service: UserService) -> None:
    search_name = "test"
    mock_users = [
        MagicMock(id=1, username="testuser1", email="test1@email.com", role="viewer"),
        MagicMock(id=2, username="testuser2", email="test@2email.com", role="viewer"),
    ]
    user_service._dao.search_by_name.return_value = mock_users

    result = user_service.search_users_by_name(search_name)

    assert len(result.root) == 2
    assert result.root[0].username == "testuser1"
    assert result.root[1].username == "testuser2"
    user_service._dao.search_by_name.assert_called_once_with(search_name)


def test_create_user_success(
    user_service: UserService, mock_user_read: MagicMock, mock_user_create_data: dict
):
    user_service._dao.create.return_value = mock_user_read

    result = user_service.create(mock_user_create_data)

    assert result.username == mock_user_read.username
    assert result.email == mock_user_read.email
