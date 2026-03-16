from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from datetime import datetime
import time

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

        start_perf = time.perf_counter()
        start_time = datetime.now()
        start_unix = to_unix_time(start_time)

        method = request.method
        path = request.url.path
        query = dict(request.query_params)

        logger.info( 
            "request | method: {} | path: {} | params: {} | time: {} | unix: {}",
            method,
            path,
            query,
            start_time,
            start_unix,
        )

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_perf) * 1000
        status = response.status_code

        logger.info(
            "response | status: {} | duration: {}ms",
            status,
            round(duration_ms, 2),
        )
        return response
