from unittest.mock import MagicMock

import pytest

from app.rbac.dao.role import RoleDAO
from app.rbac.models import Permission, Role


@pytest.fixture
def role_dao() -> RoleDAO:
    mock_session_factory = MagicMock()
    return RoleDAO(mock_session_factory)


@pytest.fixture
def mock_role_create_data() -> dict:
    return {"name": "admin"}


@pytest.fixture
def mock_role():
    mock_role = MagicMock(Role)
    mock_role.id = 1
    mock_role.name = "admin"

    return mock_role


@pytest.fixture
def mock_permission() -> MagicMock:
    mock_perm = MagicMock(Permission)
    mock_perm.id = 1
    mock_perm.name = "users.can_delete"
    return mock_perm


def test_get_role_by_id(role_dao: RoleDAO, mock_role: MagicMock):
    mock_session = MagicMock()
    role_dao._sf.return_value.__enter__.return_value = mock_session
    mock_session.get.return_value = mock_role

    result = role_dao.get_one(1)

    assert result.id == 1
    assert result.name == "admin"
    mock_session.get.assert_called_once_with(Role, 1)


def test_get_all_roles(role_dao: RoleDAO, mock_role: MagicMock):
    mock_session = MagicMock()
    role_dao._sf.return_value.__enter__.return_value = mock_session
    mock_session.scalars.return_value.all.return_value = [mock_role, mock_role]

    result = role_dao.get_all()

    assert len(result) == 2
    assert result[0].name == mock_role.name
    assert result[1].name == mock_role.name

    mock_session.scalars.assert_called_once()


def test_create_role(
    role_dao: RoleDAO,
    mock_role: MagicMock,
    mock_role_create_data: dict,
):
    mock_session = MagicMock()
    role_dao._sf.return_value.__enter__.return_value = mock_session

    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    result = role_dao.create(**mock_role_create_data)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert result.name == mock_role.name


def test_add_permission_success(role_dao: RoleDAO):
    role = Role(id=1)
    permission = Permission(id=1)
    mock_session = MagicMock()

    role_dao._sf.return_value.__enter__.return_value = mock_session
    mock_session.merge.side_effect = lambda x: x

    updated_role = role_dao.add_permission(role, permission)

    assert permission in updated_role.permissions
    mock_session.merge.assert_any_call(role)
    mock_session.merge.assert_any_call(permission)
    mock_session.refresh.assert_called_once_with(role, attribute_names=["permissions"])
    mock_session.commit.assert_called_once()
