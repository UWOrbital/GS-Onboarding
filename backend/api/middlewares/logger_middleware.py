from collections.abc import Callable
from datetime import datetime
from time import perf_counter
from typing import Awaitable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from backend.utils.logging import logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        requested_at = datetime.now()
        start_time = perf_counter()
        response = await call_next(request)
        duration_ms = (perf_counter() - start_time) * 1000

        logger.info(
            "Request completed | method={} url={} query_params={} path_params={} "
            "requested_at={} duration_ms={:.2f} status_code={}",
            request.method,
            request.url,
            dict(request.query_params),
            request.path_params,
            requested_at.isoformat(),
            duration_ms,
            response.status_code,
        )

        return response
