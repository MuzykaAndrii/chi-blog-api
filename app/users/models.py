from sqlalchemy import (
    String,
    LargeBinary,
)
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as mc

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mc(String(length=30), unique=True, nullable=False)
    email: Mapped[str] = mc(String(length=40), unique=True, nullable=False)
    password_hash: Mapped[bytes] = mc(LargeBinary, nullable=False)

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={repr(self.username)} email={repr(self.email)})"
