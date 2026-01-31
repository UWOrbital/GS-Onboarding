from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
from loguru import logger



class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """

        # My implementaiton:
        # Logs incoming requests (HTTP method and URL), measures and logs execution time,
        # records response status codes, and logs errors if a request fails
        # also, eexceptions are re-raised so FastAPI can handle them normally.

        start_time = datetime.now()

        logger.info(f"Incoming request: {request.method} {request.url}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Request failed: {request.method} {request.url} | Error: {e}")
            raise

        duration_ms = (datetime.now() - start_time).total_seconds() * 1000
        logger.info(
            f"Completed request: {request.method} {request.url} "
            f"| Status: {response.status_code} | Time: {duration_ms:.2f}ms"
        )

        return response
