from sqlalchemy import select

from app.db.dao import BaseDAO
from .models import Role, Permission


class RoleDAO(BaseDAO[Role]):
    model = Role

    def get_by_name(self, name: str) -> Role | None:
        with self._sf() as session:
            return session.scalar(select(Role).where(Role.name == name))


class PermissionDAO(BaseDAO[Permission]):
    model = Permission

    def get_by_name(self, name: str) -> Permission | None:
        with self._sf() as session:
            return session.scalar(select(Permission).where(Permission.name == name))
