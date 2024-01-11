from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.responses import UJSONResponse

from src.core.lifetime import (
    register_shutdown_event,
    register_startup_event,
)
from src.accounts.router import router as accounts_router
from src.transactions.router import router as transactions_router
from src.debug.router import router as debug_router
from src.core.settings import settings, Environment

api_router = APIRouter()
api_router.include_router(accounts_router)
api_router.include_router(transactions_router)

if settings.environment == Environment.DEV:
    api_router.include_router(debug_router)


def get_app() -> FastAPI:
    app = FastAPI(
        title="pile_capital_challenge",
        version="0.1",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    app.include_router(router=api_router, prefix="/api")

    return app
