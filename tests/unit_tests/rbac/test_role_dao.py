from unittest.mock import MagicMock

import pytest

from app.rbac.dao.role import RoleDAO
from app.rbac.models import Role


@pytest.fixture
def role_dao() -> RoleDAO:
    mock_session_factory = MagicMock()
    return RoleDAO(mock_session_factory)


@pytest.fixture
def mock_role():
    mock_role = MagicMock()
    mock_role.id = 1
    mock_role.name = "admin"

    return mock_role


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
