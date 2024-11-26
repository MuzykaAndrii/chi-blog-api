from pydantic import computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


_DB_URL_PATTERN = "postgresql://{user}:{password}@{host}:{port}/{name}"


class DbSettings(BaseSettings):
    """Config data with database connection credentials."""

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @computed_field  # type: ignore[misc]
    @property
    def DATABASE_URL(self) -> str:
        return _DB_URL_PATTERN.format(
            user=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            name=self.DB_NAME,
        )
