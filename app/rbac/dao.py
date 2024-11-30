from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.dao import BaseDAO
from .models import Role, Permission


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

    def get_by_name(self, name: str) -> Role | None:
        with self._sf() as session:
            return session.scalar(select(Role).where(Role.name == name))


class PermissionDAO(BaseDAO[Permission]):
    model = Permission

    def get_by_name(self, name: str) -> Permission | None:
        with self._sf() as session:
            return session.scalar(select(Permission).where(Permission.name == name))
