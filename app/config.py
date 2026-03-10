"""Application configuration for FinFlow."""

from pathlib import Path

from sqlalchemy.engine import make_url
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven settings for API, DB, and imports."""

    app_name: str = "FinFlow"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./data/finance.db"
    default_currency: str = "USD"
    max_upload_size_mb: int = 25

    model_config = SettingsConfigDict(env_file=".env", env_prefix="FINFLOW_")

    @staticmethod
    def _ensure_sqlite_parent_dir(database_url: str) -> None:
        """Create parent directory for file-backed SQLite databases."""
        url = make_url(database_url)
        if not url.drivername.startswith("sqlite") or not url.database or url.database == ":memory:":
            return

        db_path = Path(url.database)
        db_path.parent.mkdir(parents=True, exist_ok=True)

    def model_post_init(self, __context: object) -> None:
        self._ensure_sqlite_parent_dir(self.database_url)


settings = Settings()
