from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.users.dto import UserLoginDTO
from app.users.exceptions import (
    InvalidPassword,
    UserEmailAlreadyExists,
    UserNotFound,
    UsernameAlreadyExists,
)
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


def test_get_all_users_success(user_service: UserService) -> None:
    mock_users = [
        MagicMock(id=1, username="user1", email="user1@example.com", role="viewer"),
        MagicMock(id=2, username="user2", email="user2@example.com", role="viewer"),
    ]
    user_service._dao.get_all.return_value = mock_users

    result = user_service.get_all_users()

    assert len(result.root) == 2
    assert result.root[0].username == mock_users[0].username
    assert result.root[1].username == mock_users[1].username
    user_service._dao.get_all.assert_called_once()


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


def test_create_user_email_exists(
    user_service: UserService, mock_user_create_data: dict
):
    user_service._dao.create.side_effect = IntegrityError(
        "Duplicate entry", None, "users_email_key"
    )

    with pytest.raises(UserEmailAlreadyExists):
        user_service.create(mock_user_create_data)


@pytest.mark.parametrize(
    "side_effect_error, expected_exception",
    [
        ("users_email_key", UserEmailAlreadyExists),
        ("users_username_key", UsernameAlreadyExists),
    ],
)
def test_create_user_field_exists(
    user_service: UserService,
    mock_user_create_data: dict,
    side_effect_error: str,
    expected_exception: Exception,
):
    user_service._dao.create.side_effect = IntegrityError(
        "Duplicate entry", None, side_effect_error
    )

    with pytest.raises(expected_exception):
        user_service.create(mock_user_create_data)


def test_update_user_success(
    user_service: UserService, mock_user_read: MagicMock, mock_user_create_data: dict
):
    user_service._dao.update.return_value = mock_user_read

    result = user_service.update_user(mock_user_read.id, mock_user_create_data)

    assert result.username == mock_user_read.username
    assert result.email == mock_user_read.email


def test_update_user_not_found(
    user_service: UserService, mock_user_create_data: dict
) -> None:
    user_service._dao.get_one.return_value = None

    with pytest.raises(UserNotFound):
        user_service.update_user(999, mock_user_create_data)


def test_delete_user_success(user_service: UserService) -> None:
    user_id = 1
    user_service._dao.get_one.return_value = MagicMock(id=1)
    user_service._dao.delete.return_value = None

    user_service.delete_user(user_id)

    user_service._dao.delete.assert_called_once_with(user_id)


def test_delete_user_not_found(user_service: UserService) -> None:
    user_service._dao.get_one.return_value = None

    with pytest.raises(UserNotFound):
        user_service.delete_user(999)


@pytest.mark.parametrize(
    "permission_name, is_access_granted",
    (
        ["articles.can_edit", True],
        ["users.can_delete", False],
    ),
)
def test_user_has_permission(
    permission_name: str,
    is_access_granted: bool,
    user_service: UserService,
    mock_user_read: MagicMock,
) -> None:
    mock_role = MagicMock()
    perm_edit = MagicMock()
    perm_edit.name = "articles.can_edit"
    perm_delete = MagicMock()
    perm_delete.name = "articles.can_delete"
    mock_role.permissions = [perm_edit, perm_delete]

    mock_user_read.role = mock_role
    user_service._dao.get_with_permissions.return_value = mock_user_read

    result = user_service.user_has_permission(mock_user_read.id, permission_name)

    assert result == is_access_granted
    user_service._dao.get_with_permissions.assert_called_once_with(mock_user_read.id)


def test_user_has_permission_not_found(user_service: UserService) -> None:
    user_service._dao.get_with_permissions.return_value = None

    with pytest.raises(UserNotFound):
        user_service.user_has_permission(999, "articles.can_edit")


def test_get_by_credentials_success(
    user_service: UserService, mock_user_read: MagicMock
):
    creds = {"email": "andrymyzik@gmail.com", "password": "1234567890"}
    user_service._dao.get_by_email.return_value = mock_user_read

    with patch.object(UserLoginDTO, "verify_pwd", return_value=None) as mock_pwd_check:
        result = user_service.get_by_credentials(creds)

        mock_pwd_check.assert_called_once_with(mock_user_read.password_hash)

    assert result.username == mock_user_read.username
    assert result.email == mock_user_read.email
    user_service._dao.get_by_email.assert_called_once_with(creds["email"])


def test_get_by_credentials_email_not_found(user_service: UserService) -> None:
    creds = {"email": "andrymyzik@gmail.com", "password": "1234567890"}

    user_service._dao.get_by_email.return_value = None

    with pytest.raises(UserNotFound):
        user_service.get_by_credentials(creds)


def test_get_by_credentials_invalid_password(
    user_service: UserService, mock_user_read: MagicMock
):
    creds = {"email": "andrymyzik@gmail.com", "password": "wrongpassword"}
    user_service._dao.get_by_email.return_value = mock_user_read

    with patch.object(
        UserLoginDTO, "verify_pwd", side_effect=InvalidPassword
    ) as mock_pwd_check:
        with pytest.raises(InvalidPassword):
            user_service.get_by_credentials(creds)

        mock_pwd_check.assert_called_once_with(mock_user_read.password_hash)

    user_service._dao.get_by_email.assert_called_once_with(creds["email"])
