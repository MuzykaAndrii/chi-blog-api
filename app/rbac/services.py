from app.rbac.dao import PermissionDAO, RoleDAO
from app.rbac.dto import RoleReadDTO, RolesListReadDTO
from app.rbac.exceptions import RoleNotFound


class RoleService:
    def __init__(
        self,
        role_dao: RoleDAO,
        perm_dao: PermissionDAO,
        base_roles: set[str],
        default_role: str = "viewer",
    ):
        self._role_dao = role_dao
        self_perm_dao = perm_dao
        self._base_roles = base_roles
        self._default_role = default_role
        self._base_roles.add(default_role)

    def get_all_roles(self) -> RolesListReadDTO:
        """Get all roles."""
        roles = self._role_dao.get_all(load_permissions=True)
        return RolesListReadDTO(roles)

    def get_role_by_id(self, role_id: int) -> RoleReadDTO:
        """Get a single role by ID."""
        role = self._role_dao.get_one(role_id)

        if not role:
            raise RoleNotFound

        return RoleReadDTO.model_validate(role)

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
