from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import datetime
from backend.utils.logging import logger
from backend.utils.time import to_unix_time


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
        # TODO:(Member) Finish implementing this method
        start = time.perf_counter()
        request_time = to_unix_time(datetime.datetime.now()) * 1000

        response: Response = await call_next(request)
        duration = time.perf_counter() - start

        log_data = {
            "request params": dict(request.query_params),
            "datetime of request": request_time,
            "execution duration": duration,
        }
            
        logger.info("Log data {}", log_data)
        return response 