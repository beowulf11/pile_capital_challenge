import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Environment(str, enum.Enum):
    DEV = "dev"
    PROD = "prod"


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    workers_count: int = 1
    reload: bool = True

    environment: str = Environment.DEV

    log_level: LogLevel = LogLevel.INFO

    db_host: str = "db"
    db_port: int = 5432
    db_user: str = "postgres"
    db_pass: str = "very secure password"
    db_base: str = "bank"
    db_echo: bool = False

    @property
    def db_url(self) -> URL:
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PILE_CAPITAL_CHALLENGE_",
        env_file_encoding="utf-8",
    )


settings = Settings()
