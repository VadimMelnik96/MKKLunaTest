import os
from functools import lru_cache
from typing import Self, Sequence

from dotenv import load_dotenv
from pydantic import model_validator, PostgresDsn, computed_field
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
    title: str
    version: str
    debug: bool = True
    root_path: str = ""
    static_api_key: str = "very_secret_key"
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


class ScalingSettings(EnvBaseSettings):
    """Автовычисление ресурсов"""

    backend_workers: int | None = None
    max_db_connections: int = 100

    @computed_field
    def effective_backend_workers(self) -> int:
        return self.backend_workers or (os.cpu_count() or 1)

    @computed_field
    def db_pool_size(self) -> int:
        per_worker = self.max_db_connections // self.effective_backend_workers
        return max(1, int(per_worker * 0.8))

    @computed_field
    def db_max_overflow(self) -> int:
        per_worker = self.max_db_connections // self.effective_backend_workers
        return max(0, per_worker - self.db_pool_size)

    model_config = SettingsConfigDict(env_prefix="scale_")


class WebhookSettings(EnvBaseSettings):
    """Настройки для адаптера webhook"""
    max_attempts: int = 3
    base_delay: float = 1.0
    timeout: float = 10.0

    model_config = SettingsConfigDict(env_prefix="webhook_")


class OutboxSettings(EnvBaseSettings):
    """Настройки outbox"""

    max_attempts: int = 3
    exchange: str = 'payments'
    frequency: int = 1

    model_config = SettingsConfigDict(env_prefix="outbox_")


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
    scaling: ScalingSettings = ScalingSettings()
    outbox: OutboxSettings = OutboxSettings()


@lru_cache
def get_settings() -> Settings:
    """Предотвращает повторную инициализацию """
    return Settings()


settings = get_settings()
