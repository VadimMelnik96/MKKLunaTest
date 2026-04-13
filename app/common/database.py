from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings.settings import PostgresSettings, Settings


class Database:
    """Вспомогательный класс для работы с БД"""

    def __init__(self, config: PostgresSettings, settings: Settings):
        self.engine = create_async_engine(url=str(config.dsn), echo=config.echo,  pool_size=settings.scaling.db_pool_size,
            max_overflow=settings.scaling.db_max_overflow)

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=config.autoflush,
            autocommit=config.autocommit,
            expire_on_commit=config.expire_on_commit,

        )
