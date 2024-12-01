from sqlalchemy.exc import IntegrityError

from app.rbac.dao.permission import PermissionDAO
from app.rbac.dao.role import RoleDAO
from app.rbac.dto import (
    PermissionsListReadDTO,
    RoleReadDTO,
    RoleWithPermsReadDTO,
    RolesWithPermsListReadDTO,
)
from app.rbac.exceptions import PermissionNotFound, RoleAlreadyExists, RoleNotFound


class RoleService:
    def __init__(
        self,
        role_dao: RoleDAO,
        perm_dao: PermissionDAO,
        base_roles: set[str],
        default_role: str = "viewer",
    ):
        self._role_dao = role_dao
        self._perm_dao = perm_dao
        self._base_roles = base_roles
        self._default_role = default_role
        self._base_roles.add(default_role)

    def get_all_roles(self) -> RolesWithPermsListReadDTO:
        """Get all roles."""
        roles = self._role_dao.get_all(load_permissions=True)
        return RolesWithPermsListReadDTO(roles)

    def get_role_by_id(self, role_id: int) -> RoleWithPermsReadDTO:
        """Get a single role by ID."""
        role = self._get_or_raise(role_id)

        return RoleWithPermsReadDTO.model_validate(role)

    def create_role(self, role_data: dict) -> RoleWithPermsReadDTO:
        try:
            created_role = self._role_dao.create(**role_data)
        except IntegrityError:
            raise RoleAlreadyExists

        return RoleReadDTO.model_validate(created_role)

    def update_role(self, role_id: int, role_data: dict) -> RoleReadDTO:
        """Update a role."""
        self._get_or_raise(role_id)

        try:
            updated_role = self._role_dao.update(role_id, **role_data)
        except IntegrityError:
            raise RoleAlreadyExists

        return RoleReadDTO.model_validate(updated_role)

    def delete_role(self, role_id: int) -> None:
        """Delete a role."""
        self._get_or_raise(role_id)

        self._role_dao.delete(role_id)

    def get_role_permissions(self, role_id: int) -> PermissionsListReadDTO:
        """Retrieves all permissions assigned to a role."""
        role = self._get_or_raise(role_id, load_permissions=True)

        return PermissionsListReadDTO.model_validate(role.permissions)

    def assign_permission_to_role(self, role_id: int, permission_id: int):
        role = self._get_or_raise(role_id, load_permissions=True)

        permission = self._perm_dao.get_one(permission_id)
        if not permission:
            raise PermissionNotFound

        updated_role = self._role_dao.add_permission(role, permission)

        return PermissionsListReadDTO.model_validate(updated_role.permissions)

    def remove_permission_from_role(self, role_id: int, permission_id: int):
        role = self._get_or_raise(role_id, load_permissions=True)

        permission = self._perm_dao.get_one(permission_id)
        if not permission:
            raise PermissionNotFound

        updated_role = self._role_dao.remove_permission(role, permission)

        return PermissionsListReadDTO.model_validate(updated_role.permissions)

    def _get_or_raise(self, role_id: int, **kwargs):
        role = self._role_dao.get_one(role_id, **kwargs)

        if not role:
            raise RoleNotFound

        return role

    def create_base_roles_if_not_exists(self):
        # TODO: refactor prints to logging

        for role_name in self._base_roles:
            if self._role_dao.get_by_name(role_name):
                print(f"Role '{role_name}' already exists, creation skipped.")
                continue

            self._role_dao.create(name=role_name)
            print(f"Role '{role_name}' created successfully.")

    @property  # maybe will good to use functools.cached_property
    def default_role_id(self) -> int:
        role = self._role_dao.get_by_name(self._default_role)

        if not role:
            raise ValueError(f"Default user role '{self._default_role}' not found.")

        return role.id
