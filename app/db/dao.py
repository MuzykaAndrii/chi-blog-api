from abc import ABC
from typing import Any, Callable, Generic, Iterable, Sequence, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from .base import Base


T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T], ABC):
    """Abstract base class for Data Access Objects with CRUD operations."""

    model: type[T]

    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self._sf = session_factory

    def get_all(self) -> Sequence[T]:
        """Get all records"""

        with self._sf() as session:
            return session.scalars(select(self.model)).all()

    def get_one(self, id_: int) -> T | None:
        """Retrieve a single record by ID."""

        with self._sf() as session:
            return session.get(self.model, id_)

    def create(self, **fields: Any) -> T:
        """Create a new record with the given fields."""

        instance = self.model(**fields)
        with self._sf() as session:
            session.add(instance)
            session.flush()
            session.commit()
        return instance

    def delete(self, id_: int) -> None:
        """Delete a record by ID."""

        with self._sf() as session:
            session.execute(delete(self.model).where(self.model.id == id_))
            session.commit()

    def update(self, id_: int, **new_data) -> T:
        """Update a record by ID with new data and return the updated record."""

        with self._sf() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id_)
                .values(**new_data)
                .returning(self.model)
            )
            res = session.execute(stmt)
            session.commit()
            return res.scalar_one()
