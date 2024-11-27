from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column as mc
from sqlalchemy.sql import func

from app.db.base import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mc(primary_key=True, autoincrement=True)
    title: Mapped[str] = mc(String(length=255), nullable=False)
    body: Mapped[str] = mc(Text, nullable=False)
    created_at: Mapped[DateTime] = mc(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    owner_id: Mapped[int] = mc(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="articles")  # type: ignore

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"Article(id={self.id}, title={repr(self.title)}, created_at={repr(self.created_at)})"
