from collections.abc import Callable
from datetime import datetime
from time import perf_counter
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

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        request_time = datetime.now()
        params = dict(request.query_params)

        logger.info(
            f"Request {request.method} {request.url.path} | params={params} | "
            f"at={request_time.isoformat()}"
        )

        start = perf_counter()
        response = await call_next(request)
        duration_ms = (perf_counter() - start) * 1000

        logger.info(
            f"Response {request.method} {request.url.path} | status={response.status_code} | "
            f"duration={duration_ms:.2f}ms"
        )
        return response
