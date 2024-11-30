from app.db.dao import BaseDAO
from app.rbac.models import Permission


from sqlalchemy import select


class PermissionDAO(BaseDAO[Permission]):
    model = Permission

    def get_by_name(self, name: str) -> Permission | None:
        with self._sf() as session:
            return session.scalar(select(Permission).where(Permission.name == name))
