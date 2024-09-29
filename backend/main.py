from backend.api.endpoints import resource
from backend.api.middlewares import add_cors_middleware, LoggerMiddleware
from fastapi import FastAPI


def setup_routes(app: FastAPI) -> None:
    """Adds the routes to the app"""
    app.include_router(router=resource)


def setup_middlewares(app: FastAPI) -> None:
    """Adds the middlewares to the app"""
    add_cors_middleware(app)
    app.add_middleware(LoggerMiddleware)


app = FastAPI()
setup_routes(app)
setup_middlewares(app)
