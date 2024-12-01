from sqlalchemy.exc import IntegrityError

from app.rbac.dao.permission import PermissionDAO
from app.rbac.dto import PermissionReadDTO, PermissionsListReadDTO
from app.rbac.exceptions import PermissionAlreadyExists, PermissionNotFound


class PermissionService:
    def __init__(self, permission_dao: PermissionDAO):
        self._permission_dao = permission_dao

    def get_all_permissions(self) -> PermissionsListReadDTO:
        permissions = self._permission_dao.get_all()
        return PermissionsListReadDTO.model_validate(permissions)

    def get_permission_by_id(self, permission_id: int) -> PermissionReadDTO:
        permission = self._get_or_raise(permission_id)

        return PermissionReadDTO.model_validate(permission)

    def create_permission(self, permission_data: dict) -> PermissionReadDTO:
        try:
            permission = self._permission_dao.create(**permission_data)
        except IntegrityError:
            raise PermissionAlreadyExists

        return PermissionReadDTO.model_validate(permission)

    def update_permission(
        self, permission_id: int, permission_data: dict
    ) -> PermissionReadDTO:
        try:
            permission = self._permission_dao.update(permission_id, **permission_data)
        except IntegrityError:
            raise PermissionAlreadyExists

        if not permission:
            raise PermissionNotFound

        return PermissionReadDTO.model_validate(permission)

    def delete_permission(self, permission_id: int) -> None:
        self._get_or_raise(permission_id)

        return self._permission_dao.delete(permission_id)

    def _get_or_raise(self, permission_id: int):
        permission = self._permission_dao.get_one(permission_id)

        if not permission:
            raise PermissionNotFound

        return permission
