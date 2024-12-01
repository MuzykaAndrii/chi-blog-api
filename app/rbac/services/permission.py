from app.rbac.dao.permission import PermissionDAO
from app.rbac.dto import PermissionReadDTO, PermissionsListReadDTO
from app.rbac.exceptions import PermissionNotFound


class PermissionService:
    def __init__(self, permission_dao: PermissionDAO):
        self._permission_dao = permission_dao

    def get_all_permissions(self) -> PermissionsListReadDTO:
        permissions = self._permission_dao.get_all()
        return PermissionsListReadDTO.model_validate(permissions)

    def get_permission_by_id(self, permission_id: int) -> PermissionReadDTO:
        permission = self._permission_dao.get_one(permission_id)

        if not permission:
            raise PermissionNotFound

        return PermissionReadDTO.model_validate(permission)
