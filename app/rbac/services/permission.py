from app.rbac.dao.permission import PermissionDAO
from app.rbac.dto import PermissionsListReadDTO


class PermissionService:
    def __init__(self, permission_dao: PermissionDAO):
        self._permission_dao = permission_dao

    def get_all_permissions(self) -> PermissionsListReadDTO:
        permissions = self._permission_dao.get_all()
        return PermissionsListReadDTO.model_validate(permissions)
