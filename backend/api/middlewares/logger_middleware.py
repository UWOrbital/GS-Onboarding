from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware # Class-based middleware instead of function-based middleware
from time import perf_counter
from loguru import logger

# Middleware
class LoggerMiddleware(BaseHTTPMiddleware):
    # Must be called dispatch() for class-based middleware
    # call_next is Callable, takes Request as an input, and returns any value (Response object)
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        # Type hint that the function returns a Response object
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method
        # True if request.url.query is non-empty
        query = f"?{request.url.query}" if request.url.query else ""
        start = perf_counter()
        response = await call_next(request)
        elapsed_ms = (perf_counter() - start) * 1000
        logger.info(f"{request.method} {request.url.path}{query} -> {response.status_code} in {elapsed_ms:.2f}ms")
        # Must return response to not return None, where None is not callable
        return response
