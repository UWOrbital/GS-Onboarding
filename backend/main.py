from backend.api.endpoints import resource
from backend.api.lifespan import lifespan
from backend.api.middlewares.cors_middleware import add_cors_middleware
from backend.api.middlewares.logger_middleware import LoggerMiddleware
from fastapi import FastAPI


def setup_routes(app: FastAPI) -> None:
    """Adds the routes to the app"""
    app.include_router(router=resource)


def setup_middlewares(app: FastAPI) -> None:
    """Adds the middlewares to the app"""
    add_cors_middleware(app)
    app.add_middleware(LoggerMiddleware)


app = FastAPI(lifespan=lifespan)
setup_routes(app)
setup_middlewares(app)
