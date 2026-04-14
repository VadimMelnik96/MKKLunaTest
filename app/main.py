from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from app.api.middlewares.authentication import APIKeyMiddleware
from app.domain.exception_handlers import exception_config
from app.infrastructure.ioc import ApplicationProvider
from app.settings.settings import PostgresSettings, settings, AppSettings, Settings
from app.api.v1.routers.payments import router as payments_router


def create_app() -> FastAPI:
    """Инициализация приложения"""

    application = FastAPI(
    )
    container = make_async_container(
        ApplicationProvider(),
        FastapiProvider(),
        context={
            Settings: settings,
            PostgresSettings: settings.database,
            AppSettings: settings.app,
        }
    )
    setup_dishka(container, application)
    application.add_middleware(APIKeyMiddleware, api_key=settings.app.static_api_key,
                               exclude_paths={"/docs", "/openapi.json"})
    for exception, handler in exception_config.items():
        application.add_exception_handler(exception, handler)
    application.include_router(payments_router)
    return application


app = create_app()
