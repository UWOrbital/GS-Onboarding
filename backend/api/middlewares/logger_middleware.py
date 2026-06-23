from collections.abc import Callable
from datetime import datetime
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
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()

        duration = end_time - start_time

        for line in (
            f"{start_time} - {request.method} {request.url}",
            f"Query Params: `{request.query_params}`, Path Params: `{request.path_params}`",
            f"Finished in {duration.microseconds / 1000} ms",
        ):
            logger.info(line)

        return response
