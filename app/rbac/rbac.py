from functools import wraps
from typing import Callable

from flask import jsonify

from app.rbac.protocols import SupportsGetCurrentUser, SupportsPermissionCheck


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
