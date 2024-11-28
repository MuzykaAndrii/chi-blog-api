from typing import Set

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import mapped_column as mc

from app.db.base import Base


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mc(String(length=50), unique=True, nullable=False)
    permissions: Mapped[Set["Permission"]] = relationship(
        secondary="roles_permissions", back_populates="roles"
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f"<Role(name={self.name})>"


class Permission(Base):
    __tablename__ = "permissions"

    name: Mapped[str] = mc(String(length=100), unique=True, nullable=False)
    roles: Mapped[list[Role]] = relationship(
        secondary="roles_permissions", back_populates="permissions"
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self):
        return f"<Permission(name={self.name})>"


roles_permissions = Table(
    "roles_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)
