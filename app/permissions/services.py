from app.permissions.dao import RoleDAO


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
