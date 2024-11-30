from sqlalchemy import (
    ForeignKey,
    String,
    LargeBinary,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc

from app.articles.models import Article
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mc(String(length=30), unique=True, nullable=False)
    email: Mapped[str] = mc(String(length=40), unique=True, nullable=False)
    password_hash: Mapped[bytes] = mc(LargeBinary, nullable=False)

    role_id: Mapped[int] = mc(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(back_populates="users", lazy="joined")  # type: ignore

    articles: Mapped[list[Article]] = relationship(back_populates="owner")

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={repr(self.username)} email={repr(self.email)})"
