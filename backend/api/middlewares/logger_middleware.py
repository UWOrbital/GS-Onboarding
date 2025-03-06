from time import perf_counter
from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.utils.logging import logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        @param request: Request received to this middleware from client (it is supplied by FastAPI)
        @param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        @return Response from endpoint
        """
        logger.info(f"Request: {request.method} {request.url}")

        start_time = perf_counter()
        logger.info(f"Start Time: {start_time}")

        response = await call_next(request)
        process_time = perf_counter() - start_time

        logger.info(f"Status: {response.status_code}")
        logger.info(f"Headers: {response.headers}")
        logger.info(f"Process Time: {process_time}")

        return response
