from app.db.dao import BaseDAO
from app.rbac.models import Permission, Role


from sqlalchemy import select
from sqlalchemy.orm import selectinload


class RoleDAO(BaseDAO[Role]):
    model = Role

    def get_all(self, load_permissions: bool = False):
        if not load_permissions:
            return super().get_all()

        with self._sf() as session:
            roles_with_permissions = session.execute(
                select(Role).options(selectinload(Role.permissions))
            )

            return roles_with_permissions.scalars().all()

    def get_one(self, id_: int, load_permissions: bool = False) -> Role | None:
        if not load_permissions:
            return super().get_one(id_)

        with self._sf() as session:
            role_with_permissions = session.execute(
                select(Role)
                .where(Role.id == id_)
                .options(selectinload(Role.permissions))
            )

            return role_with_permissions.scalar_one_or_none()

    def get_by_name(self, name: str) -> Role | None:
        with self._sf() as session:
            return session.scalar(select(Role).where(Role.name == name))

    def add_permission(self, role: Role, permission: Permission) -> Role:
        """Assign a permission to a role."""
        with self._sf() as session:
            role = session.merge(role)
            permission = session.merge(permission)

            role.permissions.add(permission)
            session.refresh(role, attribute_names=["permissions"])
            session.commit()

            return role

    def remove_permission(self, role: Role, permission: Permission) -> Role:
        """Remove a permission from a role."""
        with self._sf() as session:
            role = session.merge(role)
            permission = session.merge(permission)

            role.permissions.discard(permission)
            session.refresh(role, attribute_names=["permissions"])
            session.commit()

            return role
