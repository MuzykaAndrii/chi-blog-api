from unittest.mock import MagicMock

from flask import Flask
import pytest

from app.rbac.rbac import RoleBasedAccessController


class User:
    def __init__(self, id: int):
        self.id = id


class MockSupportsGetCurrentUser:
    def get_current_user(self) -> User:
        pass


class MockSupportsPermissionCheck:
    def user_has_permission(self, user_id: int, permission: str) -> bool:
        pass


@pytest.fixture
def mock_current_user_getter():
    return MagicMock(MockSupportsGetCurrentUser)


@pytest.fixture
def mock_permission_checker():
    return MagicMock(MockSupportsPermissionCheck)


@pytest.fixture
def access_controller(
    mock_current_user_getter: RoleBasedAccessController,
    mock_permission_checker: MagicMock,
):
    return RoleBasedAccessController(mock_current_user_getter, mock_permission_checker)


def test_permission_required_authenticated_and_authorized(
    access_controller: RoleBasedAccessController,
    mock_current_user_getter: MagicMock,
    mock_permission_checker: MagicMock,
):
    user = User(id=1)
    permission_name = "users.can_update"
    mock_current_user_getter.get_current_user.return_value = user
    mock_permission_checker.user_has_permission.return_value = True

    @access_controller.permission_required(permission_name)
    def mock_route():
        return "ok", 200

    result, status_code = mock_route()

    assert result == "ok"
    assert status_code == 200
    mock_current_user_getter.get_current_user.assert_called_once()
    mock_permission_checker.user_has_permission.assert_called_once_with(
        user.id, permission_name
    )


def test_permission_required_not_authenticated(
    access_controller: RoleBasedAccessController,
    mock_current_user_getter: MagicMock,
    test_app: Flask,
):
    mock_current_user_getter.get_current_user.return_value = None

    @access_controller.permission_required("roles.can_view")
    def mock_route():
        return "Success", 200

    with test_app.test_request_context():
        response, status_code = mock_route()

    assert status_code == 401
    assert response.json == {"error": "not authenticated"}
    mock_current_user_getter.get_current_user.assert_called_once()
