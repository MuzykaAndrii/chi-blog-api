from unittest.mock import MagicMock

import pytest

from app.rbac.exceptions import RoleNotFound
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
def mock_role_data() -> dict:
    return {
        "id": 1,
        "name": "admin",
        "permissions": [
            {"id": 1, "name": "users.can_create"},
            {"id": 2, "name": "articles.can_delete"},
        ],
    }


@pytest.fixture
def mock_role(mock_role_data: dict) -> MagicMock:
    role = MagicMock()

    role.id = mock_role_data["id"]
    role.name = mock_role_data["name"]

    role.permissions.return_value = [
        MagicMock(**mock_role_data["permissions"][0]),
        MagicMock(**mock_role_data["permissions"][1]),
    ]

    return role


def test_get_role_by_id_success(role_service: RoleService, mock_role: MagicMock):
    role_service._role_dao.get_one.return_value = mock_role

    result = role_service.get_role_by_id(mock_role.id)

    assert result.name == mock_role.name
    role_service._role_dao.get_one.assert_called_once_with(mock_role.id)


def test_get_role_by_id_not_found(role_service: RoleService):
    role_id = 999
    role_service._role_dao.get_one.return_value = None

    with pytest.raises(RoleNotFound):
        role_service.get_role_by_id(role_id)

    role_service._role_dao.get_one.assert_called_once_with(role_id)
