from functools import lru_cache
from typing import Self, Sequence

from dotenv import load_dotenv
from pydantic import model_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class EnvBaseSettings(BaseSettings):
    """Базовый класс для прокидывания настроек из .env"""

    model_config = SettingsConfigDict(env_file="..env", extra="ignore")


class AppSettings(EnvBaseSettings):
    """Настройки приложения FastAPI"""

    mode: str = "DEV"
    host: str
    port: int
    access_key: str
    debug: bool = True
    root_path: str = ""
    model_config = SettingsConfigDict(env_prefix="app_")


class PostgresSettings(EnvBaseSettings):
    """Настройки Postgres"""

    engine: str = "postgresql"
    host: str
    port: int
    user: str
    password: str
    db: str
    pool_size: int | None = None
    pool_overflow_size: int | None = None
    leader_usage_coefficient: float | None = None
    use_async: bool = True
    echo: bool = False
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False
    engine_health_check_delay: int | None = None
    dsn: PostgresDsn | None = None
    slave_hosts: Sequence[str] | str = ""
    slave_dsns: Sequence[PostgresDsn] | str = ""

    @model_validator(mode="after")
    def assemble_db_connection(self) -> Self:
        """Сборка Postgres DSN"""
        if self.dsn is None:
            self.dsn = str(  # type: ignore
                PostgresDsn.build(
                    scheme=self.engine + "+asyncpg" if self.use_async else "",
                    username=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    path=f"{self.db}",
                )
            )
        return self

    model_config = SettingsConfigDict(env_prefix="postgres_")


class WebhookSettings(EnvBaseSettings):
    """Настройки для адаптера webhook"""
    max_attempts: int = 3
    base_delay: float = 1.0
    timeout: float = 10.0

    model_config = SettingsConfigDict(env_prefix="webhook_")

class XAPIKeySettings(EnvBaseSettings):
    api_key: str


class RabbitSettings(EnvBaseSettings):
    """Настрой RabbitMQ"""
    host: str = "localhost"
    port: int = 5672
    user: str = "guest"
    password: str = "guest"
    vhost: str = "/"

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"

    model_config = SettingsConfigDict(env_prefix="rabbit_")

class Settings(EnvBaseSettings):
    """Настройки приложения"""
    app: AppSettings = AppSettings()
    database: PostgresSettings = PostgresSettings()
    rabbit: RabbitSettings = RabbitSettings()
    webhook: WebhookSettings = WebhookSettings()


@lru_cache
def get_settings() -> Settings:
    """Предотвращает повторную инициализацию """
    return Settings()


settings = get_settings()
