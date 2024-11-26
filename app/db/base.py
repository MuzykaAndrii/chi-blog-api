from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models, providing a primary key ID."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
