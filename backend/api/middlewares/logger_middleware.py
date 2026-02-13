from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.utils import logging
import time
from loguru import logger
from backend.utils import time


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
        now=time.perf_counter()
        logging.logger_setup(enqueue=True,diagnose=True)
        logger.info()
        params=request.query_params
        response = await call_next(request)
        end=time.perf_counter()
        logger.info(f"Time elapsed: {now-end}. Datetime: {time.datetime()} Request params: {params}")
        return response
