from time import perf_counter
from datetime import datetime
from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from logging import getLogger
custom_logger = getLogger("my_logger")


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
        # TODO:(Member) Finish implementing this method
        start_time = perf_counter()

        timestamp = datetime.utcnow().isoformat()

        # Log incoming request
        custom_logger.info(f"[{timestamp}] Incoming request: {request.method} {request.url}")
        custom_logger.info(f"Headers: {dict(request.headers)}")
        if request.query_params:
            custom_logger.info(f"Query Params: {dict(request.query_params)}")

        # Process request
        response = await call_next(request)

        # Measure execution time
        duration = perf_counter() - start_time
        custom_logger.info(
            f"Response status: {response.status_code} | Duration: {duration:.4f} seconds"
        )

        return response
