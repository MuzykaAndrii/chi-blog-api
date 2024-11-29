from typing import Callable
from functools import wraps

from flask import jsonify

from app.rbac.dao import RoleDAO
from app.auth.services import AuthService  # refactor with protocol
from app.users.services import UserService  # refactor with protocol


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


class AuthorizationService:
    def __init__(self, auth_service: AuthService, user_service: UserService):
        self.auth = auth_service
        self.users = user_service

    def permission_required(self, permission: str):

        def decorator(router_func: Callable):

            @wraps(router_func)
            def wrapper(*args, **kwargs):
                user = self.auth.get_current_user()

                if not user:
                    raise ValueError

                has_perm = self.users.user_has_permission(user.id, permission)

                if not has_perm:
                    return jsonify({"error": "Permission denied"}), 403

                return router_func(*args, **kwargs)

            return wrapper

        return decorator
