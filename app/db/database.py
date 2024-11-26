from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .config import DbSettings


class Database:
    """Manages the database connection and provides a session factory."""

    def __init__(self, settings: DbSettings) -> None:
        self._engine = create_engine(settings.DATABASE_URL)
        self._session_factory = sessionmaker(self._engine, expire_on_commit=False)

    @property
    def session_factory(self) -> Callable[[], Session]:
        """Retrieve a callable session factory for database sessions."""
        return self._session_factory
