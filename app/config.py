"""Application configuration for FinFlow."""

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


settings = Settings()
