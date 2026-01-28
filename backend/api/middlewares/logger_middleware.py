from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
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
        start_time = time.time()

        logger.info(f"Incoming request: Method: {request.method} {request.url} URL: {request.url} Query Params: {dict(request.query_params)}")

        response = await call_next(request)

        duration = (time.time() - start_time) * 1000  # Convert to milliseconds

        logger.info (f"Outgoing response: Status Code: {response.status_code} for {request.method} {request.url} took {duration:.2f} ms")
        return response
