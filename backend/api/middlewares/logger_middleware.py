from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.utils.logging import logger_setup, logger_setup_file, logger_close
from loguru import logger
import time

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
        start_time = time.perf_counter()
        response = await call_next(request)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        logger_setup()
        logger_setup_file()

        logger.info("Received a request with paramters: {} \n Duration of execution: {}", request.params, execution_time)
        await logger_close()
        return response

