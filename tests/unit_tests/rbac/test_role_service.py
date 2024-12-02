from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.rbac.exceptions import RoleNotFound, RoleAlreadyExists
from app.rbac.services.role import RoleService
from app.rbac.dao.role import RoleDAO
from app.rbac.dao.permission import PermissionDAO


@pytest.fixture
def role_service() -> RoleService:
    return RoleService(
        role_dao=MagicMock(RoleDAO),
        perm_dao=MagicMock(PermissionDAO),
        base_roles=set(),
        default_role="viewer",
    )


@pytest.fixture
def mock_role_read_data() -> dict:
    return {
        "id": 1,
        "name": "admin",
        "permissions": [
            {"id": 1, "name": "users.can_create"},
            {"id": 2, "name": "articles.can_delete"},
        ],
    }


@pytest.fixture
def mock_role_read(mock_role_read_data: dict) -> MagicMock:
    role = MagicMock()

    role.id = mock_role_read_data["id"]
    role.name = mock_role_read_data["name"]

    role.permissions.return_value = [
        MagicMock(**mock_role_read_data["permissions"][0]),
        MagicMock(**mock_role_read_data["permissions"][1]),
    ]

    return role


@pytest.fixture
def mock_role_create_data() -> dict:
    return {"name": "admin"}


def test_get_role_by_id_success(role_service: RoleService, mock_role_read: MagicMock):
    role_service._role_dao.get_one.return_value = mock_role_read

    result = role_service.get_role_by_id(mock_role_read.id)

    assert result.name == mock_role_read.name
    role_service._role_dao.get_one.assert_called_once_with(mock_role_read.id)


def test_get_role_by_id_not_found(role_service: RoleService):
    role_id = 999
    role_service._role_dao.get_one.return_value = None

    with pytest.raises(RoleNotFound):
        role_service.get_role_by_id(role_id)

    role_service._role_dao.get_one.assert_called_once_with(role_id)


def test_create_role_success(
    role_service: RoleService,
    mock_role_read: MagicMock,
    mock_role_create_data: dict,
):
    role_service._role_dao.create.return_value = mock_role_read

    result = role_service.create_role(mock_role_create_data)

    assert result.name == mock_role_read.name
    role_service._role_dao.create.assert_called_once_with(**mock_role_create_data)


def test_create_role_name_exists(
    role_service: RoleService,
    mock_role_create_data: dict,
):
    role_service._role_dao.create.side_effect = IntegrityError(None, None, None)

    with pytest.raises(RoleAlreadyExists):
        role_service.create_role(mock_role_create_data)

    role_service._role_dao.create.assert_called_once_with(**mock_role_create_data)


def test_update_role_success(
    role_service: RoleService,
    mock_role_create_data: dict,
    mock_role_read: MagicMock,
):
    role_service._role_dao.update.return_value = mock_role_read

    result = role_service.update_role(mock_role_read.id, mock_role_create_data)

    assert result.name == mock_role_read.name
    role_service._role_dao.update.assert_called_once_with(
        mock_role_read.id,
        **mock_role_create_data,
    )


def test_update_role_not_found(role_service: RoleService, mock_role_create_data: dict):
    role_id = 999
    role_service._role_dao.get_one.return_value = None

    with pytest.raises(RoleNotFound):
        role_service.update_role(role_id, mock_role_create_data)

    role_service._role_dao.get_one.assert_called_once_with(role_id)
