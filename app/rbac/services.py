from typing import Callable
from functools import wraps

from flask import jsonify

from app.rbac.dao import RoleDAO
from app.rbac.protocols import SupportsGetCurrentUser, SupportsPermissionCheck


class RoleService:
    def __init__(
        self,
        role_dao: RoleDAO,
        base_roles: set[str],
        default_role: str = "viewer",
    ):
        self._dao = role_dao
        self._base_roles = base_roles
        self._default_role = default_role
        self._base_roles.add(default_role)

    def create_base_roles_if_not_exists(self):
        # TODO: refactor prints to logging

        for role_name in self._base_roles:
            if self._dao.get_by_name(role_name):
                print(f"Role '{role_name}' already exists, creation skipped.")
                continue

            self._dao.create(name=role_name)
            print(f"Role '{role_name}' created successfully.")

    @property  # maybe will good to use functools.cached_property
    def default_role_id(self) -> int:
        role = self._dao.get_by_name(self._default_role)

        if not role:
            raise ValueError(f"Default user role '{self._default_role}' not found.")

        return role.id


class RoleBasedAccessController:
    def __init__(
        self,
        current_user_getter: SupportsGetCurrentUser,
        permission_checker: SupportsPermissionCheck,
    ):
        self.current_user_getter = current_user_getter
        self.permission_checker = permission_checker

    def permission_required(self, permission: str):

        def decorator(router_func: Callable):

            @wraps(router_func)
            def wrapper(*args, **kwargs):
                current_user = self.current_user_getter.get_current_user()

                if not current_user:
                    return jsonify({"error": "not authenticated"}), 401

                if not self.permission_checker.user_has_permission(
                    current_user.id, permission
                ):
                    return jsonify({"error": "Permission denied"}), 403

                return router_func(*args, **kwargs)

            return wrapper

        return decorator
